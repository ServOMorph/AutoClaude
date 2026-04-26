"""Tests pour core.click_stats — statistiques de clic et agrégation temporelle.

IMPORTANT : tous les tests utilisent un répertoire temporaire via la fixture
`isolated_stats` pour ne jamais toucher aux vraies données de l'utilisateur
(~/.autoclaude/click_stats.json).
"""

import json
import tempfile
from pathlib import Path
from datetime import datetime
import pytest
from unittest.mock import patch


@pytest.fixture(autouse=True)
def isolated_stats(tmp_path):
    """Redirige click_stats vers un dossier temp et réinitialise les globals.

    Sans cette fixture, les appels à reset()/increment() modifient les
    vraies données de l'utilisateur dans ~/.autoclaude/click_stats.json.
    """
    import src.core.click_stats as cs

    fake_dir = tmp_path / "autoclaude"
    fake_dir.mkdir()
    fake_file = fake_dir / "click_stats.json"

    with patch.object(cs, "_STATS_DIR", fake_dir), \
         patch.object(cs, "_STATS_FILE", fake_file):

        # Réinitialiser les globals du module pour isolation complète
        cs._buffer_count = 0
        cs._buffer_events = []
        cs._total_on_disk = None

        yield

        # Nettoyage post-test
        cs._buffer_count = 0
        cs._buffer_events = []
        cs._total_on_disk = None


def test_import_module():
    """Vérifie que le module s'importe sans erreur."""
    from src.core import click_stats  # noqa: F401


def test_get_total_returns_integer():
    """get_total() retourne un entier."""
    from src.core import click_stats
    result = click_stats.get_total()
    assert isinstance(result, int)
    assert result >= 0


def test_initial_total_is_zero():
    """Le total initial est 0 dans un environnement vierge."""
    from src.core import click_stats
    assert click_stats.get_total() == 0


def test_increment_increases_total():
    """increment() augmente le compteur total."""
    from src.core import click_stats

    initial = click_stats.get_total()
    click_stats.increment()
    assert click_stats.get_total() == initial + 1


def test_multiple_increments():
    """increment() multiple fois compte correctement."""
    from src.core import click_stats

    for _ in range(5):
        click_stats.increment()
    assert click_stats.get_total() == 5


def test_get_daily_totals_returns_dict():
    """get_daily_totals() retourne un dictionnaire."""
    from src.core import click_stats
    result = click_stats.get_daily_totals()

    assert isinstance(result, dict)
    # Chaque clé doit être YYYY-MM-DD, chaque valeur un int
    for key, val in result.items():
        assert isinstance(key, str)
        assert isinstance(val, int)
        try:
            datetime.strptime(key, "%Y-%m-%d")
        except ValueError:
            pytest.fail(f"Format date invalide dans daily_totals: {key}")


def test_increment_updates_daily_totals():
    """Incrémenter ajoute à daily_totals pour la date du jour."""
    from src.core import click_stats
    from datetime import date

    click_stats.increment()
    click_stats.flush_buffer()

    daily = click_stats.get_daily_totals()
    today = date.today().isoformat()
    assert today in daily
    assert daily[today] >= 1


def test_aggregate_windowed_returns_tuple():
    """aggregate_windowed() retourne (data_list, stats_dict)."""
    from src.core import click_stats

    result = click_stats.aggregate_windowed("today")
    assert isinstance(result, tuple)
    assert len(result) == 2

    data, stats = result
    assert isinstance(data, list)
    assert isinstance(stats, dict)


def test_aggregate_windowed_all_windows():
    """aggregate_windowed() fonctionne pour tous les windows valides."""
    from src.core import click_stats

    windows = ["today", "7d", "30d", "12m", "all"]
    for window in windows:
        data, stats = click_stats.aggregate_windowed(window)
        assert isinstance(data, list), f"Échec pour window '{window}'"
        assert isinstance(stats, dict), f"Échec pour window '{window}'"


def test_aggregate_windowed_stats_keys():
    """aggregate_windowed() stats contient les clés requises."""
    from src.core import click_stats

    data, stats = click_stats.aggregate_windowed("today")

    required_keys = ["total", "avg_per_active_day", "record", "active_days"]
    for key in required_keys:
        assert key in stats, f"Clé manquante '{key}' dans stats"
        assert isinstance(stats[key], (int, float)), f"Type inattendu pour {key}"


def test_reset_clears_counts():
    """reset() réinitialise les compteurs à zéro."""
    from src.core import click_stats

    click_stats.increment()
    click_stats.increment()
    assert click_stats.get_total() == 2

    click_stats.reset()
    assert click_stats.get_total() == 0


def test_flush_buffer_exists():
    """flush_buffer() est appelable sans exception."""
    from src.core import click_stats
    try:
        click_stats.flush_buffer()
    except Exception as e:
        pytest.fail(f"flush_buffer() a levé une exception: {e}")


def test_get_events_returns_list():
    """get_events() retourne une liste."""
    from src.core import click_stats
    result = click_stats.get_events()
    assert isinstance(result, list)


def test_aggregate_with_no_data():
    """aggregate_windowed() fonctionne avec zéro données."""
    from src.core import click_stats

    data, stats = click_stats.aggregate_windowed("today")

    assert stats["total"] == 0
    assert stats["active_days"] == 0


def test_full_workflow():
    """Workflow complet: increment → flush → total → daily_totals → reset."""
    from src.core import click_stats
    from datetime import date

    # 1. Partir de 0
    assert click_stats.get_total() == 0

    # 2. Incrémenter
    click_stats.increment()
    click_stats.increment()
    assert click_stats.get_total() == 2

    # 3. Flush et vérifier daily_totals
    click_stats.flush_buffer()
    daily = click_stats.get_daily_totals()
    today = date.today().isoformat()
    assert today in daily
    assert daily[today] == 2

    # 4. Reset
    click_stats.reset()
    assert click_stats.get_total() == 0
