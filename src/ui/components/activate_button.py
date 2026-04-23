import customtkinter as ctk
from src.ui import theme


class ActivateButton(ctk.CTkFrame):
    def __init__(self, master, on_toggle: callable = None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._active = False
        self._on_toggle = on_toggle

        self._btn = ctk.CTkButton(
            self,
            text=self._label(),
            font=theme.font_subtitle(),
            fg_color=theme.PALETTE["bg_secondary"],
            hover_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["text_muted"],
            corner_radius=50,
            width=200,
            height=48,
            command=self._toggle,
        )
        self._btn.pack()

    def _label(self) -> str:
        dot = "🟢" if self._active else "🔴"
        state = "ACTIF" if self._active else "INACTIF"
        return f"{dot}  {state}"

    def _toggle(self):
        self._active = not self._active
        self._btn.configure(
            text=self._label(),
            fg_color=theme.PALETTE["success"] if self._active else theme.PALETTE["bg_secondary"],
            text_color=theme.PALETTE["bg"] if self._active else theme.PALETTE["text_muted"],
        )
        if self._on_toggle:
            self._on_toggle(self._active)

    def set_active(self, state: bool):
        if self._active != state:
            self._toggle()

    def is_active(self) -> bool:
        return self._active
