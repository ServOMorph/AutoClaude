"""Onglet Prompts — bibliothèque copiable depuis src/content/prompts/."""

import customtkinter as ctk
from src.ui.tabs.base_tab import BaseTab
from src.core.content_loader import load_prompts
from src.ui import theme


class PromptsTab(BaseTab):
    label = "📋 Prompts"
    icon = "📋"

    def render(self) -> ctk.CTkFrame:
        prompts = load_prompts()
        if not prompts:
            ctk.CTkLabel(
                self._frame,
                text="Aucun prompt.\nAjouter un .md dans src/content/prompts/",
                text_color=theme.PALETTE["text_muted"],
                font=theme.font_body(),
            ).pack(expand=True)
            return self._frame

        scroll = ctk.CTkScrollableFrame(self._frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        for prompt in prompts:
            self._add_card(scroll, prompt)
        return self._frame

    def _add_card(self, container: ctk.CTkScrollableFrame, prompt: dict):
        card = ctk.CTkFrame(container, fg_color=theme.PALETTE["bg_secondary"],
                            corner_radius=8, border_width=1,
                            border_color=theme.PALETTE["border"])
        card.pack(fill="x", padx=8, pady=4)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(8, 2))
        ctk.CTkLabel(header, text=prompt["title"], font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=theme.PALETTE["primary"]).pack(side="left")
        ctk.CTkLabel(header, text=prompt["ia_target"],
                     font=ctk.CTkFont(size=10),
                     text_color=theme.PALETTE["text_muted"]).pack(side="right")

        preview = prompt["content"][:180] + ("…" if len(prompt["content"]) > 180 else "")
        ctk.CTkLabel(card, text=preview, font=theme.font_body(),
                     text_color=theme.PALETTE["text_muted"],
                     wraplength=440, justify="left").pack(anchor="w", padx=10, pady=(0, 6))

        ctk.CTkButton(
            card, text="📋 Copier", font=theme.font_body(),
            fg_color=theme.PALETTE["primary"], text_color="#000000",
            hover_color=theme.PALETTE["border"],
            width=80, height=26, corner_radius=6,
            command=lambda c=prompt["content"]: self._copy(c),
        ).pack(anchor="e", padx=10, pady=(0, 8))

    def _copy(self, content: str):
        try:
            self._frame.clipboard_clear()
            self._frame.clipboard_append(content)
        except Exception:
            pass
