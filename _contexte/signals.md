# Signals — autoclaude   (MAJ 2026-07-19)

## Actions ouvertes

## Questions ouvertes

## Échéances

## Blocages

## Contexte chaud

## Dernière session (2026-07-19)
<!-- Écrasé intégralement par /close. Synthèse < 25 lignes. -->

## Décisions prises
- Roadmap badge modèle Claude clôturée (3/3 phases implémentées et testées)
- Persistance des badges identifiée par titre de fenêtre (hwnd non stable entre sessions)
- roadmap_model_badge.md archivé dans _archives/

## Livrables produits ou modifiés
- src/core/window_tracker.py : créé (énumération/suivi fenêtres VSCode Win32)
- src/ui/overlays/model_badge.py : attachement fenêtre, suivi position/visibilité, persistance
- src/ui/dialogs/model_badge_picker.py : créé (sélection fenêtre + modèle)
- src/ui/app.py : bouton création badge, multi-badges, restauration au démarrage
- src/config/settings.py : clé model_badges
- README.md, DOCS/ARCHITECTURE.md, CHANGELOG.md : documentation mise à jour
- _archives/roadmap_model_badge.md : roadmap archivée (3 phases [FAIT])
- 32 nouveaux tests unitaires, suite complète 87/87 passants

## Hypothèses validées / invalidées
- VALIDE : suivi par polling léger (pattern OVERLAY_POLL_MS) suffisant, pas besoin du remap anti-fantôme complet de StatusOverlay
- VALIDE : identification des badges persistés par titre de fenêtre plutôt que hwnd

## Prochaine étape exacte
Aucune action de suivi identifiée. Fonctionnalité badge modèle Claude complète.

## Question bloquante pour la session suivante
Aucune
