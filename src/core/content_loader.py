"""Loaders filesystem-driven pour src/content/ (tips, prompts, learnings)."""

from pathlib import Path
from src.config.constants import CONTENT_DIR


def _parse_md(path: Path) -> tuple[dict, str]:
    """Parse frontmatter + body depuis un fichier .md."""
    text = path.read_text(encoding="utf-8")
    meta: dict = {}
    content = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            content = parts[2].strip()
    return meta, content


def load_tips() -> list[dict]:
    """Scan CONTENT_DIR/tips/*.md → list[dict(title, category, content, file)]."""
    tips_dir = CONTENT_DIR / "tips"
    if not tips_dir.exists():
        return []
    result = []
    for f in sorted(tips_dir.glob("*.md")):
        meta, body = _parse_md(f)
        result.append({
            "title": meta.get("title", f.stem),
            "category": meta.get("category", f.stem),
            "content": body,
            "file": f.name,
        })
    return result


def load_prompts() -> list[dict]:
    """Scan CONTENT_DIR/prompts/*.md → list[dict(title, ia_target, tags, content, file)]."""
    prompts_dir = CONTENT_DIR / "prompts"
    if not prompts_dir.exists():
        return []
    result = []
    for f in sorted(prompts_dir.glob("*.md")):
        meta, body = _parse_md(f)
        tags_raw = meta.get("tags", "")
        result.append({
            "title": meta.get("title", f.stem),
            "ia_target": meta.get("ia_target", "all"),
            "tags": [t.strip() for t in tags_raw.split(",") if t.strip()],
            "content": body,
            "file": f.name,
        })
    return result


def load_learnings() -> dict[str, list[dict]]:
    """Scan CONTENT_DIR/learnings/**/*.md → dict[subdomain → list[dict]]."""
    learnings_dir = CONTENT_DIR / "learnings"
    if not learnings_dir.exists():
        return {}
    result: dict[str, list[dict]] = {}
    for sub in sorted(learnings_dir.iterdir()):
        if not sub.is_dir():
            continue
        items = []
        for f in sorted(sub.glob("*.md")):
            meta, body = _parse_md(f)
            items.append({
                "title": meta.get("title", f.stem),
                "severity": meta.get("severity", "low"),
                "content": body,
                "file": f.name,
            })
        if items:
            result[sub.name] = items
    return result
