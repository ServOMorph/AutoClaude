"""TODO: description du module."""

import customtkinter as ctk
from src.config.constants import (
    COLOR_BG, COLOR_BG_SECONDARY, COLOR_PRIMARY,
    COLOR_SUCCESS, COLOR_WARNING, COLOR_TEXT,
    COLOR_TEXT_MUTED, COLOR_BORDER,
)

_FONT_FAMILY_PREFERRED = "Space Grotesk"
_FONT_FAMILY_FALLBACK = "Segoe UI"


def _resolve_font_family() -> str:
    """TODO: description de _resolve_font_family."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    families = tk.font.families(root)
    root.destroy()
    return _FONT_FAMILY_PREFERRED if _FONT_FAMILY_PREFERRED in families else _FONT_FAMILY_FALLBACK


_font_family: str | None = None


def _font() -> str:
    """TODO: description de _font."""
    global _font_family
    if _font_family is None:
        try:
            _font_family = _resolve_font_family()
        except Exception:
            _font_family = _FONT_FAMILY_FALLBACK
    return _font_family


def apply():
    """TODO: description de apply."""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")


def font_title() -> ctk.CTkFont:
    """TODO: description de font_title."""
    return ctk.CTkFont(family=_font(), size=40, weight="bold")


def font_subtitle() -> ctk.CTkFont:
    """TODO: description de font_subtitle."""
    return ctk.CTkFont(family=_font(), size=13, weight="bold")


def font_body() -> ctk.CTkFont:
    """TODO: description de font_body."""
    return ctk.CTkFont(family=_font(), size=12)


def font_small() -> ctk.CTkFont:
    """TODO: description de font_small."""
    return ctk.CTkFont(family=_font(), size=20)


PALETTE = {
    "bg": COLOR_BG,
    "bg_secondary": COLOR_BG_SECONDARY,
    "primary": COLOR_PRIMARY,
    "success": COLOR_SUCCESS,
    "warning": COLOR_WARNING,
    "text": COLOR_TEXT,
    "text_muted": COLOR_TEXT_MUTED,
    "border": COLOR_BORDER,
}
