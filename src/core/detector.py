"""TODO: description du module."""

from src.core.monitors import get_all_monitors

try:
    import mss as _mss
except Exception:
    _mss = None

try:
    import cv2 as _cv2
    import numpy as _np
except Exception:
    _cv2 = None
    _np = None

try:
    import pyautogui as _pyautogui
    _pyautogui.FAILSAFE = False
except Exception:
    _pyautogui = None

_find_image_fn = None
try:
    from outils import image_finder
    for _name in ("find_image_on_screen", "find_image", "locate_image", "locate_on_screen"):
        if hasattr(image_finder, _name):
            _find_image_fn = getattr(image_finder, _name)
            break
except Exception:
    pass


def _center_from_tuple(t):
    """TODO: description de _center_from_tuple."""
    if len(t) == 2:
        return int(t[0]), int(t[1])
    if len(t) == 4:
        left, top, w, h = t
        return int(left + w / 2), int(top + h / 2)
    return None


def _mss_cv2(path: str, confidence: float = 0.8):
    """TODO: description de _mss_cv2."""
    if not _mss or not _cv2 or not _np:
        return None
    try:
        template = _cv2.imread(path)
        if template is None:
            return None
        template_gray = _cv2.cvtColor(template, _cv2.COLOR_BGR2GRAY)
        h, w = template_gray.shape
        with _mss.mss() as sct:
            for monitor in sct.monitors[1:]:
                screenshot = sct.grab(monitor)
                img = _np.array(screenshot)
                img_gray = _cv2.cvtColor(
                    _cv2.cvtColor(img, _cv2.COLOR_BGRA2BGR),
                    _cv2.COLOR_BGR2GRAY,
                )
                result = _cv2.matchTemplate(img_gray, template_gray, _cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = _cv2.minMaxLoc(result)
                if max_val >= confidence:
                    x = monitor["left"] + max_loc[0] + w // 2
                    y = monitor["top"] + max_loc[1] + h // 2
                    return (int(x), int(y))
    except Exception:
        pass
    return None


def _pyautogui_multimonitor(path: str, confidence: float = 0.8):
    """TODO: description de _pyautogui_multimonitor."""
    if not _pyautogui:
        return None
    monitors = get_all_monitors()
    if not monitors:
        return _pyautogui_single(path, confidence)
    for mon in monitors:
        try:
            region = (mon["x"], mon["y"], mon["width"], mon["height"])
            try:
                box = _pyautogui.locateOnScreen(path, confidence=confidence, region=region)
            except TypeError:
                box = _pyautogui.locateOnScreen(path, region=region)
            if box:
                x, y = _pyautogui.center(box)
                return (int(x), int(y))
        except Exception:
            continue
    return None


def _pyautogui_single(path: str, confidence: float = 0.8):
    """TODO: description de _pyautogui_single."""
    if not _pyautogui:
        return None
    try:
        try:
            box = _pyautogui.locateOnScreen(path, confidence=confidence)
        except TypeError:
            box = _pyautogui.locateOnScreen(path)
        if not box:
            return None
        x, y = _pyautogui.center(box)
        return int(x), int(y)
    except Exception:
        return None


def _outils_find(path: str):
    """TODO: description de _outils_find."""
    if not _find_image_fn:
        return None
    try:
        res = _find_image_fn(path)
        if res is None:
            return None
        if isinstance(res, tuple):
            return _center_from_tuple(res)
        if isinstance(res, dict) and {"left", "top", "width", "height"}.issubset(res.keys()):
            return int(res["left"] + res["width"] / 2), int(res["top"] + res["height"] / 2)
        if all(hasattr(res, a) for a in ("left", "top", "width", "height")):
            return int(res.left + res.width / 2), int(res.top + res.height / 2)
    except Exception:
        pass
    return None


def locate(path: str, confidence: float = 0.8) -> tuple[int, int] | None:
    """TODO: description de locate."""
    coords = _outils_find(path)
    if coords:
        return coords
    if _mss and _cv2:
        coords = _mss_cv2(path, confidence)
        if coords:
            return coords
    if get_all_monitors():
        coords = _pyautogui_multimonitor(path, confidence)
        if coords:
            return coords
    return _pyautogui_single(path, confidence)


def has_detector() -> bool:
    """TODO: description de has_detector."""
    return bool(_find_image_fn or _pyautogui)


def describe_detector() -> str:
    """TODO: description de describe_detector."""
    if _find_image_fn:
        return "outils.image_finder"
    if _pyautogui:
        return "pyautogui (fallback)"
    return "aucun"
