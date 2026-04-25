t# 🔧 Refactorisation racine — Plan détaillé

**Objectif** : Structurer racine + automatiser versioning  
**Durée estimée** : 25-30 min (6 phases)  
**Branch** : v2.4.0  
**Impact** : Documentation, build, tooling centralisés + /bump_version automatisé

---

## Phase 1 : Créer structure (2 min)

```bash
mkdir -p DOCS/PLANS_MAJ build/pyinstaller .tooling
```

**Vérification** :
```bash
ls -d DOCS DOCS/PLANS_MAJ build build/pyinstaller .tooling
# Doit afficher 5 dossiers
```

---

## Phase 2 : Déplacer fichiers (5 min)

### 2.1 — Documentation (déplacer vers `DOCS/`)
```bash
mv ARCHITECTURE_AutoClaude.md DOCS/ARCHITECTURE.md
mv CODE_OF_CONDUCT.md CONTRIBUTING.md CHANGELOG.md DOCS/
mv DOCS/PLANS_MAJ/PLAN_v2.3.0_overlay_indicator.md DOCS/PLANS_MAJ/  # Vérifier
```

**Après** : `DOCS/` contient : `README.md`, `ARCHITECTURE.md`, `SECURITY.md`, `CHARTE_GRAPHIQUE.md`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `PLANS_MAJ/`

### 2.2 — PyInstaller specs (déplacer vers `build/pyinstaller/`)
```bash
mv AutoClaude.spec AutoClaude_v2.*.spec build/pyinstaller/
```

**Après** : `build/pyinstaller/` contient :
- `AutoClaude.spec`
- `AutoClaude_v2.2.1.spec`
- `AutoClaude_v2.3.0.spec`
- `AutoClaude_v2.4.0.spec`

### 2.3 — Outils & artefacts (déplacer vers `.tooling/`)
```bash
mv build.py audit_before.json audit_after.json type_hints_todo.json .tooling/
```

**Après** : `.tooling/` contient :
- `build.py`
- `audit_before.json`
- `audit_after.json`
- `type_hints_todo.json`

### 2.4 — Nettoyer (supprimer dossiers inutilisés)
```bash
rm -rf .benchmarks

# COMET/ est conservé (Perplexity/Comet initialization) — voir Phase 3.4
# Vérifier que build/ et dist/ existent mais sont vides/artifacts
ls -la build/build dist/
```

### 2.5 — Ajouter COMET/README.md (doc intégrations IA)
```bash
# Vérifier que COMET/README.md existe
ls -la COMET/README.md
```

**Contenu** : Documentation Perplexity/Comet, usage des fichiers, régénération

---

## Phase 3 : Mettre à jour `.claude/commands/` (3 min)

### 3.1 — Mettre à jour `startV2.md`
**Ligne 6** : Changer référence ARCHITECTURE

```diff
- `ARCHITECTURE_AutoClaude.md` : arcitecture du projet
+ `DOCS/ARCHITECTURE.md` : architecture du projet
```

**Commande** :
```bash
sed -i 's|`ARCHITECTURE_AutoClaude.md`|`DOCS/ARCHITECTURE.md`|g' .claude/commands/startV2.md
```

### 3.2 — Mettre à jour `closeV2.md`
**Ligne 13** : Changer référence dans tableau

```diff
- | `ARCHITECTURE_AutoClaude.md` | Régénérer si N fichiers touchés > 3 |
+ | `DOCS/ARCHITECTURE.md` | Régénérer si N fichiers touchés > 3 |
```

**Commande** :
```bash
sed -i 's|`ARCHITECTURE_AutoClaude.md`|`DOCS/ARCHITECTURE.md`|g' .claude/commands/closeV2.md
```

### 3.3 — Mettre à jour `README.md`
**Ajouter section** après Architecture (avant Licence) :

```markdown
## Intégrations IA — Perplexity & Comet

AutoClaude peut être utilisé avec Perplexity via Comet.

### 🌌 Dossier COMET/

Fichiers d'initialisation pour Perplexity :
- `PROMPT_PERPLEXITY.txt` — Instructions système
- `ARCHITECTURE_AutoClaude.md` — Structure du projet
- `CODE_BUNDLE_AutoClaude.md` — Bundle code complet

**Usage** :
1. Copier `PROMPT_PERPLEXITY.txt`
2. Charger dans Perplexity comme contexte
3. Perplexity collabore avec compréhension du projet

Voir [COMET/README.md](COMET/README.md) pour détail.
```

**Vérification** :
```bash
grep -n "Intégrations IA" README.md
# Doit afficher la ligne
```

### 3.4 — Vérification commands
```bash
grep -n "ARCHITECTURE\|COMET" .claude/commands/startV2.md .claude/commands/closeV2.md README.md
# Doit afficher : 
#   startV2.md:6: DOCS/ARCHITECTURE.md
#   closeV2.md:13: DOCS/ARCHITECTURE.md
#   README.md: "Intégrations IA — Perplexity & Comet" + COMET/README.md
```

---

## Phase 3bis : Créer commande `/bump_version` (5 min)

Automatiser le versioning complet du projet.

### 3bis.1 — Vérifier fichiers créés
```bash
ls -la .claude/commands/bump_version.md
ls -la .tooling/bump_version*.py
ls -la .tooling/bump_version_files.json
```

**Devrait afficher** : 4 fichiers
- `.claude/commands/bump_version.md` (guide/workflow)
- `.tooling/bump_version.py` (script bump)
- `.tooling/bump_changelog.py` (script changelog)
- `.tooling/bump_version_files.json` (config fichiers à updater)

### 3bis.2 — Tester analyse version
```bash
python .tooling/bump_version.py --analyze
# Output: ✅ LISTED src/config/constants.py
#         ✅ LISTED pyproject.toml
#         ✅ LISTED README.md
#         ⚠️  NEW?   (si fichiers trouvés non listés)
# Action: si NEW?, ajouter à .tooling/bump_version_files.json
```

### 3bis.3 — Vérifier contenu config
```bash
cat .tooling/bump_version_files.json | grep -E '"path"|"pattern"|"required"'
# Vérifier: X.Y.Z pattern dans constants.py, pyproject.toml, README.md, etc.
```

### 3bis.4 — Vérifier scripts intégrité
```bash
grep "def bump_files\|def create_changelog_entry" .tooling/bump_version*.py
# Vérifier: fonctions clés présentes
python .tooling/bump_version.py --help 2>/dev/null || echo "Script OK"
python .tooling/bump_changelog.py --help 2>/dev/null || echo "Script OK"
```

### 3bis.5 — Documenter usage
Vérifier que `.claude/commands/bump_version.md` contient :
```bash
grep -E "Analyser|Bumper|Documenter|Commit" .claude/commands/bump_version.md
# Doit afficher: 4 étapes du workflow
```

---

## Phase 5 : Mettre à jour `.gitignore` (2 min)

**Ajouter au `.gitignore`** (si pas déjà présent) :
```
# Build artifacts
build/build/
build/dist/
dist/
*.exe
*.pyc

# Cache & benchmarks
.benchmarks/
.pytest_cache/
__pycache__/
*.egg-info/
```

**Vérifier** :
```bash
git status
# Doit afficher : .tooling/, build/pyinstaller/, DOCS/*.md (modifiés ou nouveaux)
# Ne doit PAS afficher : build/build/, dist/, .benchmarks/
```

---

## Phase 6 : Commit (2 min)

```bash
git add -A
git status  # Vérifier
git commit -m "$(cat <<'EOF'
refactor: restructurer racine — docs/build/.tooling centralisés

Structure nouvelle (racine claire) :
  DOCS/           : documentation (ARCHITECTURE, SECURITY, CHANGELOG, etc.)
  COMET/          : Perplexity/Comet initialization (CONSERVÉ + documenté)
  build/          : PyInstaller specs + build artifacts
  .tooling/       : outils (build.py, audit_*.json, type_hints_todo.json)
  .gitignore      : build/, dist/, .benchmarks/ cachés

Changements :
  • Déplacé ARCHITECTURE_AutoClaude.md → DOCS/ARCHITECTURE.md
  • Déplacé *.spec → build/pyinstaller/
  • Déplacé audit_*.json, type_hints_todo.json → .tooling/
  • Déplacé CODE_OF_CONDUCT.md, CONTRIBUTING.md, CHANGELOG.md → DOCS/
  • Créé COMET/README.md (documentation intégrations IA Perplexity)
  • Supprimé .benchmarks/ (non utilisé)
  • Ajouté section "Intégrations IA" à README.md → lien vers COMET/
  • Mis à jour startV2.md, closeV2.md (références ARCHITECTURE)
  • Créé /bump_version : commande + scripts + config
    - .claude/commands/bump_version.md (guide workflow)
    - .tooling/bump_version.py (script bump automatisé)
    - .tooling/bump_changelog.py (script changelog template)
    - .tooling/bump_version_files.json (liste fichiers + patterns)
  • Mis à jour .gitignore (build/, dist/, .benchmarks/ cachés)

Racine avant : 13 fichiers + clutter  
Racine après : 7 fichiers + structure claire (COMET/ conservé comme ressource)

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
EOF
)"
```

---

## Vérification finale

**Après commit**, la structure doit être :

```
AutoClaude/ (racine)
├── README.md                    (inclut section "Intégrations IA")
├── LICENSE
├── pyproject.toml
├── run.py
├── .gitignore
├── .claude/
├── .github/
├── assets/
├── src/
├── tests/
├── COMET/                       (Perplexity/Comet — CONSERVÉ)
│   ├── README.md                (documentation intégrations IA)
│   ├── ARCHITECTURE_AutoClaude.md
│   ├── CODE_BUNDLE_AutoClaude.md
│   └── PROMPT_PERPLEXITY.txt
├── DOCS/
│   ├── README.md
│   ├── ARCHITECTURE.md          (ancien ARCHITECTURE_AutoClaude.md)
│   ├── SECURITY.md
│   ├── CHARTE_GRAPHIQUE.md
│   ├── CHANGELOG.md
│   ├── CODE_OF_CONDUCT.md
│   ├── CONTRIBUTING.md
│   └── PLANS_MAJ/
├── build/
│   ├── pyinstaller/             (*.spec files)
│   ├── build/                   (.gitignore)
│   └── dist/                    (.gitignore)
├── .tooling/
│   ├── build.py
│   ├── audit_before.json
│   ├── audit_after.json
│   ├── type_hints_todo.json
│   ├── bump_version.py              (script bump version)
│   ├── bump_changelog.py            (script changelog)
│   └── bump_version_files.json      (config fichiers)
│
└── .claude/commands/
    ├── startV2.md                   (démarrage session)
    ├── closeV2.md                   (clôture session)
    └── bump_version.md              (versioning automatis)
```

**Commandes de vérification** :
```bash
# Racine (7 fichiers)
ls -1 *.md *.py *.toml .gitignore 2>/dev/null | wc -l
# Doit afficher : 6 (README.md, LICENSE, pyproject.toml, run.py, .gitignore = 5 + 1 autodetecté)

# Dossiers (6 principaux)
ls -d .claude .github assets src tests DOCS build .tooling 2>/dev/null | wc -l
# Doit afficher : 8

# Pas de clutter
ls -la | grep -E "AutoClaude.*\.spec|audit_|type_hints_todo|ARCHITECTURE_Auto"
# Doit être vide
```

---

## Rollback (si nécessaire)

```bash
git reset --hard HEAD~1
```

---

**Prêt ?** Exécute chaque phase ou lance tout d'un coup ?
