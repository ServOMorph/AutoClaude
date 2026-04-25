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
