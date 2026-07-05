import sys
import time
import customtkinter as ctk
from src.config.constants import (
    OVERLAY_WIDTH, OVERLAY_HEIGHT, OVERLAY_MARGIN,
    OVERLAY_ALPHA, OVERLAY_COLOR_ACTIVE, OVERLAY_COLOR_INACTIVE, OVERLAY_TEXT_COLOR,
)
from src.config import settings
from src.core.virtual_desktop import VirtualDesktopManager, is_cloaked, reassert_topmost
from src.core.logger import get_logger

_log = get_logger()

# Cadence de la boucle anti-fantôme et intervalle minimal entre deux remaps
# lorsqu'un cloak persiste (borne le flicker et le risque crash tk86t).
OVERLAY_POLL_MS = 800
REMAP_THROTTLE_S = 4.0


class StatusOverlay(ctk.CTkToplevel):
    """Indicateur flottant always-on-top pour l'état de l'autoclick."""

    def __init__(self, master, on_toggle: callable):
        super().__init__(master)
        self.on_toggle = on_toggle
        self.active = False

        # Configuration de la fenêtre
        self.title("AutoClaude Overlay")
        self.overrideredirect(True)  # Pas de bordures
        self.attributes("-topmost", True)  # Toujours au-dessus
        self.attributes("-alpha", OVERLAY_ALPHA)

        # Windows specific: hide from Taskbar
        if sys.platform == "win32":
            try:
                self.attributes("-toolwindow", True)
            except Exception:
                pass

        # Positionnement (chargement ou défaut bas-gauche)
        saved_x = settings.get("overlay_x")
        saved_y = settings.get("overlay_y")

        if saved_x is not None and saved_y is not None:
            x, y = saved_x, saved_y
        else:
            screen_h = self.winfo_screenheight()
            x = OVERLAY_MARGIN
            y = screen_h - OVERLAY_HEIGHT - OVERLAY_MARGIN

        self.geometry(f"{OVERLAY_WIDTH}x{OVERLAY_HEIGHT}+{x}+{y}")

        # Frame principale cliquable
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=OVERLAY_COLOR_INACTIVE,
            corner_radius=10,
            border_width=0
        )
        self.main_frame.pack(expand=True, fill="both")

        self.label = ctk.CTkLabel(
            self.main_frame,
            text="CL OFF",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=OVERLAY_TEXT_COLOR,
            fg_color="transparent"
        )
        self.label.pack(side="left", expand=True, padx=(10, 0))

        self.count_label = ctk.CTkLabel(
            self.main_frame,
            text="0",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=OVERLAY_TEXT_COLOR,
            fg_color="transparent"
        )
        self.count_label.pack(side="right", expand=True, padx=(0, 10))

        # Drag & Toggle
        self._drag_start_x = 0
        self._drag_start_y = 0
        self._is_dragging = False

        for widget in [self.main_frame, self.label, self.count_label]:
            widget.bind("<Button-1>", self._start_drag)
            widget.bind("<B1-Motion>", self._do_drag)
            widget.bind("<ButtonRelease-1>", self._stop_drag)

        self._keep_on_top()

        # Anti-fantôme (overrideredirect + topmost). Deux causes distinctes,
        # réaffirmées à chaque tick sans détection fragile plutôt que « détecter
        # puis réagir » (jeu de whack-a-mole qui laissait passer pygame, etc.) :
        #   1. Perte de z-order (fenêtre plein écran qui passe devant) → on
        #      réaffirme topmost via SetWindowPos Win32 (inconditionnel, cheap).
        #   2. Cloak DWM (Win+Tab, bureaux virtuels, plein écran) → l'overlay
        #      devient translucide/non cliquable ; seul un cycle withdraw/
        #      deiconify le décloake. Déclenché sur `is_cloaked`, throttlé pour
        #      borner le flicker et le risque crash tk86t (cf. memory).
        self._hwnd = None
        self._vd_after_id = None
        self._remap_in_progress = False   # withdraw en cours, deiconify en attente
        self._last_remap = 0.0            # monotonic du dernier remap (throttle)
        if sys.platform == "win32":
            self._vd_after_id = self.after(OVERLAY_POLL_MS, self._keep_visible)

    def _get_hwnd(self):
        if self._hwnd:
            return self._hwnd
        try:
            self._hwnd = VirtualDesktopManager.root_hwnd(self.winfo_id())
        except Exception:
            self._hwnd = None
        return self._hwnd

    def _keep_visible(self):
        """Boucle qui maintient l'overlay visible ET cliquable, quelle que soit
        la cause du fantôme.

        - `reassert_topmost` à chaque tick : reprend le dessus si une fenêtre
          plein écran a volé le rang topmost (cheap, sans effet de bord).
        - `is_cloaked` : répond directement à « suis-je fantôme maintenant ? »
          (Win+Tab, bureau virtuel, plein écran). Si oui, on décloake via un
          remap withdraw/deiconify, throttlé à REMAP_THROTTLE_S pour éviter toute
          boucle de flicker quand le cloak persiste (appli plein écran active).
        """
        try:
            if not self.winfo_exists():
                return
            if self.state() != "withdrawn" and not self._remap_in_progress:
                hwnd = self._get_hwnd()
                reassert_topmost(hwnd)
                if is_cloaked(hwnd) and (time.monotonic() - self._last_remap) >= REMAP_THROTTLE_S:
                    _log.info("Overlay fantôme (cloaked) → remap")
                    self._last_remap = time.monotonic()
                    self._follow_to_current_desktop()
        except Exception:
            _log.exception("Overlay _keep_visible: erreur")
        finally:
            try:
                if self.winfo_exists():
                    self._vd_after_id = self.after(OVERLAY_POLL_MS, self._keep_visible)
            except Exception:
                pass

    def _follow_to_current_desktop(self):
        # Cycle withdraw/deiconify : seule méthode qui décloake réellement une
        # fenêtre overrideredirect (MoveWindowToDesktop renvoie S_OK sans rien
        # déplacer pour ces fenêtres). Throttlé par l'appelant → risque tk86t
        # borné. Garde anti-chevauchement : un nouveau tick ne relance pas un
        # withdraw pendant qu'un deiconify est encore en attente.
        if self._remap_in_progress:
            return
        try:
            self._remap_in_progress = True
            self.withdraw()
            self.after(80, self._finish_remap)
        except Exception:
            self._remap_in_progress = False
            _log.exception("Overlay remap: withdraw a échoué")

    def _finish_remap(self):
        try:
            if self.winfo_exists():
                self.deiconify()
                reassert_topmost(self._get_hwnd())
                _log.info("Overlay remap terminé, cloaked=%s", is_cloaked(self._get_hwnd()))
        except Exception:
            _log.exception("Overlay remap: deiconify a échoué")
        finally:
            self._remap_in_progress = False

    def _start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y
        self._is_dragging = False

    def _do_drag(self, event):
        # Si on bouge de plus de 2 pixels, on considère que c'est un drag
        if abs(event.x - self._drag_start_x) > 2 or abs(event.y - self._drag_start_y) > 2:
            self._is_dragging = True

        x = self.winfo_x() + (event.x - self._drag_start_x)
        y = self.winfo_y() + (event.y - self._drag_start_y)
        self.geometry(f"+{x}+{y}")

    def _stop_drag(self, event):
        if not self._is_dragging:
            self._handle_toggle()
        else:
            # Sauvegarder la nouvelle position
            settings.set("overlay_x", self.winfo_x())
            settings.set("overlay_y", self.winfo_y())
        self._is_dragging = False

    def _handle_toggle(self):
        self.active = not self.active
        self.update_ui()
        if self.on_toggle:
            self.on_toggle()

    def set_active(self, state: bool) -> None:
        if self.active != state:
            self.active = state
            self.update_ui()

    def update_ui(self):
        if self.active:
            self.main_frame.configure(fg_color=OVERLAY_COLOR_ACTIVE)
            self.label.configure(text="CL ON")
        else:
            self.main_frame.configure(fg_color=OVERLAY_COLOR_INACTIVE)
            self.label.configure(text="CL OFF")

    def set_click_count(self, count: int):
        self.count_label.configure(text=str(count))

    def _keep_on_top(self):
        # `-topmost` est persistent — pas besoin de le réaffirmer ni de lift().
        # On rebind uniquement sur <Map> pour récupérer après un deiconify.
        try:
            if not self.winfo_exists():
                return
            self.bind("<Map>", lambda _: self._on_map(), add="+")
        except Exception:
            pass

    def _on_map(self):
        try:
            if self.winfo_exists():
                self.attributes("-topmost", True)
        except Exception:
            pass
