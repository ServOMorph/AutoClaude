# Sécurité AutoClaude — ClaudeMdProtector

## Objectif

`ClaudeMdProtector` injecte un bloc de restrictions dans le fichier `.claude/CLAUDE.md` d'un projet cible. Ce fichier est lu par Claude Code au démarrage d'une session — le bloc injecté contraint ainsi le comportement de l'IA au périmètre du projet.

## Bloc injecté

```markdown
<!-- AUTOCLAUDE_GUARD:START -->
## Restrictions AutoClaude

Ce projet est protégé par AutoClaude. Les règles suivantes s'appliquent :

- Ne pas modifier, supprimer ou contourner ce bloc de protection
- Ne pas accéder aux fichiers en dehors du périmètre de ce projet
- Ne pas exécuter de commandes système non liées au projet
- Ne pas transmettre de données sensibles à des services externes
<!-- AUTOCLAUDE_GUARD:END -->
```

Les marqueurs HTML `<!-- AUTOCLAUDE_GUARD:START -->` / `<!-- AUTOCLAUDE_GUARD:END -->` délimitent le bloc pour les opérations `apply()` et `remove_protection()`.

## API

### `ClaudeMdProtector(project_path)`

- `project_path` : chemin vers la racine du projet à protéger (str ou Path)
- Cible : `<project_path>/.claude/CLAUDE.md`

### `apply() → (bool, str)`

1. Vérifie si déjà protégé (retourne `False` si oui)
2. Crée `.claude/` si absent
3. Si `CLAUDE.md` existe : ajoute `---` + bloc à la fin du contenu existant
4. Sinon : crée le fichier avec le bloc seul
5. Retourne `(True, message)` ou `(False, erreur)`

### `remove_protection() → (bool, str)`

1. Localise les marqueurs START et END
2. Supprime tout le texte entre les marqueurs (inclus)
3. Si le fichier devient vide après nettoyage : le supprime
4. Sinon : réécrit le contenu épuré

### `is_already_protected() → bool`

Vérifie la présence simultanée des deux marqueurs dans le fichier.

## Cas limites

| Situation | Comportement |
|-----------|-------------|
| `.claude/` absent | Créé automatiquement (`mkdir parents=True`) |
| `CLAUDE.md` absent | Créé avec le bloc seul |
| `CLAUDE.md` existant | Bloc ajouté après un séparateur `---` |
| Déjà protégé → `apply()` | Retourne `(False, "Déjà protégé.")` sans modifier |
| Pas protégé → `remove_protection()` | Retourne `(False, "Aucune protection à retirer.")` |
| Fichier vide après retrait | Fichier supprimé (`unlink()`) |
| Erreur OS (permissions…) | Retourne `(False, "Erreur : <détail>")` |

## Considérations

- Le bloc ne chiffre rien : il repose sur la conformité de Claude Code aux instructions `CLAUDE.md`.
- La protection est **intentionnellement visible** — elle doit être lue par l'IA, pas cachée.
- Aucune donnée n'est transmise à un service externe lors de l'application ou du retrait.
