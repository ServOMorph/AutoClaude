"""TODO: description du module."""

import faulthandler
from pathlib import Path

from src.ui.app import AutoClaudeApp

if __name__ == "__main__":
    _crash_log = Path.home() / ".autoclaude" / "logs" / "crash.log"
    _crash_log.parent.mkdir(parents=True, exist_ok=True)
    faulthandler.enable(open(_crash_log, "a"))

    app = AutoClaudeApp()
    app.mainloop()
