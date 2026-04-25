"""TODO: description du module."""

import customtkinter as ctk
from PIL import Image
from src.config.constants import ASSET_LOGO_PNG, APP_NAME
from src.ui import theme


class Header(ctk.CTkFrame):
    """TODO: description de Header."""
    def __init__(self, master, **kwargs):
        """TODO: description de __init__."""
        super().__init__(master, fg_color=theme.PALETTE["bg_secondary"], corner_radius=12, **kwargs)

        try:
            img = Image.open(ASSET_LOGO_PNG)
            self._logo_img = ctk.CTkImage(img, size=(80, 80))
            logo_label = ctk.CTkLabel(self, image=self._logo_img, text="")
            logo_label.pack(pady=(12, 4))
        except Exception:
            pass

        ctk.CTkLabel(
            self, text=APP_NAME,
            font=theme.font_title(),
            text_color="#DB7759",
        ).pack(pady=(0, 12))
