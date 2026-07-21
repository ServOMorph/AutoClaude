"""TODO: description du module."""

import threading
import time

try:
    from screeninfo import get_monitors as _get_monitors
except Exception:
    _get_monitors = None

try:
    import mss as _mss
except Exception:
    _mss = None

# screeninfo interroge l'API Win32 (EnumDisplayMonitors) à chaque appel — coûteux
# et instable en boucle serrée depuis un thread secondaire. La configuration des
# moniteurs change rarement : un cache avec TTL évite de la réinterroger à
# chaque tick de détection (toutes les 0.5s) sans perdre les reconfigurations.
_CACHE_TTL = 30.0
_cache: list[dict] = []
_cache_time = 0.0
_cache_lock = threading.Lock()


def _query_monitors() -> list[dict]:
    """TODO: description de _query_monitors."""
    monitors = []
    if _get_monitors:
        try:
            for m in _get_monitors():
                monitors.append({
                    "x": m.x, "y": m.y,
                    "width": m.width, "height": m.height,
                    "name": getattr(m, "name", "Unknown"),
                })
        except Exception:
            pass
    if not monitors and _mss:
        try:
            with _mss.mss() as sct:
                for i, m in enumerate(sct.monitors[1:], 1):
                    monitors.append({
                        "x": m["left"], "y": m["top"],
                        "width": m["width"], "height": m["height"],
                        "name": f"Monitor {i}",
                    })
        except Exception:
            pass
    return monitors


def get_all_monitors() -> list[dict]:
    """Retourne la liste des moniteurs, mise en cache pendant _CACHE_TTL secondes."""
    global _cache, _cache_time
    with _cache_lock:
        now = time.monotonic()
        if not _cache or now - _cache_time >= _CACHE_TTL:
            _cache = _query_monitors()
            _cache_time = now
        return _cache
