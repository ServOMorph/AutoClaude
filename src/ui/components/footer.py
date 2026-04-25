"""TODO: description du module."""

import customtkinter as ctk
from src.config.constants import VERSION, URL_WEBSITE
from src.ui import theme


class Footer(ctk.CTkFrame):
    """TODO: description de Footer."""
    def __init__(self, master, **kwargs):
        """TODO: description de __init__."""
        super().__init__(master, fg_color="transparent", **kwargs)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", pady=(0, 8))


        version = ctk.CTkLabel(
            container, text=f"v{VERSION}",
            font=ctk.CTkFont(size=10),
            text_color=theme.PALETTE["text_muted"],
        )
        version.pack(side="top")
