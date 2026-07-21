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

## Dernière session (2026-07-21)
Analyse des crash.log fournis par l'utilisateur (session plantée plusieurs fois). Diagnostic :
crash déplacé du badge modèle (résolu) vers le worker AutoclickService — double capture GDI
(mss+cv2 + pyautogui/screeninfo) et requêtes screeninfo en boucle serrée. Correctifs appliqués :
cache moniteurs (TTL 30s) et suppression du fallback redondant quand mss+cv2 disponible. Tests
de non-régression ajoutés. Version bumpée 2.5.10 -> 2.5.11.

## Décisions prises
- Diagnostic du crash : cause dans autoclick_service/detector (double moteur de capture GDI +
  screeninfo en boucle serrée), pas dans model_badge — le correctif précédent (tk86t.dll) tient.
- Correctif : cache TTL 30s sur monitors.get_all_monitors() ; detector.locate() n'utilise plus
  le fallback pyautogui/screeninfo quand mss+cv2 est disponible.
- Bump version 2.5.10 -> 2.5.11 (correction, pas de rupture de structure).

## Livrables produits ou modifiés
- src/core/monitors.py : cache TTL 30s (_query_monitors + get_all_monitors)
- src/core/detector.py : locate() ne cumule plus mss_cv2 + fallback pyautogui/screeninfo
- tests/unit/test_monitors.py, tests/unit/test_detector.py : tests de non-régression ajoutés
- src/config/constants.py : VERSION 2.5.11
- CHANGELOG.md, README.md : version 2.5.11
- suite complète : 96/96 tests passants

## Hypothèses validées / invalidées
- VALIDE : le correctif tk86t.dll/model_badge (throttle+geometry, session 2026-07-19) tient —
  aucune fault dans model_badge.py sur les 13 sessions v2.5.10 analysées.
- INVALIDE : l'hypothèse "crash résolu" de la session précédente -> pivot : nouvelle cause
  identifiée (double capture GDI + screeninfo en boucle serrée), corrigée cette session.
- EN ATTENTE : le nouveau correctif (cache moniteurs + suppression fallback) n'a pas été
  confirmé par une session longue réelle — seuls les tests unitaires valident le comportement.

## Prochaine étape exacte
Lancer une session longue (plusieurs heures, badges + autoclick actifs) et vérifier crash.log :
absence de nouvelle entrée toutes causes confondues (model_badge et autoclick_service).

## Question bloquante pour la session suivante
Aucune
