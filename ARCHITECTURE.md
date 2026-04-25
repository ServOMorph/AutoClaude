# Architecture AutoClaude v2.4.0

## Vue d'ensemble

```
AutoClaude/
├── run.py                      # Point d'entrée (4 lignes)
├── requirements.txt            # Dépendances Python
├── ROADMAP.md                  # Phases, statuts, priorités (organe de communication)
├── CHANGELOG.md                # Historique versions + features
├── assets/
│   ├── yes.png                 # Template de détection par défaut
│   └── logo.png                # Branding SéréniaTech
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── constants.py        # Constantes globales (couleurs, paths, URLs, fenêtre, VERSION)
│   │   └── settings.py         # Persistance JSON (~/.autoclaude/settings.json)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── monitors.py         # Énumération des moniteurs
│   │   ├── detector.py         # Détection image par template matching
│   │   ├── clicker.py          # Clic souris
│   │   ├── listener.py         # Écoute clavier/souris (Esc, auto-stop)
│   │   ├── autoclick_service.py# Orchestration thread + événements
│   │   ├── logger.py           # Logs rotatifs + monitoring
│   │   ├── health_monitor.py   # Watchdog de stabilité long-run (24h+)
│   │   └── click_stats.py      # Buffering stats + persistence
│   ├── security/
│   │   ├── __init__.py
│   │   └── claude_md_protector.py  # Injection restrictions dans .claude/CLAUDE.md
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── theme.py            # Palette SéréniaTech + fonts CTk
│   │   ├── app.py              # Fenêtre principale AutoClaudeApp
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── header.py       # Titre + statut
│   │   │   ├── warning_banner.py# Banneau info/warning
│   │   │   ├── activate_button.py# Bouton start/stop autoclick
│   │   │   ├── protection_button.py# Bouton protection CLAUDE.md
│   │   │   ├── footer.py       # Boutons stats + settings
│   │   │   ├── click_counter.py# Affichage + reset compteur clics
│   │   │   └── overlay_toggle.py# Toggle affichage overlay flottant
│   │   ├── dialogs/
│   │   │   ├── __init__.py
│   │   │   ├── folder_picker.py# Sélection dossier projet
│   │   │   └── analytics_window.py# Graphes analyses clics
│   │   └── overlays/
│   │       ├── __init__.py
│   │       └── status_overlay.py# Indicateur flottant always-on-top
│   └── content/                # Source unique pour tips, prompts, learnings
│       └── (filesystem driven — scanné au démarrage)
├── .claude/
│   ├── CLAUDE.md               # Directives essentielles + cycle travail
│   ├── commands/
│   │   ├── start.md            # `/start` — analyser + charger apprentissages
│   │   ├── close.md            # `/close` — documenter + commit
│   │   └── bump_version.md     # `/bump_version` — versioning auto
│   └── learnings/              # (optionnel) learnings project-spécifiques
├── APPRENTISSAGES/             # System d'apprentissage inter-sessions
│   ├── meta.json               # Index (version, count, domains, severity)
│   ├── README.md               # Format + bonnes pratiques
│   ├── core/
│   ├── ui/
│   ├── security/
│   ├── bugs_resolved/
│   └── workflows/
├── ARCHIVES/                   # Stockage fichiers obsolètes + searchable index
│   ├── meta.json               # Index : reason, tags, recall_when
│   ├── README.md               # Système d'archivage
│   ├── docs_legacy/            # Docs historiques remplacées
│   ├── specs_pyinstaller/      # Specs anciennes versions
│   ├── tooling_artifacts/      # Outils legacy
│   └── old_builds/             # Anciens .exe (gitignored)
├── COMET/                      # Intégration Perplexity (docs générées)
│   └── README.md
├── DOCS/                       # Documentation additionnelle
│   ├── SECURITY.md             # Bonnes pratiques sécurité
│   └── PLANS_MAJ/              # (Archived — voir ARCHIVES/)
├── .tooling/                   # Outils de développement
│   ├── bump_version.py         # Script versioning
│   ├── bump_changelog.py       # Script changelog
│   ├── bump_version_files.json # Config patterns
│   └── archive_search.py       # Recherche dans ARCHIVES/
├── build/
│   └── pyinstaller/            # Specs PyInstaller par version
├── dist/                       # Builds compilées
├── .gitignore                  # Ignore build/, dist/, .benchmarks/, etc.
└── LICENSE
```

## Flux d'exécution

```
run.py
  └── AutoClaudeApp (CTk)
        ├── AutoclickService.start()
        │     ├── InputListener (thread)        ← Esc / auto-stop
        │     ├── HealthMonitor (thread)       ← Watchdog stabilité 24h+
        │     └── _run() (thread daemon)
        │           └── loop: detector.locate() → clicker.click() → stats.buffer()
        ├── StatusOverlay (Toplevel always-on-top)  ← Indicateur flottant
        └── ClaudeMdProtector.apply()          ← sur demande utilisateur
```

## Décisions techniques

### Détection image — dégradation progressive

`detector.locate()` essaie les backends dans cet ordre :

| Priorité | Backend | Condition |
|----------|---------|-----------|
| 1 | `outils.image_finder` | Module custom présent |
| 2 | `mss` + `cv2` | Les deux importables |
| 3 | `pyautogui` multi-moniteur | `screeninfo` disponible |
| 4 | `pyautogui` simple | Fallback minimal |

Chaque backend est importé au chargement du module avec `try/except` silencieux. L'absence d'une dépendance optionnelle ne bloque jamais.

### Thread daemon + threading.Event

`AutoclickService` lance son thread en mode `daemon=True` — la VM Python peut quitter sans rejoindre le thread. L'arrêt propre passe par `threading.Event.set()`, testé à chaque itération de la boucle de détection.

### Séparation UI / service

`AutoClaudeApp` ne contient aucune logique de détection. Elle instancie `AutoclickService` et passe des callbacks (`on_click`, `on_stop`) pour mettre à jour l'UI depuis le thread principal via `after()`.

### Persistance paramètres

`src/config/settings.py` lit/écrit `~/.autoclaude/settings.json`. Aucun chemin absolu personnel dans le code source — `Path.home()` est résolu à l'exécution.

## Stabilité & Observabilité (v2.3.0+)

### Logging rotatif

`src/core/logger.py` émet des logs en fichiers rotatifs dans `~/.autoclaude/logs/` avec maximum 10 fichiers de 10MB chacun. Pas de logs console — tout capturé en fichiers pour analyse offline. Gère exceptions réseau, timeouts, click failures sans interruption.

### Health Monitor

`src/core/health_monitor.py` thread daemon qui vérifie chaque 60s :
- Consommation mémoire (seuil 300MB → redémarrage)
- Processus crashed (auto-restart AutoclickService)
- Log file size (rotation manuelle si limite approche)

Permet fonctionnement 24h+ en production sans supervision.

### Stats Buffering

`src/core/click_stats.py` accumule clics en mémoire (buffer 1000 items) puis persiste sur disque toutes les 5 min ou au shutdown. Prévient perte data en cas crash. `ClickCounter` UI affiche les stats persistées. `AnalyticsWindow` offre graphes par période (Récent / Tout) avec navigation temporelle.

## Overlay Flottant (v2.3.0+)

### StatusOverlay — Always-on-top

`src/ui/overlays/status_overlay.py` crée une fenêtre Toplevel CTkToplevel avec :
- **Taille réduite** : 100×60px en bas à gauche de l'écran
- **Always-on-top** : attribute `-topmost True`
- **Clickable** : toggle autoclick on/off sans quitter application active
- **Dynamique** : affiche statut (vert=ON, rouge=OFF) + nombre clics du jour

Fenêtre sans border, parfaitement transparente sauf indicateur couleur. Permet monitoring/control depuis n'importe quelle app (VS Code, navigateur, etc.).

## Dépendances

| Lib | Rôle | Obligatoire |
|-----|------|-------------|
| `customtkinter` | UI mode sombre | Oui |
| `Pillow` | Logo PNG dans CTk | Oui |
| `pyautogui` | Détection + clic fallback | Oui |
| `pynput` | Listener clavier/souris | Oui |
| `matplotlib` | Graphes analyses (Analytics window) | Oui |
| `psutil` | Monitoring mémoire + health check | Oui |
| `opencv-python` | Template matching précis | Non |
| `mss` | Capture multi-moniteur | Non |
| `numpy` | Traitement image cv2 | Non |
| `screeninfo` | Énumération moniteurs | Non |
| `requests` | HTTP GitHub API (v2.5.0 updater) | Non |
| `packaging` | Version comparison (v2.5.0 updater) | Non |
