"""TODO: description du module."""

try:
    from screeninfo import get_monitors as _get_monitors
except Exception:
    _get_monitors = None

try:
    import mss as _mss
except Exception:
    _mss = None


def get_all_monitors() -> list[dict]:
    """TODO: description de get_all_monitors."""
    monitors = []
    if _get_monitors:
        try:
            for m in _get_monitors():
                monitors.append({
                    "x": m.x, "y": m.y,
                    "width": m.width, "height": m.height,
                    "name": getattr(m, "name", "Unknown"),
                })
        except Exception:
            pass
    if not monitors and _mss:
        try:
            with _mss.mss() as sct:
                for i, m in enumerate(sct.monitors[1:], 1):
                    monitors.append({
                        "x": m["left"], "y": m["top"],
                        "width": m["width"], "height": m["height"],
                        "name": f"Monitor {i}",
                    })
        except Exception:
            pass
    return monitors
