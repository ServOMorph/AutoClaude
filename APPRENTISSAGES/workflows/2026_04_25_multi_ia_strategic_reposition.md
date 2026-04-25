---
title: Reposition stratégique vers centre de commande multi-IA
domain: workflows
tags: architecture, multi-ia, docs-coherence, strategy
severity: medium
created: 2026-04-25T16:00:00Z
updated: 2026-04-25T16:00:00Z
version: v2.4.0
---

## Problème

Projet existant (v2.4.0) : "outil de clic auto" — cohérent mais limité scope.
Nouvelle mission révélée : "centre de commande multi-IA" (orchestrer Claude Code, Comet, Antigravity, autres).

**Challenge** :
- Adapter vision sans casser cohérence docs existants
- Identifier what stays (autoclick module), what expands (UI hub), what's added (adapters, workflow unifié)
- Garder 4 organes de communication synchronisés (README/ROADMAP/ARCHITECTURE/WORKFLOW)
- Planifier phases d'implémentation sans disruption

## Solution

### 1. Reposition pragmatique (non-destructive)

Garder v2.0-v2.4 historique intact, annoncer NEW mission explicitement :

```markdown
# README.md (nouvelle intro)
> Centre de commande multi-IA…
> L'autoclick est un module parmi d'autres.
```

Avantage : zéro régression, clarté immédiate.

### 2. Architecture 4 organes cohérents

| Organe | Scope | Responsable |
|--------|-------|-------------|
| README.md | Mission, features utilisateur | README lire en premier |
| ROADMAP.md | Phases, priorités, implémentation | Plan exécution |
| ARCHITECTURE.md | Code structure, décisions techniques | Details techniques |
| WORKFLOW.md (NEW) | Cycle /start /close /doc IA-agnostique | Toutes IA appliquent même |

**Clé** : WORKFLOW.md unifie multi-IA — sans lui, chaque IA invente sa propre procédure.

### 3. Phases délimitées clairement

```
v2.5.0 (v2.3.0+autoclick+tests+sidebar)
v2.6.0 (/doc audit + workflow unifié)
v2.7.0 (connecteurs IA + orchestration)
v2.8.0 (auto-updater + final)
```

Pas d'overlap : chaque version ajoute 1-3 features cohérentes.

### 4. Handoff inter-IA via `TASKS/` + `HANDOFF_*`

Quand contexte saturé :
- IA-A crée `HANDOFF_<task_id>.md` → état fichiers, pièges, prochaine étape précise
- IA-B lit WORKFLOW.md `/start` → reprend via HANDOFF
- Continuum garantie

**Apprentissage** : token budget ~5k/session = 1-2 phases max. Reset = handoff obligatoire dès v2.7.0.

## Code pattern

### WORKFLOW.md template

```markdown
## /start — Démarrage
1. Lire 4 organes
2. Charger apprentissages
3. Analyser ROADMAP → recommander tâches

## Travail
- Implémenter + tests

## /doc (v2.6.0+)
- Auditer cohérence + compliance multi-LLM
- Proposer fixes

## /close
- Documenter apprentissages
- Commit normalisé
- Tag version
```

Tous adapters appliquent MÊME workflow (traduction syntaxe cible seulement).

### Session management

```json
{
  "token_budget": 5000,
  "phases_per_session": "1-2 majeures",
  "context_reset_trigger": "≥60% max",
  "handoff_required": "v2.7.0+"
}
```

**Clé** : budgétiser AVANT implémenter, sinon contexte overflow = travail perdu.

## Pièges

### ❌ Piège 1 : Garder 3 organes (sans WORKFLOW.md)
Multi-IA divergent → chacune invente `/start` `/close` différemment. Incohérence garantie.

**Mitigation** : WORKFLOW.md obligatoire dès v2.6.0. Valider `/doc` audit le vérifie.

### ❌ Piège 2 : Adapter syntaxe MAIS oublier cycle unifié
Chaque IA lit organes différemment → comprend mission différemment.

**Mitigation** : WORKFLOW.md décrit cycle IA-agnostique. Adapters = traduction SEULEMENT.

### ❌ Piège 3 : Token budget ignoré
Essayer implémenter 3 phases en 1 session → contexte overflow = features boileplate/broken.

**Mitigation** : Session mgmt Phase 13.4. Handoff systématique dès 60% context.

### ❌ Piège 4 : Phase 11.5 (/doc audit) oubliée
Créer sidebar sans audit cohérence doc → v2.5.0 release avec inconsistencies.

**Mitigation** : `/doc` appelé obligatoirement avant `/close` (fail si warnings majeurs).

## Checklist future repositioning

Pour futurs projets multi-IA :

- [ ] Identifier mission NEW
- [ ] Créer 4ème organe (workflow unifié)
- [ ] Adapter phases (1-2 par version)
- [ ] Définir handoff format (TASKS/ + HANDOFF_*)
- [ ] Budgétiser sessions (tokens per phase)
- [ ] Audit cohérence AVANT release (/doc)
- [ ] Tester multi-IA (CC + Comet + Antigravity minimum)
