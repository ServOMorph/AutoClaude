"""Renderer .md → CTkScrollableFrame avec formatage basique."""

import customtkinter as ctk
from src.ui import theme


class MarkdownView(ctk.CTkScrollableFrame):
    """Affiche un contenu markdown en texte formaté dans un frame scrollable."""

    def __init__(self, parent, content: str, **kwargs):
        super().__init__(parent, fg_color=theme.PALETTE["bg_secondary"], **kwargs)
        self._render(content)

    def _render(self, text: str):
        in_code_block = False
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                self._add_code_line(stripped or " ")
            else:
                self._render_line(stripped)

    def _render_line(self, line: str):
        if not line:
            ctk.CTkLabel(self, text="", height=4).pack(anchor="w")
            return
        if line.startswith("### "):
            self._add_label(line[4:], size=12, weight="bold", color=theme.PALETTE["primary"])
        elif line.startswith("## "):
            self._add_label(line[3:], size=13, weight="bold", color=theme.PALETTE["text"])
        elif line.startswith("# "):
            self._add_label(line[2:], size=15, weight="bold", color=theme.PALETTE["primary"])
        elif line.startswith(("- ", "* ")):
            self._add_label("  • " + line[2:], size=11, color=theme.PALETTE["text"])
        elif line.startswith("|"):
            self._add_label(line, size=10, color=theme.PALETTE["text_muted"])
        else:
            self._add_label(line, size=11, color=theme.PALETTE["text"])

    def _add_label(self, text: str, size: int = 11, weight: str = "normal",
                   color: str | None = None):
        ctk.CTkLabel(
            self, text=text,
            font=ctk.CTkFont(size=size, weight=weight),
            text_color=color or theme.PALETTE["text"],
            wraplength=500, justify="left", anchor="w",
        ).pack(anchor="w", padx=8, pady=1)

    def _add_code_line(self, text: str):
        ctk.CTkLabel(
            self, text=text,
            font=ctk.CTkFont(family="Courier New", size=10),
            text_color=theme.PALETTE["primary"],
            wraplength=500, justify="left", anchor="w",
            fg_color=theme.PALETTE["bg"],
            corner_radius=4,
        ).pack(anchor="w", padx=12, pady=0, fill="x")
