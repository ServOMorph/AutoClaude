"""Fenêtre flottante always-on-top indiquant l'état de l'autoclick."""

import sys
import customtkinter as ctk
from src.config.constants import (
    OVERLAY_WIDTH, OVERLAY_HEIGHT, OVERLAY_MARGIN,
    OVERLAY_ALPHA, OVERLAY_COLOR_ACTIVE, OVERLAY_COLOR_INACTIVE, OVERLAY_TEXT_COLOR,
)

_TOPMOST_REFRESH_MS = 2000


class StatusOverlay(ctk.CTkToplevel):
    """Indicateur flottant sans décoration, toujours au-dessus de toutes les fenêtres."""

    def __init__(self, master, on_click: callable = None):
        super().__init__(master)
        self._on_click = on_click
        self._active = False
        self._visible = False

        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-alpha", OVERLAY_ALPHA)

        # N'apparaît pas dans Alt+Tab ni la barre des tâches (Windows uniquement)
        if sys.platform == "win32":
            try:
                self.attributes("-toolwindow", True)
            except Exception:
                pass

        self.configure(fg_color=OVERLAY_COLOR_INACTIVE)

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = OVERLAY_MARGIN
        y = sh - OVERLAY_HEIGHT - OVERLAY_MARGIN
        self.geometry(f"{OVERLAY_WIDTH}x{OVERLAY_HEIGHT}+{x}+{y}")

        self._label = ctk.CTkLabel(
            self,
            text="● AutoClaude OFF",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=OVERLAY_TEXT_COLOR,
            fg_color="transparent",
        )
        self._label.pack(expand=True, fill="both", padx=8)

        self._label.bind("<Button-1>", self._handle_click)
        self.bind("<Button-1>", self._handle_click)

        self.withdraw()
        self._schedule_keep_on_top()

    def set_active(self, state: bool) -> None:
        self._active = state
        color = OVERLAY_COLOR_ACTIVE if state else OVERLAY_COLOR_INACTIVE
        text = "● AutoClaude ON" if state else "● AutoClaude OFF"
        self.configure(fg_color=color)
        self._label.configure(text=text)

    def show(self) -> None:
        self._visible = True
        self.deiconify()
        self.attributes("-topmost", True)

    def hide(self) -> None:
        self._visible = False
        self.withdraw()

    def _handle_click(self, _event=None):
        if self._on_click:
            try:
                self._on_click()
            except Exception:
                pass

    def _schedule_keep_on_top(self):
        """Re-applique topmost périodiquement pour rester au-dessus."""
        if self._visible:
            try:
                self.attributes("-topmost", True)
                self.lift()
            except Exception:
                pass
        self.after(_TOPMOST_REFRESH_MS, self._schedule_keep_on_top)
