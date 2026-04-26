"""TODO: description du module."""

import json
import threading
import time
from datetime import datetime, timezone, timedelta, date
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
        return {"total": 0, "events": [], "daily_totals": {}}
    try:
        data = json.loads(_STATS_FILE.read_text(encoding="utf-8"))
        if "daily_totals" not in data:
            data["daily_totals"] = {}
        return data
    except (json.JSONDecodeError, OSError):
        return {"total": 0, "events": [], "daily_totals": {}}


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

    # Mise à jour daily_totals — jamais purgé, source pour l'historique multi-année
    today_key = date.today().isoformat()
    daily = data.get("daily_totals", {})
    daily[today_key] = daily.get(today_key, 0) + _buffer_count
    data["daily_totals"] = daily

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
        _write_raw({"total": 0, "events": [], "daily_totals": {}})


def get_events() -> list[str]:
    """TODO: description de get_events."""
    with _lock:
        data = _load_raw()
        return data.get("events", []) + list(_buffer_events)


def get_daily_totals() -> dict[str, int]:
    """Retourne le dict daily_totals depuis disque, avec le buffer du jour en cours inclus."""
    with _lock:
        data = _load_raw()
        daily = dict(data.get("daily_totals", {}))
        if _buffer_count > 0:
            today_key = date.today().isoformat()
            daily[today_key] = daily.get(today_key, 0) + _buffer_count
        return daily


def aggregate_windowed(window: str) -> tuple[list[tuple[str, int]], dict]:
    """
    Agrège les clics sur une fenêtre temporelle précise.

    Fenêtres disponibles :
      "today"   — aujourd'hui heure par heure (source : events bruts)
      "7d"      — 7 derniers jours jour par jour (source : events bruts)
      "30d"     — 30 derniers jours jour par jour (source : events bruts)
      "12m"     — 12 derniers mois mois par mois (source : daily_totals)
      "all"     — toutes les années (source : daily_totals)

    Retourne (data, stats) où :
      data  = [(label, count), ...] trié chronologiquement
      stats = {"total": int, "avg_per_active_day": float, "record": int, "active_days": int}
    """
    now = datetime.now().astimezone()
    today = now.date()

    if window in ("today", "7d", "30d"):
        events = get_events()
        counts: dict[str, int] = defaultdict(int)
        day_counts: dict[str, int] = defaultdict(int)

        if window == "today":
            cutoff = now.replace(hour=0, minute=0, second=0, microsecond=0)
            for ts in events:
                try:
                    dt = datetime.fromisoformat(ts).astimezone()
                    if dt >= cutoff:
                        key = dt.strftime("%Hh")
                        counts[key] += 1
                except ValueError:
                    pass
            # Garantir toutes les heures 00h–heure actuelle dans l'ordre
            all_keys = [f"{h:02d}h" for h in range(now.hour + 1)]
            data = [(k, counts.get(k, 0)) for k in all_keys]
            day_counts["today"] = sum(v for v in counts.values())

        else:
            n_days = 7 if window == "7d" else 30
            cutoff_date = today - timedelta(days=n_days - 1)
            for ts in events:
                try:
                    dt = datetime.fromisoformat(ts).astimezone()
                    d = dt.date()
                    if d >= cutoff_date:
                        key = dt.strftime("%d/%m")
                        counts[key] += 1
                        day_counts[d.isoformat()] += 1
                except ValueError:
                    pass
            # Garantir tous les jours dans l'ordre
            all_keys = [
                (cutoff_date + timedelta(days=i)).strftime("%d/%m")
                for i in range(n_days)
            ]
            data = [(k, counts.get(k, 0)) for k in all_keys]

    else:
        daily = get_daily_totals()
        counts = defaultdict(int)
        day_counts: dict[str, int] = defaultdict(int)

        if window == "12m":
            # 12 derniers mois (mois glissant)
            months = []
            for i in range(11, -1, -1):
                if today.month - i > 0:
                    m = today.replace(month=today.month - i, day=1)
                else:
                    m = today.replace(year=today.year - 1, month=today.month - i + 12, day=1)
                months.append(m)

            for day_str, cnt in daily.items():
                try:
                    d = date.fromisoformat(day_str)
                    key = d.strftime("%b %Y")
                    counts[key] += cnt
                    day_counts[day_str] += cnt
                except ValueError:
                    pass

            all_keys = [m.strftime("%b %Y") for m in months]
            data = [(k, counts.get(k, 0)) for k in all_keys]

        else:  # "all"
            for day_str, cnt in daily.items():
                try:
                    d = date.fromisoformat(day_str)
                    key = str(d.year)
                    counts[key] += cnt
                    day_counts[day_str] += cnt
                except ValueError:
                    pass
            data = sorted(counts.items())

    # Calcul des stats
    total = sum(v for _, v in data)
    active_days = sum(1 for v in day_counts.values() if v > 0) if day_counts else sum(1 for _, v in data if v > 0)
    record = max((v for _, v in data), default=0)
    avg = round(total / active_days, 1) if active_days > 0 else 0.0

    stats = {
        "total": total,
        "avg_per_active_day": avg,
        "record": record,
        "active_days": active_days,
    }
    return data, stats


def aggregate(period: str) -> list[tuple[str, int]]:
    """Compatibilité — préférer aggregate_windowed()."""
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
