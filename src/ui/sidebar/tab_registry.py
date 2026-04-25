"""Génère la registry d'onglets depuis src/content/ (filesystem-driven)."""

from src.config.constants import CONTENT_DIR

_TAB_CONFIG = {
    "tips": {"label": "💡 Tips", "order": 0},
    "prompts": {"label": "📋 Prompts", "order": 1},
    "learnings": {"label": "📚 Learnings", "order": 2},
}


def build_registry() -> list[dict]:
    """Scan CONTENT_DIR, retourne onglets ayant du contenu .md."""
    if not CONTENT_DIR.exists():
        return []
    registry = []
    for subdir in CONTENT_DIR.iterdir():
        if not subdir.is_dir() or subdir.name not in _TAB_CONFIG:
            continue
        if any(subdir.rglob("*.md")):
            cfg = _TAB_CONFIG[subdir.name]
            registry.append({"id": subdir.name, "label": cfg["label"], "order": cfg["order"]})
    registry.sort(key=lambda x: x["order"])
    return registry
