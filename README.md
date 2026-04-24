# AutoClaude

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Tests](https://github.com/ServOMorph/AutoClaude/actions/workflows/tests.yml/badge.svg)](https://github.com/ServOMorph/AutoClaude/actions/workflows/tests.yml)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/ServOMorph/AutoClaude/releases)


Outil Python qui détecte et clique automatiquement sur un bouton récurrent à l'écran — avec une interface graphique CustomTkinter en mode sombre.

> Développé par [SéréniaTech](https://serenia-tech.fr) · [GitHub](https://github.com/ServOMorph)

---

## Fonctionnalités

- Détection d'image par template matching (OpenCV + mss)
- Support multi-moniteur
- Dégradation progressive : si une dépendance optionnelle manque, l'outil continue de fonctionner
- Arrêt via Esc, fermeture fenêtre ou mouvement souris (mode auto-stop)
- Protection de projet Claude Code via injection dans `.claude/CLAUDE.md`
- **Compteur de clics** avec historique persisté
- **Analyses graphiques** : visualiser les clics par heure/jour/semaine/mois/année
- Interface sombre SéréniaTech (CustomTkinter)
- Paramètres persistés localement (`~/.autoclaude/settings.json`)

---

## Installation

### Option 1 : Télécharger l'exécutable (Windows)

Télécharge `AutoClaude.exe` depuis les [releases](https://github.com/ServOMorph/AutoClaude/releases) et double-clique pour lancer. Aucune dépendance Python requise.

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
5. **Visualiser les analyses** — graphes interactifs par période (heure/jour/semaine/mois/année)

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

## Architecture

```
src/core/       détection, clic, listener, service autoclick
src/ui/         interface CustomTkinter + composants + dialogs
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

Date : 24 avril 2026 (v2.2.0)


---

## Contribuer

Les contributions sont les bienvenues ! Consulter [CONTRIBUTING.md](CONTRIBUTING.md) pour démarrer.
