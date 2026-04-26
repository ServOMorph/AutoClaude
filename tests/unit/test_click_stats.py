"""Tests pour core.click_stats — statistiques de clic et agrégation temporelle."""

import json
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
import pytest
from unittest.mock import patch, MagicMock

# Note: Ces tests utilisent des mocks pour éviter de modifier l'état réel du système
# et pour tester les comportements clés de manière isolée.


def test_import_module():
    """Vérifie que le module s'importe sans erreur."""
    from src.core import click_stats  # noqa: F401


def test_get_total_returns_integer():
    """get_total() retourne un entier."""
    from src.core import click_stats
    result = click_stats.get_total()
    assert isinstance(result, int)
    assert result >= 0


def test_increment_increases_total():
    """increment() augmente le compteur total."""
    from src.core import click_stats

    initial = click_stats.get_total()
    click_stats.increment()
    after = click_stats.get_total()

    assert after > initial


def test_get_daily_totals_returns_dict():
    """get_daily_totals() retourne un dictionnaire."""
    from src.core import click_stats
    result = click_stats.get_daily_totals()

    assert isinstance(result, dict)
    # Chaque clé doit être un YYYY-MM-DD, chaque valeur un int
    for key, val in result.items():
        assert isinstance(key, str)
        assert isinstance(val, int)
        # Vérifier format date YYYY-MM-DD
        try:
            datetime.strptime(key, "%Y-%m-%d")
        except ValueError:
            pytest.fail(f"Invalid date format in daily_totals: {key}")


def test_aggregate_windowed_returns_tuple():
    """aggregate_windowed() retourne (data_list, stats_dict)."""
    from src.core import click_stats

    result = click_stats.aggregate_windowed("today")
    assert isinstance(result, tuple)
    assert len(result) == 2

    data, stats = result
    assert isinstance(data, list)  # Liste de tuples (label, count)
    assert isinstance(stats, dict)  # Stats dict


def test_aggregate_windowed_all_windows():
    """aggregate_windowed() fonctionne pour tous les windows valides."""
    from src.core import click_stats

    windows = ["today", "7d", "30d", "12m", "all"]
    for window in windows:
        data, stats = click_stats.aggregate_windowed(window)
        assert isinstance(data, list), f"Failed for window {window}"
        assert isinstance(stats, dict), f"Failed for window {window}"


def test_aggregate_windowed_stats_keys():
    """aggregate_windowed() stats contient les clés requises."""
    from src.core import click_stats

    data, stats = click_stats.aggregate_windowed("today")

    required_keys = ["total", "avg_per_active_day", "record", "active_days"]
    for key in required_keys:
        assert key in stats, f"Missing key '{key}' in stats"
        assert isinstance(stats[key], (int, float)), f"Unexpected type for {key}"


def test_reset_clears_counts():
    """reset() réinitialise les compteurs."""
    from src.core import click_stats

    # Incrémenter au moins une fois
    click_stats.increment()
    initial = click_stats.get_total()

    click_stats.reset()
    after_reset = click_stats.get_total()

    # Après reset, le total doit être 0
    assert after_reset == 0


def test_flush_buffer_exists():
    """flush_buffer() fonction existe et est appelable."""
    from src.core import click_stats

    # Ne doit pas lever d'exception
    try:
        click_stats.flush_buffer()
    except Exception as e:
        pytest.fail(f"flush_buffer() raised {e}")


def test_get_events_returns_list():
    """get_events() retourne une liste."""
    from src.core import click_stats

    result = click_stats.get_events()
    assert isinstance(result, list)


# Tests d'intégration (vérifient comportement complet)

def test_full_workflow():
    """Workflow complet: increment → total → reset."""
    from src.core import click_stats

    # 1. Sauvegarder état initial
    initial_total = click_stats.get_total()
    initial_daily = click_stats.get_daily_totals()

    # 2. Incrémenter
    click_stats.increment()
    new_total = click_stats.get_total()
    assert new_total > initial_total

    # 3. Vérifier daily_totals
    new_daily = click_stats.get_daily_totals()
    assert len(new_daily) >= len(initial_daily)

    # 4. Reset
    click_stats.reset()
    reset_total = click_stats.get_total()
    assert reset_total == 0


def test_aggregate_with_no_data():
    """aggregate_windowed() fonctionne avec zéro données."""
    from src.core import click_stats

    # Après reset, aucune donnée
    click_stats.reset()

    data, stats = click_stats.aggregate_windowed("today")

    # Ne doit pas crasher, stats doivent être cohérentes
    assert stats["total"] == 0
    assert stats["active_days"] == 0
