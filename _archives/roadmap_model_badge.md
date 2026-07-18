# Roadmap — Badge overlay modèle Claude

## Objectif
Bouton dans l'UI AutoClaude qui crée des overlays badge (violet foncé) affichant le modèle
Claude utilisé (Haiku, Sonnet, Opus, Fable) dans une fenêtre VSCode + extension Claude Code.

## Spécifications validées
- Fenêtres cibles : VSCode avec extension Claude Code (chat intégré).
- Le badge est attaché à une fenêtre VSCode : il la suit quand elle bouge.
- Visible uniquement quand la fenêtre est affichée (masqué si minimisée/fermée).
- Repositionnable par drag & drop (position relative à la fenêtre, choisie par l'utilisateur).
- Couleur : violet foncé (`MODEL_BADGE_COLOR = #5A189A`, déjà dans constants.py).
- Modèle défini manuellement à la création (pas de détection automatique).
- Clic gauche : uniquement drag & drop (pas d'action au clic simple).
- Clic droit : menu contextuel — changer le modèle affiché ou supprimer le badge.

## Phases

### Phase 1 — Badge overlay de base [FAIT]
- Créer `src/ui/overlays/model_badge.py` : CTkToplevel sans bordure, topmost,
  badge violet foncé affichant le nom du modèle.
- Drag & drop au clic gauche (réutiliser le pattern StatusOverlay).
- Clic droit : menu contextuel — changer le modèle (Haiku, Sonnet, Opus, Fable)
  ou supprimer le badge.
- Tests unitaires (changement modèle, suppression, drag, rendu).

**⏸ Checkpoint** — Demander à l'utilisateur de faire `/compact` avant de continuer.
Attendre sa réponse écrite. Ne pas commencer la phase suivante sans confirmation.

### Phase 2 — Attachement à une fenêtre VSCode [FAIT]
- `src/core/window_tracker.py` : énumération des fenêtres VSCode (Win32 EnumWindows,
  filtre sur classe/titre), suivi position/taille/état d'une fenêtre par hwnd.
- Le badge suit la fenêtre : position relative maintenue quand la fenêtre bouge
  (polling léger, pattern OVERLAY_POLL_MS existant).
- Visibilité synchronisée : masqué si fenêtre minimisée/fermée/cloaked (réutiliser
  `is_cloaked` de virtual_desktop.py), réaffiché sinon.
- Drag & drop met à jour la position relative à la fenêtre.
- Tests unitaires (calcul position relative, transitions visibilité).

**⏸ Checkpoint** — Demander à l'utilisateur de faire `/compact` avant de continuer.
Attendre sa réponse écrite. Ne pas commencer la phase suivante sans confirmation.

### Phase 3 — Intégration UI et persistance [FAIT]
- Bouton "Créer un badge modèle" dans l'UI principale (app.py) : sélection de la
  fenêtre VSCode cible + modèle initial, puis création du badge.
- Gestion multi-badges (un par fenêtre VSCode).
- Persistance dans settings : fenêtre cible, position relative, modèle ; restauration
  au démarrage si la fenêtre existe encore.
- Tests unitaires (persistance, restauration, multi-badges).

**⏸ Checkpoint** — Demander à l'utilisateur de faire `/compact` avant de continuer.
Attendre sa réponse écrite. Ne pas commencer la phase suivante sans confirmation.
