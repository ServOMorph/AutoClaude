# /close — Clôture de session

## 1️⃣ Analyser
- Tâches accomplies, fichiers touchés
- Décisions & problèmes résolus
- Points en suspens

## 2️⃣ Mettre à jour docs
| Doc | Action |
|-----|--------|
| `ROADMAP.md` | Cocher ✅ tâches, mettre date |
| `README.md` | Refléter état, nouvelles features |
| `ARCHITECTURE_AutoClaude.md` | Régénérer si N fichiers touchés > 3 |
| `.claude/CLAUDE.md` | Ajouter patterns/décisions si clé |

## 3️⃣ Apprentissages 📚
Si **itérations multiples** ou **pattern essai→succès** :
```bash
python /c/Users/raph6/Documents/ServOMorph/Agents_IA_V2/.claude/learnings/learning_manager.py \
  analyze "[projet]"
```
→ Reporter N apprentissages enregistrés

## 4️⃣ Commit
```bash
git add .
git status
# Créer commit : [type]: description
# Types : feat|fix|docs|refactor|test|chore
# Footer : Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
```

## 5️⃣ Rapport final (6-10 lignes)
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
```

---
**Cohérence** :
- ✅ Format compact comme `startV2.md` (listes, tableaux, symboles)
- ✅ Pas redondance (références exactes, pas explication)
- ✅ Suit `CLAUDE.md` économie tokens (bullet points, 1 ligne/concept)
- ✅ Inclut ARCHITECTURE_AutoClaude.md régénération (> 3 fichiers)
- ✅ Apprentissages détectés automatiquement
