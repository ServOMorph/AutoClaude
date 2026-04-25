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

## 6️⃣ Afficher apprentissages stockés (optionnel)

```bash
# Lister tous les apprentissages documentés
python .tooling/archive_search.py --learnings

# Ou via meta.json
cat APPRENTISSAGES/meta.json | python -m json.tool
```

**Output attendu** :
```
## 📚 Apprentissages stockés

| Domain | Severity | Count | Fichiers |
|--------|----------|-------|----------|
| core | HIGH | 2 | logger_patterns.md, detector_robustness.md |
| ui | MEDIUM | 1 | overlay_threading.md |
| bugs_resolved | HIGH | 3 | ... |
| workflows | MEDIUM | 2 | ... |

**Total** : [N] apprentissages | **Dernière MAJ** : 2026-04-25
```

→ Permet de visualiser le capital connaissance accumulé avant `/start` suivant.

