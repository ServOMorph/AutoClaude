"""Fenêtre Bibliothèque — hub dynamique (tips, prompts, learnings)."""

import customtkinter as ctk
from src.ui.sidebar.tab_registry import build_registry
from src.ui.sidebar.sidebar_panel import SidebarPanel
from src.ui.sidebar.content_view import ContentView
from src.ui import theme


class LibraryWindow(ctk.CTkToplevel):
    """Fenêtre hub bibliothèque."""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("📚 Bibliothèque AutoClaude")
        self.geometry("820x560")
        self.resizable(True, True)
        self.configure(fg_color=theme.PALETTE["bg"])
        self.lift()
        self.focus_force()

        registry = build_registry()
        if not registry:
            ctk.CTkLabel(
                self,
                text="Aucun contenu trouvé.\nAjouter des .md dans src/content/",
                text_color=theme.PALETTE["text_muted"],
                font=ctk.CTkFont(size=13),
            ).pack(expand=True)
            return

        self._content_view = ContentView(self)

        SidebarPanel(self, registry, on_select=self._content_view.show_tab).pack(
            side="left", fill="y"
        )
        ctk.CTkFrame(self, fg_color=theme.PALETTE["border"], width=1).pack(
            side="left", fill="y"
        )
        self._content_view.pack(side="left", fill="both", expand=True)
