# Contexte — autoclaude

## Objectif (immuable sauf décision explicite)
Outil Python qui détecte et clique automatiquement sur les boutons de confirmation récurrents de Claude Code, pour donner plus d'autonomie à l'IA sans interrompre son flux de travail.

## Stack / contraintes techniques (stable, rarement modifié)
Python 3.10+, CustomTkinter (UI), OpenCV/mss (détection d'image), PyInstaller (packaging)

## État actuel (réécrit intégralement à chaque /close)
Roadmap du badge overlay modèle Claude définie (roadmap_model_badge.md, 3 phases).
Constantes UI ajoutées (MODEL_BADGE_*). Phase 1 (badge de base) non démarrée.

## Décisions structurantes (append only — 10 entrées max, archiver au-delà)
- 2026-07-18 : Initialisation du protocole vibecoding.
- 2026-07-18 : Badge overlay modèle Claude (Haiku/Sonnet/Opus/Fable) — violet foncé,
  attaché à une fenêtre VSCode+Claude Code, modèle choisi manuellement, clic droit
  pour changer le modèle ou supprimer le badge (pas d'action au clic gauche, réservé
  au drag & drop).
