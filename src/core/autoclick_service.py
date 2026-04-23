import time
import threading

from src.core import detector, clicker
from src.core.listener import InputListener
from src.core.monitors import get_all_monitors


class AutoclickService:
    def __init__(
        self,
        image_path: str,
        interval: float = 0.5,
        auto_stop: bool = False,
        on_click: callable = None,
        on_stop: callable = None,
    ):
        self._image_path = image_path
        self._interval = interval
        self._auto_stop = auto_stop
        self._on_click = on_click
        self._on_stop = on_stop
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._listener: InputListener | None = None

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._listener = InputListener(self._stop_event, self._auto_stop)
        self._listener.start()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._listener:
            self._listener.stop()

    def is_running(self) -> bool:
        return bool(self._thread and self._thread.is_alive())

    def _run(self):
        try:
            while not self._stop_event.is_set():
                coords = detector.locate(self._image_path)
                if coords:
                    x, y = coords
                    if clicker.click(x, y):
                        if self._on_click:
                            self._on_click(x, y)
                        time.sleep(0.4)
                    else:
                        time.sleep(self._interval)
                else:
                    time.sleep(self._interval)
        finally:
            if self._listener:
                self._listener.stop()
            if self._on_stop:
                self._on_stop()
