# Signals — autoclaude   (MAJ 2026-07-18)

## Actions ouvertes
- [P1|ouvert] Implémenter Phase 1 de roadmap_model_badge.md (badge overlay de base)
  fait quand: src/ui/overlays/model_badge.py existe, drag & drop + clic droit
  (changer modèle / supprimer) fonctionnels, tests unitaires passants
  réf: roadmap_model_badge.md, src/ui/overlays/status_overlay.py (pattern de référence)

## Questions ouvertes

## Échéances

## Blocages

## Contexte chaud
- Fenêtres cibles du badge modèle : VSCode + extension Claude Code (chat intégré)
- Choix du modèle sur le badge : manuel (pas de détection auto), cycle via clic droit

## Dernière session (2026-07-18)
<!-- Écrasé intégralement par /close. Synthèse < 25 lignes. -->

## Décisions prises
- Badge overlay violet foncé (#5A189A) pour afficher le modèle Claude actif
- Suit la fenêtre VSCode ciblée, drag & drop au clic gauche
- Clic droit : menu contextuel (changer modèle / supprimer badge) — pas d'action au clic gauche
- Modèle choisi manuellement, pas de détection automatique
- Roadmap en 3 phases : badge de base, attachement fenêtre VSCode, intégration UI + persistance

## Livrables produits ou modifiés
- roadmap_model_badge.md : créé (3 phases, spécifications validées)
- src/config/constants.py : ajout MODEL_BADGE_WIDTH/HEIGHT/COLOR/TEXT_COLOR

## Hypothèses validées / invalidées
- VALIDE : approche manuelle pour le choix du modèle (pas d'OCR/détection auto)
- VALIDE : clic droit pour changer modèle + supprimer (pas de clic gauche)
- EN ATTENTE : aucun code fonctionnel implémenté (Phase 1 non démarrée)

## Prochaine étape exacte
Démarrer Phase 1 : créer src/ui/overlays/model_badge.py (CTkToplevel, drag & drop,
menu contextuel clic droit) en réutilisant le pattern de status_overlay.py.

## Question bloquante pour la session suivante
Aucune
