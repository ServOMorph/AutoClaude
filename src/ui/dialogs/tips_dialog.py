"""Dialog tip du jour — design soigné, centré sur la fenêtre principale."""

import random
import customtkinter as ctk
from src.config import settings
from src.core.content_loader import load_tips
from src.ui import theme
from src.ui.tabs.markdown_tab import MarkdownView

_W, _H = 460, 480
_HEADER_COLOR = "#1C2F3F"
_ACCENT = "#A5C9CA"
_BADGE_BG = "#24404F"


class TipsDialog(ctk.CTkToplevel):
    """Tip du jour — superposé à la fenêtre principale, design SéréniaTech."""

    def __init__(self, parent):
        super().__init__(parent)

        tips = load_tips()
        if not tips:
            self.destroy()
            return

        random.shuffle(tips)
        self._tips = tips
        self._index = 0

        self.overrideredirect(True)
        self.configure(fg_color=theme.PALETTE["bg"])
        self.attributes("-topmost", True)

        # Bordure visible via frame wrapper
        border = ctk.CTkFrame(self, fg_color=_ACCENT, corner_radius=14)
        border.pack(fill="both", expand=True, padx=1, pady=1)

        self._inner = ctk.CTkFrame(border, fg_color=theme.PALETTE["bg"], corner_radius=12)
        self._inner.pack(fill="both", expand=True, padx=1, pady=1)

        self._build()
        self._center_on(parent)
        self.lift()
        self.focus_force()

    # ─── Layout ───────────────────────────────────────────────────────────────

    def _build(self):
        for w in self._inner.winfo_children():
            w.destroy()

        tip = self._tips[self._index]

        # Header
        header = ctk.CTkFrame(self._inner, fg_color=_HEADER_COLOR, corner_radius=0,
                               height=72)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Bouton fermer custom
        ctk.CTkButton(
            header, text="✕", width=28, height=28,
            fg_color="transparent", hover_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["text_muted"],
            font=ctk.CTkFont(size=14), corner_radius=6,
            command=self.destroy,
        ).place(relx=1.0, rely=0.0, anchor="ne", x=-8, y=8)

        # Icône + label
        icon_frame = ctk.CTkFrame(header, fg_color=_BADGE_BG, corner_radius=10,
                                   width=38, height=38)
        icon_frame.place(x=16, rely=0.5, anchor="w")
        icon_frame.pack_propagate(False)
        ctk.CTkLabel(icon_frame, text="💡", font=ctk.CTkFont(size=20),
                     fg_color="transparent").pack(expand=True)

        title_col = ctk.CTkFrame(header, fg_color="transparent")
        title_col.place(x=64, rely=0.5, anchor="w")

        ctk.CTkLabel(
            title_col, text="Tip du jour",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=_ACCENT,
        ).pack(anchor="w")

        badge_row = ctk.CTkFrame(title_col, fg_color="transparent")
        badge_row.pack(anchor="w", pady=(2, 0))

        self._badge(badge_row, tip["category"])

        # Navigation
        nav = ctk.CTkFrame(header, fg_color="transparent")
        nav.place(relx=1.0, rely=1.0, anchor="se", x=-12, y=-8)

        ctk.CTkLabel(
            nav,
            text=f"{self._index + 1} / {len(self._tips)}",
            font=ctk.CTkFont(size=11),
            text_color=theme.PALETTE["text_muted"],
        ).pack(side="left", padx=(0, 6))

        if len(self._tips) > 1:
            ctk.CTkButton(
                nav, text="›", width=28, height=24,
                fg_color=_BADGE_BG, hover_color=theme.PALETTE["border"],
                text_color=_ACCENT, font=ctk.CTkFont(size=14, weight="bold"),
                corner_radius=6,
                command=self._next,
            ).pack(side="left")

        # Séparateur
        ctk.CTkFrame(self._inner, fg_color=_ACCENT, height=1).pack(fill="x")

        # Titre tip
        ctk.CTkLabel(
            self._inner, text=tip["title"],
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=theme.PALETTE["text"],
            wraplength=400, justify="left",
        ).pack(anchor="w", padx=20, pady=(14, 4))

        # Contenu markdown
        MarkdownView(
            self._inner, tip["content"],
            height=230,
            fg_color=theme.PALETTE["bg_secondary"],
        ).pack(fill="x", padx=16, pady=(0, 12))

        # Footer
        ctk.CTkFrame(self._inner, fg_color=theme.PALETTE["border"], height=1).pack(fill="x", padx=0)

        footer = ctk.CTkFrame(self._inner, fg_color="transparent")
        footer.pack(fill="x", padx=16, pady=10)

        self._no_show_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            footer,
            text="Ne plus afficher au démarrage",
            variable=self._no_show_var,
            font=ctk.CTkFont(size=11),
            text_color=theme.PALETTE["text_muted"],
            fg_color=_ACCENT, checkmark_color="#000000",
            hover_color=_BADGE_BG,
            border_color=theme.PALETTE["border"],
            width=20, height=20,
        ).pack(side="left")

        ctk.CTkButton(
            footer, text="Fermer",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=_ACCENT, text_color="#000000",
            hover_color="#8ab5b6",
            width=90, height=32, corner_radius=8,
            command=self._close,
        ).pack(side="right")

    # ─── Helpers ──────────────────────────────────────────────────────────────

    def _badge(self, parent, text: str):
        ctk.CTkLabel(
            parent, text=text,
            font=ctk.CTkFont(size=10),
            text_color=_ACCENT,
            fg_color=_BADGE_BG,
            corner_radius=6,
            padx=8, pady=2,
        ).pack(side="left", padx=(0, 4))

    def _next(self):
        self._index = (self._index + 1) % len(self._tips)
        self._build()

    def _close(self):
        if self._no_show_var.get():
            settings.set("show_tips_on_start", False)
        self.destroy()

    def _center_on(self, parent):
        self.update_idletasks()
        px = parent.winfo_x()
        py = parent.winfo_y()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        x = px + (pw - _W) // 2
        y = py + (ph - _H) // 2
        self.geometry(f"{_W}x{_H}+{x}+{y}")
