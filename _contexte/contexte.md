# Contexte — autoclaude

## Objectif (immuable sauf décision explicite)
Outil Python qui détecte et clique automatiquement sur les boutons de confirmation récurrents de Claude Code, pour donner plus d'autonomie à l'IA sans interrompre son flux de travail.

## Stack / contraintes techniques (stable, rarement modifié)
Python 3.10+, CustomTkinter (UI), OpenCV/mss (détection d'image), PyInstaller (packaging)

## État actuel (réécrit intégralement à chaque /close)
Correctif anti-crash tk86t.dll/model_badge validé par l'analyse de 13 sessions crash.log
(aucune récidive). Correctif crash access violation AutoclickWorker (cache TTL 30s moniteurs,
suppression fallback GDI redondant) en place depuis v2.5.11, confirmation longue durée
toujours en attente. CI Lint (Ruff) remis au vert après retrait d'un import mort. v2.5.12.

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
