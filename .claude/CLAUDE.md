# CLAUDE.md

Ce fichier guide Claude Code pour ce repository.

## Communication

- Langue : français exclusivement
- Ton : professionnel, synthétique, direct
- Émojis : uniquement les marqueurs définis ci-dessous

## Comportement

- Exécuter uniquement les tâches demandées explicitement
- Ne pas prendre d'initiatives non sollicitées
- Ne pas extrapoler au-delà de la demande
- Ne pas créer de contenu supplémentaire non demandé
- Ne pas ajouter de commentaires non nécessaires dans le code

## Contraintes de code

### Taille des fichiers
- **Maximum 500 lignes par fichier**
- Si un fichier dépasse cette limite : proposer une refactorisation urgente avant de poursuivre

### Architecture modulaire
- À chaque script créé, évaluer systématiquement la division en plusieurs fichiers
- Principe de responsabilité unique : 1 fichier = 1 responsabilité claire
- Privilégier un code modulable et scalable

### Tests
- Créer les tests associés dès qu'une nouvelle fonction est ajoutée
- Voir `tests/README.md` pour la stratégie de couverture

### Conventions de nommage
- Variables/fonctions : camelCase
- Composants React : PascalCase
- Fichiers : kebab-case ou selon framework

## Économie de tokens

### Communication
- ✅ Bullet points plutôt que paragraphes
- ✅ Listes compactes au lieu de texte prosaïque
- ✅ Symboles (🔥, ✅, ⏳) au lieu de longues explications
- ✅ Une ligne par concept → pas de redondance
- ❌ Pas de paraphrases inutiles
- ❌ Pas de contexte déjà dans le repo (lire le code plutôt qu'expliquer)

### Code & Documentation
- ✅ Imports groupés, jamais éparpillés
- ✅ Fonctions compactes (< 20 lignes si possible)
- ✅ Variables nommées explicitement (pas de `x`, `tmp`)
- ✅ Docstrings : 1 ligne max, sinon voir le code
- ✅ Tableaux pour comparaisons (ROI, features, etc.)
- ❌ Pas de commentaires sur le QUOI (le code l'explique)
- ❌ Pas de docstrings verbeux (une phrase suffit)
- ❌ Pas de logs/prints de debug en prod

### Fichiers & Structure
- ✅ Réutiliser les fichiers existants plutôt que créer de nouveaux
- ✅ Consolidate related functions → moins de fichiers
- ✅ `.claude/commands/` : guide en format compact (lire `startV2.md`)
- ❌ Pas de fichiers documentaires superflus
- ❌ Pas de code dupliqué (DRY)
- ❌ Ne pas créer 10 fichiers pour 1 feature

### Reads & Searches
- ✅ Cibler spécifiquement les sections nécessaires (`limit`, `offset` dans Read)
- ✅ Utiliser Grep plutôt que Bash cat/find pour les recherches
- ✅ Glob pour les patterns de fichiers
- ❌ Pas de lectures massives de fichiers volumineux
- ❌ Pas de `git log` complet (utiliser `-n 5` ou `-n 20`)
- ❌ Pas de requêtes imprécises (préparer la requête avant)

## Architecture dynamique (v2.5.0+)

**Contrainte centrale** : Tout contenu est dynamique, aucun hardcodé.

### Principes

- ✅ **Source unique** : `src/content/` est la source de vérité pour tous les contenus (tips, prompts, learnings)
- ✅ **Loaders** : Scannent toujours les dossiers, jamais de listes statiques
- ✅ **UI auto-générée** : Reconstruit depuis fichiers/registry, pas de widgets hardcodés
- ✅ **Extensibilité** : Ajouter un fichier .md ou dossier = fonctionnalité disponible immédiatement
- ❌ Pas de contenu hardcodé dans le code (strings, listes, configurations)
- ❌ Pas de UI générées manuellement (tout dynamique via loaders)
- ❌ Pas de registry statiques (scanned à chaque session)

### Implémentation

**Tips** :
- Scannent `src/content/tips/*.md` au démarrage
- Ajouter un .md = tip disponible, aucun code changeé

**Sidebar & Onglets** :
- `tab_registry.py` : scanne `src/content/` toutes les phases UI (au démarrage, on refresh)
- Chaque dossier en `src/content/` = onglet (tips, prompts, learnings, custom...)
- Sous-dossiers en `src/content/learnings/` = sous-onglets auto (core/, ui/, security/...)

**Fichiers de contenu** :
- Format : `.md` (Markdown)
- Parsage dynamique : `tips_loader`, `markdown_tab` renderer
- Contenu = source de vérité, pas de réplica dans le code

### Anti-patterns

❌ Hardcoder une liste : `tips = [{"id": "tip1", "title": "..."}]`
✅ Scanner et charger : `def load_all_tips() -> list[dict]: ...`

❌ Créer des widgets statiques : `self.buttons = [CTkButton(...), CTkButton(...)]`
✅ Générer depuis registry : `for tab in registry: self.add_tab(tab)`

❌ Dupliquer contenu : `src/ui/tips.py` contient une copie des tips
✅ Une source : `src/content/tips/` lue par `tips_loader` et `tips_dialog`

## Cycle de travail standardisé (OBLIGATOIRE)

Chaque session suit ce cycle pour garantir continuité et apprentissage :

### 1️⃣ Démarrage — `/start` (startV2.md)
- Lire ROADMAP, README, ARCHITECTURE
- Analyser contexte projet (technologies, type de travail)
- **Charger apprentissages pertinents** depuis APPRENTISSAGES/
  - Scanner meta.json
  - Sélectionner TOP 5-7 docs (HIGH severity + domaine)
  - Intégrer dans contexte (max 3000 tokens)
- Afficher recommandation ROI (meilleur choix)

### 2️⃣ Travail
- Utiliser contexte + apprentissages chargés
- Logger issues et solutions
- Tester et valider changements

### 3️⃣ Clôture — `/close` (closeV2.md)
- Mettre à jour ROADMAP, README, ARCHITECTURE
- **Documenter apprentissage si nouveau** (bug résolu / pattern)
  - Créer APPRENTISSAGES/<domain>/<topic>.md
  - Format : title, domain, tags, severity, code, pièges
  - Mettre à jour APPRENTISSAGES/meta.json
  - Vérifier compact (< 500 tokens)
- Commit avec message explicite
- Fin session

### Continuité inter-sessions
Les apprentissages documentés dans `/close` sont automatiquement chargés dans `/start` suivant, créant une accumulation progressive de savoir.

## Système d'apprentissage

### Structure
```
APPRENTISSAGES/                  ← Racine (parallèle à DOCS/, src/)
├── meta.json                    ← Index (version, count, domains)
├── core/                        ← Patterns : détection, clic, listener
├── ui/                          ← Patterns : CustomTkinter, theme, components
├── security/                    ← Sécurité : protection, permissions
├── bugs_resolved/               ← Bugs résolus (datés)
└── workflows/                   ← Workflows : versioning, build, update
```

### Format apprentissage (.md)

```markdown
---
title: "Titre apprentissage"
domain: "core|ui|security|bugs_resolved|workflows"
tags: ["tag1", "tag2"]
severity: "high|medium|low"       # HIGH = critical, MEDIUM = useful, LOW = nice-to-know
created: "2024-04-25"
updated: "2024-04-25"
version: "v2.4.0"                 # Version du projet quand découvert
---

## Problème
Description du problème/pattern

## Solution
Comment ça a été résolu

## Code pattern (si applicable)
```python
# code example
```

## Pièges à éviter
- ❌ Piège 1
- ✅ Good practice 1
```

### Sélection apprentissages (optimisé tokens)
- Chargement : max 5-7 docs, max 3000 tokens
- Critères : domaine + sévérité HIGH/MEDIUM
- Meta.json = index (petit fichier, peut être toujours chargé pour filtrage rapide)
- Fallback : si aucun apprentissage pertinent = "Pas d'apprentissages (première session / domaine nouveau)"

### Gestion meta.json
```json
{
  "version": "v2.4.0",
  "last_updated": "2024-04-25T09:47:00Z",
  "total_learnings": 15,
  "domains": {
    "core": 4,
    "ui": 5,
    "security": 2,
    "bugs_resolved": 3,
    "workflows": 1
  },
  "by_severity": {
    "high": ["detector.md", "listener.md", ...],
    "medium": ["customtkinter_patterns.md", ...],
    "low": [...]
  }
}
```
