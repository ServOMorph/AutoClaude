# Signals — autoclaude   (MAJ 2026-07-21)

## Actions ouvertes
- [P1] Confirmer sur une session longue (plusieurs heures, badges + autoclick actifs) que
  plus aucun crash access violation ne se produit (ni model_badge, ni autoclick_service/screeninfo).
  fait quand: une session de plusieurs heures se termine sans que session.lock persiste au
  prochain démarrage (pas de warning "session précédente terminée anormalement") et sans
  nouvelle entrée dans crash.log.
  réf: run.py (sentinelle session.lock, marqueur horodaté crash.log), src/core/detector.py,
  src/core/monitors.py, src/core/autoclick_service.py

## Contexte chaud
- Analyse de ~/.autoclaude/logs/crash.log (13 sessions v2.5.10) : le correctif tk86t.dll/
  model_badge (throttle 4s + geometry conditionnel, session 2026-07-19) tient — aucune fault
  dans model_badge.py sur ces sessions. Mais l'app a continué à crasher, cette fois dans le
  thread AutoclickWorker : double moteur de capture GDI (mss+cv2 puis pyautogui/screeninfo)
  empilés à chaque tick (0.5s), avec screeninfo interrogé en boucle serrée depuis un thread
  secondaire — signature classique de corruption mémoire différée (site de fault natif variable
  d'un crash à l'autre : screeninfo, matchTemplate, time.sleep).
- Correctif appliqué cette session (cache TTL 30s sur get_all_monitors, suppression du fallback
  pyautogui/screeninfo quand mss+cv2 disponible) mais non confirmé en conditions réelles longue
  durée — seuls les tests unitaires valident le comportement. À rouvrir si nouvelle fault dans
  crash.log malgré le correctif, y compris avec un site natif différent.

## Dernière session (2026-08-05)
CI Lint (GitHub Actions) en échec : import `Mock` inutilisé dans
tests/unit/test_window_tracker.py (Ruff F401, bloquant). Corrigé (import retiré, `patch` reste
utilisé). `ruff check src/ tests/` repasse sans erreur. Version bumpée 2.5.11 -> 2.5.12.

## Décisions prises
- Correctif CI : suppression de l'import `Mock` inutilisé dans test_window_tracker.py (Ruff F401).
- Bump version 2.5.11 -> 2.5.12 (correction, pas de rupture de structure).

## Livrables produits ou modifiés
- tests/unit/test_window_tracker.py : import Mock retiré (patch conservé, toujours utilisé)
- src/config/constants.py : VERSION 2.5.12
- CHANGELOG.md, README.md : version 2.5.12

## Hypothèses validées / invalidées
- VALIDE : `ruff check src/ tests/` repasse sans erreur après retrait de l'import mort.
- EN ATTENTE : le correctif crash access violation (2.5.11, cache moniteurs + suppression
  fallback) n'a toujours pas été confirmé par une session longue réelle.

## Prochaine étape exacte
Lancer une session longue (plusieurs heures, badges + autoclick actifs) et vérifier crash.log :
absence de nouvelle entrée toutes causes confondues (model_badge et autoclick_service).

## Question bloquante pour la session suivante
Aucune
