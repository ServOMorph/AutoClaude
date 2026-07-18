"""Tests pour config.settings."""

from unittest.mock import patch


def test_import_module():
    """Vérifie que le module s'importe sans erreur."""
    import config.settings  # noqa: F401


def test_defaults_includes_model_badges():
    """Les settings par défaut incluent une liste vide de badges modèle."""
    from src.config import settings

    assert settings._DEFAULTS["model_badges"] == []


def test_load_missing_file_returns_defaults_with_model_badges(tmp_path):
    """load() sur un fichier absent renvoie les défauts, y compris model_badges."""
    from src.config import settings

    fake_file = tmp_path / "settings.json"
    with patch.object(settings, "_SETTINGS_FILE", fake_file):
        data = settings.load()
        assert data["model_badges"] == []


def test_set_and_get_model_badges(tmp_path):
    """set()/get() persistent la liste model_badges sur disque."""
    from src.config import settings

    fake_dir = tmp_path / "autoclaude"
    fake_file = fake_dir / "settings.json"
    with patch.object(settings, "_SETTINGS_DIR", fake_dir), \
         patch.object(settings, "_SETTINGS_FILE", fake_file):
        badges = [{"title": "t", "rel_x": 1, "rel_y": 2, "model": "Opus"}]
        settings.set("model_badges", badges)
        assert settings.get("model_badges") == badges
