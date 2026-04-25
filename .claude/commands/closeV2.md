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
| `DOCS/ARCHITECTURE.md` | Régénérer si N fichiers touchés > 3 |

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

