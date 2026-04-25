"""Onglet Tips — liste de tips depuis src/content/tips/."""

import customtkinter as ctk
from src.ui.tabs.base_tab import BaseTab
from src.ui.tabs.markdown_tab import MarkdownView
from src.core.content_loader import load_tips
from src.ui import theme


class TipsTab(BaseTab):
    label = "💡 Tips"
    icon = "💡"

    def render(self) -> ctk.CTkFrame:
        tips = load_tips()
        if not tips:
            ctk.CTkLabel(
                self._frame,
                text="Aucun tip.\nAjouter un .md dans src/content/tips/",
                text_color=theme.PALETTE["text_muted"],
                font=theme.font_body(),
            ).pack(expand=True)
            return self._frame

        categories = sorted({t["category"] for t in tips})
        self._current_cat = ctk.StringVar(value="all")

        filter_row = ctk.CTkFrame(self._frame, fg_color="transparent")
        filter_row.pack(fill="x", padx=8, pady=(8, 4))
        ctk.CTkLabel(filter_row, text="Catégorie :", font=theme.font_body(),
                     text_color=theme.PALETTE["text_muted"]).pack(side="left", padx=(0, 6))

        self._content_area = ctk.CTkScrollableFrame(self._frame, fg_color="transparent")
        self._content_area.pack(fill="both", expand=True)

        ctk.CTkOptionMenu(
            filter_row, variable=self._current_cat,
            values=["all"] + categories,
            command=lambda _: self._refresh(tips),
            fg_color=theme.PALETTE["bg_secondary"],
            button_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["text"],
            width=140,
        ).pack(side="left")

        self._refresh(tips)
        return self._frame

    def _refresh(self, tips: list):
        for w in self._content_area.winfo_children():
            w.destroy()
        cat = self._current_cat.get()
        filtered = tips if cat == "all" else [t for t in tips if t["category"] == cat]
        for tip in filtered:
            self._add_card(tip)

    def _add_card(self, tip: dict):
        card = ctk.CTkFrame(self._content_area, fg_color=theme.PALETTE["bg_secondary"],
                            corner_radius=8, border_width=1,
                            border_color=theme.PALETTE["border"])
        card.pack(fill="x", padx=8, pady=4)
        ctk.CTkLabel(card, text=tip["title"], font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=theme.PALETTE["primary"]).pack(anchor="w", padx=10, pady=(8, 4))
        MarkdownView(card, tip["content"], height=130).pack(fill="x", padx=4, pady=(0, 8))
