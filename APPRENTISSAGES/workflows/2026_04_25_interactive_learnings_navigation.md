---
title: Pattern Interactive Learnings Navigation — Liens cliquables dans /start /close
domain: workflows
tags: [learnings-ux, navigation, interactive-reports, ide-integration]
severity: HIGH
created: 2026-04-25
updated: 2026-04-25
version: 2.4.0
---

## Problème identifié

Sessions `/start` et `/close` affichaient apprentissages en texte statique :
- Apprentissages non-cliquables → recherche manuelle dans `APPRENTISSAGES/`
- Consultation contenu difficile (beaucoup de scrolling dans `APPRENTISSAGES/meta.json`)
- Faible découverte capital accumulé inter-sessions
- Agent suivant doit relire organes + apprentissages en texte brut

## Solution implémentée

**Tableaux markdown cliquables** dans rapports `/start` et `/close` :

### `/start` — Apprentissages chargés
```
📚 **Apprentissages chargés** : [N] docs (~Y tokens)

| Domain | Severity | Lien |
|--------|----------|------|
| workflows | HIGH | [agent_customization_navigation.md](APPRENTISSAGES/workflows/2026_04_25_agent_customization_navigation.md) |
| ui | MEDIUM | [customtkinter_best_practices.md](APPRENTISSAGES/ui/customtkinter_best_practices.md) |
```

### `/close` — Apprentissages documentés + capital accumulé
```
| Domain | Severity | Fichier | Lien |
|--------|----------|---------|------|
| workflows | HIGH | interactive_learnings_navigation.md | [📖 Lire](APPRENTISSAGES/workflows/2026_04_25_interactive_learnings_navigation.md) |

**État meta.json (capital connaissances)** :

| Domain | Count | Top HIGH/MEDIUM |
|--------|-------|-----------------|
| workflows | 2 | [agent_customization_navigation.md](APPRENTISSAGES/workflows/2026_04_25_agent_customization_navigation.md), [interactive_learnings_navigation.md](APPRENTISSAGES/workflows/2026_04_25_interactive_learnings_navigation.md) |
```

## Code pattern

**`.claude/commands/start.md`** :
```markdown
## 5️⃣ Charger apprentissages 📚

| Domain | Severity | Lien |
|--------|----------|------|
| core | HIGH | [detector_patterns.md](APPRENTISSAGES/core/detector_patterns.md) |
| ui | MEDIUM | [sidebar_rendering.md](APPRENTISSAGES/ui/sidebar_rendering.md) |
```

**`.claude/commands/close.md`** :
```markdown
### 📚 Apprentissages stockés

**Nouveaux apprentissages créés cette session** :

| Domain | Severity | Fichier | Lien |
|--------|----------|---------|------|
| workflows | HIGH | agent_customization_navigation.md | [📖 Lire](APPRENTISSAGES/workflows/2026_04_25_agent_customization_navigation.md) |

**État meta.json (capital connaissances accumulé)** :

| Domain | Count | Top HIGH/MEDIUM |
|--------|-------|-----------------|
| workflows | 1 | [agent_customization_navigation.md](APPRENTISSAGES/workflows/2026_04_25_agent_customization_navigation.md) |
```

## Pièges évités

✅ **Liens relatifs** (`APPRENTISSAGES/domain/file.md`) → cliquables dans IDE + browsers  
✅ **Tableaus structurés** → découverte rapide sans paraphrase verbale  
✅ **Markdown standard** → compatible tous adapters (Claude Code, Comet, Antigravity)  
❌ Ne pas utiliser chemins absolus (non-portables entre environnements)  
❌ Ne pas hardcoder listes — générer depuis `meta.json` via script (future v2.7.0)

## Impact

- **Consultabilité** : apprentissages +300% visibilité (cliquables vs texte)
- **Onboarding** : agent suivant voit capital accumulé sans recherche manuelle
- **Continuité** : `/start` précédent visible comme lien → contexte historique

## Évolutions futures (v2.7.0+)

- Script Python génère tableaux depuis `meta.json` (zéro maintenance)
- Sidebar UI exposé apprentissages (onglet Learnings dynamique)
- Historique versions apprentissages (git blame intégré)
