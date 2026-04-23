import os
import sys
import time
import argparse

# Configuration : chemin de l'image, configurable via CLI ou env
DEFAULT_IMAGE_PATH = os.getenv("AUTOCLAUDE_IMAGE_PATH", "./yes.png")
IMAGE_PATH = None

find_image_fn = None
click_fn = None

try:
    from outils import image_finder
    for name in ("find_image_on_screen", "find_image", "locate_image", "locate_on_screen"):
        if hasattr(image_finder, name):
            find_image_fn = getattr(image_finder, name)
            break
except Exception as e:
    find_image_fn = None
    # Silencieux car le fallback pyautogui sera utilisé

try:
    from outils import mouse_controller
    for name in ("click_at", "click", "mouse_click"):
        if hasattr(mouse_controller, name):
            click_fn = getattr(mouse_controller, name)
            break
except Exception:
    click_fn = None

pyautogui = None
try:
    import pyautogui
    pyautogui.FAILSAFE = False
except Exception:
    pyautogui = None

screeninfo_mod = None
try:
    from screeninfo import get_monitors
    screeninfo_mod = get_monitors
except Exception:
    screeninfo_mod = None

mss_mod = None
try:
    import mss
    mss_mod = mss
except Exception:
    mss_mod = None

cv2_mod = None
numpy_mod = None
try:
    import cv2
    import numpy as np
    cv2_mod = cv2
    numpy_mod = np
except Exception:
    cv2_mod = None
    numpy_mod = None

keyboard_mod = None
mouse_mod = None
try:
    from pynput import keyboard, mouse
    keyboard_mod = keyboard
    mouse_mod = mouse
except Exception:
    keyboard_mod = None
    mouse_mod = None

stop_requested = False
auto_stop_on_input = False
last_mouse_pos = None
mouse_move_threshold = 50

def _center_from_tuple(t):
    if len(t) == 2:
        return int(t[0]), int(t[1])
    if len(t) == 4:
        left, top, w, h = t
        return int(left + w / 2), int(top + h / 2)
    return None

def get_all_monitors():
    monitors = []
    if screeninfo_mod:
        try:
            for m in screeninfo_mod():
                monitors.append({"x": m.x, "y": m.y, "width": m.width, "height": m.height, "name": getattr(m, "name", "Unknown")})
        except Exception:
            pass
    if not monitors and mss_mod:
        try:
            with mss_mod.mss() as sct:
                for i, m in enumerate(sct.monitors[1:], 1):
                    monitors.append({"x": m["left"], "y": m["top"], "width": m["width"], "height": m["height"], "name": f"Monitor {i}"})
        except Exception:
            pass
    return monitors

def locate_image_multimonitor_mss(path, confidence=0.8):
    if not mss_mod or not cv2_mod or not numpy_mod:
        return None
    try:
        template = cv2_mod.imread(path)
        if template is None:
            return None
        template_gray = cv2_mod.cvtColor(template, cv2_mod.COLOR_BGR2GRAY)
        h, w = template_gray.shape
        with mss_mod.mss() as sct:
            for monitor in sct.monitors[1:]:
                screenshot = sct.grab(monitor)
                img = numpy_mod.array(screenshot)
                img_bgr = cv2_mod.cvtColor(img, cv2_mod.COLOR_BGRA2BGR)
                img_gray = cv2_mod.cvtColor(img_bgr, cv2_mod.COLOR_BGR2GRAY)
                result = cv2_mod.matchTemplate(img_gray, template_gray, cv2_mod.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2_mod.minMaxLoc(result)
                if max_val >= confidence:
                    x = monitor["left"] + max_loc[0] + w // 2
                    y = monitor["top"] + max_loc[1] + h // 2
                    return (int(x), int(y))
    except Exception:
        pass
    return None

def locate_image_multimonitor_pyautogui(path, confidence=0.8):
    if pyautogui is None:
        return None
    monitors = get_all_monitors()
    if not monitors:
        return locate_image_single_pyautogui(path, confidence)
    for mon in monitors:
        try:
            region = (mon["x"], mon["y"], mon["width"], mon["height"])
            try:
                box = pyautogui.locateOnScreen(path, confidence=confidence, region=region)
            except TypeError:
                box = pyautogui.locateOnScreen(path, region=region)
            if box:
                x, y = pyautogui.center(box)
                return (int(x), int(y))
        except Exception:
            continue
    return None

def locate_image_single_pyautogui(path, confidence=0.8):
    if pyautogui is None:
        return None
    try:
        try:
            box = pyautogui.locateOnScreen(path, confidence=confidence)
        except TypeError:
            box = pyautogui.locateOnScreen(path)
        if not box:
            return None
        x, y = pyautogui.center(box)
        return int(x), int(y)
    except Exception:
        return None

def locate_image_with_project(path):
    if not find_image_fn:
        return None
    try:
        res = find_image_fn(path)
        if res is None:
            return None
        if isinstance(res, tuple):
            return _center_from_tuple(res)
        if isinstance(res, dict) and {"left", "top", "width", "height"}.issubset(res.keys()):
            left = res["left"]; top = res["top"]; w = res["width"]; h = res["height"]
            return int(left + w / 2), int(top + h / 2)
        if hasattr(res, "left") and hasattr(res, "top") and hasattr(res, "width") and hasattr(res, "height"):
            left = getattr(res, "left"); top = getattr(res, "top")
            w = getattr(res, "width"); h = getattr(res, "height")
            return int(left + w / 2), int(top + h / 2)
    except Exception:
        return None
    return None

def locate_image_with_pyautogui(path, confidence=0.8):
    if mss_mod and cv2_mod and numpy_mod:
        result = locate_image_multimonitor_mss(path, confidence)
        if result:
            return result
    if screeninfo_mod or mss_mod:
        result = locate_image_multimonitor_pyautogui(path, confidence)
        if result:
            return result
    return locate_image_single_pyautogui(path, confidence)

def click_with_project(x, y):
    if not click_fn:
        return False
    try:
        click_fn(x, y)
        return True
    except TypeError:
        try:
            click_fn((x, y))
            return True
        except Exception:
            return False
    except Exception:
        return False

def click_with_pyautogui(x, y):
    if pyautogui is None:
        return False
    try:
        pyautogui.click(x, y)
        return True
    except Exception:
        return False

def on_press(key):
    global stop_requested
    try:
        if key == keyboard_mod.Key.esc:
            stop_requested = True
            return False
        if auto_stop_on_input:
            stop_requested = True
            return False
    except Exception:
        pass

def on_mouse_move(x, y):
    global stop_requested, last_mouse_pos
    if not auto_stop_on_input:
        return
    if last_mouse_pos is None:
        last_mouse_pos = (x, y)
        return
    dx = abs(x - last_mouse_pos[0])
    dy = abs(y - last_mouse_pos[1])
    if dx > mouse_move_threshold or dy > mouse_move_threshold:
        stop_requested = True
        return False
    last_mouse_pos = (x, y)

def main(image_path=None, poll_interval=0.5, auto_stop=False):
    global stop_requested, last_mouse_pos, auto_stop_on_input, IMAGE_PATH

    # Configuration de l'image path
    IMAGE_PATH = image_path or DEFAULT_IMAGE_PATH
    if not os.path.isfile(IMAGE_PATH):
        print(f"❌ Erreur : Image introuvable : {IMAGE_PATH}")
        print(f"   Utilisez : python run.py --image <chemin/vers/image.png>")
        print(f"   Ou : export AUTOCLAUDE_IMAGE_PATH=<chemin>")
        sys.exit(1)

    print(f"✓ Image chargée : {IMAGE_PATH}")
    auto_stop_on_input = auto_stop
    last_mouse_pos = None
    monitors = get_all_monitors()

    if find_image_fn:
        print("Utilisation de outils.image_finder pour la detection.")
    elif pyautogui:
        print("Utilisation de pyautogui pour la detection (fallback).")
    else:
        print("Aucun moyen de detecter. Installez pyautogui.")
        sys.exit(1)

    if monitors:
        print(f"Detection multi-ecran ACTIVE: {len(monitors)} moniteur(s)")
        for i, mon in enumerate(monitors, 1):
            print(f"  Moniteur {i}: {mon['width']}x{mon['height']} @ ({mon['x']}, {mon['y']})")
        if mss_mod and cv2_mod:
            print("  Methode: mss + opencv")
        elif screeninfo_mod:
            print("  Methode: screeninfo + pyautogui")
        else:
            print("  Methode: mss + pyautogui")
    else:
        print("Detection mono-ecran (installez screeninfo ou mss pour multi-ecran)")

    if click_fn:
        print("Utilisation de outils.mouse_controller pour cliquer.")
    elif pyautogui:
        print("Utilisation de pyautogui pour le clic (fallback).")
    else:
        print("Aucun moyen de cliquer.")
        sys.exit(1)

    kb_listener = None
    mouse_listener = None

    if keyboard_mod:
        kb_listener = keyboard_mod.Listener(on_press=on_press)
        kb_listener.start()
        print("Appuyez sur Esc pour arreter.")
    else:
        print("pynput non installe; utilisez Ctrl+C.")

    if mouse_mod and auto_stop_on_input:
        mouse_listener = mouse_mod.Listener(on_move=on_mouse_move)
        mouse_listener.start()

    try:
        while not stop_requested:
            coords = None
            if find_image_fn:
                coords = locate_image_with_project(IMAGE_PATH)
            if coords is None:
                coords = locate_image_with_pyautogui(IMAGE_PATH)
            if coords:
                x, y = coords
                clicked = False
                if click_fn:
                    clicked = click_with_project(x, y)
                if not clicked:
                    clicked = click_with_pyautogui(x, y)
                if clicked:
                    print(f"Clic effectue en {x},{y}")
                    time.sleep(0.4)
                else:
                    print("Detecte mais impossible de cliquer.")
                    time.sleep(poll_interval)
            else:
                time.sleep(poll_interval)
    except KeyboardInterrupt:
        pass
    finally:
        stop_requested = True
        if kb_listener:
            kb_listener.stop()
        if mouse_listener:
            mouse_listener.stop()
        print("Arret demande, sortie.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Automatise les clics sur un bouton détecté à l'écran.",
        epilog="Exemple: python run.py --image yes.png --interval 0.5 --auto-stop"
    )
    parser.add_argument(
        "--image", "-i",
        default=DEFAULT_IMAGE_PATH,
        help=f"Chemin vers l'image template (défaut: {DEFAULT_IMAGE_PATH})"
    )
    parser.add_argument(
        "--interval", "-t",
        type=float,
        default=0.5,
        help="Intervalle de polling en secondes (défaut: 0.5)"
    )
    parser.add_argument(
        "--auto-stop",
        action="store_true",
        help="Arrête au premier mouvement souris ou input clavier (sauf Esc)"
    )

    args = parser.parse_args()
    main(image_path=args.image, poll_interval=args.interval, auto_stop=args.auto_stop)
