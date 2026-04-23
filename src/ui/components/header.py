import webbrowser
import customtkinter as ctk
from PIL import Image
from src.config.constants import ASSET_LOGO_PNG, URL_WEBSITE, APP_NAME
from src.ui import theme


class Header(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=theme.PALETTE["bg_secondary"], corner_radius=12, **kwargs)

        try:
            img = Image.open(ASSET_LOGO_PNG)
            self._logo_img = ctk.CTkImage(img, size=(120, 120))
            logo_label = ctk.CTkLabel(self, image=self._logo_img, text="")
            logo_label.pack(pady=(16, 4))
        except Exception:
            pass

        link = ctk.CTkLabel(
            self, text=URL_WEBSITE,
            font=theme.font_small(),
            text_color=theme.PALETTE["primary"],
            cursor="hand2",
        )
        link.pack(pady=(0, 6))
        link.bind("<Button-1>", lambda _: webbrowser.open(URL_WEBSITE))

        ctk.CTkLabel(
            self, text=APP_NAME,
            font=theme.font_title(),
            text_color=theme.PALETTE["primary"],
        ).pack()

        ctk.CTkLabel(
            self, text="Automatiseur de clics GUI",
            font=theme.font_small(),
            text_color=theme.PALETTE["text_muted"],
        ).pack(pady=(2, 12))
