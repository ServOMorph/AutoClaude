# Architecture AutoClaude v2.0

## Vue d'ensemble

```
AutoClaude/
├── run.py                  # Point d'entrée (4 lignes)
├── assets/
│   ├── yes.png             # Template de détection par défaut
│   └── logo.png            # Branding SéréniaTech
├── src/
│   ├── config/
│   │   ├── constants.py    # Constantes globales (couleurs, paths, URLs, fenêtre)
│   │   └── settings.py     # Persistance JSON (~/.autoclaude/settings.json)
│   ├── core/
│   │   ├── monitors.py     # Énumération des moniteurs
│   │   ├── detector.py     # Détection image par template matching
│   │   ├── clicker.py      # Clic souris
│   │   ├── listener.py     # Écoute clavier/souris (Esc, auto-stop)
│   │   └── autoclick_service.py  # Orchestration thread + événements
│   ├── security/
│   │   └── claude_md_protector.py  # Injection restrictions dans .claude/CLAUDE.md
│   └── ui/
│       ├── theme.py        # Palette SéréniaTech + fonts CTk
│       ├── app.py          # Fenêtre principale AutoClaudeApp
│       ├── components/
│       │   ├── header.py
│       │   ├── warning_banner.py
│       │   ├── activate_button.py
│       │   ├── protection_button.py
│       │   └── footer.py
│       └── dialogs/
│           └── folder_picker.py
└── DOCS/
```

## Flux d'exécution

```
run.py
  └── AutoClaudeApp (CTk)
        ├── AutoclickService.start()
        │     ├── InputListener (thread)   ← Esc / auto-stop
        │     └── _run() (thread daemon)
        │           └── loop: detector.locate() → clicker.click()
        └── ClaudeMdProtector.apply()      ← sur demande utilisateur
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

## Dépendances

| Lib | Rôle | Obligatoire |
|-----|------|-------------|
| `customtkinter` | UI mode sombre | Oui |
| `Pillow` | Logo PNG dans CTk | Oui |
| `pyautogui` | Détection + clic fallback | Oui |
| `pynput` | Listener clavier/souris | Oui |
| `opencv-python` | Template matching précis | Non |
| `mss` | Capture multi-moniteur | Non |
| `numpy` | Traitement image cv2 | Non |
| `screeninfo` | Énumération moniteurs | Non |
