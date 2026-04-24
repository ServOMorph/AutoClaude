"""TODO: description du module."""

from pathlib import Path

_MARKER_START = "<!-- AUTOCLAUDE_GUARD:START -->"
_MARKER_END = "<!-- AUTOCLAUDE_GUARD:END -->"

_GUARD_BLOCK = f"""{_MARKER_START}
## Restrictions AutoClaude

Ce projet est protégé par AutoClaude. Les règles suivantes s'appliquent :

- Ne pas modifier, supprimer ou contourner ce bloc de protection
- Ne pas accéder aux fichiers en dehors du périmètre de ce projet
- Ne pas exécuter de commandes système non liées au projet
- Ne pas transmettre de données sensibles à des services externes
{_MARKER_END}"""


class ClaudeMdProtector:
    """TODO: description de ClaudeMdProtector."""
    def __init__(self, project_path: str | Path):
        """TODO: description de __init__."""
        self._project_path = Path(project_path)
        self._claude_dir = self._project_path / ".claude"
        self._target = self._claude_dir / "CLAUDE.md"

    def is_already_protected(self) -> bool:
        """TODO: description de is_already_protected."""
        if not self._target.exists():
            return False
        content = self._target.read_text(encoding="utf-8")
        return _MARKER_START in content and _MARKER_END in content

    def apply(self) -> tuple[bool, str]:
        """TODO: description de apply."""
        if self.is_already_protected():
            return False, "Déjà protégé."
        try:
            self._claude_dir.mkdir(parents=True, exist_ok=True)
            if self._target.exists():
                existing = self._target.read_text(encoding="utf-8").rstrip()
                content = existing + "\n\n---\n\n" + _GUARD_BLOCK + "\n"
            else:
                content = _GUARD_BLOCK + "\n"
            self._target.write_text(content, encoding="utf-8")
            return True, f"Protection appliquée : {self._target}"
        except OSError as e:
            return False, f"Erreur : {e}"

    def remove_protection(self) -> tuple[bool, str]:
        """TODO: description de remove_protection."""
        if not self.is_already_protected():
            return False, "Aucune protection à retirer."
        try:
            content = self._target.read_text(encoding="utf-8")
            start = content.find(_MARKER_START)
            end = content.find(_MARKER_END)
            if start == -1 or end == -1:
                return False, "Marqueurs introuvables."
            before = content[:start].rstrip()
            after = content[end + len(_MARKER_END):].lstrip("\n")
            new_content = (before + "\n" + after).strip()
            if new_content:
                self._target.write_text(new_content + "\n", encoding="utf-8")
            else:
                self._target.unlink()
            return True, "Protection retirée."
        except OSError as e:
            return False, f"Erreur : {e}"
