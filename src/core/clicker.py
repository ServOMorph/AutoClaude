try:
    import pyautogui as _pyautogui
    _pyautogui.FAILSAFE = False
except Exception:
    _pyautogui = None

_click_fn = None
try:
    from outils import mouse_controller
    for _name in ("click_at", "click", "mouse_click"):
        if hasattr(mouse_controller, _name):
            _click_fn = getattr(mouse_controller, _name)
            break
except Exception:
    pass


def click(x: int, y: int) -> bool:
    if _click_fn:
        try:
            _click_fn(x, y)
            return True
        except TypeError:
            try:
                _click_fn((x, y))
                return True
            except Exception:
                pass
        except Exception:
            pass
    if _pyautogui:
        try:
            _pyautogui.click(x, y)
            return True
        except Exception:
            pass
    return False


def has_clicker() -> bool:
    return bool(_click_fn or _pyautogui)


def describe_clicker() -> str:
    if _click_fn:
        return "outils.mouse_controller"
    if _pyautogui:
        return "pyautogui (fallback)"
    return "aucun"
