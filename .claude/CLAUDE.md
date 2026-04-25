# CLAUDE.md

## 🤝 Organes de communication (OBLIGATOIRE)

**3 fichiers racine = source de vérité unique pour toute IA** :
- **[README.md](../README.md)** : usage + install + features
- **[ROADMAP.md](../ROADMAP.md)** : phases, statuts, priorités
- **[ARCHITECTURE.md](../ARCHITECTURE.md)** : structure technique, décisions

**Règles** :
- ✅ Lire ces 3 fichiers au `/start` pour contexte complet
- ✅ Mettre à jour ces 3 fichiers au `/close` si pertinent
- ✅ Toute commande IA (`/start`, `/close`, `/bump_version`) y fait référence
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

**1️⃣ `/start`** : Lire les **3 organes** (README.md + ROADMAP.md + ARCHITECTURE.md à la racine) • Charger apprentissages (TOP 5-7 HIGH, max 3000 tokens de APPRENTISSAGES/meta.json) • Afficher recommandation ROI

**2️⃣ Travail** : Utiliser contexte + apprentissages • Logger issues/solutions • Tester

**3️⃣ `/close`** : Mettre à jour les **3 organes** (README/ROADMAP/ARCHITECTURE racine) si pertinent • Documenter apprentissage si nouveau (créer APPRENTISSAGES/<domain>/<topic>.md, update meta.json, <500 tokens) • Commit

**Continuité** : `/close` → `/start` suivant crée accumulation de savoir automatique

## Système d'apprentissage

**Voir `APPRENTISSAGES/README.md`** pour détails complets.

**Structure** : `APPRENTISSAGES/` racine avec domains (core, ui, security, bugs_resolved, workflows)

**Format .md** : Frontmatter (title, domain, tags, severity, created, updated, version) + Problème/Solution/Code pattern/Pièges

**Sélection** : MAX 5-7 docs HIGH/MEDIUM, MAX 3000 tokens • meta.json = index filtrage rapide

**Gestion meta.json** : version, last_updated, total_learnings, domains (count), by_severity (file lists)
