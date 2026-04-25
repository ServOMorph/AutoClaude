"""Tests pour config.settings."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch
from src.config.settings import load, save, get, set, _DEFAULTS


def test_import_module():
    """Vérifie que le module s'importe sans erreur."""
    import config.settings  # noqa: F401


class TestSaveAndLoad:
    """Tests intégrés pour save/load."""

    def test_save_creates_file(self, temp_dir):
        """save() crée fichier JSON."""
        settings_file = temp_dir / "settings.json"
        settings_dir = temp_dir

        with patch("config.settings._SETTINGS_DIR", settings_dir), \
             patch("config.settings._SETTINGS_FILE", settings_file):
            test_data = {"interval": 100, "auto_stop": True}
            save(test_data)

            assert settings_file.exists()
            saved = json.loads(settings_file.read_text(encoding="utf-8"))
            assert saved == test_data

    def test_load_returns_saved_data(self, temp_dir):
        """load() lit fichier JSON sauvegardé."""
        settings_file = temp_dir / "settings.json"
        test_data = {"interval": 200, "custom": "value"}
        settings_file.write_text(json.dumps(test_data), encoding="utf-8")

        with patch("config.settings._SETTINGS_FILE", settings_file):
            result = load()
            assert result["interval"] == 200
            assert result["custom"] == "value"

    def test_load_fallback_defaults(self, temp_dir):
        """load() revient aux defaults si fichier absent."""
        settings_file = temp_dir / "nonexistent.json"

        with patch("config.settings._SETTINGS_FILE", settings_file):
            result = load()
            # Should have defaults
            assert "interval" in result
            assert "auto_stop" in result


class TestGetAndSet:
    """Tests pour get/set."""

    def test_set_then_get(self, temp_dir):
        """set() suivi de get() retourne la valeur."""
        settings_file = temp_dir / "settings.json"
        settings_dir = temp_dir

        with patch("config.settings._SETTINGS_DIR", settings_dir), \
             patch("config.settings._SETTINGS_FILE", settings_file):
            set("interval", 150)
            result = get("interval")
            assert result == 150

    def test_get_with_missing_key(self, temp_dir):
        """get() sur clé absente retourne default."""
        settings_file = temp_dir / "settings.json"
        settings_file.write_text(json.dumps({}), encoding="utf-8")

        with patch("config.settings._SETTINGS_FILE", settings_file):
            result = get("interval")
            assert result == _DEFAULTS.get("interval", 0.5)
