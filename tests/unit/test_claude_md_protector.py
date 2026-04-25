"""Tests pour security.claude_md_protector."""

import pytest
from pathlib import Path
from src.security.claude_md_protector import ClaudeMdProtector, _MARKER_START, _MARKER_END, _GUARD_BLOCK


def test_import_module():
    """Vérifie que le module s'importe sans erreur."""
    import security.claude_md_protector  # noqa: F401


class TestClaudeMdProtector:
    """Tests pour ClaudeMdProtector."""

    def test_init(self, temp_dir):
        """__init__ définit les chemins correctement."""
        protector = ClaudeMdProtector(temp_dir)
        assert protector._project_path == temp_dir
        assert protector._claude_dir == temp_dir / ".claude"
        assert protector._target == temp_dir / ".claude" / "CLAUDE.md"

    def test_is_already_protected_false_no_file(self, temp_dir):
        """is_already_protected() retourne False si fichier n'existe pas."""
        protector = ClaudeMdProtector(temp_dir)
        assert protector.is_already_protected() is False

    def test_is_already_protected_false_no_markers(self, temp_dir):
        """is_already_protected() retourne False si marqueurs absent."""
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()
        claude_file = claude_dir / "CLAUDE.md"
        claude_file.write_text("Some content without markers", encoding="utf-8")

        protector = ClaudeMdProtector(temp_dir)
        assert protector.is_already_protected() is False

    def test_is_already_protected_true_with_markers(self, temp_dir):
        """is_already_protected() retourne True si marqueurs présents."""
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()
        claude_file = claude_dir / "CLAUDE.md"
        claude_file.write_text(f"Content\n{_MARKER_START}\nGuard\n{_MARKER_END}\nMore", encoding="utf-8")

        protector = ClaudeMdProtector(temp_dir)
        assert protector.is_already_protected() is True


class TestApplyProtection:
    """Tests pour apply()."""

    def test_apply_creates_directory(self, temp_dir):
        """apply() crée le répertoire .claude s'il n'existe pas."""
        protector = ClaudeMdProtector(temp_dir)
        assert not (temp_dir / ".claude").exists()

        success, msg = protector.apply()

        assert (temp_dir / ".claude").exists()

    def test_apply_creates_new_file(self, temp_dir):
        """apply() crée CLAUDE.md avec guard block."""
        protector = ClaudeMdProtector(temp_dir)

        success, msg = protector.apply()

        assert success is True
        claude_file = temp_dir / ".claude" / "CLAUDE.md"
        assert claude_file.exists()
        content = claude_file.read_text(encoding="utf-8")
        assert _MARKER_START in content
        assert _MARKER_END in content

    def test_apply_appends_to_existing(self, temp_dir):
        """apply() ajoute le guard block au fichier existant."""
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()
        claude_file = claude_dir / "CLAUDE.md"
        original_content = "# Existing content"
        claude_file.write_text(original_content, encoding="utf-8")

        protector = ClaudeMdProtector(temp_dir)
        success, msg = protector.apply()

        assert success is True
        content = claude_file.read_text(encoding="utf-8")
        assert "Existing content" in content
        assert _MARKER_START in content

    def test_apply_already_protected(self, temp_dir):
        """apply() retourne False si déjà protégé."""
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()
        claude_file = claude_dir / "CLAUDE.md"
        claude_file.write_text(f"{_MARKER_START}\nguard\n{_MARKER_END}", encoding="utf-8")

        protector = ClaudeMdProtector(temp_dir)
        success, msg = protector.apply()

        assert success is False
        assert "Déjà protégé" in msg

    def test_apply_handles_os_error(self, temp_dir, monkeypatch):
        """apply() retourne False en cas d'erreur OS."""
        protector = ClaudeMdProtector(temp_dir)

        def mock_mkdir(*args, **kwargs):
            raise OSError("Permission denied")

        monkeypatch.setattr("pathlib.Path.mkdir", mock_mkdir)

        success, msg = protector.apply()

        assert success is False
        assert "Erreur" in msg


class TestRemoveProtection:
    """Tests pour remove_protection()."""

    def test_remove_no_protection(self, temp_dir):
        """remove_protection() retourne False si pas protégé."""
        protector = ClaudeMdProtector(temp_dir)

        success, msg = protector.remove_protection()

        assert success is False
        assert "Aucune protection" in msg

    def test_remove_protection_success(self, temp_dir):
        """remove_protection() supprime le guard block."""
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()
        claude_file = claude_dir / "CLAUDE.md"
        content = f"Before\n{_MARKER_START}\nguard\n{_MARKER_END}\nAfter"
        claude_file.write_text(content, encoding="utf-8")

        protector = ClaudeMdProtector(temp_dir)
        success, msg = protector.remove_protection()

        assert success is True
        remaining = claude_file.read_text(encoding="utf-8")
        assert _MARKER_START not in remaining
        assert _MARKER_END not in remaining
        assert "Before" in remaining
        assert "After" in remaining

    def test_remove_protection_empty_file(self, temp_dir):
        """remove_protection() supprime le fichier si guard est seul contenu."""
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()
        claude_file = claude_dir / "CLAUDE.md"
        claude_file.write_text(f"{_MARKER_START}\nguard\n{_MARKER_END}", encoding="utf-8")

        protector = ClaudeMdProtector(temp_dir)
        success, msg = protector.remove_protection()

        assert success is True
        assert not claude_file.exists()

    def test_remove_protection_handles_os_error(self, temp_dir, monkeypatch):
        """remove_protection() retourne False en cas d'erreur OS."""
        claude_dir = temp_dir / ".claude"
        claude_dir.mkdir()
        claude_file = claude_dir / "CLAUDE.md"
        claude_file.write_text(f"{_MARKER_START}\nguard\n{_MARKER_END}", encoding="utf-8")

        protector = ClaudeMdProtector(temp_dir)

        # Mock le read_text pour raise OSError après la première lecture
        original_read = Path.read_text
        call_count = 0

        def mock_read(self, *args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count > 1:  # is_already_protected() lit une fois, remove_protection() lit la deuxième
                raise OSError("Permission denied")
            return original_read(self, *args, **kwargs)

        monkeypatch.setattr("pathlib.Path.read_text", mock_read)

        success, msg = protector.remove_protection()

        assert success is False
        assert "Erreur" in msg
