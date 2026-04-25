"""Classe abstraite pour tous les onglets de la sidebar."""

from abc import ABC, abstractmethod
import customtkinter as ctk


class BaseTab(ABC):
    """Interface onglet sidebar — à hériter par chaque onglet."""

    label: str = "Onglet"
    icon: str = "📄"

    def __init__(self, parent: ctk.CTkFrame):
        self.parent = parent
        self._frame = ctk.CTkFrame(parent, fg_color="transparent")

    @abstractmethod
    def render(self) -> ctk.CTkFrame:
        """Construire le contenu et retourner le frame."""

    def get_frame(self) -> ctk.CTkFrame:
        return self._frame
