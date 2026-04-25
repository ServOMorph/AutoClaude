# CLAUDE.md

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

**1️⃣ `/start`** : `/model haiku` (optimiser token budget) • Lire **4 organes** (README + ROADMAP + ARCHITECTURE + WORKFLOW) • Charger apprentissages (TOP 5-7 HIGH, max 3000 tokens) • Analyser ROADMAP → recommander tâches ROI • Afficher plan d'action

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
