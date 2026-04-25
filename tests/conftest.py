"""Configuration pytest partagée pour les tests."""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Permet d'importer depuis src/ sans installation
RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))


@pytest.fixture
def temp_dir():
    """Crée un dossier temporaire pour les tests."""
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


@pytest.fixture
def temp_json_file(temp_dir):
    """Crée un fichier JSON temporaire."""
    file_path = temp_dir / "test.json"
    file_path.write_text('{"key": "value"}', encoding="utf-8")
    return file_path


@pytest.fixture
def temp_markdown_file(temp_dir):
    """Crée un fichier markdown avec frontmatter."""
    md_path = temp_dir / "test.md"
    content = """---
title: Test Document
category: test
---

Body content here."""
    md_path.write_text(content, encoding="utf-8")
    return md_path


@pytest.fixture
def mock_logger():
    """Mock du logger pour capturer logs."""
    with patch("config.logger") as mock:
        yield mock


@pytest.fixture
def mock_pynput():
    """Mock pynput pour tests listener."""
    with patch("pynput.keyboard.Listener") as mock_kb, \
         patch("pynput.mouse.Listener") as mock_mouse:
        yield {"keyboard": mock_kb, "mouse": mock_mouse}


@pytest.fixture
def mock_cv2():
    """Mock opencv pour tests detector."""
    mock = MagicMock()
    mock.matchTemplate.return_value = __import__("numpy").array([[0.95]])
    mock.minMaxLoc.return_value = (None, 0.95, (0, 0), (100, 100))
    with patch.dict("sys.modules", {"cv2": mock}):
        yield mock
