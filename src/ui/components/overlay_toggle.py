import customtkinter as ctk
from src.config import settings

class OverlayToggle(ctk.CTkFrame):
    """Sélecteur pour afficher ou masquer l'overlay."""
    def __init__(self, master, on_change: callable = None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._on_change = on_change
        
        # État initial depuis les settings
        initial_state = settings.get("overlay_enabled")
        self._var = ctk.BooleanVar(value=initial_state)

        self._switch = ctk.CTkSwitch(
            self,
            text="Afficher l'indicateur flottant",
            variable=self._var,
            command=self._handle_change,
            font=ctk.CTkFont(size=12),
        )
        self._switch.pack()

    def _handle_change(self):
        enabled = self._var.get()
        settings.set("overlay_enabled", enabled)
        if self._on_change:
            self._on_change(enabled)
