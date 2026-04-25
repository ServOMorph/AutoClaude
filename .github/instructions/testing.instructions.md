---
name: testing
description: "Testing strategy for AutoClaude v2.5.0+. Use when: creating unit tests, implementing functions with test coverage requirements (90% minimum), validating pytest coverage, writing pytest fixtures, testing core modules (detector, autoclick_service, etc.). DO NOT USE: for debugging existing tests, CI/CD pipeline configuration."
applyTo: ["tests/**/*.py", "src/**/*.py"]
---

# Testing Instructions — AutoClaude v2.5.0+

> **Minimum 90% couverture requis** avant \/close\\ (v2.5.0+).
>
> Stratégie : pytest + pytest-cov, test unitaires dès création fonction, fixtures partagées.

---

## Commande validation couverture

\\\ash
pytest tests/ --cov=src --cov-fail-under=90
\\\

Exécuter avant \\/close\\ obligatoirement. Fail si coverage < 90%.

---

## Structure tests

\\\
tests/
├── unit/
│   ├── test_detector.py
│   ├── test_clicker.py
│   ├── test_listener.py
│   ├── test_autoclick_service.py
│   ├── test_app.py
│   ├── test_sidebar.py          # v2.5.0+
│   └── conftest.py              # Fixtures pytest partagées
└── fixtures/                    # Données test
\\\

---

## Minimal test pattern

Créer dès création fonction :

\\\python
\"\"\"Tests pour src.core.detector — détection image.\"\"\"
import pytest
from src.core.detector import ImageDetector

class TestImageDetectorInit:
    \"\"\"Groupe tests initialisation.\"\"\"
    
    def test_init_default(self):
        \"\"\"Test initialisation avec paramètres par défaut.\"\"\"
        detector = ImageDetector()
        assert detector is not None
\\\

---

## Fixtures pytest partagées (conftest.py)

\\\python
import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_screenshot():
    \"\"\"Mock capture d'écran.\"\"\"
    with patch('src.core.detector.mss') as mock_mss:
        yield mock_mss

@pytest.fixture  
def mock_template(tmp_path):
    \"\"\"Template image fake.\"\"\"
    template_file = tmp_path / "template.png"
    template_file.write_bytes(b"fake_png_data")
    return template_file
\\\

---

## Commandes utiles

\\\ash
# Coverage rapide
pytest tests/ --cov=src --cov-report=term-missing

# Couverture HTML
pytest tests/ --cov=src --cov-report=html && start htmlcov/index.html

# Tests spécifiques
pytest tests/unit/test_detector.py::TestImageDetectorInit::test_init_default -v

# Watch mode
ptw tests/
\\\

---

## Checklist avant \\/close\\

- [ ] \\pytest tests/ --cov=src --cov-fail-under=90\\ ✅ passe
- [ ] Tous test_*.py ont docstrings descriptions
- [ ] Fixtures centralisées dans conftest.py
- [ ] Mocks dépendances externes
- [ ] Tests isolés sans ordre dépendance
