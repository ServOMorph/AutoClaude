"""Bannière tips inline — remplace WarningBanner au démarrage."""

import customtkinter as ctk
from src.core.content_loader import load_tips
from src.config import settings
from src.ui import theme

_ACCENT = "#A5C9CA"
_BG = "#0f2030"


class TipsBanner(ctk.CTkFrame):
    """Tip du jour inline avec navigation et option désactivation."""

    def __init__(self, master, on_close: callable, **kwargs):
        super().__init__(master, fg_color=_BG, corner_radius=8, **kwargs)
        self._on_close = on_close
        self._tips = load_tips()
        self._index = 0

        # Bordure gauche accent (comme WarningBanner)
        ctk.CTkFrame(self, width=4, fg_color=_ACCENT, corner_radius=0).pack(
            side="left", fill="y"
        )

        self._body = ctk.CTkFrame(self, fg_color="transparent")
        self._body.pack(side="left", fill="both", expand=True, padx=10, pady=8)

        self._render()

    def _render(self):
        for w in self._body.winfo_children():
            w.destroy()

        if not self._tips:
            self._on_close()
            return

        tip = self._tips[self._index % len(self._tips)]

        # Ligne 1 — icône + titre
        top = ctk.CTkFrame(self._body, fg_color="transparent")
        top.pack(fill="x")

        ctk.CTkLabel(
            top, text="💡",
            font=ctk.CTkFont(size=14),
            text_color=_ACCENT,
        ).pack(side="left", padx=(0, 6))

        ctk.CTkLabel(
            top, text=tip["title"],
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=_ACCENT,
            anchor="w",
        ).pack(side="left", fill="x", expand=True)

        # Ligne 2 — contenu (2 premières lignes)
        lines = [l.strip() for l in tip["content"].splitlines() if l.strip() and not l.startswith("#")]
        preview = "  ".join(lines[:2])
        if len(lines) > 2:
            preview += " …"

        ctk.CTkLabel(
            self._body, text=preview,
            font=ctk.CTkFont(size=12),
            text_color=theme.PALETTE["text_muted"],
            wraplength=380, justify="left", anchor="w",
        ).pack(fill="x", pady=(4, 6))

        # Ligne 3 — boutons
        btns = ctk.CTkFrame(self._body, fg_color="transparent")
        btns.pack(fill="x")

        ctk.CTkButton(
            btns, text="💡 Autre tip",
            font=ctk.CTkFont(size=11),
            fg_color=theme.PALETTE["bg_secondary"],
            hover_color=theme.PALETTE["border"],
            text_color=_ACCENT,
            border_color=_ACCENT, border_width=1,
            height=26, width=100, corner_radius=6,
            command=self._next,
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            btns, text="Ne plus voir",
            font=ctk.CTkFont(size=11),
            fg_color="transparent",
            hover_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["text_muted"],
            height=26, width=100, corner_radius=6,
            command=self._disable,
        ).pack(side="left")

        ctk.CTkButton(
            btns, text="Fermer",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=_ACCENT, text_color="#000000",
            hover_color="#8ab5b6",
            height=26, width=80, corner_radius=6,
            command=self._on_close,
        ).pack(side="right")

    def _next(self):
        self._index = (self._index + 1) % len(self._tips)
        self._render()

    def _disable(self):
        settings.set("show_tips_on_start", False)
        self._on_close()
