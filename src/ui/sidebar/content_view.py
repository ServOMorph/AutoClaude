"""Zone droite de la fenêtre Bibliothèque — affiche l'onglet actif."""

import customtkinter as ctk
from src.ui import theme
from src.ui.tabs.tips_tab import TipsTab
from src.ui.tabs.prompts_tab import PromptsTab
from src.ui.tabs.learning_tab import LearningTab

_TAB_CLASSES: dict[str, type] = {
    "tips": TipsTab,
    "prompts": PromptsTab,
    "learnings": LearningTab,
}


class ContentView(ctk.CTkFrame):
    """Zone de contenu — swap d'onglets dynamique."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=theme.PALETTE["bg"], **kwargs)
        self._current: ctk.CTkFrame | None = None

    def show_tab(self, tab_id: str):
        if self._current:
            self._current.destroy()
            self._current = None

        tab_cls = _TAB_CLASSES.get(tab_id)
        if tab_cls is None:
            ctk.CTkLabel(self, text=f"Onglet '{tab_id}' non implémenté.",
                         text_color=theme.PALETTE["text_muted"]).pack(expand=True)
            return

        tab = tab_cls(self)
        self._current = tab.render()
        self._current.pack(fill="both", expand=True)
