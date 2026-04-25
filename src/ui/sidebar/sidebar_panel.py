"""Panneau gauche de navigation — boutons onglets dynamiques."""

import customtkinter as ctk
from src.ui import theme


class SidebarPanel(ctk.CTkFrame):
    """Nav gauche avec boutons dynamiques depuis la registry."""

    def __init__(self, parent, registry: list[dict], on_select, **kwargs):
        super().__init__(parent, fg_color=theme.PALETTE["bg_secondary"],
                         corner_radius=0, width=160, **kwargs)
        self.pack_propagate(False)
        self._buttons: dict[str, ctk.CTkButton] = {}
        self._on_select = on_select

        ctk.CTkLabel(self, text="Bibliothèque", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=theme.PALETTE["text"]).pack(pady=(16, 8), padx=12, anchor="w")

        for tab in registry:
            btn = ctk.CTkButton(
                self, text=tab["label"], font=theme.font_body(),
                fg_color="transparent", hover_color=theme.PALETTE["border"],
                text_color=theme.PALETTE["text"],
                anchor="w", corner_radius=6, height=36,
                command=lambda t=tab: self._select(t["id"]),
            )
            btn.pack(fill="x", padx=8, pady=2)
            self._buttons[tab["id"]] = btn

        if registry:
            self._select(registry[0]["id"])

    def _select(self, tab_id: str):
        for bid, btn in self._buttons.items():
            active = bid == tab_id
            btn.configure(
                fg_color=theme.PALETTE["primary"] if active else "transparent",
                text_color="#000000" if active else theme.PALETTE["text"],
            )
        self._on_select(tab_id)
