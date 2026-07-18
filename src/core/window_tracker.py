"""Suivi de fenêtres VSCode (Win32 EnumWindows) pour l'attachement du badge modèle.

Le badge overlay (model_badge.py) doit suivre une fenêtre VSCode : position,
visibilité (masqué si minimisée/fermée/cloaked). Ce module isole les appels
Win32 nécessaires, dégradation progressive sur OS non-Windows (renvoie
None/False/liste vide, l'appelant ignore la fonctionnalité).
"""

import sys
import ctypes
from ctypes import wintypes

from src.core.virtual_desktop import is_cloaked

_WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

_VSCODE_CLASS = "Chrome_WidgetWin_1"
_VSCODE_TITLE_MARKER = "Visual Studio Code"


def list_vscode_windows():
    """Liste des fenêtres VSCode top-level visibles : [(hwnd, titre), ...].

    Filtre sur la classe Electron (`Chrome_WidgetWin_1`) et un titre contenant
    "Visual Studio Code", pour exclure les autres applications Electron.
    """
    if sys.platform != "win32":
        return []

    user32 = ctypes.windll.user32
    windows = []

    def _cb(hwnd, _lparam):
        try:
            if not user32.IsWindowVisible(hwnd):
                return True
            length = user32.GetWindowTextLengthW(hwnd)
            if length == 0:
                return True
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            title = buf.value
            if _VSCODE_TITLE_MARKER not in title:
                return True
            class_buf = ctypes.create_unicode_buffer(256)
            user32.GetClassNameW(hwnd, class_buf, 256)
            if class_buf.value != _VSCODE_CLASS:
                return True
            windows.append((hwnd, title))
        except Exception:
            pass
        return True

    try:
        user32.EnumWindows(_WNDENUMPROC(_cb), 0)
    except Exception:
        pass
    return windows


def get_window_rect(hwnd):
    """Rectangle écran `(left, top, right, bottom)` d'une fenêtre, ou None."""
    if not hwnd or sys.platform != "win32":
        return None
    try:
        rect = wintypes.RECT()
        ok = ctypes.windll.user32.GetWindowRect(wintypes.HWND(hwnd), ctypes.byref(rect))
        if not ok:
            return None
        return (rect.left, rect.top, rect.right, rect.bottom)
    except Exception:
        return None


def is_window_valid(hwnd) -> bool:
    """True si le hwnd désigne encore une fenêtre existante."""
    if not hwnd or sys.platform != "win32":
        return False
    try:
        return bool(ctypes.windll.user32.IsWindow(wintypes.HWND(hwnd)))
    except Exception:
        return False


def is_window_minimized(hwnd) -> bool:
    if not hwnd or sys.platform != "win32":
        return False
    try:
        return bool(ctypes.windll.user32.IsIconic(wintypes.HWND(hwnd)))
    except Exception:
        return False


class WindowTracker:
    """Suit une fenêtre VSCode par hwnd : existence, position, visibilité."""

    def __init__(self, hwnd: int):
        self.hwnd = hwnd

    def exists(self) -> bool:
        return is_window_valid(self.hwnd)

    def get_rect(self):
        return get_window_rect(self.hwnd)

    def is_visible(self) -> bool:
        """False si la fenêtre n'existe plus, est minimisée, ou cloaked (DWM)."""
        if not self.exists():
            return False
        if is_window_minimized(self.hwnd):
            return False
        if is_cloaked(self.hwnd):
            return False
        return True
