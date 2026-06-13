import sys
import customtkinter as ctk
from src.config.constants import (
    OVERLAY_WIDTH, OVERLAY_HEIGHT, OVERLAY_MARGIN,
    OVERLAY_ALPHA, OVERLAY_COLOR_ACTIVE, OVERLAY_COLOR_INACTIVE, OVERLAY_TEXT_COLOR,
)
from src.config import settings
from src.core.virtual_desktop import VirtualDesktopManager
from src.core.logger import get_logger

_log = get_logger()


class StatusOverlay(ctk.CTkToplevel):
    """Indicateur flottant always-on-top pour l'état de l'autoclick."""

    def __init__(self, master, on_toggle: callable):
        super().__init__(master)
        self.on_toggle = on_toggle
        self.active = False

        # Configuration de la fenêtre
        self.title("AutoClaude Overlay")
        self.overrideredirect(True)  # Pas de bordures
        self.attributes("-topmost", True)  # Toujours au-dessus
        self.attributes("-alpha", OVERLAY_ALPHA)

        # Windows specific: hide from Taskbar
        if sys.platform == "win32":
            try:
                self.attributes("-toolwindow", True)
            except Exception:
                pass

        # Positionnement (chargement ou défaut bas-gauche)
        saved_x = settings.get("overlay_x")
        saved_y = settings.get("overlay_y")

        if saved_x is not None and saved_y is not None:
            x, y = saved_x, saved_y
        else:
            screen_h = self.winfo_screenheight()
            x = OVERLAY_MARGIN
            y = screen_h - OVERLAY_HEIGHT - OVERLAY_MARGIN

        self.geometry(f"{OVERLAY_WIDTH}x{OVERLAY_HEIGHT}+{x}+{y}")

        # Frame principale cliquable
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=OVERLAY_COLOR_INACTIVE,
            corner_radius=10,
            border_width=0
        )
        self.main_frame.pack(expand=True, fill="both")

        self.label = ctk.CTkLabel(
            self.main_frame,
            text="CL OFF",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=OVERLAY_TEXT_COLOR,
            fg_color="transparent"
        )
        self.label.pack(side="left", expand=True, padx=(10, 0))

        self.count_label = ctk.CTkLabel(
            self.main_frame,
            text="0",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=OVERLAY_TEXT_COLOR,
            fg_color="transparent"
        )
        self.count_label.pack(side="right", expand=True, padx=(0, 10))

        # Drag & Toggle
        self._drag_start_x = 0
        self._drag_start_y = 0
        self._is_dragging = False

        for widget in [self.main_frame, self.label, self.count_label]:
            widget.bind("<Button-1>", self._start_drag)
            widget.bind("<B1-Motion>", self._do_drag)
            widget.bind("<ButtonRelease-1>", self._stop_drag)

        self._keep_on_top()

        # Suivi des bureaux virtuels Windows : sur une fenêtre overrideredirect
        # topmost, Windows laisse un « fantôme » non cliquable quand on change de
        # bureau. On déplace l'overlay vers le bureau courant dès qu'on détecte
        # un changement. cf. memory crash_tk86t_signature (on évite map/unmap).
        self._vd = VirtualDesktopManager()
        self._hwnd = None
        self._last_desktop_bytes = None
        self._vd_after_id = None
        _log.info("Overlay VD tracking: available=%s", self._vd.available)
        if self._vd.available:
            self._last_desktop_bytes = self._desktop_bytes(self._vd.current_desktop_id())
            _log.info("Overlay VD initial desktop=%s", self._fmt(self._last_desktop_bytes))
            self._vd_after_id = self.after(1500, self._check_desktop_switch)

    @staticmethod
    def _desktop_bytes(guid):
        return bytes(guid) if guid is not None else None

    @staticmethod
    def _fmt(b):
        return b.hex()[:12] if b else "None"

    def _get_hwnd(self):
        if self._hwnd:
            return self._hwnd
        try:
            self._hwnd = self._vd.root_hwnd(self.winfo_id())
        except Exception:
            self._hwnd = None
        return self._hwnd

    def _check_desktop_switch(self):
        """Re-déplace l'overlay vers le bureau virtuel actif si l'utilisateur a changé."""
        try:
            if not self.winfo_exists():
                return
            # Ignore quand l'overlay est masqué (désactivé par l'utilisateur).
            if self.state() != "withdrawn":
                current = self._desktop_bytes(self._vd.current_desktop_id())
                if current is not None and current != self._last_desktop_bytes:
                    _log.info(
                        "VD switch détecté: %s -> %s — remap overlay",
                        self._fmt(self._last_desktop_bytes), self._fmt(current),
                    )
                    self._last_desktop_bytes = current
                    self._follow_to_current_desktop()
        except Exception:
            _log.exception("VD poll: erreur")
        finally:
            try:
                if self.winfo_exists():
                    self._vd_after_id = self.after(1500, self._check_desktop_switch)
            except Exception:
                pass

    def _follow_to_current_desktop(self):
        hwnd = self._get_hwnd()
        # Tentative non intrusive d'abord (MoveWindowToDesktop, sans map/unmap)...
        moved = False
        try:
            gid = self._vd.current_desktop_id()
            if gid is not None and hwnd:
                moved = self._vd.move_window_to_desktop(hwnd, gid)
        except Exception:
            moved = False
        on_current = self._vd.is_on_current_desktop(hwnd)
        _log.info("VD remap: hwnd=%s move_ok=%s is_on_current=%s", hwnd, moved, on_current)
        # ...puis ré-affichage sur le bureau courant (méthode prouvée, équivalente
        # au toggle manuel). map/unmap rare → risque tk86t négligeable vs per-click.
        try:
            self.withdraw()
            self.after(80, self._finish_remap)
        except Exception:
            _log.exception("VD remap: withdraw a échoué")

    def _finish_remap(self):
        try:
            if self.winfo_exists():
                self.deiconify()
                self.attributes("-topmost", True)
                _log.info("VD remap: deiconify OK, is_on_current=%s",
                          self._vd.is_on_current_desktop(self._get_hwnd()))
        except Exception:
            _log.exception("VD remap: deiconify a échoué")

    def _start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y
        self._is_dragging = False

    def _do_drag(self, event):
        # Si on bouge de plus de 2 pixels, on considère que c'est un drag
        if abs(event.x - self._drag_start_x) > 2 or abs(event.y - self._drag_start_y) > 2:
            self._is_dragging = True

        x = self.winfo_x() + (event.x - self._drag_start_x)
        y = self.winfo_y() + (event.y - self._drag_start_y)
        self.geometry(f"+{x}+{y}")

    def _stop_drag(self, event):
        if not self._is_dragging:
            self._handle_toggle()
        else:
            # Sauvegarder la nouvelle position
            settings.set("overlay_x", self.winfo_x())
            settings.set("overlay_y", self.winfo_y())
        self._is_dragging = False

    def _handle_toggle(self):
        self.active = not self.active
        self.update_ui()
        if self.on_toggle:
            self.on_toggle()

    def set_active(self, state: bool) -> None:
        if self.active != state:
            self.active = state
            self.update_ui()

    def update_ui(self):
        if self.active:
            self.main_frame.configure(fg_color=OVERLAY_COLOR_ACTIVE)
            self.label.configure(text="CL ON")
        else:
            self.main_frame.configure(fg_color=OVERLAY_COLOR_INACTIVE)
            self.label.configure(text="CL OFF")

    def set_click_count(self, count: int):
        self.count_label.configure(text=str(count))

    def _keep_on_top(self):
        # `-topmost` est persistent — pas besoin de le réaffirmer ni de lift().
        # On rebind uniquement sur <Map> pour récupérer après un deiconify.
        try:
            if not self.winfo_exists():
                return
            self.bind("<Map>", lambda _: self._on_map(), add="+")
        except Exception:
            pass

    def _on_map(self):
        try:
            if self.winfo_exists():
                self.attributes("-topmost", True)
        except Exception:
            pass
