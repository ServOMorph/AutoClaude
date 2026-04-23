import customtkinter as ctk
from src.ui import theme


class WarningBanner(ctk.CTkFrame):
    def __init__(self, master, text: str, **kwargs):
        super().__init__(
            master,
            fg_color="#2d1f0a",
            border_color=theme.PALETTE["warning"],
            border_width=0,
            corner_radius=8,
            **kwargs,
        )
        # Bordure gauche simulée avec un frame coloré
        border = ctk.CTkFrame(self, width=4, fg_color=theme.PALETTE["warning"], corner_radius=0)
        border.pack(side="left", fill="y")

        ctk.CTkLabel(
            self, text=text,
            font=theme.font_small(),
            text_color=theme.PALETTE["warning"],
            wraplength=380,
            justify="left",
        ).pack(side="left", padx=12, pady=10)
