import json
import threading
from datetime import datetime
from pathlib import Path
from collections import defaultdict

_STATS_DIR = Path.home() / ".autoclaude"
_STATS_FILE = _STATS_DIR / "click_stats.json"

_lock = threading.Lock()


def _load_raw() -> dict:
    if not _STATS_FILE.exists():
        return {"total": 0, "events": []}
    try:
        return json.loads(_STATS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"total": 0, "events": []}


def _flush(data: dict) -> None:
    _STATS_DIR.mkdir(parents=True, exist_ok=True)
    _STATS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def increment() -> None:
    with _lock:
        ts = datetime.now().astimezone().isoformat()
        data = _load_raw()
        data["total"] = data.get("total", 0) + 1
        data["events"] = data.get("events", []) + [ts]
        _flush(data)


def flush_buffer() -> None:
    pass


def get_total() -> int:
    with _lock:
        return _load_raw().get("total", 0)


def reset() -> None:
    with _lock:
        _flush({"total": 0, "events": []})


def get_events() -> list[str]:
    with _lock:
        return _load_raw().get("events", [])


def aggregate(period: str) -> list[tuple[str, int]]:
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
