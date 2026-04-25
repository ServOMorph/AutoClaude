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

Si travail sur feature connue (bug fix, refacto, dev) :
```bash
# Vérifier APPRENTISSAGES/meta.json (tags, sévérité)
grep -r "domain\|severity" APPRENTISSAGES/meta.json | grep -E "core|ui|bugs_resolved|workflows"
# Sélectionner TOP 5-7 docs (HIGH severity + domaine pertinent)
```

Afficher : "Apprentissages chargés : X docs (~Y tokens pertinents)"

Sinon (première session / domaine nouveau) : "Pas d'apprentissages pertinents"

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
