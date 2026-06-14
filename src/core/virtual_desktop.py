"""Détection et gestion des bureaux virtuels Windows (IVirtualDesktopManager).

Utilisé par l'overlay pour le suivre quand l'utilisateur change de bureau virtuel.
Sur une fenêtre `overrideredirect` + topmost, Windows ne déplace pas
automatiquement la fenêtre vers le bureau actif : elle reste « fantôme » sur le
bureau d'origine (rendu translucide, non cliquable). On la déplace explicitement
via `MoveWindowToDesktop`, ce qui évite le cycle withdraw/deiconify (map/unmap)
connu pour déclencher le crash natif `tk86t.dll`.

Dégradation progressive : si l'API COM est indisponible (échec, OS non-Windows),
toutes les méthodes renvoient None/False et l'appelant ignore la fonctionnalité.

API COM utilisée (documentée, stable Win10/Win11) :
    IVirtualDesktopManager
        [3] IsWindowOnCurrentVirtualDesktop(HWND, BOOL*)
        [4] GetWindowDesktopId(HWND, GUID*)
        [5] MoveWindowToDesktop(HWND, REFGUID)
"""

import sys
import ctypes
from ctypes import wintypes


class _GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", ctypes.c_ulong),
        ("Data2", ctypes.c_ushort),
        ("Data3", ctypes.c_ushort),
        ("Data4", ctypes.c_ubyte * 8),
    ]


_CLSID_VirtualDesktopManager = "{aa509086-5ca9-4c25-8f95-589d3c07b48a}"
_IID_IVirtualDesktopManager = "{a5cd92ff-29be-454c-8d04-d82879fb3f1b}"
_CLSCTX_ALL = 0x17
_GA_ROOT = 2
_DWMWA_CLOAKED = 14  # DwmGetWindowAttribute : !=0 => fenêtre masquée/cloakée


def is_cloaked(hwnd):
    """État cloaked DWM d'une fenêtre : 0 = visible, !=0 = masquée, None = erreur.

    Le DWM cloake (`DWM_CLOAKED_SHELL=2`) toute fenêtre qui n'appartient pas au
    bureau virtuel affiché — y compris quand Task View (Win+Tab) la « laisse »
    sur l'ancien bureau sans changer son GUID. Détecte directement l'état
    fantôme de l'overlay, indépendamment de la fenêtre au premier plan.
    """
    if not hwnd:
        return None
    try:
        val = wintypes.DWORD()
        hr = ctypes.windll.dwmapi.DwmGetWindowAttribute(
            wintypes.HWND(hwnd), _DWMWA_CLOAKED,
            ctypes.byref(val), ctypes.sizeof(val),
        )
        return None if hr != 0 else val.value
    except Exception:
        return None


class VirtualDesktopManager:
    """Wrapper ctypes minimal autour de IVirtualDesktopManager."""

    def __init__(self):
        self._ptr = None
        if sys.platform != "win32":
            return
        try:
            ole32 = ctypes.windll.ole32
            ole32.CoInitialize(None)
            clsid = self._guid(_CLSID_VirtualDesktopManager)
            iid = self._guid(_IID_IVirtualDesktopManager)
            ptr = ctypes.c_void_p()
            hr = ole32.CoCreateInstance(
                ctypes.byref(clsid), None, _CLSCTX_ALL,
                ctypes.byref(iid), ctypes.byref(ptr),
            )
            if hr == 0 and ptr.value:
                self._ptr = ptr
        except Exception:
            self._ptr = None

    @property
    def available(self) -> bool:
        return self._ptr is not None

    def _guid(self, s: str) -> _GUID:
        g = _GUID()
        ctypes.windll.ole32.CLSIDFromString(ctypes.c_wchar_p(s), ctypes.byref(g))
        return g

    def _call(self, index, argtypes, *args):
        """Appelle la méthode COM à l'index `index` de la vtable. Renvoie le HRESULT."""
        vtbl = ctypes.cast(self._ptr, ctypes.POINTER(ctypes.c_void_p)).contents.value
        fn_addr = ctypes.cast(vtbl, ctypes.POINTER(ctypes.c_void_p))[index]
        proto = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_void_p, *argtypes)
        fn = proto(fn_addr)
        return fn(self._ptr, *args)

    @staticmethod
    def root_hwnd(child_hwnd: int):
        """Remonte au HWND top-level (overrideredirect → pas de frame parente)."""
        try:
            root = ctypes.windll.user32.GetAncestor(child_hwnd, _GA_ROOT)
            return root or child_hwnd
        except Exception:
            return child_hwnd

    def is_on_current_desktop(self, hwnd):
        """True/False, ou None si indisponible/erreur."""
        if not self._ptr or not hwnd:
            return None
        try:
            result = wintypes.BOOL()
            hr = self._call(
                3, (wintypes.HWND, ctypes.POINTER(wintypes.BOOL)),
                wintypes.HWND(hwnd), ctypes.byref(result),
            )
            if hr != 0:
                return None
            return bool(result.value)
        except Exception:
            return None

    def get_window_desktop_id(self, hwnd):
        """GUID du bureau d'une fenêtre, ou None (erreur / fenêtre épinglée)."""
        if not self._ptr or not hwnd:
            return None
        try:
            guid = _GUID()
            hr = self._call(
                4, (wintypes.HWND, ctypes.POINTER(_GUID)),
                wintypes.HWND(hwnd), ctypes.byref(guid),
            )
            if hr != 0:
                return None
            is_null = (
                guid.Data1 == 0 and guid.Data2 == 0
                and guid.Data3 == 0 and not any(guid.Data4)
            )
            return None if is_null else guid
        except Exception:
            return None

    def move_window_to_desktop(self, hwnd, desktop_guid) -> bool:
        if not self._ptr or not hwnd or desktop_guid is None:
            return False
        try:
            hr = self._call(
                5, (wintypes.HWND, ctypes.POINTER(_GUID)),
                wintypes.HWND(hwnd), ctypes.byref(desktop_guid),
            )
            return hr == 0
        except Exception:
            return False

    def current_desktop_id(self):
        """GUID du bureau virtuel actuellement affiché, ou None.

        Déduit d'abord via la fenêtre au premier plan (`GetForegroundWindow`),
        qui est toujours sur le bureau visible. Mais cette fenêtre n'a pas
        toujours de GUID exploitable (console, fenêtre `overrideredirect` ou
        cloakée, animation de transition) — c'était la cause du fantôme : on
        renvoyait None et le changement de bureau passait inaperçu.

        Fallback robuste : si le premier plan n'a pas de GUID, on énumère les
        fenêtres pour trouver n'importe quelle fenêtre *normale* présente sur le
        bureau courant. Une fenêtre normale, elle, a toujours un GUID fiable.
        """
        if not self._ptr:
            return None
        try:
            foreground = ctypes.windll.user32.GetForegroundWindow()
            if foreground:
                gid = self.get_window_desktop_id(foreground)
                if gid is not None:
                    return gid
            return self._scan_current_desktop_id()
        except Exception:
            return None

    def _scan_current_desktop_id(self):
        """Cherche le GUID du bureau courant via une fenêtre normale visible.

        Parcourt les fenêtres top-level : la première qui est visible, sur le
        bureau courant (`IsWindowOnCurrentVirtualDesktop` — fiable pour une
        fenêtre normale) et porteuse d'un GUID non-null donne le bureau affiché.
        Renvoie None si aucune (bureau réellement vide — fantôme alors sans
        conséquence, rien à survoler).
        """
        if not self._ptr:
            return None
        user32 = ctypes.windll.user32
        found = {"gid": None}

        @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        def _cb(hwnd, _lparam):
            try:
                if not user32.IsWindowVisible(hwnd):
                    return True
                if self.is_on_current_desktop(hwnd) is True:
                    gid = self.get_window_desktop_id(hwnd)
                    if gid is not None:
                        found["gid"] = gid
                        return False  # stop l'énumération
            except Exception:
                pass
            return True

        try:
            user32.EnumWindows(_cb, 0)
        except Exception:
            return None
        return found["gid"]

    def follow_to_current_desktop(self, hwnd) -> bool:
        """Déplace `hwnd` vers le bureau virtuel actuellement affiché.

        On déduit le bureau courant via la fenêtre au premier plan
        (`GetForegroundWindow`), qui est forcément sur le bureau visible.
        Renvoie True si le déplacement a réussi.
        """
        if not self._ptr or not hwnd:
            return False
        try:
            foreground = ctypes.windll.user32.GetForegroundWindow()
            if not foreground:
                return False
            target = self.get_window_desktop_id(foreground)
            if target is None:
                return False
            return self.move_window_to_desktop(hwnd, target)
        except Exception:
            return False
