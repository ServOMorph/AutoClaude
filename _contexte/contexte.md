# Contexte — autoclaude

## Objectif (immuable sauf décision explicite)
Outil Python qui détecte et clique automatiquement sur les boutons de confirmation récurrents de Claude Code, pour donner plus d'autonomie à l'IA sans interrompre son flux de travail.

## Stack / contraintes techniques (stable, rarement modifié)
Python 3.10+, CustomTkinter (UI), OpenCV/mss (détection d'image), PyInstaller (packaging)

## État actuel (réécrit intégralement à chaque /close)
Badge overlay modèle Claude fonctionnel, mais avait provoqué des crashs intermittents
(access violation tk86t.dll) via des cycles withdraw/deiconify et geometry() non throttlés.
Correctif appliqué (throttle 4s, geometry conditionnel, pattern StatusOverlay) + logs de
crash rendus datables/exploitables. Non confirmé en conditions réelles longue durée.
94 tests unitaires passants, v2.5.9.

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
