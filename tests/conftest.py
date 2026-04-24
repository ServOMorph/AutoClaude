"""Configuration pytest partagée pour les tests."""

import sys
from pathlib import Path

# Permet d'importer depuis src/ sans installation
RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))
