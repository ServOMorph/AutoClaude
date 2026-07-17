"""TODO: description du module."""

import faulthandler
import gc
from pathlib import Path

from src.ui.app import AutoClaudeApp

if __name__ == "__main__":
    _crash_log = Path.home() / ".autoclaude" / "logs" / "crash.log"
    _crash_log.parent.mkdir(parents=True, exist_ok=True)
    faulthandler.enable(open(_crash_log, "a"))

    # Le gc automatique peut se déclencher dans n'importe quel thread (ex. le
    # worker autoclick, qui alloue des arrays numpy en continu). Finaliser un
    # objet Tk (CTkFont, Variable, image...) hors du thread principal corrompt
    # l'état natif de l'interpréteur Tcl → crash access violation différé dans
    # tk86t.dll. On désactive le gc générationnel automatique ; AutoClaudeApp
    # déclenche un gc.collect() explicite, périodiquement, dans le thread Tk.
    gc.disable()

    app = AutoClaudeApp()
    app.mainloop()
