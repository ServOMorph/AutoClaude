"""Tests pour core.detector."""

from unittest.mock import patch

import core.detector as detector


def test_import_module():
    """Vérifie que le module s'importe sans erreur."""
    import core.detector  # noqa: F401


def test_locate_skips_pyautogui_fallback_when_mss_cv2_available():
    """Quand mss+cv2 sont disponibles, locate() ne doit pas empiler le fallback
    pyautogui/screeninfo (double moteur de capture GDI, source d'instabilité)."""
    with (
        patch.object(detector, "_outils_find", return_value=None),
        patch.object(detector, "_mss", object()),
        patch.object(detector, "_cv2", object()),
        patch.object(detector, "_mss_cv2", return_value=None) as mss_cv2,
        patch.object(detector, "_pyautogui_multimonitor") as multimonitor,
        patch.object(detector, "_pyautogui_single") as single,
    ):
        result = detector.locate("dummy.png")

    assert result is None
    mss_cv2.assert_called_once()
    multimonitor.assert_not_called()
    single.assert_not_called()


# TODO: ajouter des tests pour les fonctions/classes publiques de core.detector
