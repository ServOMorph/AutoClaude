# Signals — autoclaude   (MAJ 2026-07-19)

## Actions ouvertes
- [P1] Confirmer sur une session longue (plusieurs heures, badges actifs) que le crash
  access violation tk86t.dll ne se reproduit plus.
  fait quand: une session de plusieurs heures avec badges actifs se termine sans que
  session.lock persiste au prochain démarrage (pas de warning "session précédente
  terminée anormalement") et sans nouvelle entrée dans crash.log.
  réf: run.py (sentinelle session.lock, marqueur horodaté crash.log), src/ui/overlays/model_badge.py

## Questions ouvertes

## Échéances

## Blocages

## Contexte chaud
- Le crash n'est pas confirmé résolu, seulement corrigé par hypothèse (throttle
  withdraw/deiconify + geometry conditionnel, pattern aligné sur StatusOverlay).
  À rouvrir si un nouveau crash apparaît dans crash.log malgré le correctif.

## Dernière session (2026-07-19)
Bug remonté : plantages intermittents depuis l'ajout des badges modèle. Diagnostic via
crash.log (faulthandler) : access violation native tk86t.dll, signature connue (cf. doc
virtual_desktop.py), pas de fuite mémoire (RSS/handles/threads stables). Cause identifiée :
ModelBadge._track_window() faisait withdraw/deiconify et geometry() sans throttle ni
condition, contrairement au pattern anti-crash déjà validé dans StatusOverlay. Correctif
appliqué + instrumentation du système de logs pour rendre le prochain crash exploitable
(non testé en conditions réelles longue durée dans cette session).

## Décisions prises
- Aligner ModelBadge sur le pattern anti-crash de StatusOverlay : throttle 4s sur les
  transitions withdraw/deiconify, geometry() conditionné à un changement de position réel,
  reassert_topmost Win32 après deiconify, annulation du after() de suivi à la destruction.
- Instrumenter run.py pour rendre les crashs futurs analysables : marqueur de session
  horodaté dans crash.log, sentinelle session.lock (détection fin anormale), purge de
  crash.log au-delà de 1 Mo.
- Bump version 2.5.8 -> 2.5.9 (correctifs, pas de rupture de structure).

## Livrables produits ou modifiés
- src/ui/overlays/model_badge.py : throttle visibilité, geometry conditionnel,
  reassert_topmost, destroy() annule le after, logs INFO/ERROR sur les transitions
- run.py : marqueur de session horodaté, sentinelle session.lock, purge crash.log
- src/config/constants.py : VERSION 2.5.9
- tests/unit/test_model_badge.py : 5 nouveaux tests + 2 tests existants ajustés
- tests/unit/test_run_entry.py : créé (3 tests purge crash.log)
- suite complète : 94/94 tests passants

## Hypothèses validées / invalidées
- VALIDE : la signature crash (access violation tk86t.dll, pas de fuite mémoire) confirme
  un problème de cycle map/unmap Tk, pas une fuite de ressources.
- EN ATTENTE : le correctif throttle/geometry conditionnel élimine réellement le crash —
  seule une session longue en conditions réelles peut le confirmer.

## Prochaine étape exacte
Faire tourner l'application en usage normal (badges actifs) sur une session longue.
Vérifier au prochain démarrage l'absence de warning "session précédente terminée
anormalement" et l'absence de nouvelle entrée dans crash.log.

## Question bloquante pour la session suivante
Aucune
