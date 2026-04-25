"""Switch pour activer/désactiver l'overlay flottant."""

import customtkinter as ctk
from src.config import settings
from src.ui import theme


class OverlayToggle(ctk.CTkFrame):
    """Switch 'Afficher l'indicateur flottant' avec persistance automatique."""

    def __init__(self, master, on_change: callable = None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._on_change = on_change

        self._switch = ctk.CTkSwitch(
            self,
            text="Afficher l'indicateur flottant",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=theme.PALETTE["text_muted"],
            progress_color=theme.PALETTE["primary"],
            command=self._on_toggle,
        )
        self._switch.pack()

        if settings.get("overlay_enabled"):
            self._switch.select()
        else:
            self._switch.deselect()

    def _on_toggle(self):
        enabled = self._switch.get() == 1
        settings.set("overlay_enabled", enabled)
        if self._on_change:
            self._on_change(enabled)
