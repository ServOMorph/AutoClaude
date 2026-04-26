"""TODO: description du module."""

import json
import threading
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import defaultdict

from src.core.logger import get_logger

_STATS_DIR = Path.home() / ".autoclaude"
_STATS_FILE = _STATS_DIR / "click_stats.json"

_lock = threading.Lock()

# Buffer en mémoire pour éviter un write disque à chaque clic
_buffer_count = 0
_buffer_events: list[str] = []
_FLUSH_EVERY = 20       # flush toutes les 20 clics
_FLUSH_INTERVAL = 60.0  # flush toutes les 60 secondes au plus tard
_EVENTS_MAX_DAYS = 365  # on ne conserve que les 365 derniers jours d'événements

_last_flush_time = time.monotonic()

# Cache du total sur disque — évite de relire le JSON à chaque appel get_total()
_total_on_disk: int | None = None


def _load_raw() -> dict:
    if not _STATS_FILE.exists():
        return {"total": 0, "events": []}
    try:
        return json.loads(_STATS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"total": 0, "events": []}


def _prune_events(events: list[str]) -> list[str]:
    """Supprime les événements de plus de _EVENTS_MAX_DAYS jours."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=_EVENTS_MAX_DAYS)
    pruned = []
    for ts in events:
        try:
            if datetime.fromisoformat(ts).astimezone(timezone.utc) >= cutoff:
                pruned.append(ts)
        except ValueError:
            pass
    return pruned


def _write_raw(data: dict) -> None:
    _STATS_DIR.mkdir(parents=True, exist_ok=True)
    tmp = _STATS_FILE.with_suffix(".tmp")
    try:
        tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(_STATS_FILE)
    except OSError as exc:
        get_logger().error("Erreur écriture click_stats : %s", exc)
        try:
            tmp.unlink(missing_ok=True)
        except OSError:
            pass


def _ensure_total_cache() -> None:
    """Charge le total depuis le disque si le cache est vide. Doit être appelé sous _lock."""
    global _total_on_disk
    if _total_on_disk is None:
        _total_on_disk = _load_raw().get("total", 0)


def _flush_locked(data: dict | None = None) -> None:
    """Flush le buffer vers le disque. Doit être appelé sous _lock."""
    global _buffer_count, _buffer_events, _last_flush_time, _total_on_disk
    if not _buffer_events and _buffer_count == 0:
        return
    if data is None:
        data = _load_raw()
    new_total = data.get("total", 0) + _buffer_count
    data["total"] = new_total
    data["events"] = _prune_events(data.get("events", []) + _buffer_events)
    _write_raw(data)
    _total_on_disk = new_total
    _buffer_count = 0
    _buffer_events = []
    _last_flush_time = time.monotonic()


def increment() -> None:
    """TODO: description de increment."""
    global _buffer_count, _buffer_events
    with _lock:
        ts = datetime.now().astimezone().isoformat()
        _buffer_count += 1
        _buffer_events.append(ts)
        if _buffer_count >= _FLUSH_EVERY or (time.monotonic() - _last_flush_time) >= _FLUSH_INTERVAL:
            _flush_locked()


def flush_buffer() -> None:
    """Flush explicite — à appeler à l'arrêt du service."""
    with _lock:
        _flush_locked()


def get_total() -> int:
    """TODO: description de get_total."""
    with _lock:
        _ensure_total_cache()
        return _total_on_disk + _buffer_count


def reset() -> None:
    """TODO: description de reset."""
    global _buffer_count, _buffer_events, _total_on_disk
    with _lock:
        _buffer_count = 0
        _buffer_events = []
        _total_on_disk = 0
        _write_raw({"total": 0, "events": []})


def get_events() -> list[str]:
    """TODO: description de get_events."""
    with _lock:
        data = _load_raw()
        return data.get("events", []) + list(_buffer_events)


def aggregate(period: str) -> list[tuple[str, int]]:
    """TODO: description de aggregate."""
    events = get_events()
    counts: dict[str, int] = defaultdict(int)

    for ts in events:
        try:
            dt = datetime.fromisoformat(ts).astimezone()
        except ValueError:
            continue
        if period == "hour":
            key = dt.strftime("%H:00")
        elif period == "day":
            key = dt.strftime("%d/%m")
        elif period == "week":
            key = f"S{dt.isocalendar().week:02d}"
        elif period == "month":
            key = dt.strftime("%b %Y")
        elif period == "year":
            key = dt.strftime("%Y")
        else:
            key = dt.strftime("%d/%m")
        counts[key] += 1

    return sorted(counts.items())
