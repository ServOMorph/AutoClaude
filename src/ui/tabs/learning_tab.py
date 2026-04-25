"""Onglet Learnings — sous-onglets par domaine depuis src/content/learnings/."""

import customtkinter as ctk
from src.ui.tabs.base_tab import BaseTab
from src.ui.tabs.markdown_tab import MarkdownView
from src.core.content_loader import load_learnings
from src.ui import theme

_SEVERITY_COLORS = {
    "high": "#DB7857",
    "medium": "#A5C9CA",
    "low": "#718096",
}


class LearningTab(BaseTab):
    label = "📚 Learnings"
    icon = "📚"

    def render(self) -> ctk.CTkFrame:
        learnings = load_learnings()
        if not learnings:
            ctk.CTkLabel(
                self._frame,
                text="Aucun learning.\nAjouter des .md dans src/content/learnings/<domaine>/",
                text_color=theme.PALETTE["text_muted"],
                font=theme.font_body(),
            ).pack(expand=True)
            return self._frame

        tab_view = ctk.CTkTabview(
            self._frame,
            fg_color=theme.PALETTE["bg"],
            segmented_button_fg_color=theme.PALETTE["bg_secondary"],
            segmented_button_selected_color=theme.PALETTE["primary"],
            segmented_button_unselected_color=theme.PALETTE["bg_secondary"],
            text_color=theme.PALETTE["text"],
        )
        tab_view.pack(fill="both", expand=True, padx=4, pady=4)

        for domain, items in learnings.items():
            tab = tab_view.add(domain.capitalize())
            scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
            scroll.pack(fill="both", expand=True)
            for item in items:
                self._add_card(scroll, item)

        return self._frame

    def _add_card(self, container: ctk.CTkScrollableFrame, item: dict):
        color = _SEVERITY_COLORS.get(item["severity"].lower(), _SEVERITY_COLORS["low"])
        card = ctk.CTkFrame(container, fg_color=theme.PALETTE["bg_secondary"],
                            corner_radius=8, border_width=1,
                            border_color=theme.PALETTE["border"])
        card.pack(fill="x", padx=6, pady=3)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(7, 3))
        ctk.CTkLabel(header, text=item["title"], font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=theme.PALETTE["text"]).pack(side="left")
        ctk.CTkLabel(header, text=item["severity"].upper(),
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=color).pack(side="right")

        MarkdownView(card, item["content"], height=110).pack(fill="x", padx=4, pady=(0, 6))
