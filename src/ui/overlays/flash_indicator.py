"""Indicateur visuel réutilisable affiché à la position d'un clic (debug)."""

import sys
import tkinter as tk


class FlashIndicator(tk.Toplevel):
    """Cercle rouge déplacé/affiché à chaque appel — instance unique réutilisée.

    Évite la création/destruction de CTkToplevel à chaque clic, qui sur de longues
    sessions peut causer des fuites de HWND/handles côté Tk + customtkinter.
    """

    SIZE = 48

    def __init__(self, master):
        super().__init__(master)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-transparentcolor", "black")

        if sys.platform == "win32":
            try:
                self.attributes("-toolwindow", True)
            except Exception:
                pass

        self.geometry(f"{self.SIZE}x{self.SIZE}+0+0")

        self._canvas = tk.Canvas(
            self,
            width=self.SIZE,
            height=self.SIZE,
            bg="black",
            highlightthickness=0,
        )
        self._canvas.pack()
        self._canvas.create_oval(
            3, 3, self.SIZE - 3, self.SIZE - 3,
            outline="red", width=4, fill="",
        )

        self._hide_after_id: str | None = None
        self.withdraw()

    def flash(self, x: int, y: int, duration_ms: int = 400) -> None:
        """Repositionne et affiche brièvement l'indicateur à (x, y)."""
        try:
            if not self.winfo_exists():
                return
            half = self.SIZE // 2
            self.geometry(f"{self.SIZE}x{self.SIZE}+{x - half}+{y - half}")
            self.deiconify()
            self.lift()
            if self._hide_after_id is not None:
                try:
                    self.after_cancel(self._hide_after_id)
                except Exception:
                    pass
            self._hide_after_id = self.after(duration_ms, self._hide)
        except Exception:
            pass

    def _hide(self) -> None:
        self._hide_after_id = None
        try:
            if self.winfo_exists():
                self.withdraw()
        except Exception:
            pass
