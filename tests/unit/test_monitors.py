"""Tests pour core.monitors."""

from unittest.mock import patch

import core.monitors as monitors


def test_import_module():
    """Vérifie que le module s'importe sans erreur."""
    import core.monitors  # noqa: F401


def test_get_all_monitors_uses_cache():
    """La liste des moniteurs ne doit pas être requêtée à chaque appel (cache TTL)."""
    monitors._cache = []
    monitors._cache_time = 0.0
    fake = [{"x": 0, "y": 0, "width": 1920, "height": 1080, "name": "Monitor 1"}]
    with patch.object(monitors, "_query_monitors", return_value=fake) as query:
        result1 = monitors.get_all_monitors()
        result2 = monitors.get_all_monitors()
    assert result1 == fake
    assert result2 == fake
    query.assert_called_once()
