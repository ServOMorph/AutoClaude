"""TODO: description du module."""

import json
from pathlib import Path
from src.config.constants import DEFAULT_INTERVAL

_SETTINGS_DIR = Path.home() / ".autoclaude"
_SETTINGS_FILE = _SETTINGS_DIR / "settings.json"

_DEFAULTS = {
    "interval": DEFAULT_INTERVAL,
    "auto_stop": False,
    "image_path": "",
    "overlay_enabled": True,
}


def load() -> dict:
    """TODO: description de load."""
    if not _SETTINGS_FILE.exists():
        return dict(_DEFAULTS)
    try:
        data = json.loads(_SETTINGS_FILE.read_text(encoding="utf-8"))
        return {**_DEFAULTS, **data}
    except (json.JSONDecodeError, OSError):
        return dict(_DEFAULTS)


def save(settings: dict) -> None:
    """TODO: description de save."""
    _SETTINGS_DIR.mkdir(parents=True, exist_ok=True)
    _SETTINGS_FILE.write_text(
        json.dumps(settings, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def get(key: str):
    """TODO: description de get."""
    return load().get(key, _DEFAULTS.get(key))


def set(key: str, value) -> None:
    """TODO: description de set."""
    data = load()
    data[key] = value
    save(data)
