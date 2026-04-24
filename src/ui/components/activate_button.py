import customtkinter as ctk
from src.ui import theme

_INACTIVE_COLOR = "#3886E5"
_ACTIVE_COLOR = "#E53838"


class ActivateButton(ctk.CTkFrame):
    def __init__(self, master, on_toggle: callable = None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._active = False
        self._on_toggle = on_toggle

        self._btn = ctk.CTkButton(
            self,
            text=self._label(),
            font=ctk.CTkFont(family=theme._font(), size=20, weight="bold"),
            fg_color=_INACTIVE_COLOR,
            hover_color="#2563d4",
            text_color="#fff",
            corner_radius=50,
            width=200,
            height=48,
            command=self._toggle,
        )
        self._btn.pack()

    def _label(self) -> str:
        return "Désactiver" if self._active else "Activer"

    def _toggle(self):
        self._active = not self._active
        color = _ACTIVE_COLOR if self._active else _INACTIVE_COLOR
        hover = "#c92c2c" if self._active else "#2563d4"
        self._btn.configure(
            text=self._label(),
            fg_color=color,
            hover_color=hover,
        )
        if self._on_toggle:
            self._on_toggle(self._active)

    def set_active(self, state: bool):
        if self._active != state:
            self._toggle()

    def is_active(self) -> bool:
        return self._active
