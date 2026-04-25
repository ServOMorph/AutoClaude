---
name: multiia-workflow
description: "Multi-IA workflow orchestration for AutoClaude. Use when: implementing /start /close /doc /bump_version commands, creating adapter integrations (Claude Code, Comet, Antigravity), implementing session management, managing token budgets across agents, creating handoff mechanisms between agents."
applyTo: [".claude/commands/*.md", ".comet/commands/*.md", ".antigravity/commands/*.md", "src/integrations/*.py"]
---

# Multi-IA Workflow Orchestration — AutoClaude v2.6.0+

> Cycle unifié : \\/start\\ → Travail → \\/doc\\ → \\/close\\
>
> IA-agnostique : Claude Code, Comet, Antigravity, autres partagent même cycle.

---

## Architecture Adapters

\\\
src/integrations/
├── base_adapter.py              # Interface abstraite
├── claude_code.py               # Adapter Claude Code
├── comet.py                     # Adapter Comet
└── antigravity.py               # Adapter Antigravity
\\\

Chaque adapter traduit :
- Syntaxe /start unifié → format LLM cible
- Commandes markdown → prompts natifs IA
- Réponses → format normalisation interne

---

## Session Token Budget

Budget par session : **~5000-6500 tokens**

| Phase | Budget | Notes |
|-------|--------|-------|
| Lire 4 organes + apprentissages | 500-800 | \\/start\\ |
| Implémentation | 2000-3000 | tests inclus |
| \\/doc\\ audit | 500 | avant \\/close\\ |
| \\/close\\ | 300 | apprentissages + commit |

**Context reset** : ≥60% budget → créer \\HANDOFF_<task_id>.md\\, handoff suivant agent.

---

## Handoff Format

Créer \\HANDOFF_<task_id>.md\\ si contexte ≥60% :

\\\markdown
# Handoff — [Tâche] v2.4.0

## État fichiers
- ✅ src/ui/sidebar.py — implémentation 80%
- 🔄 tests/unit/test_sidebar.py — TODO: 12 cas
- ⏳ ROADMAP.md — update Phase 11.1 dès completion

## Prochaine étape
[Précise, actionnable, estimée en tokens]

## Pièges identifiés
[Problèmes rencontrés, solutions tentées, anti-patterns]

## Apprentissages chargés
[2-3 docs HIGH/MEDIUM contexte]

## Adapter spécifique
Claude Code ↔ [adapter notes si multi-IA transition]
\\\

---

## Commandes standards

### /start — Démarrage session

Procédure 4 étapes :

1. **Lire 4 organes** (README, ROADMAP, ARCHITECTURE, WORKFLOW)
2. **Charger apprentissages** (max 5-7 HIGH/MEDIUM, ~3000 tokens)
3. **Analyser ROADMAP** (phase actuelle, priorités)
4. **Recommander TOP tâches** (ROI, token budget)

Affichage type :

\\\
=== SESSION DÉMARRÉE ===

Apprentissages: 2 docs (~1200 tokens)
Phase: v2.5.0 Phase 11 🔄

TOP priorités:
1. Finaliser sidebar → impact ROADMAP
2. Couvrir tests → requis v2.5.0

Prochaines étapes:
→ Vérifier src/ui/sidebar/ état
→ Lancer pytest --cov=src
\\\

### /close — Finaliser + Commit

Procédure :

1. **Documenter apprentissages** → \\APPRENTISSAGES/<domain>/<topic>.md\\
2. **Update meta.json** → version, last_updated, total_learnings, by_severity
3. **Valider tests** → \\pytest tests/ --cov=src --cov-fail-under=90\\
4. **Commit normalisé** → \\[type]: description\\

Commit format : \\[feat|fix|refactor|test|docs|chore]: description\\

### /doc — Audit cohérence (v2.6.0+)

Procédure (quand implémentée) :

1. Analyser 4 organes (README, ROADMAP, ARCHITECTURE, WORKFLOW)
2. Vérifier compliance multi-LLM
3. Proposer fixes si warnings majeurs
4. Générer rapport audit
5. Exécuter **avant** \\/close\\ obligatoirement

---

## Principes multi-IA

- **Workflow identique** : /start /close /doc même pour Comet, Antigravity
- **Adapters abstraient** : chaque IA a .comet/, .antigravity/, .claude/
- **Handoff automatisé** : TASKS/ avec frontmatter, assignation, contexte
- **Apprentissages partagés** : APPRENTISSAGES/ centralisé (pas de silos)
- **4 organes vérité unique** : README/ROADMAP/ARCHITECTURE/WORKFLOW sync

---

## Anti-patterns

❌ Documenter apprentissages 1 IA uniquement → Créer HANDOFF au lieu de \\/close\\

❌ Modifier ROADMAP sans update WORKFLOW/ARCHITECTURE → Désync catastrophique

❌ Token budget exceeded sans handoff → Context loss

❌ Hardcoder commandes IA → Adapter indirection = réutilisabilité

✅ Toujours charger apprentissages \\/start\\

✅ Toujours docum apprentissages \\/close\\

✅ Toujours vérifier 4 organes sync

---

## Checklist Adapter implémentation

- [ ] Inherite \\ase_adapter.BaseAdapter\\
- [ ] Implémente \\
ormalize_start_output()\\
- [ ] Implémente \\
ormalize_close_output()\\
- [ ] Tests couverture ≥90%
- [ ] Commandes markdown (.claude/commands/*.md) valides
