# /close — Clôture de session

## 1️⃣ Analyser
- Tâches accomplies, fichiers touchés
- Décisions & problèmes résolus
- Points en suspens

## 2️⃣ Mettre à jour les 3 organes de communication (OBLIGATOIRE si pertinent)
| Doc (racine) | Action |
|--------------|--------|
| **`ROADMAP.md`** | Cocher ✅ tâches, mettre date, ajuster priorités |
| **`README.md`** | Refléter nouvelles features, version, install |
| **`ARCHITECTURE.md`** | Régénérer si N fichiers structurels touchés > 3 |

→ Ces 3 fichiers = source de vérité pour toute IA collaborant sur le projet

## 3️⃣ Documenter apprentissages 📚

Si **bug résolu** ou **pattern découvert** :

1. **Créer** : `APPRENTISSAGES/<domain>/<topic>.md`
   - Domaines : core, ui, security, bugs_resolved, workflows
   
2. **Contenu** : title, domain, tags, severity, problème, solution, code, pièges
   
3. **Mettre à jour** : `APPRENTISSAGES/meta.json` (count, by_severity)
   
4. **Vérifier** : Compact (< 500 tokens)

Sinon : "Aucun apprentissage à documenter"

## 4️⃣ Commit
```bash
git add .
git status
# Créer commit : [type]: description
# Types : feat|fix|docs|refactor|test|chore
# Footer : Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
```

## 5️⃣ Rapport final complet

```
## ✅ Session clôturée

**Fichiers** : [N modifiés] | **Commits** : [M]

### Accompli
- [réalisation 1]
- [réalisation 2]

### Suspens
- [tâche future]

### Prochaines étapes
- [suggestions]

### 📚 Apprentissages stockés

**Nouveaux apprentissages créés cette session** :

| Domain | Severity | Fichier | Lien |
|--------|----------|---------|------|
| core | HIGH | detector_edge_cases.md | [📖 Lire](APPRENTISSAGES/core/detector_edge_cases.md) |
| ui | MEDIUM | sidebar_rendering.md | [📖 Lire](APPRENTISSAGES/ui/sidebar_rendering.md) |
| workflows | HIGH | async_handoff_pattern.md | [📖 Lire](APPRENTISSAGES/workflows/async_handoff_pattern.md) |

**État meta.json (capital connaissances accumulé)** :

| Domain | Count | Top HIGH/MEDIUM |
|--------|-------|-----------------|
| core | 5 | [detector_patterns.md](APPRENTISSAGES/core/detector_patterns.md), [autoclick_optimization.md](APPRENTISSAGES/core/autoclick_optimization.md) |
| ui | 3 | [customtkinter_best_practices.md](APPRENTISSAGES/ui/customtkinter_best_practices.md) |
| workflows | 2 | [multi_ia_handoff.md](APPRENTISSAGES/workflows/multi_ia_handoff.md), [agent_customization_navigation.md](APPRENTISSAGES/workflows/2026_04_25_agent_customization_navigation.md) |
| bugs_resolved | 4 | [thread_freeze_fix.md](APPRENTISSAGES/bugs_resolved/thread_freeze_fix.md), … |

**Total** : [N] apprentissages | **Dernière MAJ** : YYYY-MM-DD

→ Capital connaissance accumulé visible avant `/start` suivant. **Clique sur liens pour consulter**.

