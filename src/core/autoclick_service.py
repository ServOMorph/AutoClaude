"""TODO: description du module."""

import time
import threading

from src.core import detector, clicker, click_stats
from src.core.listener import InputListener
from src.core.monitors import get_all_monitors
from src.core.logger import get_logger

_MAX_RESTARTS = 3


class AutoclickService:
    """TODO: description de AutoclickService."""
    def __init__(
        self,
        image_path: str,
        interval: float = 0.5,
        auto_stop: bool = False,
        on_click: callable = None,
        on_stop: callable = None,
    ):
        """TODO: description de __init__."""
        self._image_path = image_path
        self._interval = interval
        self._auto_stop = auto_stop
        self._on_click = on_click
        self._on_stop = on_stop
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._listener: InputListener | None = None
        self._log = get_logger()

    def start(self):
        """TODO: description de start."""
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._listener = InputListener(self._stop_event, self._auto_stop)
        self._listener.start()
        self._thread = threading.Thread(target=self._run_with_restart, daemon=True, name="AutoclickWorker")
        self._thread.start()
        self._log.info("AutoclickService démarré (image=%s, interval=%.2fs)", self._image_path, self._interval)

    def stop(self):
        """TODO: description de stop."""
        self._stop_event.set()
        if self._listener:
            self._listener.stop()
        self._log.info("AutoclickService arrêté (signal envoyé)")

    def is_running(self) -> bool:
        """TODO: description de is_running."""
        return bool(self._thread and self._thread.is_alive())

    def _run_with_restart(self):
        """Wrapper qui relance _run jusqu'à _MAX_RESTARTS fois sur exception inattendue."""
        restarts = 0
        while not self._stop_event.is_set():
            try:
                self._run()
                break  # sortie propre
            except Exception as exc:
                restarts += 1
                self._log.error(
                    "Exception inattendue dans AutoclickService._run (tentative %d/%d) : %s",
                    restarts, _MAX_RESTARTS, exc, exc_info=True,
                )
                if restarts >= _MAX_RESTARTS:
                    self._log.error("Nombre max de redémarrages atteint — service arrêté définitivement")
                    break
                if not self._stop_event.is_set():
                    time.sleep(1)
        click_stats.flush_buffer()
        if self._listener:
            self._listener.stop()
        if self._on_stop:
            self._on_stop()

    def _run(self):
        """TODO: description de _run."""
        while not self._stop_event.is_set():
            coords = detector.locate(self._image_path)
            if coords:
                x, y = coords
                if clicker.click(x, y):
                    clicker.move_away()
                    click_stats.increment()
                    if self._on_click:
                        self._on_click(x, y)
                    time.sleep(2.0)  # laisser le bouton disparaître + Claude Code traiter avant la prochaine détection
                else:
                    time.sleep(self._interval)
            else:
                time.sleep(self._interval)
