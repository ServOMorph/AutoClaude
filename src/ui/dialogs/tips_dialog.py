"""Dialog tip aléatoire au démarrage (Phase 11.3)."""

import random
import customtkinter as ctk
from src.core.content_loader import load_tips
from src.ui import theme
from src.ui.tabs.markdown_tab import MarkdownView


class TipsDialog(ctk.CTkToplevel):
    """Affiche un tip aléatoire au démarrage."""

    def __init__(self, parent):
        super().__init__(parent)
        tips = load_tips()
        if not tips:
            self.destroy()
            return

        tip = random.choice(tips)
        self.title("💡 Tip du jour")
        self.geometry("480x360")
        self.resizable(False, False)
        self.configure(fg_color=theme.PALETTE["bg"])
        self.lift()
        self.focus_force()

        ctk.CTkLabel(self, text="💡 Tip du jour",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=theme.PALETTE["primary"]).pack(pady=(16, 4))
        ctk.CTkLabel(self, text=tip["title"],
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=theme.PALETTE["text"]).pack(pady=(0, 8))

        MarkdownView(self, tip["content"], height=200).pack(fill="x", padx=16, pady=(0, 8))

        ctk.CTkButton(
            self, text="Fermer", font=theme.font_body(),
            fg_color=theme.PALETTE["bg_secondary"],
            hover_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["text"],
            width=100, height=32, command=self.destroy,
        ).pack(pady=(0, 16))
