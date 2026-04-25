# /bump_version — Bump version automatisé

Workflow complet : analyser → bumper → documenter changelog.

> ℹ️ **Avant de bumper** : vérifier que les **3 organes** (`README.md`, `ROADMAP.md`, `ARCHITECTURE.md` racine) reflètent l'état du projet. La version est référencée dans README.md (badge) et ROADMAP.md (statut).

## Workflow

```
1. Analyser        → détecter tous les fichiers avec version
   ↓
2. Bumper          → mettre à jour X.Y.Z → X.Y+1.Z
   ↓
3. Documenter      → ajouter entrée CHANGELOG.md
   ↓
4. Commit          → git commit avec message versioning
```

## 1️⃣ Analyser fichiers

```bash
python .tooling/bump_version.py --analyze
```

**Output** :
```
✅ LISTED  src/config/constants.py
✅ LISTED  pyproject.toml
✅ LISTED  README.md
⚠️  NEW?   DOCS/something.md  (ligne 123)
```

**Action** : Si nouveaux fichiers → vérifier, puis ajouter à `.tooling/bump_version_files.json`

## 2️⃣ Bumper version

```bash
python .tooling/bump_version.py 2.5.0
```

**Output** :
```
✅ src/config/constants.py
✅ pyproject.toml
✅ README.md (2 occurrences)
✅ build/pyinstaller/AutoClaude_v2.5.0.spec (créé)
✓ Updated 5 files
```

## 3️⃣ Documenter changelog

```bash
python .tooling/bump_changelog.py 2.5.0
```

**Output** :
```
✅ Added changelog entry for v2.5.0
📝 Edit CHANGELOG.md to fill in details
```

**Éditer CHANGELOG.md** :
```markdown
## [2.5.0] — 2026-04-26

### Added
- Feature 1
- Feature 2

### Changed
- Improvement 1

### Fixed
- Bug fix 1

### Removed
- Deprecation 1
```

## 4️⃣ Commit

```bash
git add -A
git commit -m "bump: version 2.4.0 → 2.5.0

- Updated VERSION in src/config/constants.py
- Updated version in pyproject.toml
- Updated badges/exe references in README.md
- Created build/pyinstaller/AutoClaude_v2.5.0.spec
- Updated CHANGELOG.md with v2.5.0 entry

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

## Config & Fichiers

| Fichier | Rôle |
|---------|------|
| `.tooling/bump_version_files.json` | Liste fichiers à updater + patterns |
| `.tooling/bump_version.py` | Script bump automatisé |
| `.tooling/bump_changelog.py` | Script changelog |

## Tips

- **Analyser d'abord** : `--analyze` détecte tous les fichiers avec version
- **Ajouter patterns** : si nouveau fichier trouvé, l'ajouter à `.tooling/bump_version_files.json`
- **Editer changelog** : le script crée template, toi remplir détails
- **Semantic Versioning** : MAJOR.MINOR.PATCH (2.4.0 → 2.5.0 = MINOR bump)
- **Synchroniser organes** : après bump, vérifier que ROADMAP.md (statut version) et README.md (badge + install) sont alignés

---

**One-liner complet** (4 commandes en cascade) :
```bash
python .tooling/bump_version.py --analyze && \
python .tooling/bump_version.py 2.5.0 && \
python .tooling/bump_changelog.py 2.5.0 && \
git add -A && git commit -m "bump: version 2.4.0 → 2.5.0"
```
