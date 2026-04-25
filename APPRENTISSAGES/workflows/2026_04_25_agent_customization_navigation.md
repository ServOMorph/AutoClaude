---
title: Pattern Agent Customization — Navigation guidée + Matrice décision
domain: workflows
tags: [agent-onboarding, customization, instructions, multi-ia]
severity: HIGH
created: 2026-04-25
updated: 2026-04-25
version: 2.4.0
---

## Problème identifié

Agents IA collaborant sur AutoClaude avaient contexte fragmenté :
- Nombreux fichiers instructions (testing, learnings, multi-ia, dynamic-content)
- Agents ignoraient quelle instruction charger selon contexte
- Onboarding compliqué, risque désalignement

## Solution implémentée

**AGENTS.md racine** = source vérité unique avec :

1. **Section "Instructions spécialisées (load as-needed)"** — 5 blocs avec conditions déclenchement
2. **Matrice décision rapide** — tableau "Je fais… | Lire…"
3. **Navigation centralisée** — liens vers 4 organes + instructions + commandes

## Pièges évités

✅ AGENTS.md = hub central, toutes conditions, découverte guidée
✅ Matrice décision rapide sans scrolling
✅ Impact: Réduction onboarding agent (30s pour démarrer), alignement unifié multi-IA
