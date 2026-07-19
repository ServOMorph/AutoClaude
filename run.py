"""Point d'entrée : crash-log faulthandler, sentinelle de session, gc manuel."""

import faulthandler
import gc
import os
from datetime import datetime
from pathlib import Path

from src.config.constants import VERSION
from src.core.logger import get_logger
from src.ui.app import AutoClaudeApp

_LOG_DIR = Path.home() / ".autoclaude" / "logs"
_CRASH_LOG = _LOG_DIR / "crash.log"
_CRASH_LOG_MAX_BYTES = 1024 * 1024
_SENTINEL = _LOG_DIR / "session.lock"


def _trim_crash_log():
    """Tronque crash.log en conservant la fin (pas de rotation faulthandler)."""
    try:
        if _CRASH_LOG.exists() and _CRASH_LOG.stat().st_size > _CRASH_LOG_MAX_BYTES:
            _CRASH_LOG.write_bytes(_CRASH_LOG.read_bytes()[-_CRASH_LOG_MAX_BYTES // 2:])
    except OSError:
        pass


if __name__ == "__main__":
    _LOG_DIR.mkdir(parents=True, exist_ok=True)
    _trim_crash_log()

    log = get_logger()
    if _SENTINEL.exists():
        log.warning("Session précédente terminée anormalement (crash probable) — voir crash.log")
    _SENTINEL.touch()

    # faulthandler n'horodate pas ses dumps : chaque crash est daté par
    # encadrement entre deux marqueurs de session.
    _crash_file = open(_CRASH_LOG, "a", encoding="utf-8")
    _crash_file.write(
        f"\n=== session {datetime.now().isoformat(timespec='seconds')} "
        f"pid={os.getpid()} v{VERSION} ===\n"
    )
    _crash_file.flush()
    faulthandler.enable(_crash_file)

    # Le gc automatique peut se déclencher dans n'importe quel thread (ex. le
    # worker autoclick, qui alloue des arrays numpy en continu). Finaliser un
    # objet Tk (CTkFont, Variable, image...) hors du thread principal corrompt
    # l'état natif de l'interpréteur Tcl → crash access violation différé dans
    # tk86t.dll. On désactive le gc générationnel automatique ; AutoClaudeApp
    # déclenche un gc.collect() explicite, périodiquement, dans le thread Tk.
    gc.disable()

    app = AutoClaudeApp()
    app.mainloop()

    _SENTINEL.unlink(missing_ok=True)
