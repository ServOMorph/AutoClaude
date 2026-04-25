import sys
import customtkinter as ctk
from src.config.constants import (
    OVERLAY_WIDTH, OVERLAY_HEIGHT, OVERLAY_MARGIN,
    OVERLAY_ALPHA, OVERLAY_COLOR_ACTIVE, OVERLAY_COLOR_INACTIVE, OVERLAY_TEXT_COLOR,
)

class StatusOverlay(ctk.CTkToplevel):
    """Indicateur flottant always-on-top pour l'état de l'autoclick."""
    
    def __init__(self, master, on_toggle: callable):
        super().__init__(master)
        self._on_toggle = on_toggle
        self._active = False

        # Configuration de la fenêtre
        self.overrideredirect(True)  # Pas de bordures
        self.attributes("-topmost", True)  # Toujours au-dessus
        self.attributes("-alpha", OVERLAY_ALPHA)
        
        # Windows specific: hide from Taskbar
        if sys.platform == "win32":
            try:
                self.attributes("-toolwindow", True)
            except Exception:
                pass

        # Positionnement en bas à gauche
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
        self.main_frame.bind("<Button-1>", lambda e: self._handle_toggle())

        self.label = ctk.CTkLabel(
            self.main_frame,
            text="CL OFF",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=OVERLAY_TEXT_COLOR,
            fg_color="transparent"
        )
        self.label.pack(side="left", expand=True, padx=(10, 0))
        self.label.bind("<Button-1>", lambda e: self._handle_toggle())

        self.count_label = ctk.CTkLabel(
            self.main_frame,
            text="0",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=OVERLAY_TEXT_COLOR,
            fg_color="transparent"
        )
        self.count_label.pack(side="right", expand=True, padx=(0, 10))
        self.count_label.bind("<Button-1>", lambda e: self._handle_toggle())

        self._keep_on_top()

    def _handle_toggle(self):
        self._active = not self._active
        self.update_ui()
        if self._on_toggle:
            self._on_toggle()

    def set_active(self, state: bool) -> None:
        if self._active != state:
            self._active = state
            self.update_ui()

    def update_ui(self):
        if self._active:
            self.main_frame.configure(fg_color=OVERLAY_COLOR_ACTIVE)
            self.label.configure(text="CL ON")
        else:
            self.main_frame.configure(fg_color=OVERLAY_COLOR_INACTIVE)
            self.label.configure(text="CL OFF")

    def set_click_count(self, count: int):
        self.count_label.configure(text=str(count))

    def _keep_on_top(self):
        try:
            self.attributes("-topmost", True)
            self.lift()
        except Exception:
            pass
        self.after(2000, self._keep_on_top)
