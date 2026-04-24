"""TODO: description du module."""

import threading

try:
    from pynput import keyboard as _keyboard, mouse as _mouse
except Exception:
    _keyboard = None
    _mouse = None

_MOUSE_THRESHOLD = 50


class InputListener:
    """TODO: description de InputListener."""
    def __init__(self, stop_event: threading.Event, auto_stop: bool = False):
        """TODO: description de __init__."""
        self._stop_event = stop_event
        self._auto_stop = auto_stop
        self._last_mouse_pos = None
        self._kb_listener = None
        self._mouse_listener = None

    def start(self):
        """TODO: description de start."""
        if _keyboard:
            self._kb_listener = _keyboard.Listener(on_press=self._on_press)
            self._kb_listener.start()
        if _mouse and self._auto_stop:
            self._mouse_listener = _mouse.Listener(on_move=self._on_mouse_move)
            self._mouse_listener.start()

    def stop(self):
        """TODO: description de stop."""
        if self._kb_listener:
            self._kb_listener.stop()
        if self._mouse_listener:
            self._mouse_listener.stop()

    def has_keyboard(self) -> bool:
        """TODO: description de has_keyboard."""
        return bool(_keyboard)

    def _on_press(self, key):
        """TODO: description de _on_press."""
        try:
            if key == _keyboard.Key.esc:
                self._stop_event.set()
                return False
            if self._auto_stop:
                self._stop_event.set()
                return False
        except Exception:
            pass

    def _on_mouse_move(self, x, y):
        """TODO: description de _on_mouse_move."""
        if not self._auto_stop:
            return
        if self._last_mouse_pos is None:
            self._last_mouse_pos = (x, y)
            return
        dx = abs(x - self._last_mouse_pos[0])
        dy = abs(y - self._last_mouse_pos[1])
        if dx > _MOUSE_THRESHOLD or dy > _MOUSE_THRESHOLD:
            self._stop_event.set()
            return False
        self._last_mouse_pos = (x, y)
