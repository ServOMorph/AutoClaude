# 📦 ARCHIVES — Système de rappel rapide

Stockage des fichiers obsolètes ou legacy avec **index searchable** pour rappel rapide si besoin.

---

## 🎯 Principe

- ✅ **Rien ne se perd** : tout fichier obsolète est archivé, pas supprimé
- ✅ **Rappel rapide** : `meta.json` indexe tous les fichiers avec tags + raison + cas de rappel
- ✅ **Recherchable** : par tag, version, mot-clé via grep ou script
- ❌ **Pas de réutilisation directe** : ces fichiers sont historiques, ne pas les éditer

---

## 📁 Structure

```
ARCHIVES/
├── meta.json                   ← Index centralisé (cas de rappel, tags, dates)
├── README.md                   ← Ce fichier
├── docs_legacy/                ← Docs remplacées par les 3 organes ou consolidées
│   ├── ARCHITECTURE_AutoClaude.md
│   ├── ARCHITECTURE_v2.0.md
│   ├── ROADMAP_v2.3.0_historical.md
│   ├── DEVELOPMENT_PLAN.md
│   ├── PLAN_DE_TRAVAIL.md
│   ├── REFACTOR_PLAN.md
│   ├── PLAN_v2.3.0_overlay_indicator.md
│   └── ROADMAP_v2.5.0.md
├── specs_pyinstaller/          ← Specs PyInstaller anciennes versions
│   ├── AutoClaude.spec
│   ├── AutoClaude_v2.2.1.spec
│   ├── AutoClaude_v2.3.0.spec
│   └── AutoClaude_v2.4.0.spec
├── tooling_artifacts/          ← Outils & snapshots dev
│   ├── audit_before.json
│   ├── audit_after.json
│   ├── type_hints_todo.json
│   └── build.py
└── old_builds/                 ← Anciens .exe (gitignored)
```

---

## 🔍 Système de rappel

Chaque fichier dans `meta.json` a :
- **`reason`** : pourquoi archivé
- **`tags`** : mots-clés (version, domaine, type)
- **`recall_when`** : cas concret où le ressortir
- **`archived_on`** : date archivage

### Recherche par tag

```bash
# Tous les fichiers v2.3.0
grep -B1 "v2.3.0" ARCHIVES/meta.json

# Tous les fichiers concernant l'auto-updater
grep -B1 "auto-updater" ARCHIVES/meta.json
```

### Recherche par usage

```bash
# Quand a-t-on besoin de tel fichier ?
grep -A1 "PLAN_DE_TRAVAIL" ARCHIVES/meta.json | grep recall_when
```

### Liste complète

```bash
python -c "
import json
d = json.load(open('ARCHIVES/meta.json'))
for cat, val in d['categories'].items():
    print(f'\n## {cat}')
    for fname, meta in val.get('files', {}).items():
        print(f'  • {fname}')
        print(f'    → {meta.get(\"recall_when\", \"—\")}')
"
```

---

## 📋 Fichiers archivés (snapshot)

### `docs_legacy/` (8 fichiers)

| Fichier | Tags | Cas de rappel |
|---------|------|--------------|
| `ARCHITECTURE_AutoClaude.md` | architecture, v2.0 | Référence ancienne structure src/ détaillée |
| `ARCHITECTURE_v2.0.md` | architecture, v2.0 | Comparaison historique avec ARCHITECTURE.md actuel |
| `ROADMAP_v2.3.0_historical.md` | roadmap, v1, v2.0, v2.3.0 | Détails livrables phases 1-9 (tâches × fichiers) |
| `DEVELOPMENT_PLAN.md` | plan, v2.0 | Référence design original UI/refacto v2.0 |
| `PLAN_DE_TRAVAIL.md` | plan, v2.5.0, updater, tips, sidebar | Détails techniques auto-updater (workflow, API) |
| `REFACTOR_PLAN.md` | refacto, v2.4.0 | Détails commandes shell pour refacto racine |
| `PLAN_v2.3.0_overlay_indicator.md` | plan, v2.3.0, overlay, released | Référence design overlay flottant + watchdog |
| `ROADMAP_v2.5.0.md` | roadmap, v2.5.0, apprentissage | Détails algorithme sélection apprentissages |

### `specs_pyinstaller/` (4 fichiers)

| Fichier | Tags | Cas de rappel |
|---------|------|--------------|
| `AutoClaude.spec` | pyinstaller | Spec générique legacy |
| `AutoClaude_v2.2.1.spec` | pyinstaller, v2.2.1 | Régénérer build v2.2.1 pour debug |
| `AutoClaude_v2.3.0.spec` | pyinstaller, v2.3.0, released | Reproduire build de la release v2.3.0 |
| `AutoClaude_v2.4.0.spec` | pyinstaller, v2.4.0 | Template pour v2.5.0 |

### `tooling_artifacts/` (4 fichiers)

| Fichier | Tags | Cas de rappel |
|---------|------|--------------|
| `audit_before.json` | audit, refacto | Snapshot pré-refacto v2.0 |
| `audit_after.json` | audit, refacto | Validation refacto v2.0 |
| `type_hints_todo.json` | type-hints, todo | Reprendre amélioration type hints |
| `build.py` | build, legacy | Référence ancienne logique de build |

---

## 🔄 Workflow d'archivage

### Archiver un nouveau fichier

```bash
# 1. Déplacer dans bonne catégorie
mv <obsolete_file> ARCHIVES/<category>/

# 2. Ajouter entrée dans meta.json
# (catégorie → files → <filename>)
{
  "from": "<chemin original>",
  "archived_on": "YYYY-MM-DD",
  "reason": "<pourquoi obsolète>",
  "tags": ["tag1", "tag2"],
  "recall_when": "<cas concret de rappel>"
}
```

### Restaurer un fichier (rappel)

```bash
# 1. Localiser dans meta.json
grep "<keyword>" ARCHIVES/meta.json

# 2. Copier (NE PAS déplacer — garder l'archive)
cp ARCHIVES/<category>/<file> <destination>/

# 3. Adapter au contexte courant
```

---

## 🏷️ Convention tags

| Tag | Usage |
|-----|-------|
| `vX.Y.Z` | Version concernée |
| `architecture` `roadmap` `plan` | Type de doc |
| `refacto` `audit` `build` | Domaine |
| `historique` `legacy` `duplicate` | Statut |
| `released` `transition` | État cycle |

---

## ⚠️ Règles

- ❌ **Ne pas éditer** les fichiers archivés (ils représentent un état historique)
- ❌ **Ne pas supprimer** sans validation (l'archive = mémoire projet)
- ✅ **Toujours référencer** via `meta.json` (pas de raccourcis directs)
- ✅ **Mettre à jour `meta.json`** à chaque archivage
- ✅ **Tagguer généreusement** pour faciliter la recherche

---

**Dernière mise à jour** : 2026-04-25 • **Catégories** : 4 • **Fichiers archivés** : 16
