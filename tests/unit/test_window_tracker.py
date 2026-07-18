"""Tests pour core.window_tracker — suivi de fenêtres VSCode (Win32)."""

from unittest.mock import Mock, patch


def test_import_module():
    """Vérifie que le module s'importe sans erreur."""
    from src.core import window_tracker  # noqa: F401


def test_list_vscode_windows_non_windows_returns_empty():
    """Sur un OS non-Windows, list_vscode_windows renvoie une liste vide."""
    from src.core import window_tracker

    with patch.object(window_tracker.sys, "platform", "linux"):
        assert window_tracker.list_vscode_windows() == []


def test_get_window_rect_non_windows_returns_none():
    from src.core import window_tracker

    with patch.object(window_tracker.sys, "platform", "linux"):
        assert window_tracker.get_window_rect(123) is None


def test_get_window_rect_no_hwnd_returns_none():
    from src.core import window_tracker

    assert window_tracker.get_window_rect(None) is None


def test_is_window_valid_false_without_hwnd():
    from src.core import window_tracker

    assert window_tracker.is_window_valid(None) is False


def test_is_window_valid_non_windows():
    from src.core import window_tracker

    with patch.object(window_tracker.sys, "platform", "linux"):
        assert window_tracker.is_window_valid(123) is False


def test_is_window_minimized_false_without_hwnd():
    from src.core import window_tracker

    assert window_tracker.is_window_minimized(None) is False


def test_window_tracker_exists_delegates():
    from src.core import window_tracker

    with patch.object(window_tracker, "is_window_valid", return_value=True) as mock_valid:
        tracker = window_tracker.WindowTracker(42)
        assert tracker.exists() is True
        mock_valid.assert_called_once_with(42)


def test_window_tracker_get_rect_delegates():
    from src.core import window_tracker

    with patch.object(window_tracker, "get_window_rect", return_value=(0, 0, 100, 100)) as mock_rect:
        tracker = window_tracker.WindowTracker(42)
        assert tracker.get_rect() == (0, 0, 100, 100)
        mock_rect.assert_called_once_with(42)


def test_window_tracker_is_visible_true():
    from src.core import window_tracker

    tracker = window_tracker.WindowTracker(42)
    with patch.object(window_tracker.WindowTracker, "exists", return_value=True), \
         patch.object(window_tracker, "is_window_minimized", return_value=False), \
         patch.object(window_tracker, "is_cloaked", return_value=0):
        assert tracker.is_visible() is True


def test_window_tracker_is_visible_false_when_not_exists():
    from src.core import window_tracker

    tracker = window_tracker.WindowTracker(42)
    with patch.object(window_tracker.WindowTracker, "exists", return_value=False):
        assert tracker.is_visible() is False


def test_window_tracker_is_visible_false_when_minimized():
    from src.core import window_tracker

    tracker = window_tracker.WindowTracker(42)
    with patch.object(window_tracker.WindowTracker, "exists", return_value=True), \
         patch.object(window_tracker, "is_window_minimized", return_value=True):
        assert tracker.is_visible() is False


def test_window_tracker_is_visible_false_when_cloaked():
    from src.core import window_tracker

    tracker = window_tracker.WindowTracker(42)
    with patch.object(window_tracker.WindowTracker, "exists", return_value=True), \
         patch.object(window_tracker, "is_window_minimized", return_value=False), \
         patch.object(window_tracker, "is_cloaked", return_value=2):
        assert tracker.is_visible() is False
