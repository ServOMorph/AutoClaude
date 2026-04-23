from tkinter import filedialog


def pick_folder(title: str = "Sélectionner un dossier projet") -> str | None:
    path = filedialog.askdirectory(title=title)
    return path if path else None
