"""Tests pour ui.app."""

from unittest.mock import Mock, patch


def test_import_module():
    """Vérifie que le module s'importe sans erreur."""
    import ui.app  # noqa: F401


def test_add_model_badge_appends_and_wires_remove():
    """_add_model_badge() crée le badge, l'ajoute à la liste et cable on_remove."""
    from src.ui.app import AutoClaudeApp

    app = Mock(spec=AutoClaudeApp)
    app._model_badges = []
    fake_badge = Mock()

    with patch("src.ui.app.ModelBadge", return_value=fake_badge) as mock_cls:
        AutoClaudeApp._add_model_badge(app, 111, "titre", "Opus", rel_x=5, rel_y=6)

    mock_cls.assert_called_once_with(
        app, model="Opus", target_hwnd=111, window_title="titre",
        rel_x=5, rel_y=6, on_state_change=app._save_model_badges,
    )
    assert app._model_badges == [fake_badge]
    assert fake_badge.on_remove is not None


def test_remove_model_badge_removes_and_saves():
    """_remove_model_badge() retire le badge de la liste et persiste l'état."""
    from src.ui.app import AutoClaudeApp

    app = Mock(spec=AutoClaudeApp)
    badge = Mock()
    app._model_badges = [badge]

    AutoClaudeApp._remove_model_badge(app, badge)

    assert app._model_badges == []
    app._save_model_badges.assert_called_once()


def test_remove_model_badge_unknown_badge_still_saves():
    """_remove_model_badge() ne plante pas si le badge n'est pas dans la liste."""
    from src.ui.app import AutoClaudeApp

    app = Mock(spec=AutoClaudeApp)
    app._model_badges = []

    AutoClaudeApp._remove_model_badge(app, Mock())

    assert app._model_badges == []
    app._save_model_badges.assert_called_once()


def test_save_model_badges_writes_states():
    """_save_model_badges() sérialise l'état de chaque badge dans les settings."""
    from src.ui.app import AutoClaudeApp

    app = Mock(spec=AutoClaudeApp)
    badge = Mock()
    badge.get_state.return_value = {"title": "t", "rel_x": 1, "rel_y": 2, "model": "Sonnet"}
    app._model_badges = [badge]

    with patch("src.ui.app.settings") as mock_settings:
        AutoClaudeApp._save_model_badges(app)

    mock_settings.set.assert_called_once_with("model_badges", [badge.get_state.return_value])


def test_restore_model_badges_skips_missing_window():
    """_restore_model_badges() ignore les entrées dont la fenêtre n'existe plus."""
    from src.ui.app import AutoClaudeApp

    app = Mock(spec=AutoClaudeApp)
    with patch("src.ui.app.settings") as mock_settings, \
         patch("src.ui.app.list_vscode_windows", return_value=[]):
        mock_settings.get.return_value = [{"title": "missing", "rel_x": 1, "rel_y": 2, "model": "Opus"}]
        AutoClaudeApp._restore_model_badges(app)

    app._add_model_badge.assert_not_called()


def test_restore_model_badges_creates_when_found():
    """_restore_model_badges() recrée un badge quand la fenêtre cible existe encore."""
    from src.ui.app import AutoClaudeApp

    app = Mock(spec=AutoClaudeApp)
    with patch("src.ui.app.settings") as mock_settings, \
         patch("src.ui.app.list_vscode_windows", return_value=[(42, "found")]):
        mock_settings.get.return_value = [{"title": "found", "rel_x": 1, "rel_y": 2, "model": "Opus"}]
        AutoClaudeApp._restore_model_badges(app)

    app._add_model_badge.assert_called_once_with(42, "found", "Opus", rel_x=1, rel_y=2)


def test_restore_model_badges_no_saved_entries_does_nothing():
    """_restore_model_badges() ne fait rien si aucun badge n'est enregistré."""
    from src.ui.app import AutoClaudeApp

    app = Mock(spec=AutoClaudeApp)
    with patch("src.ui.app.settings") as mock_settings:
        mock_settings.get.return_value = []
        AutoClaudeApp._restore_model_badges(app)

    app._add_model_badge.assert_not_called()
