"""Watchdog interne : snapshots mémoire/handles/threads toutes les 5 minutes."""

import gc
import threading
import time

try:
    import psutil as _psutil
except ImportError:
    _psutil = None

from src.core.logger import get_logger

_INTERVAL = 300  # 5 minutes
_WARN_RSS_MB = 500
_WARN_HANDLES = 5000
_WARN_THREADS = 20

_monitor_thread: threading.Thread | None = None
_stop_event = threading.Event()


def _snapshot() -> dict:
    if not _psutil:
        return {}
    try:
        p = _psutil.Process()
        return {
            "rss_mb": round(p.memory_info().rss / 1024 / 1024, 1),
            "handles": p.num_handles() if hasattr(p, "num_handles") else 0,
            "threads": p.num_threads(),
        }
    except Exception:
        return {}


def _loop():
    log = get_logger()
    log.info("HealthMonitor démarré")
    while not _stop_event.wait(_INTERVAL):
        # Force la collecte cyclique — Tk garde des références circulaires
        # (after callbacks, widget→master) qui s'accumulent sur sessions longues.
        collected = gc.collect()
        snap = _snapshot()
        if not snap:
            continue
        log.info(
            "Santé — RSS: %(rss_mb)s Mo | handles: %(handles)s | threads: %(threads)s | gc: %(gc)s",
            {**snap, "gc": collected},
        )
        if snap.get("rss_mb", 0) > _WARN_RSS_MB:
            log.warning("RSS élevé : %.1f Mo (seuil %d Mo)", snap["rss_mb"], _WARN_RSS_MB)
        if snap.get("handles", 0) > _WARN_HANDLES:
            log.warning("Handles élevés : %d (seuil %d)", snap["handles"], _WARN_HANDLES)
        if snap.get("threads", 0) > _WARN_THREADS:
            log.warning("Threads élevés : %d (seuil %d)", snap["threads"], _WARN_THREADS)
    log.info("HealthMonitor arrêté")


def start():
    global _monitor_thread
    if _monitor_thread and _monitor_thread.is_alive():
        return
    _stop_event.clear()
    _monitor_thread = threading.Thread(target=_loop, daemon=True, name="HealthMonitor")
    _monitor_thread.start()


def stop():
    _stop_event.set()


def get_health_snapshot() -> dict:
    return _snapshot()
