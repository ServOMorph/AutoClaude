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

## Dernière session (2026-07-21)
Demande esthétique sur le badge modèle : cadre trop grand, fond trop opaque. Réduction des
dimensions et du padding, ajout d'une transparence de fenêtre. Modification purement visuelle,
aucun changement de comportement (throttle/tracking inchangés).

## Décisions prises
- Réduire le badge modèle : 140x50 -> 80x26px, corner_radius 10 -> 6, padding 10/5 -> 4/2px,
  police 13 -> 11.
- Fond semi-transparent via attributes("-alpha", MODEL_BADGE_ALPHA=0.65) sur la fenêtre
  entière (limite connue : rend aussi le texte translucide, pas de transparence sélective
  du fond seul sans passer par -transparentcolor).
- Bump version 2.5.9 -> 2.5.10 (changement cosmétique, pas de rupture de structure).

## Livrables produits ou modifiés
- src/config/constants.py : MODEL_BADGE_WIDTH/HEIGHT réduits, MODEL_BADGE_ALPHA ajouté,
  VERSION 2.5.10
- src/ui/overlays/model_badge.py : alpha appliqué, corner_radius/padding/police réduits
- CHANGELOG.md, README.md : version 2.5.10
- suite complète : 94/94 tests passants (aucun test cassé par le changement visuel)

## Hypothèses validées / invalidées
- VALIDE : la signature crash (access violation tk86t.dll, pas de fuite mémoire) confirme
  un problème de cycle map/unmap Tk, pas une fuite de ressources (session précédente).
- EN ATTENTE : le correctif throttle/geometry conditionnel élimine réellement le crash —
  seule une session longue en conditions réelles peut le confirmer. Non testé cette session
  (changement purement visuel, pas de session longue lancée).
- EN ATTENTE : le rendu visuel du badge réduit/transparent n'a pas été vérifié à l'écran
  (pas d'accès à l'exécution UI dans cet environnement) — à valider au prochain lancement.

## Prochaine étape exacte
Lancer l'application, vérifier visuellement le badge modèle (taille, transparence) et
poursuivre la session longue en attente (badges actifs, plusieurs heures) pour confirmer
l'absence de crash tk86t.dll.

## Question bloquante pour la session suivante
Aucune
