# AGENTS.md

## 🤝 Organes de communication (OBLIGATOIRE)

**4 fichiers racine = source de vérité unique pour toute IA** :
- **[README.md](../README.md)** : mission, features, usage
- **[ROADMAP.md](../ROADMAP.md)** : phases, statuts, priorités
- **[ARCHITECTURE.md](../ARCHITECTURE.md)** : structure technique, décisions
- **[WORKFLOW.md](../WORKFLOW.md)** : cycle `/start` `/close` `/doc` IA-agnostique (v2.6.0+)

**Règles** :
- ✅ Lire ces 4 fichiers au `/start` pour contexte complet
- ✅ Mettre à jour ces 4 fichiers au `/close` si pertinent
- ✅ Toute commande IA (`/start`, `/close`, `/doc`, `/bump_version`) y fait référence
- ❌ Ne pas créer de doc concurrente — détails additionnels dans `DOCS/`

## Directives essentielles

**Langue** : français | **Ton** : synthétique, direct | **Initiatives** : aucune hors demande explicite

### Contraintes code
- **Max 500 lignes/fichier** (refacto urgente sinon)
- **SRP** : 1 fichier = 1 responsabilité
- **Nommage** : camelCase (vars/foncs), PascalCase (composants), kebab-case (fichiers)
- Tests associés dès création fonction

### Économie tokens
**Communication** : bullets/listes/symboles • pas de paraphrases • pas de contexte repo (lire le code)

**Code** : imports groupés • fonctions <20L • vars explicites • docstrings 1L max • tables pour comparaisons

**Fichiers** : réutiliser existants • consolidate • pas de dupes • pas de docs superflus

**Recherches** : cibler sections • Grep/Glob vs Bash • pas de lectures massives

## Architecture dynamique (v2.5.0+)

**Principe** : Tout depuis `src/content/` (tips, prompts, learnings) — aucun hardcodé

- ✅ Source unique (dossiers) • Loaders scannent toujours • UI auto-générée • Extensible (ajouter .md = feature)
- ❌ Pas de contenu/UI hardcodés • Pas de registry statiques

**Implémentation** : Tips scannent `src/content/tips/*.md` • Sidebar/onglets via `tab_registry.py` • Sous-dossiers = sous-onglets auto

**Anti-patterns** :
- ❌ `tips = [{"id": "...", "title": "..."}]` → ✅ `def load_all_tips() -> list`
- ❌ `self.buttons = [CTkButton(...), ...]` → ✅ `for tab in registry: add_tab(tab)`
- ❌ Dupliquer tips dans code → ✅ Une source `src/content/tips/`

## Cycle de travail (obligatoire)

**1️⃣ `/start`** : Lire **4 organes** (README + ROADMAP + ARCHITECTURE + WORKFLOW) • Charger apprentissages (TOP 5-7 HIGH, max 3000 tokens) • Analyser ROADMAP → recommander tâches ROI • Afficher plan d'action

**2️⃣ Travail** : Implémenter selon plan • Tests associés (v2.5.0+) • Logger issues/solutions → apprentissages

**3️⃣ `/doc`** (v2.6.0+) : Exécuter avant `/close` → audit cohérence 4 organes + multi-LLM compliance • Proposer fixes si warnings majeurs • Générer rapport

**4️⃣ `/close`** : Exécuter `/doc` → fix warnings si nécessaire • Documenter apprentissages (APPRENTISSAGES/<domain>/<topic>.md <500 tokens) • Update meta.json • Commit normalisé • Tag version si applicable

**Continuité** : `/close` → `/start` suivant crée accumulation savoir auto

## Session & Context management

**Token budget/session** : ~5000-6500 tokens = 1-2 phases majeures max

| Phase | Budget | Notes |
|-------|--------|-------|
| Lire 4 organes + apprentissages | 500-800 | `/start` |
| Implémentation | 2000-3000 | tests inclus (v2.5.0+) |
| `/doc` audit | 500 | avant `/close` (v2.6.0+) |
| `/close` | 300 | apprentissages + commit |

**Context reset** : ≥60% max context → créer `HANDOFF_<task_id>.md`, handoff à IA suivante, exécuter `/close`

**Handoff format** (lire [WORKFLOW.md](../WORKFLOW.md) section 📋) :
- État fichiers modifiés (✅/🔄/⏳)
- Prochaine étape précise
- Pièges identifiés
- Apprentissages chargés

## Tests & Couverture (v2.5.0+)

**Minimum 90% couverture** → fail `/close` si <90%

**Exécuter** : `pytest tests/ --cov=src --cov-fail-under=90`

**Tests associés** : créer `tests/` dès création fonction (unit + integration)

## Système d'apprentissage

**Voir `APPRENTISSAGES/README.md`** pour détails complets.

**Structure** : `APPRENTISSAGES/` racine avec domains (core, ui, security, bugs_resolved, workflows)

**Format .md** : Frontmatter (title, domain, tags, severity, created, updated, version) + Problème/Solution/Code pattern/Pièges

**Sélection** : MAX 5-7 docs HIGH/MEDIUM, MAX 3000 tokens • meta.json = index filtrage rapide

**Gestion meta.json** : version, last_updated, total_learnings, domains (count), by_severity (file lists)


---

## 🎓 Instructions spécialisées (load as-needed)

Quand vous identifiez l'une de ces conditions, **charger l'instruction correspondante** pour détails complets :

### 1️⃣ Création de tests | Implémentation de fonctions

**Condition** : Vous écrivez du code Python nécessitant tests, ou validez couverture 90%+ requis v2.5.0

**File** : [.github/instructions/testing.instructions.md](.github/instructions/testing.instructions.md)

**Contenu clé** :
- Commande validation : \pytest tests/ --cov=src --cov-fail-under=90- Structure tests/unit/, conftest.py fixtures partagées
- Minimal test pattern + anti-patterns courants
- Checklist \/close\ : tests must pass 90%

---

### 2️⃣ Documenter apprentissages | Session \/start\ ou \/close
**Condition** : Vous exécutez \/start\ (charger contexte) ou \/close\ (documenter découvertes), ou managez APPRENTISSAGES/meta.json

**File** : [.github/instructions/learnings-workflow.instructions.md](.github/instructions/learnings-workflow.instructions.md)

**Contenu clé** :
- Structure APPRENTISSAGES/ + domaines (core, ui, security, bugs_resolved, workflows)
- Frontmatter YAML format (title, domain, tags, severity, dates)
- Meta.json management (version, total_learnings, by_severity)
- Intégration \/start\ charge apprentissages ↔ \/close\ documente

---

### 3️⃣ Orchestration multi-IA | Adapters | Session management | Handoff

**Condition** : Vous implémentez adapters (Claude Code ↔ Comet ↔ Antigravity), gérez token budget inter-sessions, créez handoffs entre agents

**File** : [.github/instructions/multiia-workflow.instructions.md](.github/instructions/multiia-workflow.instructions.md)

**Contenu clé** :
- Architecture adapters (base_adapter abstraite → concrete)
- Token budget par session (~5000-6500 = 1-2 phases majeures)
- Handoff format (état fichiers, prochaines étapes, pièges, apprentissages)
- Procédures détaillées \/start\ \/close\ \/doc\ pour multi-IA

---

### 4️⃣ Contenu dynamique | Loaders | Sidebar registry | Extensibilité

**Condition** : Vous implémentez content loaders (tips, prompts, learnings), générez sidebar/tabs dynamiquement depuis \src/content/\, ou étendez système contenu

**File** : [.github/instructions/dynamic-content.instructions.md](.github/instructions/dynamic-content.instructions.md)

**Contenu clé** :
- Structure src/content/ (tips/, prompts/, learnings/, workflows/)
- Loaders pattern (FS scan → data structures normalisées)
- Tab registry auto-généré depuis sous-dossiers
- Extension pattern : ajouter .md = feature automatique

---

### 5️⃣ Commandes IA standardisées

**Files** : [.claude/commands/](.claude/commands/)

| Commande | Procédure |
|----------|-----------|
| \/start\ | Lire 4 organes → charger apprentissages → recommander tâches |
| \/close\ | Documenter apprentissages → update meta.json → commit |
| \/doc\ | Audit cohérence doc (v2.6.0+) |
| \/bump_version\ | Auto-versioning (VERSION + CHANGELOG + refs) |

---

## 📍 Navigation

- [README.md](README.md) — Mission, features, usage
- [ROADMAP.md](ROADMAP.md) — Phases, statuts, priorités
- [ARCHITECTURE.md](ARCHITECTURE.md) — Structure technique
- [WORKFLOW.md](WORKFLOW.md) — Cycle IA-agnostique
- [.claude/CLAUDE.md](.claude/CLAUDE.md) — Directives essentielles

**Instructions spécialisées** :
- [testing.instructions.md](.github/instructions/testing.instructions.md)
- [learnings-workflow.instructions.md](.github/instructions/learnings-workflow.instructions.md)
- [multiia-workflow.instructions.md](.github/instructions/multiia-workflow.instructions.md)
- [dynamic-content.instructions.md](.github/instructions/dynamic-content.instructions.md)

---

**Développé par [SéréniaTech](https://serenia-tech.fr) · [GitHub](https://github.com/ServOMorph)**
