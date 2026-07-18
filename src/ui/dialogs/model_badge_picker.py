"""Dialogue de création de badge modèle : sélection fenêtre VSCode + modèle."""

import customtkinter as ctk
from src.core.window_tracker import list_vscode_windows
from src.ui.overlays.model_badge import MODEL_OPTIONS
from src.ui import theme


class ModelBadgePicker(ctk.CTkToplevel):
    """Modal de sélection : fenêtre VSCode cible + modèle initial du badge."""

    def __init__(self, master):
        super().__init__(master)
        self.title("Créer un badge modèle")
        self.geometry("360x220")
        self.resizable(False, False)
        self.configure(fg_color=theme.PALETTE["bg"])
        self.result = None

        self._windows = list_vscode_windows()
        titles = [title for _, title in self._windows] or ["Aucune fenêtre VSCode détectée"]

        ctk.CTkLabel(self, text="Fenêtre VSCode cible", text_color=theme.PALETTE["text"]).pack(pady=(16, 4))
        self._window_var = ctk.StringVar(value=titles[0])
        ctk.CTkOptionMenu(self, values=titles, variable=self._window_var).pack(pady=(0, 12))

        ctk.CTkLabel(self, text="Modèle", text_color=theme.PALETTE["text"]).pack(pady=(0, 4))
        self._model_var = ctk.StringVar(value=MODEL_OPTIONS[0])
        ctk.CTkOptionMenu(self, values=MODEL_OPTIONS, variable=self._model_var).pack(pady=(0, 16))

        btn_row = ctk.CTkFrame(self, fg_color="transparent")
        btn_row.pack()
        ctk.CTkButton(btn_row, text="Créer", command=self._confirm).pack(side="left", padx=8)
        ctk.CTkButton(btn_row, text="Annuler", command=self._cancel).pack(side="left", padx=8)

        self.protocol("WM_DELETE_WINDOW", self._cancel)
        self.transient(master)
        self.grab_set()

    def _confirm(self):
        if not self._windows:
            self._cancel()
            return
        title = self._window_var.get()
        hwnd = next((h for h, t in self._windows if t == title), None)
        if hwnd is None:
            self._cancel()
            return
        self.result = (hwnd, title, self._model_var.get())
        self.destroy()

    def _cancel(self):
        self.result = None
        self.destroy()


def pick_model_badge_target(master):
    """Ouvre le dialogue modal, renvoie `(hwnd, titre, modele)` ou None si annulé."""
    dialog = ModelBadgePicker(master)
    master.wait_window(dialog)
    return dialog.result
