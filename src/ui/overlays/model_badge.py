import sys
import time
import tkinter as tk
import customtkinter as ctk
from src.config.constants import (
    MODEL_BADGE_WIDTH, MODEL_BADGE_HEIGHT, MODEL_BADGE_COLOR, MODEL_BADGE_TEXT_COLOR,
    MODEL_BADGE_ALPHA,
)
from src.core.window_tracker import WindowTracker
from src.core.virtual_desktop import VirtualDesktopManager, reassert_topmost
from src.core.logger import get_logger

_log = get_logger()

MODEL_OPTIONS = ["Haiku", "Sonnet", "Opus", "Fable"]

# Cadence du suivi de la fenêtre attachée (position + visibilité).
MODEL_BADGE_POLL_MS = 800

# Intervalle minimal entre deux transitions withdraw/deiconify : le cycle
# map/unmap est impliqué dans le crash natif tk86t.dll (cf. virtual_desktop.py),
# même valeur que REMAP_THROTTLE_S de StatusOverlay.
MODEL_BADGE_VIS_THROTTLE_S = 4.0


class ModelBadge(ctk.CTkToplevel):
    """Badge flottant always-on-top affichant le modèle Claude actif.

    Si `target_hwnd` est fourni, le badge se positionne relativement à cette
    fenêtre (VSCode) et suit ses déplacements ; masqué quand elle est
    minimisée, fermée ou cloakée (bureau virtuel), réaffiché sinon.
    """

    def __init__(self, master, model: str = "Sonnet", on_remove: callable = None,
                 target_hwnd: int = None, window_title: str = None,
                 on_state_change: callable = None, rel_x: int = 20, rel_y: int = 20):
        super().__init__(master)
        self.on_remove = on_remove
        self.on_state_change = on_state_change
        self.window_title = window_title
        self.model = model if model in MODEL_OPTIONS else MODEL_OPTIONS[0]

        self.title("AutoClaude Model Badge")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-alpha", MODEL_BADGE_ALPHA)

        if sys.platform == "win32":
            try:
                self.attributes("-toolwindow", True)
            except Exception:
                pass

        self.tracker = WindowTracker(target_hwnd) if target_hwnd else None
        self._rel_x, self._rel_y = rel_x, rel_y
        self._track_after_id = None
        self._was_hidden = False
        self._last_vis_change = 0.0
        self._last_pos = None
        self._hwnd = None

        win_rect = self.tracker.get_rect() if self.tracker else None
        if win_rect:
            x, y = win_rect[0] + self._rel_x, win_rect[1] + self._rel_y
        else:
            screen_h = self.winfo_screenheight()
            x, y = 20, screen_h - MODEL_BADGE_HEIGHT - 80
        self.geometry(f"{MODEL_BADGE_WIDTH}x{MODEL_BADGE_HEIGHT}+{x}+{y}")

        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=MODEL_BADGE_COLOR,
            corner_radius=6,
            border_width=0
        )
        self.main_frame.pack(expand=True, fill="both")

        self.label = ctk.CTkLabel(
            self.main_frame,
            text=self.model,
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=MODEL_BADGE_TEXT_COLOR,
            fg_color="transparent"
        )
        self.label.pack(expand=True, fill="both", padx=4, pady=2)

        self._drag_start_x = 0
        self._drag_start_y = 0
        self._is_dragging = False

        self._menu = tk.Menu(self, tearoff=0)
        model_menu = tk.Menu(self._menu, tearoff=0)
        for name in MODEL_OPTIONS:
            model_menu.add_command(label=name, command=lambda n=name: self.set_model(n))
        self._menu.add_cascade(label="Changer modèle", menu=model_menu)
        self._menu.add_separator()
        self._menu.add_command(label="Supprimer", command=self._remove)

        for widget in [self.main_frame, self.label]:
            widget.bind("<Button-1>", self._start_drag)
            widget.bind("<B1-Motion>", self._do_drag)
            widget.bind("<ButtonRelease-1>", self._stop_drag)
            widget.bind("<Button-3>", self._show_menu)

        self._keep_on_top()

        if self.tracker and sys.platform == "win32":
            self._track_after_id = self.after(MODEL_BADGE_POLL_MS, self._track_window)

    def _start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y
        self._is_dragging = False

    def _do_drag(self, event):
        if abs(event.x - self._drag_start_x) > 2 or abs(event.y - self._drag_start_y) > 2:
            self._is_dragging = True

        x = self.winfo_x() + (event.x - self._drag_start_x)
        y = self.winfo_y() + (event.y - self._drag_start_y)
        self.geometry(f"+{x}+{y}")

    def _stop_drag(self, event):
        if self._is_dragging and self.tracker:
            win_rect = self.tracker.get_rect()
            if win_rect:
                self._rel_x = self.winfo_x() - win_rect[0]
                self._rel_y = self.winfo_y() - win_rect[1]
                self._last_pos = (self.winfo_x(), self.winfo_y())
                if self.on_state_change:
                    self.on_state_change()
        self._is_dragging = False

    def _get_hwnd(self):
        if self._hwnd:
            return self._hwnd
        try:
            self._hwnd = VirtualDesktopManager.root_hwnd(self.winfo_id())
        except Exception:
            self._hwnd = None
        return self._hwnd

    def _throttle_ok(self) -> bool:
        return (time.monotonic() - self._last_vis_change) >= MODEL_BADGE_VIS_THROTTLE_S

    def _track_window(self):
        """Suit la fenêtre attachée : position relative maintenue, visibilité
        synchronisée (masqué si minimisée/fermée/cloaked).

        Les transitions withdraw/deiconify sont throttlées (map/unmap = risque
        crash tk86t) et geometry() n'est appelé que si la position a changé."""
        try:
            if not self.winfo_exists() or not self.tracker:
                return

            if not self.tracker.is_visible():
                if not self._was_hidden and self._throttle_ok():
                    self._was_hidden = True
                    self._last_vis_change = time.monotonic()
                    _log.info("ModelBadge '%s' : cible invisible → withdraw", self.window_title)
                    self.withdraw()
            else:
                if self._was_hidden and self._throttle_ok():
                    self._was_hidden = False
                    self._last_vis_change = time.monotonic()
                    _log.info("ModelBadge '%s' : cible visible → deiconify", self.window_title)
                    self.deiconify()
                    reassert_topmost(self._get_hwnd())
                if not self._was_hidden:
                    win_rect = self.tracker.get_rect()
                    if win_rect:
                        pos = (win_rect[0] + self._rel_x, win_rect[1] + self._rel_y)
                        if pos != self._last_pos:
                            self._last_pos = pos
                            self.geometry(f"+{pos[0]}+{pos[1]}")
        except Exception:
            _log.exception("ModelBadge _track_window: erreur")
        finally:
            try:
                if self.winfo_exists():
                    self._track_after_id = self.after(MODEL_BADGE_POLL_MS, self._track_window)
            except Exception:
                pass

    def _show_menu(self, event):
        try:
            self._menu.tk_popup(event.x_root, event.y_root)
        finally:
            self._menu.grab_release()

    def set_model(self, model: str) -> None:
        if model not in MODEL_OPTIONS:
            return
        self.model = model
        self.label.configure(text=model)
        if self.on_state_change:
            self.on_state_change()

    def get_state(self) -> dict:
        """Snapshot sérialisable de l'état du badge (persistance settings)."""
        return {
            "title": self.window_title,
            "rel_x": self._rel_x,
            "rel_y": self._rel_y,
            "model": self.model,
        }

    def _remove(self):
        if self.on_remove:
            self.on_remove()
        self.destroy()

    def destroy(self):
        if self._track_after_id:
            try:
                self.after_cancel(self._track_after_id)
            except Exception:
                pass
            self._track_after_id = None
        super().destroy()

    def _keep_on_top(self):
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
