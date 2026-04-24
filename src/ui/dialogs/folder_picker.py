"""TODO: description du module."""

from tkinter import filedialog


def pick_folder(title: str = "Sélectionner un dossier projet") -> str | None:
    """TODO: description de pick_folder."""
    path = filedialog.askdirectory(title=title)
    return path if path else None
