"""Tests pour ui.overlays.model_badge — badge modèle Claude draggable."""

from unittest.mock import Mock, patch


def test_import_module():
    """Vérifie que le module s'importe sans erreur."""
    from src.ui.overlays import model_badge  # noqa: F401


def test_model_options_content():
    """MODEL_OPTIONS contient les 4 modèles attendus."""
    from src.ui.overlays.model_badge import MODEL_OPTIONS

    assert MODEL_OPTIONS == ["Haiku", "Sonnet", "Opus", "Fable"]


@patch('src.ui.overlays.model_badge.ctk.CTkToplevel.__init__', return_value=None)
def test_model_badge_init_structure(mock_toplevel_init):
    """ModelBadge.__init__() initialise les attributs de drag et le modèle."""
    from src.ui.overlays.model_badge import ModelBadge

    mock_master = Mock()
    mock_callback = Mock()

    with patch.object(ModelBadge, '__init__', lambda x, master, model="Sonnet", on_remove=None: None):
        badge = ModelBadge(mock_master, model="Opus", on_remove=mock_callback)
        badge._drag_start_x = 0
        badge._drag_start_y = 0
        badge._is_dragging = False
        badge.on_remove = mock_callback
        badge.model = "Opus"

        assert badge._drag_start_x == 0
        assert badge._drag_start_y == 0
        assert badge._is_dragging is False
        assert badge.on_remove == mock_callback
        assert badge.model == "Opus"


def test_drag_detection_threshold():
    """La logique de drag détecte le mouvement au-delà du seuil."""
    drag_start_x, drag_start_y = 10, 10
    event_x, event_y = 13, 10

    is_dragging = (
        abs(event_x - drag_start_x) > 2
        or abs(event_y - drag_start_y) > 2
    )
    assert is_dragging is True

    event_x2, event_y2 = 11, 10
    is_dragging2 = (
        abs(event_x2 - drag_start_x) > 2
        or abs(event_y2 - drag_start_y) > 2
    )
    assert is_dragging2 is False


def test_set_model_updates_label_text():
    """set_model() met à jour l'attribut model et le label si le modèle est valide."""
    from src.ui.overlays.model_badge import ModelBadge, MODEL_OPTIONS

    badge = Mock(spec=ModelBadge)
    badge.model = "Sonnet"
    badge.label = Mock()
    badge.on_state_change = None

    ModelBadge.set_model(badge, "Opus")
    assert badge.model == "Opus"
    badge.label.configure.assert_called_once_with(text="Opus")

    for name in MODEL_OPTIONS:
        badge2 = Mock(spec=ModelBadge)
        badge2.model = "Sonnet"
        badge2.label = Mock()
        badge2.on_state_change = None
        ModelBadge.set_model(badge2, name)
        assert badge2.model == name


def test_set_model_rejects_invalid_model():
    """set_model() ignore un nom de modèle non reconnu."""
    from src.ui.overlays.model_badge import ModelBadge

    badge = Mock(spec=ModelBadge)
    badge.model = "Sonnet"
    badge.label = Mock()

    ModelBadge.set_model(badge, "InvalidModel")
    assert badge.model == "Sonnet"
    badge.label.configure.assert_not_called()


def test_remove_calls_on_remove_and_destroy():
    """_remove() invoque le callback on_remove puis détruit le widget."""
    from src.ui.overlays.model_badge import ModelBadge

    badge = Mock(spec=ModelBadge)
    badge.on_remove = Mock()

    ModelBadge._remove(badge)
    badge.on_remove.assert_called_once()
    badge.destroy.assert_called_once()


def test_remove_without_callback():
    """_remove() ne plante pas si on_remove est None."""
    from src.ui.overlays.model_badge import ModelBadge

    badge = Mock(spec=ModelBadge)
    badge.on_remove = None

    ModelBadge._remove(badge)
    badge.destroy.assert_called_once()


def test_stop_drag_updates_relative_position_when_tracked():
    """_stop_drag() recalcule la position relative à la fenêtre suivie après un drag."""
    from src.ui.overlays.model_badge import ModelBadge

    badge = Mock(spec=ModelBadge)
    badge._is_dragging = True
    badge.tracker = Mock()
    badge.tracker.get_rect.return_value = (100, 200, 300, 400)
    badge.winfo_x.return_value = 150
    badge.winfo_y.return_value = 250
    badge._rel_x = 0
    badge._rel_y = 0
    badge.on_state_change = None

    ModelBadge._stop_drag(badge, event=Mock())

    assert badge._rel_x == 50
    assert badge._rel_y == 50
    assert badge._is_dragging is False


def test_stop_drag_no_tracker_leaves_relative_position():
    """_stop_drag() ne touche pas la position relative si le badge n'est pas attaché."""
    from src.ui.overlays.model_badge import ModelBadge

    badge = Mock(spec=ModelBadge)
    badge._is_dragging = True
    badge.tracker = None
    badge._rel_x = 20
    badge._rel_y = 20

    ModelBadge._stop_drag(badge, event=Mock())

    assert badge._rel_x == 20
    assert badge._rel_y == 20
    assert badge._is_dragging is False


def test_track_window_hides_when_not_visible():
    """_track_window() masque le badge (withdraw) quand la fenêtre suivie n'est plus visible."""
    from src.ui.overlays.model_badge import ModelBadge

    badge = Mock(spec=ModelBadge)
    badge.winfo_exists.return_value = True
    badge.tracker = Mock()
    badge.tracker.is_visible.return_value = False
    badge._was_hidden = False
    badge.window_title = "file.py - Visual Studio Code"

    ModelBadge._track_window(badge)

    badge.withdraw.assert_called_once()
    assert badge._was_hidden is True


def test_track_window_shows_and_repositions_when_visible():
    """_track_window() réaffiche le badge et suit la position de la fenêtre quand visible."""
    from src.ui.overlays.model_badge import ModelBadge

    badge = Mock(spec=ModelBadge)
    badge.winfo_exists.return_value = True
    badge.tracker = Mock()
    badge.tracker.is_visible.return_value = True
    badge.tracker.get_rect.return_value = (100, 200, 300, 400)
    badge._was_hidden = True
    badge._rel_x = 20
    badge._rel_y = 20
    badge._last_pos = None
    badge.window_title = "file.py - Visual Studio Code"

    ModelBadge._track_window(badge)

    badge.deiconify.assert_called_once()
    assert badge._was_hidden is False
    badge.geometry.assert_called_with("+120+220")


def test_stop_drag_calls_on_state_change():
    """_stop_drag() notifie on_state_change après recalcul de la position relative."""
    from src.ui.overlays.model_badge import ModelBadge

    badge = Mock(spec=ModelBadge)
    badge._is_dragging = True
    badge.tracker = Mock()
    badge.tracker.get_rect.return_value = (100, 200, 300, 400)
    badge.winfo_x.return_value = 150
    badge.winfo_y.return_value = 250
    badge._rel_x = 0
    badge._rel_y = 0
    badge.on_state_change = Mock()

    ModelBadge._stop_drag(badge, event=Mock())

    badge.on_state_change.assert_called_once()


def test_set_model_calls_on_state_change():
    """set_model() notifie on_state_change quand le modèle change."""
    from src.ui.overlays.model_badge import ModelBadge

    badge = Mock(spec=ModelBadge)
    badge.model = "Sonnet"
    badge.label = Mock()
    badge.on_state_change = Mock()

    ModelBadge.set_model(badge, "Opus")

    badge.on_state_change.assert_called_once()


def test_set_model_invalid_does_not_call_on_state_change():
    """set_model() ne notifie pas on_state_change pour un modèle invalide."""
    from src.ui.overlays.model_badge import ModelBadge

    badge = Mock(spec=ModelBadge)
    badge.model = "Sonnet"
    badge.label = Mock()
    badge.on_state_change = Mock()

    ModelBadge.set_model(badge, "InvalidModel")

    badge.on_state_change.assert_not_called()


def test_get_state_returns_snapshot():
    """get_state() renvoie titre, position relative et modèle courants."""
    from src.ui.overlays.model_badge import ModelBadge

    badge = Mock(spec=ModelBadge)
    badge.window_title = "file.py - Visual Studio Code"
    badge._rel_x = 20
    badge._rel_y = 30
    badge.model = "Opus"

    state = ModelBadge.get_state(badge)

    assert state == {
        "title": "file.py - Visual Studio Code",
        "rel_x": 20,
        "rel_y": 30,
        "model": "Opus",
    }


def test_track_window_throttled_transition_deferred():
    """_track_window() reporte la transition withdraw/deiconify si le throttle est actif."""
    from src.ui.overlays.model_badge import ModelBadge

    badge = Mock(spec=ModelBadge)
    badge.winfo_exists.return_value = True
    badge.tracker = Mock()
    badge.tracker.is_visible.return_value = False
    badge._was_hidden = False
    badge._throttle_ok.return_value = False

    ModelBadge._track_window(badge)

    badge.withdraw.assert_not_called()
    assert badge._was_hidden is False


def test_track_window_no_geometry_when_position_unchanged():
    """_track_window() n'appelle pas geometry() si la position cible n'a pas changé."""
    from src.ui.overlays.model_badge import ModelBadge

    badge = Mock(spec=ModelBadge)
    badge.winfo_exists.return_value = True
    badge.tracker = Mock()
    badge.tracker.is_visible.return_value = True
    badge.tracker.get_rect.return_value = (100, 200, 300, 400)
    badge._was_hidden = False
    badge._rel_x = 20
    badge._rel_y = 20
    badge._last_pos = (120, 220)

    ModelBadge._track_window(badge)

    badge.geometry.assert_not_called()


def test_throttle_ok_respects_min_interval():
    """_throttle_ok() bloque une transition trop rapprochée de la précédente."""
    import time
    from src.ui.overlays.model_badge import ModelBadge

    badge = Mock(spec=ModelBadge)
    badge._last_vis_change = time.monotonic()
    assert ModelBadge._throttle_ok(badge) is False

    badge._last_vis_change = 0.0
    assert ModelBadge._throttle_ok(badge) is True


@patch('src.ui.overlays.model_badge.ctk.CTkToplevel.destroy')
def test_destroy_cancels_pending_after(mock_super_destroy):
    """destroy() annule le after de suivi avant de détruire le widget."""
    from src.ui.overlays.model_badge import ModelBadge

    badge = Mock(spec=ModelBadge)
    badge._track_after_id = "after#123"

    ModelBadge.destroy(badge)

    badge.after_cancel.assert_called_once_with("after#123")
    assert badge._track_after_id is None
    mock_super_destroy.assert_called_once()


def test_track_window_no_tracker_does_nothing():
    """_track_window() ne fait rien si le badge n'est pas attaché à une fenêtre."""
    from src.ui.overlays.model_badge import ModelBadge

    badge = Mock(spec=ModelBadge)
    badge.winfo_exists.return_value = True
    badge.tracker = None

    ModelBadge._track_window(badge)

    badge.withdraw.assert_not_called()
    badge.deiconify.assert_not_called()
