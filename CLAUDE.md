# CLAUDE.md

## Langue
Réponds toujours en français.

## Économie de tokens
- Réponses courtes et directes — pas de résumé en fin de message
- Pas de commentaires dans le code sauf si la logique est non-évidente
- Pas de docstrings multi-lignes
- Lire uniquement les sections de fichier nécessaires (offset/limit)
- Ne pas relire un fichier déjà lu dans la même session
- Proposer une approche en 1-2 phrases avant d'implémenter ; attendre validation si l'impact dépasse 3 fichiers
- Pas de fichiers de doc intermédiaires (analyses, plans) sauf si explicitement demandé

## Lancer
```bash
python run.py [--image yes.png] [--interval 0.5] [--auto-stop]
```

## Install
```bash
pip install -r requirements.txt
```

## Architecture v1
`run.py` : dégradation progressive — `outils/image_finder` → cv2+mss → screeninfo+pyautogui → pyautogui. Clic : `outils/mouse_controller` → pyautogui. Arrêt : Esc / Ctrl+C / `--auto-stop`.

## Architecture v2.0 (planifiée)
Voir [DOCS/DEVELOPMENT_PLAN.md](DOCS/DEVELOPMENT_PLAN.md) et [DOCS/ROADMAP.md](DOCS/ROADMAP.md).

```
src/core/       detector, clicker, monitors, listener, autoclick_service
src/ui/         CTk app + thème sombre SéréniaTech + components/ + dialogs/
src/security/   claude_md_protector.py
src/config/     constants.py, settings.py (JSON)
assets/         yes.png, logo.png
```

Décisions clés :
- `AutoclickService` : thread daemon + `threading.Event` pour arrêt propre
- `ClaudeMdProtector` : injecte restrictions périmètre dans `.claude/CLAUDE.md` — fonctionnalité intentionnelle
- Paramètres persistés en JSON (`~/.autoclaude/settings.json`)
