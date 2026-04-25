# Bundle de code pour le projet AutoClaude

Ce fichier regroupe le contenu des fichiers suivants, afin d'être lisible par Perplexity :

- README.md
- src\ui\app.py
- run.py
- src\config\settings.py

---

----- README.md -----

# AutoClaude

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Tests](https://github.com/ServOMorph/AutoClaude/actions/workflows/tests.yml/badge.svg)](https://github.com/ServOMorph/AutoClaude/actions/workflows/tests.yml)
[![Version](https://img.shields.io/badge/version-2.3.0-blue.svg)](https://github.com/ServOMorph/AutoClaude/releases)

> **Conçu pour [Claude Code](https://claude.ai/code) dans VS Code** — donne plus d'autonomie à Claude Code en cliquant automatiquement sur les boutons de confirmation récurrents, sans interrompre le flux de travail de l'IA.

Outil Python qui détecte et clique automatiquement sur un bouton récurrent à l'écran — avec une interface graphique CustomTkinter en mode sombre.

Quand Claude Code travaille dans VS Code, il demande régulièrement une confirmation utilisateur (bouton "Continuer", "Approuver", etc.). AutoClaude surveille l'écran en arrière-plan et clique à ta place, permettant à Claude Code de tourner en continu sans surveillance constante.

> Développé par [SéréniaTech](https://serenia-tech.fr) · [GitHub](https://github.com/ServOMorph)

---

## Fonctionnalités

- Détection d'image par template matching (OpenCV + mss)
- Support multi-moniteur
- Dégradation progressive : si une dépendance optionnelle manque, l'outil continue de fonctionner
- Arrêt via Esc, fermeture fenêtre ou mouvement souris (mode auto-stop)
- Protection de projet Claude Code via injection dans `.claude/CLAUDE.md`
- **Compteur de clics** avec historique persisté
- **Analyses graphiques** : navigation temporelle (Récent / Tout), bandeau de statistiques (total, moyenne, record, jours actifs), graphes par heure/jour/semaine/mois/année
- **Indicateur flottant** : overlay always-on-top en bas à gauche de l'écran, cliquable pour activer/désactiver l'autoclick depuis n'importe quelle application
- Logs rotatifs (`~/.autoclaude/logs/`) et watchdog de stabilité pour une utilisation longue durée
- Interface sombre SéréniaTech (CustomTkinter)
- Paramètres persistés localement (`~/.autoclaude/settings.json`)

---

## Installation

### Option 1 : Télécharger l'exécutable (Windows)

Télécharge `AutoClaude_v2.3.0.exe` depuis les [releases](https://github.com/ServOMorph/AutoClaude/releases) et double-clique pour lancer. Aucune dépendance Python requise.

### Option 2 : Installation depuis le code source

```bash
# Cloner le dépôt
git clone https://github.com/ServOMorph/AutoClaude.git
cd AutoClaude

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python run.py
```

### Dépendances (installation depuis source)

**Obligatoires**

| Package | Rôle |
|---------|------|
| `pyautogui` | Détection et clic d'image (fallback) |
| `pynput` | Écoute clavier/souris |
| `customtkinter` | Interface graphique |
| `Pillow` | Affichage des images |
| `matplotlib` | Graphes d'analyse |
| `psutil` | Monitoring mémoire/stabilité |

**Optionnelles** (meilleures performances)

| Package | Rôle |
|---------|------|
| `opencv-python` | Template matching haute précision |
| `mss` | Capture multi-moniteur rapide |
| `numpy` | Traitement d'image (requis par OpenCV) |
| `screeninfo` | Énumération des moniteurs |

---

## Interface

![AutoClaude UI](assets/ui-screenshot.png)

---

## Utilisation

```bash
# Lancer l'interface graphique
python run.py
```

L'interface permet de :
1. **Activer / désactiver** l'autoclick via le bouton bleu/rouge
2. **Sélectionner un dossier de projet** à protéger
3. **Appliquer ou retirer** la protection Claude Code sur ce dossier
4. **Compter les clics** — affichage en temps réel du nombre total, avec reset possible
5. **Visualiser les analyses** — navigation par période, mode Récent/Tout, stats chiffrées
6. **Afficher/masquer l'indicateur flottant** — overlay visible par-dessus toutes les applications

### Indicateur flottant

Un petit indicateur apparaît en bas à gauche de l'écran, par-dessus toutes les fenêtres :

- 🔵 **Bleu — AutoClaude OFF** : autoclick inactif
- 🔴 **Rouge — AutoClaude ON** : autoclick actif

Un clic sur l'indicateur active ou désactive l'autoclick directement, sans revenir à la fenêtre principale. L'affichage se contrôle via le switch **"Afficher l'indicateur flottant"** dans l'UI.

### Analyses

La fenêtre d'analyses offre :
- **5 périodes** : Heure, Jour, Semaine, Mois, Année
- **Mode Récent** (défaut) : fenêtre glissante — 24h / 30 jours / 12 semaines / 12 mois
- **Mode Tout** : historique complet avec navigation Précédent / Suivant (paginé par jour, mois ou année)
- **Bandeau de stats** : total, moyenne par jour actif, record journalier, jours actifs

### Arrêt

- Touche **Esc** — arrête l'autoclick
- **Fermeture de la fenêtre** — arrête proprement le thread
- **Mouvement souris** — si le mode auto-stop est actif

---

## Image cible

Par défaut, AutoClaude cherche `assets/yes.png`. Remplace ce fichier par un screenshot du bouton que tu veux automatiser (PNG, JPG ou BMP recommandé).

---

## Protection Claude Code

Le bouton **Protéger** injecte un bloc de restrictions dans `.claude/CLAUDE.md` du projet sélectionné. Ce bloc est lu par Claude Code au démarrage de chaque session et contraint le comportement de l'IA au périmètre du projet.

Voir [DOCS/SECURITY.md](DOCS/SECURITY.md) pour le détail du bloc injecté et de l'API.

---

## Logs & stabilité

AutoClaude est conçu pour tourner en continu. Les logs sont disponibles dans `~/.autoclaude/logs/autoclaude.log` (rotation automatique, 5 Mo × 3 fichiers). En cas de crash ou de comportement anormal, ce fichier est le premier endroit à consulter.

---

## Architecture

```
src/core/       détection, clic, listener, service autoclick, logger, health monitor
src/ui/         interface CustomTkinter + composants + dialogs + overlays
src/security/   ClaudeMdProtector
src/config/     constantes et persistance JSON
assets/         yes.png, logo.png
```

Voir [DOCS/ARCHITECTURE.md](DOCS/ARCHITECTURE.md) pour le détail des décisions techniques.

---

## Licence

MIT — voir [LICENSE](LICENSE)

---

Projet réalisé par ServOMorph avec ClaudeCode pour SérénIA Tech :
https://serenia-tech.fr/

Date : 25 avril 2026 (v2.3.0)

---

## Contribuer

Les contributions sont les bienvenues ! Consulter [CONTRIBUTING.md](CONTRIBUTING.md) pour démarrer.


---

----- src\ui\app.py -----

"""TODO: description du module."""

import customtkinter as ctk
from src.config.constants import APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, ASSET_LOGO_ICO, ASSET_YES_PNG
from src.config import settings
from src.core.autoclick_service import AutoclickService
from src.core import health_monitor
from src.core.logger import get_logger
from src.ui import theme
from src.ui.components.header import Header
from src.ui.components.warning_banner import WarningBanner
from src.ui.components.activate_button import ActivateButton
from src.ui.components.protection_button import ProtectionButton
from src.ui.components.footer import Footer
from src.ui.components.click_counter import ClickCounter
from src.ui.components.overlay_toggle import OverlayToggle
from src.ui.dialogs.folder_picker import pick_folder
from src.ui.dialogs.analytics_window import AnalyticsWindow
from src.ui.overlays.status_overlay import StatusOverlay


class AutoClaudeApp(ctk.CTk):
    """TODO: description de AutoClaudeApp."""
    def __init__(self):
        """TODO: description de __init__."""
        theme.apply()
        super().__init__()

        self._log = get_logger()
        self.report_callback_exception = self._on_tk_exception

        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        self.configure(fg_color=theme.PALETTE["bg"])

        self.update_idletasks()
        x = (self.winfo_screenwidth() - WINDOW_WIDTH) // 2
        y = (self.winfo_screenheight() - WINDOW_HEIGHT) // 2
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

        try:
            self.iconbitmap(str(ASSET_LOGO_ICO))
        except Exception:
            pass

        self._service: AutoclickService | None = None
        self._project_path: str = ""

        self._build_ui()
        self.bind("<Escape>", lambda _: self._stop_service())
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._overlay = StatusOverlay(self, on_click=self._activate_btn._toggle)
        if settings.get("overlay_enabled"):
            self._overlay.show()
        else:
            self._overlay.hide()

        health_monitor.start()
        self._log.info("AutoClaude démarré (v%s)", APP_NAME)

    def _on_tk_exception(self, exc_type, exc_val, exc_tb):
        """Hook global Tk — log les exceptions silencieuses au lieu de crasher."""
        self._log.error(
            "Exception Tk non gérée : %s: %s",
            exc_type.__name__, exc_val, exc_info=(exc_type, exc_val, exc_tb),
        )

    def _build_ui(self):
        """TODO: description de _build_ui."""
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)

        Header(self).pack(fill="x", padx=20, pady=(20, 12))

        WarningBanner(
            self,
            text=(
                "• AutoClaude clique automatiquement sur les YES de ClaudeCode (VSCode)\n\n"
                "• ⚠️ À utiliser avec beaucoup de prudence — augmente l'autonomie de ClaudeCode\n\n"
                "• 🔒 Sécurité : protégez votre projet en le sélectionnant et en cliquant "
                "\"Protéger\" — restrictions périmètre injectées automatiquement dans .claude/CLAUDE.md du projet"
            ),
        ).pack(fill="x", padx=20, pady=(0, 16))

        ctk.CTkButton(
            self,
            text="📁  Choisir dossier projet",
            font=ctk.CTkFont(family=theme._font(), size=18, weight="bold"),
            fg_color=theme.PALETTE["bg_secondary"],
            hover_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["text"],
            border_color=theme.PALETTE["border"],
            border_width=1,
            corner_radius=8,
            width=360,
            height=38,
            command=self._pick_folder,
        ).pack(pady=(0, 4))

        self._folder_label = ctk.CTkLabel(
            self, text="Aucun dossier sélectionné",
            font=ctk.CTkFont(size=18),
            text_color=theme.PALETTE["text_muted"],
            wraplength=360,
        )
        self._folder_label.pack(pady=(0, 12))

        self._protection_btn = ProtectionButton(self, button_width=360)
        self._protection_btn.pack(pady=(0, 8))

        center_frame = ctk.CTkFrame(self, fg_color="transparent")
        center_frame.pack(pady=(0, 4))

        self._activate_btn = ActivateButton(center_frame, on_toggle=self._on_toggle)
        self._activate_btn.pack()

        ctk.CTkLabel(
            self, text="Appuyer sur ESC pour désactiver",
            font=ctk.CTkFont(size=11),
            text_color=theme.PALETTE["text_muted"],
        ).pack(pady=(0, 12))

        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(pady=(0, 16))

        self._click_counter = ClickCounter(row, width=170)
        self._click_counter.pack(side="left", padx=(0, 4))

        ctk.CTkButton(
            row,
            text="📊  Graphiques",
            font=theme.font_body(),
            fg_color=theme.PALETTE["bg_secondary"],
            hover_color=theme.PALETTE["border"],
            text_color=theme.PALETTE["text"],
            border_color=theme.PALETTE["border"],
            border_width=1,
            corner_radius=8,
            width=170,
            height=38,
            command=self._open_analytics,
        ).pack(side="right", padx=(4, 0))

        OverlayToggle(self, on_change=self._on_overlay_toggle).pack(pady=(0, 8))

        quit_btn = ctk.CTkButton(
            self,
            text="Quitter",
            font=ctk.CTkFont(family=theme._font(), size=18, weight="bold"),
            fg_color="#1A202C",
            hover_color="#2d3748",
            text_color="#DB775B",
            corner_radius=8,
            width=200,
            height=38,
            command=self._on_close,
        )
        quit_btn.pack(pady=(0, 12))

        Footer(self).pack(fill="x", padx=20, pady=(0, 20), side="bottom")

    def _on_toggle(self, active: bool):
        """TODO: description de _on_toggle."""
        if active:
            self._start_service()
        else:
            self._stop_service()
        self._overlay.set_active(active)

    def _start_service(self):
        """TODO: description de _start_service."""
        image_path = str(ASSET_YES_PNG)
        interval = settings.get("interval")
        auto_stop = settings.get("auto_stop")
        self._service = AutoclickService(
            image_path=image_path,
            interval=interval,
            auto_stop=auto_stop,
            on_stop=self._on_service_stopped,
        )
        self._service.start()

    def _stop_service(self):
        """TODO: description de _stop_service."""
        if self._service:
            self._service.stop()
            self._service = None
        self._activate_btn.set_active(False)
        self._overlay.set_active(False)

    def _on_service_stopped(self):
        """TODO: description de _on_service_stopped."""
        self.after(0, lambda: (
            self._activate_btn.set_active(False),
            self._overlay.set_active(False),
        ))

    def _on_overlay_toggle(self, enabled: bool):
        if enabled:
            self._overlay.show()
        else:
            self._overlay.hide()

    def _pick_folder(self):
        """TODO: description de _pick_folder."""
        path = pick_folder()
        if path:
            self._project_path = path
            self._folder_label.configure(text=path)
            self._protection_btn.set_project_path(path)

    def _open_analytics(self):
        """TODO: description de _open_analytics."""
        AnalyticsWindow(self)

    def _on_close(self):
        """TODO: description de _on_close."""
        self._stop_service()
        health_monitor.stop()
        try:
            self._overlay.destroy()
        except Exception:
            pass
        self._log.info("AutoClaude fermé")
        self.destroy()


---

----- run.py -----

"""TODO: description du module."""

from src.ui.app import AutoClaudeApp

if __name__ == "__main__":
    app = AutoClaudeApp()
    app.mainloop()


---

----- src\config\settings.py -----

"""TODO: description du module."""

import json
from pathlib import Path
from src.config.constants import DEFAULT_INTERVAL

_SETTINGS_DIR = Path.home() / ".autoclaude"
_SETTINGS_FILE = _SETTINGS_DIR / "settings.json"

_DEFAULTS = {
    "interval": DEFAULT_INTERVAL,
    "auto_stop": False,
    "image_path": "",
    "overlay_enabled": True,
}


def load() -> dict:
    """TODO: description de load."""
    if not _SETTINGS_FILE.exists():
        return dict(_DEFAULTS)
    try:
        data = json.loads(_SETTINGS_FILE.read_text(encoding="utf-8"))
        return {**_DEFAULTS, **data}
    except (json.JSONDecodeError, OSError):
        return dict(_DEFAULTS)


def save(settings: dict) -> None:
    """TODO: description de save."""
    _SETTINGS_DIR.mkdir(parents=True, exist_ok=True)
    _SETTINGS_FILE.write_text(
        json.dumps(settings, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def get(key: str):
    """TODO: description de get."""
    return load().get(key, _DEFAULTS.get(key))


def set(key: str, value) -> None:
    """TODO: description de set."""
    data = load()
    data[key] = value
    save(data)


---

