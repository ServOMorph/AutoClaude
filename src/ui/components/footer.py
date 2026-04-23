import webbrowser
import customtkinter as ctk
from src.config.constants import VERSION, URL_WEBSITE, URL_GITHUB
from src.ui import theme


class Footer(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        link = ctk.CTkLabel(
            self, text=URL_GITHUB,
            font=ctk.CTkFont(size=11),
            text_color=theme.PALETTE["text_muted"],
            cursor="hand2",
        )
        link.pack(pady=(0, 8))
        link.bind("<Button-1>", lambda _: webbrowser.open(URL_GITHUB))
