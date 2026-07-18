"""Tests pour ui.dialogs.model_badge_picker — dialogue de création de badge."""

from unittest.mock import Mock


def test_import_module():
    """Vérifie que le module s'importe sans erreur."""
    from src.ui.dialogs import model_badge_picker  # noqa: F401


def test_confirm_sets_result_when_window_found():
    """_confirm() résout le hwnd correspondant au titre sélectionné."""
    from src.ui.dialogs.model_badge_picker import ModelBadgePicker

    picker = Mock(spec=ModelBadgePicker)
    picker._windows = [(111, "file.py - Visual Studio Code")]
    picker._window_var = Mock()
    picker._window_var.get.return_value = "file.py - Visual Studio Code"
    picker._model_var = Mock()
    picker._model_var.get.return_value = "Opus"

    ModelBadgePicker._confirm(picker)

    assert picker.result == (111, "file.py - Visual Studio Code", "Opus")
    picker.destroy.assert_called_once()


def test_confirm_cancels_when_no_windows():
    """_confirm() annule si aucune fenêtre VSCode n'a été détectée."""
    from src.ui.dialogs.model_badge_picker import ModelBadgePicker

    picker = Mock(spec=ModelBadgePicker)
    picker._windows = []

    ModelBadgePicker._confirm(picker)

    picker._cancel.assert_called_once()


def test_confirm_cancels_when_title_not_found():
    """_confirm() annule si le titre sélectionné ne correspond à aucun hwnd connu."""
    from src.ui.dialogs.model_badge_picker import ModelBadgePicker

    picker = Mock(spec=ModelBadgePicker)
    picker._windows = [(111, "other")]
    picker._window_var = Mock()
    picker._window_var.get.return_value = "missing"

    ModelBadgePicker._confirm(picker)

    picker._cancel.assert_called_once()


def test_cancel_sets_result_none():
    """_cancel() réinitialise le résultat et détruit le dialogue."""
    from src.ui.dialogs.model_badge_picker import ModelBadgePicker

    picker = Mock(spec=ModelBadgePicker)

    ModelBadgePicker._cancel(picker)

    assert picker.result is None
    picker.destroy.assert_called_once()
