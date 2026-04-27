"""TODO: description du module."""

import customtkinter as ctk
from src.core import click_stats
from src.ui import theme


class ClickCounter(ctk.CTkFrame):
    """TODO: description de ClickCounter."""
    def __init__(self, master, **kwargs):
        """TODO: description de __init__."""
        super().__init__(master, fg_color=theme.PALETTE["bg_secondary"], corner_radius=10, **kwargs)

        self._label = ctk.CTkLabel(
            self,
            text=self._format(click_stats.get_total()),
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=theme.PALETTE["primary"],
        )
        self._label.pack(side="left", padx=(16, 8), pady=10)

        ctk.CTkButton(
            self,
            text="↻ Reset",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            fg_color="transparent",
            hover_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["text_muted"],
            border_width=1,
            border_color=theme.PALETTE["border"],
            corner_radius=6,
            width=70,
            height=26,
            command=self._on_reset,
        ).pack(side="right", padx=(8, 16), pady=10)
        # Plus de polling 1s — refresh() est appelé directement par l'app
        # depuis _refresh_click_ui() à chaque clic détecté.

    def _format(self, total: int) -> str:
        """TODO: description de _format."""
        return f"🖱  {total:,} clic{'s' if total > 1 else ''}".replace(",", " ")

    def _on_reset(self):
        """TODO: description de _on_reset."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirmer le reset")
        dialog.geometry("300x130")
        dialog.resizable(False, False)
        dialog.configure(fg_color=theme.PALETTE["bg"])
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="Remettre le compteur à zéro ?",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=theme.PALETTE["text"],
        ).pack(pady=(24, 16))

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack()

        confirmed = [False]

        def on_yes():
            """TODO: description de on_yes."""
            confirmed[0] = True
            dialog.destroy()

        ctk.CTkButton(
            btn_frame, text="Oui", width=100, height=32,
            fg_color=theme.PALETTE["warning"],
            hover_color="#c97a2e",
            text_color="#fff",
            corner_radius=6,
            command=on_yes,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            btn_frame, text="Non", width=100, height=32,
            fg_color=theme.PALETTE["bg_secondary"],
            hover_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["text"],
            border_width=1,
            border_color=theme.PALETTE["border"],
            corner_radius=6,
            command=dialog.destroy,
        ).pack(side="left")

        dialog.wait_window()
        if confirmed[0]:
            click_stats.reset()
            self._label.configure(text=self._format(0))

    def refresh(self):
        """TODO: description de refresh."""
        total = click_stats.get_total()
        self._label.configure(text=self._format(total))
