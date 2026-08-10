# Contexte — autoclaude

## Objectif (immuable sauf décision explicite)
Outil Python qui détecte et clique automatiquement sur les boutons de confirmation récurrents de Claude Code, pour donner plus d'autonomie à l'IA sans interrompre son flux de travail.

## Stack / contraintes techniques (stable, rarement modifié)
Python 3.10+, CustomTkinter (UI), OpenCV/mss (détection d'image), PyInstaller (packaging)

## État actuel (réécrit intégralement à chaque /close)
Release GitHub v2.5.12 publiée (tag + `AutoClaude.exe` fonctionnel) — jusqu'ici seul un exe
périmé v2.5.0 était disponible publiquement. Premier build publié par erreur avec des
dépendances manquantes (customtkinter absent de l'environnement de build), corrigé et asset
remplacé. Correctif crash access violation AutoclickWorker (v2.5.11) toujours en attente de
confirmation longue durée. Incohérence pyproject.toml (2.5.6) vs constants.py (2.5.12) non corrigée.

## Décisions structurantes (append only — 10 entrées max, archiver au-delà)
- 2026-07-18 : Initialisation du protocole vibecoding.
- 2026-07-18 : Badge overlay modèle Claude (Haiku/Sonnet/Opus/Fable) — violet foncé,
  attaché à une fenêtre VSCode+Claude Code, modèle choisi manuellement, clic droit
  pour changer le modèle ou supprimer le badge (pas d'action au clic gauche, réservé
  au drag & drop).
- 2026-07-19 : Persistance des badges par titre de fenêtre (hwnd non stable entre sessions) ;
  restauration au démarrage uniquement si la fenêtre existe encore.
- 2026-07-19 : Crash tk86t.dll causé par les cycles withdraw/deiconify + geometry non
  throttlés de ModelBadge ; corrigé en réutilisant le pattern anti-crash de StatusOverlay
  (throttle 4s, geometry conditionnel, reassert_topmost). Logs de crash instrumentés
  (marqueur de session horodaté, sentinelle session.lock) pour rendre tout futur crash
  analysable.
- 2026-07-21 : Badge modèle redimensionné (80x26px) et rendu semi-transparent (alpha 0.65)
  sur demande esthétique ; changement purement visuel, sans impact sur le correctif
  anti-crash tk86t.dll.
- 2026-07-21 : Crash access violation résiduel identifié dans AutoclickWorker (double capture
  GDI mss+cv2/pyautogui + screeninfo en boucle serrée depuis thread secondaire) ; corrigé par
  cache TTL 30s sur get_all_monitors() et suppression du fallback pyautogui/screeninfo quand
  mss+cv2 disponible.
- 2026-08-05 : CI Lint en échec (import Mock inutilisé, Ruff F401) ; corrigé sans impact
  fonctionnel.
- 2026-08-10 : Publication de la release GitHub v2.5.12 (tag + `AutoClaude.exe`), absente
  jusqu'ici. Premier build publié cassé (dépendances de build non installées, customtkinter
  manquant) ; corrigé et asset remplacé. Procédure de build validée : toujours installer
  requirements.txt avant `python build.py` et contrôler warn-AutoClaude.txt avant publication.
