# /start — Analyse Roadmap

## 1️⃣ Lire les 3 organes de communication (OBLIGATOIRE)
- **`README.md`** (racine) : contexte global, usage, features
- **`ROADMAP.md`** (racine) : phase actuelle, statuts ✅/🔄/⏳, priorités
- **`ARCHITECTURE.md`** (racine) : structure technique, décisions

→ Identifier tâches "En cours" / "À démarrer" + métriques de succès

## 2️⃣ Rapport (5-7 lignes)
```
**Phase** : [num] [nom]
**Statut** : [✅ COMPLET | 🔄 EN COURS | ⏳ PLANIFIÉ]

**Priorités** :
1. [Tâche A] — [description court]
2. [Tâche B] — [description court]

**Stack** : [technologies clés]
**Action** : [prêt pour]
```

## 3️⃣ Analyse ROI (tâches candidates)
| Tâche | Impact | Effort | ROI | Score |
|-------|--------|--------|-----|-------|
| Cand. 1 | ⭐⭐⭐⭐ | 1-2j | 4:1 | 🔥 BEST |
| Cand. 2 | ⭐⭐⭐ | 2-3j | 1.5:1 | ✅ |
| Cand. 3 | ⭐⭐ | 3-4j | 0.7:1 | ⏳ |

**Métrique ROI** : Impact / Effort

## 4️⃣ Recommandation
```
🎯 **[Meilleur] — ROI 4:1**
• Impact : [1 ligne]
• Effort : [durée]
• Raison : [pourquoi maintenant]

**Alternatives** :
2. [Option B] — ROI 1.5:1 (2-3j)
3. [Option C] — ROI 0.7:1 (3-4j)
```

## 5️⃣ Charger apprentissages 📚

### Démarche
1. Lire `APPRENTISSAGES/meta.json` → identifier docs HIGH/MEDIUM pertinents par domaine
2. Sélectionner TOP 5-7 docs (max 3000 tokens)
3. **Afficher liens cliquables** vers fichiers .md chargés

### Affichage apprentissages chargés

**Si docs HIGH/MEDIUM trouvés** :
```
📚 **Apprentissages chargés** : [N] docs (~Y tokens)

| Domain | Severity | Lien |
|--------|----------|------|
| core | HIGH | [detector_patterns.md](APPRENTISSAGES/core/detector_patterns.md) |
| ui | HIGH | [customtkinter_best_practices.md](APPRENTISSAGES/ui/customtkinter_best_practices.md) |
| workflows | HIGH | [multi_ia_handoff.md](APPRENTISSAGES/workflows/multi_ia_handoff.md) |
```

**Si aucun apprentissage pertinent** :
```
📚 Pas d'apprentissages pertinents pour cette phase (système neuf ou domaine nouveau).
```

→ Clique sur liens pour consulter contenu directement

---

## 6️⃣ Question
> "Commencer par [Meilleur] ou autre ?"

---
**Cycle de travail** :
- ✅ /start : analyse + apprentissages → **vous êtes ici**
- 🔧 Travail : implémentation, debug, refacto
- 📝 /close : documenter apprentissages + commit

**Économies d'optimisation** :
- ✂️ Sections verbales → listes compactes
- ✂️ Explications longues → 1 ligne max
- ✂️ Format code → tableau pour ROI
- ✂️ Redondances supprimées
- ✂️ Symboles plutôt que texte long
