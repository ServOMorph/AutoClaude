import sys
import customtkinter as ctk
from src.config.constants import (
    OVERLAY_WIDTH, OVERLAY_HEIGHT, OVERLAY_MARGIN,
    OVERLAY_ALPHA, OVERLAY_COLOR_ACTIVE, OVERLAY_COLOR_INACTIVE, OVERLAY_TEXT_COLOR,
)
from src.config import settings

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
        
        # Drag & Drop et Toggle
        self._drag_start_x = 0
        self._drag_start_y = 0
        self._is_dragging = False

        for widget in [self.main_frame, self.label, self.count_label]:
            widget.bind("<Button-1>", self._start_drag)
            widget.bind("<B1-Motion>", self._do_drag)
            widget.bind("<ButtonRelease-1>", self._stop_drag)

        self._keep_on_top()

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
            if not self.winfo_exists():
                return  # widget détruit — stop la boucle
            if self.state() == "normal":
                self.attributes("-topmost", True)
                self.lift()
            self.after(2000, self._keep_on_top)
        except Exception:
            pass
