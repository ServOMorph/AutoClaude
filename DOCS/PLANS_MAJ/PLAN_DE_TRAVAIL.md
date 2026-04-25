# 📋 PLAN DE TRAVAIL CONSOLIDÉ — AutoClaude v2.4.0 → v2.5.0

**Vue d'ensemble** : Phases 1-6 (refactorisation racine) + Phase 7 (v2.5.0 features) + système d'apprentissage scalable

**Cycle de travail** : `/start` (démarrage) → travail → `/close` (clôture) → apprentissages documentés

---

## 🔄 Cycle de travail standardisé (CLAUDE.md)

### Principes

```
Chaque session de travail suit ce cycle :

1️⃣ /start        → Analyse projet + charge apprentissages pertinents
2️⃣ Travail       → Implémentation / debug / refacto
3️⃣ /close        → Documenter apprentissages + commit + update ROADMAP
```

**Continuité** : Les apprentissages documentés lors de `/close` sont chargés au `/start` suivant, créant une accumulation de savoir entre sessions.

---

## 📚 Système d'apprentissage scalable

### Architecture

```
APPRENTISSAGES/                     ← Racine (parallèle à DOCS/, src/, tests/)
├── meta.json                       ← Index centralisé (version, count, updated)
├── core/
│   ├── detector.md                 ← Apprentissage : détection d'image
│   ├── clicker.md                  ← Apprentissage : clic automatisé
│   └── listener.md                 ← Apprentissage : écoute clavier/souris
├── ui/
│   ├── customtkinter_patterns.md   ← Patterns CustomTkinter
│   ├── theme_system.md             ← Système de thème
│   └── components_architecture.md  ← Architecture composants UI
├── bugs_resolved/
│   ├── 2024-04-25_thread_freeze.md ← Bug résolu : freeze UI dans thread
│   ├── 2024-04-26_release_api.md   ← Bug résolu : API GitHub rate limit
│   └── ...
└── workflows/
    ├── bump_version.md             ← Workflow : versioning automatisé
    ├── update_checker.md           ← Workflow : auto-updater implementation
    └── ...
```

### Format d'un apprentissage

```markdown
---
title: "Détection d'image avec OpenCV"
domain: "core"              # core, ui, security, bugs_resolved, workflows
tags: ["detection", "opencv", "template-matching"]
severity: "high"            # high, medium, low (pour le contexte)
created: "2024-04-25"
updated: "2024-04-25"
version: "v2.4.0"           # Version du projet quand c'est appris
context: "Implémentation du detector.py"
---

## Problème

Détection d'image multimoniteur inefficace avec OpenCV.

## Solution

Utiliser `mss` + `cv2.matchTemplate()` avec seuil 0.8.
OpenCV seul trop lent sur multi-moniteur (400ms).
mss + cv2 = 100ms sur 2 moniteurs.

## Code pattern

\`\`\`python
import mss
import cv2

def locate(image_path, threshold=0.8):
    with mss.mss() as sct:
        for monitor in sct.monitors[1:]:
            screenshot = sct.grab(monitor)
            # ...
\`\`\`

## Pièges à éviter

- ❌ Charger l'image à chaque iteration (I/O)
- ❌ Rechercher sur tous les moniteurs même si présent sur le 1er
- ❌ Seuil trop bas (> 0.95 = détections ratées, < 0.8 = faux positifs)
```

### meta.json (index)

```json
{
  "version": "v2.4.0",
  "last_updated": "2024-04-25T09:47:00Z",
  "total_learnings": 15,
  "domains": {
    "core": 4,
    "ui": 5,
    "security": 2,
    "bugs_resolved": 3,
    "workflows": 1
  },
  "by_severity": {
    "high": ["detector.md", "listener.md", "thread_freeze.md"],
    "medium": ["customtkinter_patterns.md", "theme_system.md"],
    "low": ["..."]
  }
}
```

### Chargement des apprentissages dans `/start`

Dans **startV2.md**, ajouter étape :

```
## 4️⃣ Charger apprentissages pertinents 📚

Basé sur le contexte du projet (technologies identifiées + type de travail) :
1. Scanner APPRENTISSAGES/meta.json
2. Identifier domaines pertinents (core, ui, bugs_resolved si fix, workflows si refacto)
3. Charger apprentissages HIGH + MEDIUM du domaine
4. Intégrer dans le contexte des prompts (max 5-7 apprentissages pour économiser tokens)
5. Afficher liste chargée : "Apprentissages pertinents (X docs, ~Y tokens)"
```

**Algorithme de sélection** :

```python
# startV2_learning_loader.py
def select_learnings(project_context: dict) -> list[str]:
    """
    Sélectionne max 5-7 apprentissages pertinents.
    Critères : domaine + sévérité + tokens restants
    """
    meta = load_meta()
    
    # 1. Domaines détectés (core, ui, security, workflows, bugs)
    detected_domains = infer_domains(project_context)
    
    # 2. Charger HIGH + MEDIUM de ces domaines
    candidates = meta.by_severity["high"] + meta.by_severity["medium"]
    candidates = [c for c in candidates if c.domain in detected_domains]
    
    # 3. Limiter par taille (max 3000 tokens ≈ 6-7 docs)
    selected = []
    token_count = 0
    for doc in sorted(candidates, key=lambda x: x.severity):
        doc_tokens = estimate_tokens(doc)
        if token_count + doc_tokens <= 3000:
            selected.append(doc)
            token_count += doc_tokens
    
    return selected
```

### Documentation d'apprentissage dans `/close`

Dans **closeV2.md**, ajouter étape :

```
## 4️⃣ Documenter apprentissages 📚

Si bug résolu ou pattern découvert :

1. **Créer APPRENTISSAGES/<domain>/<topic>.md**
   - Format : title, domain, tags, severity, code patterns, pièges
   
2. **Ajouter à APPRENTISSAGES/meta.json**
   - Incrémenter count
   - Ajouter entry dans by_severity
   
3. **Exemple : bug thread_freeze résolu**
   - Filename : APPRENTISSAGES/bugs_resolved/2024-04-25_thread_freeze.md
   - Domain : bugs_resolved
   - Severity : high
   - Tags : threading, tkinter, UI-freeze

4. **Vérifier tokens** : doc < 500 tokens (compact et réutilisable)
```

---

## Phase 1-6 : Refactorisation racine (25-30 min)

Voir détails complets dans `REFACTOR_PLAN.md` ou copier depuis commit précédent.

### Phase 1 : Créer structure (2 min)
```bash
mkdir -p DOCS/PLANS_MAJ build/pyinstaller .tooling
```

### Phase 2 : Déplacer fichiers (5 min)
- DOCS/ : documentation
- build/pyinstaller/ : specs PyInstaller
- .tooling/ : outils (build.py, bump_version.py, etc.)
- COMET/ : conservé (Perplexity integration)

### Phase 3 : Mettre à jour commands (3 min)
- startV2.md : référence DOCS/ARCHITECTURE.md
- closeV2.md : même
- README.md : section Intégrations IA

### Phase 3bis : /bump_version (5 min)
- Créé ✅ (voir session précédente)
- Scripts : .tooling/bump_version.py, bump_changelog.py

### Phase 5 : .gitignore (2 min)
- Ajouter : build/, dist/, .benchmarks/, __pycache__/

### Phase 6 : Commit refacto (2 min)
- Message : "refactor: restructurer racine — docs/build/.tooling"

---

## Phase 7 : Fonctionnalités v2.5.0 (3-4 jours)

### 7.1 — Auto-updater GitHub Releases (1j)

**Fichiers à créer** :
- `src/core/update_checker.py` — GitHub API, version comparison
- `src/ui/components/update_button.py` — Button "Check updates"
- `src/ui/dialogs/update_dialog.py` — Dialog + progress
- `updater/updater.py` — Standalone (download → kill → replace → relaunch)
- `updater/updater_config.json` — Config
- `updater/AutoClaude_Updater.spec` — PyInstaller (15-20 MB)

**Fichiers à modifier** :
- `src/config/constants.py` — +URL_GITHUB_API
- `src/config/settings.py` — +update_check_enabled
- `src/ui/app.py` — +update_button + thread daemon check
- `requirements.txt` — +requests>=2.31.0, packaging>=24.0

**Workflow** :
```
GitHub API → compare VERSION → dialog → Popen(updater) → app.quit() → updater replaces → relaunch
```

### 7.2 — Tips dynamiques (0.5j)

**Fichiers à créer** :
- `src/content/tips/*.md` — Tips content files
- `src/core/tips_loader.py` — Scanner + parser
- `src/ui/dialogs/tips_dialog.py` — Random tip on startup

**Fichiers à modifier** :
- `src/config/settings.py` — +show_tips_on_startup
- `src/ui/app.py` — Integrate tips_dialog

**Scalabilité** : Ajouter .md = tip dispo immédiatement

### 7.3 — Sidebar menu dynamique (1.5j)

**Architecture** :
```
src/content/
  ├── tips/
  ├── prompts/
  └── learnings/
      ├── core/
      ├── ui/
      └── security/
```

**Fichiers à créer** :
- `src/ui/sidebar/sidebar_panel.py` — Left nav
- `src/ui/sidebar/tab_registry.py` — Scans + registers
- `src/ui/sidebar/content_view.py` — Right panel
- `src/ui/tabs/*.py` — Tab classes (base, markdown, learning, prompts, tips)

**Scalabilité** : Ajouter dossier = onglet auto-généré

### 7.4 — CLAUDE.md contraintes (0.25j)

Ajouter :
- Cycle de travail : /start → travail → /close
- Architecture dynamique : tout depuis src/content/
- Système d'apprentissage : documenter bugs + patterns
- Chargement apprentissages : startV2 intègre contexte

---

## 🎯 Mise à jour des fichiers references

### .claude/commands/startV2.md

Ajouter étape 4️⃣ après "Rapport" :

```markdown
## 4️⃣ Charger apprentissages 📚

Si travail sur feature connue (bug fix, refacto, etc.) :
1. Scanner APPRENTISSAGES/meta.json
2. Lister apprentissages HIGH du domaine détecté
3. Intégrer dans contexte (max 5-7 docs)
4. Afficher : "Apprentissages chargés : X docs (~Y tokens)"

Sinon : "Pas d'apprentissages pertinents (première session / nouveau domaine)"
```

### .claude/commands/closeV2.md

Ajouter étape avant commit :

```markdown
## 4️⃣ Documenter apprentissages 📚

Si bug résolu ou pattern découvert :
1. Créer APPRENTISSAGES/<domain>/<topic>.md
2. Format : title, domain, tags, severity, code, pièges
3. Ajouter à APPRENTISSAGES/meta.json (count, by_severity)
4. Vérifier : doc compact (< 500 tokens)

Sinon : "Aucun apprentissage à documenter"
```

### .claude/CLAUDE.md

Ajouter section :

```markdown
## Cycle de travail (obligatoire)

Chaque session suit ce cycle :

1️⃣ **/start** (startV2.md)
   - Lit ROADMAP + README + ARCHITECTURE
   - Charge apprentissages pertinents depuis APPRENTISSAGES/
   - Affiche recommandation ROI
   
2️⃣ **Travail** (implémentation / debug / refacto)
   - Utilise contexte apprentissages chargés
   - Log issues et solutions
   
3️⃣ **/close** (closeV2.md)
   - Met à jour ROADMAP / README / ARCHITECTURE si besoin
   - Documente apprentissage si nouveau bug/pattern
   - Commit avec message explicite

## Système d'apprentissage

**Répertoire** : `APPRENTISSAGES/` à la racine

**Structure** : Domaines (core, ui, security, bugs_resolved, workflows)

**Sévérité** : HIGH (critical patterns) / MEDIUM (useful to know) / LOW (optional)

**Chargement** : /start détecte domaine → charge TOP apprentissages (max 3000 tokens)

**Documentation** : /close crée apprentissage si pattern nouveau / bug résolu

**Scalabilité** : Meta.json = index (token-efficient, peut être priorisé)
```

---

## 📊 Résumé travaux

| Phase | Durée | Status | Type |
|-------|-------|--------|------|
| 1-6 | 30 min | ✅ À faire | Refacto racine |
| 7.1 | 1j | ⏳ v2.5.0 | Auto-updater |
| 7.2 | 0.5j | ⏳ v2.5.0 | Tips |
| 7.3 | 1.5j | ⏳ v2.5.0 | Sidebar |
| 7.4 | 0.25j | ⏳ v2.5.0 | Constraints |
| Apprentissage | - | ✨ Nouveau | System |

---

## 🚀 Prochaines étapes

1. Créer dossier `APPRENTISSAGES/` + structure de base
2. Mettre à jour `startV2.md`, `closeV2.md`, `CLAUDE.md`
3. Exécuter Phases 1-6 (refacto racine)
4. Documenter apprentissages premiers bugs/patterns
5. Démarrer Phase 7 (v2.5.0 features)

---

**Version** : v2.4.0 (branch v2.4.0)  
**Créé** : 2024-04-25  
**Consolidated into** : DOCS/PLANS_MAJ/PLAN_DE_TRAVAIL.md
