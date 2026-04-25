# WORKFLOW.md — Cycle multi-IA unifié

> **Cycle de travail standard** pour toute IA collaborant sur AutoClaude (Claude Code, Comet, Antigravity, autres).
>
> Indépendant de la plateforme LLM. Adapters (`.claude/`, `.comet/`, `.antigravity/`) traduisent vers syntaxe cible.

---

## 🔄 Cycle complet

```
/start
  ├─ Lire 4 organes (README, ROADMAP, ARCHITECTURE, WORKFLOW)
  ├─ Charger apprentissages (APPRENTISSAGES/meta.json)
  ├─ Identifier tâches prioritaires (depuis ROADMAP)
  └─ Exécuter plan d'action

Travail
  ├─ Implémenter selon plan
  ├─ Tester (v2.5.0+)
  └─ Documenter issues/solutions

/doc (avant /close — v2.6.0+)
  ├─ Analyser cohérence 4 organes
  ├─ Vérifier multi-LLM compliance
  ├─ Proposer fixes si warnings
  └─ Valider avant commit

/close
  ├─ Documenter apprentissages (APPRENTISSAGES/)
  ├─ Créer/mettre à jour meta.json
  ├─ Commit message normalisé
  └─ Tag version si applicable
```

---

## 1️⃣ `/start` — Démarrage de session

### Objectif
Charger contexte complet projet + apprentissages, identifier tâches prioritaires, planifier session.

### Procédure

#### 1.1 — Lire les 4 organes

**Fichiers obligatoires** (source de vérité unique) :
1. **[README.md](README.md)** — mission, features, usage
2. **[ROADMAP.md](ROADMAP.md)** — phases actuelles, statuts, priorités
3. **[ARCHITECTURE.md](ARCHITECTURE.md)** — structure technique, décisions
4. **[WORKFLOW.md](WORKFLOW.md)** — ce fichier, cycle IA-agnostique

**Questions à traiter** :
- Quelle est la phase actuelle ? (voir ROADMAP)
- Quel est le statut ? (✅ fait, 🔄 en cours, ⏳ planifié)
- Quelles sont les priorités ? (impact vs effort)
- Quels fichiers/modules dois-je toucher ? (voir ARCHITECTURE)
- Quel est le contexte technique pertinent ? (décisions, pièges)

#### 1.2 — Charger apprentissages

**Fichier** : `APPRENTISSAGES/meta.json`

```bash
# Repérer learnings pertinents
grep -E "^  \"high\"|^  \"medium\"" APPRENTISSAGES/meta.json
```

**Sélection** : max 5-7 docs HIGH/MEDIUM, max 3000 tokens.
- Parcourir domaines pertinents : core, ui, security, bugs_resolved, workflows
- Charger `.md` docs mentionnés dans `by_severity[high]` + `by_severity[medium]`

**Affichage** : "Apprentissages chargés : X docs (~Y tokens)" OU "Pas d'apprentissages pertinents (système neuf)".

#### 1.3 — Identifier tâches prioritaires

**Analyser ROADMAP** :
- Phase actuelle ? Statut global (✅/🔄/⏳) ?
- Tâches "en cours" (`🔄`) ou "à démarrer" (`⏳`) ?
- Critères de validation pour cette phase ?

**Estimer effort vs impact** :

| Tâche | Impact | Effort | ROI | Score |
|-------|--------|--------|-----|-------|
| — | ⭐… | Xj | Y:1 | 🔥/✅/⏳ |

**Recommander TOP 1-2 tâches** pour cette session (tenant compte du token budget : ~5000-6500 tokens).

#### 1.4 — Plan d'action

```
Prochaines étapes :
1. [Meilleure tâche] — raison ROI, durée estimée
2. [Alternative] — raison secondaire
3. [Blocage potentiel] — si applicable
```

---

## 2️⃣ Travail — Implémenter selon plan

### Principes généraux

- **Lire avant modifier** : utiliser Read tool avant Edit/Write
- **SRP** : 1 fichier = 1 responsabilité (max 500L)
- **Tests** (v2.5.0+) : créer tests associés dès création fonction
- **Pas de hardcodé** : contenu depuis `src/content/` (filesystem-driven)
- **Logging issues** : documenter bugs rencontrés, solutions appliquées (→ apprentissages `/close`)

### Gestion context & token budget

Si contexte ≈ 60% du max ou session ≈ 2-3 phases majeures :
1. Créer `HANDOFF_<task_id>.md` (voir section 📋 ci-dessous)
2. Assigné tâche à IA suivante dans `TASKS/<id>.md` (status = ready_for_handoff)
3. Exécuter `/close`
4. IA suivante exécute `/start` + reprend depuis HANDOFF

---

## 3️⃣ `/doc` — Audit cohérence doc (v2.6.0+)

### Objectif
Vérifier cohérence 4 organes + compliance multi-LLM, avant commit.

### Procédure

#### 3.1 — Analyser incohérences

Chercher :
- **Versions désynchronisées** : `constants.py VERSION` vs `CHANGELOG` vs `ROADMAP.md` ("Version actuelle")
- **Références mortes** : fichiers mentionnés/supprimés, liens rompus
- **Contenu hardcodé** : `tips = [...]` vs `src/content/tips/*.md` scannés
- **Multi-LLM compliance** : README mentionne adapters ? WORKFLOW mentionné ? `.comet/` `.antigravity/` existent ?

#### 3.2 — Vérifier compliance multi-LLM

Questions :
- ✅ README mentionne "centre de commande multi-IA" ?
- ✅ ROADMAP phases incluent adapters ? (v2.6.0+)
- ✅ ARCHITECTURE décrit `src/integrations/` ?
- ✅ WORKFLOW.md mentionné dans CLAUDE.md/COMET.md/ANTIGRAVITY.md ?
- ✅ Tous les `/start` `/close` `/doc` adapters existent-ils ?

#### 3.3 — Générer rapport audit

Créer **`DOCS/doc_audit_<date>.md`** :

```markdown
# Audit cohérence doc — YYYY-MM-DD

## ✅ Cohérences établies
- Version 2.4.0 synchronisée (constants.py, CHANGELOG, ROADMAP)
- ARCHITECTURE à jour (ref Phase 12, src/core/doc_analyzer.py)
- Adaptership mentionnés dans README

## ⚠️ Warnings
- WORKFLOW.md créé mais pas encore intégré dans CLAUDE.md (bloquant v2.6.0)
- Section "Archives" obsolète dans DOCS/ (ref fichier supprimé)

## 🔧 Propositions
1. Mettre à jour CLAUDE.md L42 : ajouter "Lire WORKFLOW.md" dans organes
2. Supprimer section DOCS/REFACTOR_PLAN.md (archivé L270 ROADMAP)
3. Ajouter `.antigravity/ANTIGRAVITY.md` (modèle : `.claude/CLAUDE.md`)
```

#### 3.4 — Valider avant `/close`

**Fail `/close`** si warnings **majeurs** :
- Versions désynchronisées
- Adapters IA manquants (v2.6.0+)
- Contenu hardcodé repéré (pattern checker)

**Info/warning** : non-bloquant mais proposé dans `/close` pour fix rapide.

---

## 4️⃣ `/close` — Clôture de session

### Objectif
Documenter apprentissages, créer commit, tagger version si applicable.

### Procédure

#### 4.1 — Exécuter `/doc` audit (v2.6.0+)

Avant tout commit :
```bash
/doc  # Générer rapport audit
# Si warnings majeurs → fix + recommit
```

#### 4.2 — Documenter apprentissages

**Créer** si nouveau (bugs résolus, patterns découverts, workflows) :
- Fichier : `APPRENTISSAGES/<domain>/<topic>.md` (<500 tokens)
- Frontmatter : title, domain, tags, severity, created, updated, version
- Format : Problème / Solution / Code pattern / Pièges

**Domaines** : core, ui, security, bugs_resolved, workflows

**Exemple** :
```markdown
---
title: Détection image timeout sur multi-moniteur
domain: core
tags: detector, edge_case
severity: medium
created: 2026-04-25
updated: 2026-04-25
version: v2.5.0
---

## Problème
Detector.locate() timeout 30s si moniteur secondaire désactivé entre scans.

## Solution
Ajouter try/except autour moniteur enumeration, fallback primary screen si error.

## Code pattern
\`\`\`python
def _get_monitors():
    try:
        return screeninfo.get_monitors()
    except Exception:
        return [screeninfo.get_monitors()[0]]  # fallback
\`\`\`

## Pièges
- Ne pas silencier exception — log.warning() pour debug
- Test multi-moniteur requis (mock secondaire)
```

#### 4.3 — Mettre à jour `meta.json`

Ajouter/retirer learnings dans `APPRENTISSAGES/meta.json` :

```json
{
  "version": "v2.5.0",
  "last_updated": "2026-04-25T15:30:00Z",
  "total_learnings": 1,
  "domains": {
    "core": 1,
    "ui": 0,
    ...
  },
  "by_severity": {
    "high": [],
    "medium": ["core/detector_image_timeout.md"],
    "low": []
  }
}
```

#### 4.4 — Créer commit

**Format message** :

```
<type>: <description> (<phase>)

<body — 2-3 lignes : contexte + raison>

Co-Authored-By: <AI Name> <noreply@anthropic.com>
```

**Types** : `feat`, `fix`, `refactor`, `docs`, `test`, `chore`

**Exemple** :
```
feat: implement sidebar dynamic loader (Phase 11.1)

Scans src/content/ filesystem, generates tabs on startup.
Enables extensibility: add .md = feature live (zero code).

Co-Authored-By: Claude Code <noreply@anthropic.com>
```

#### 4.5 — Tag version (si applicable)

Si `/bump_version` exécuté, tagger après commit :
```bash
git tag -a v2.5.0 -m "Release v2.5.0 — Hub UI dynamique"
```

---

## 📋 Handoff inter-IA (v2.6.0+)

### Quand utiliser

Quand context ≈ 60-70% du max OU tâche demande >2 phases majeures.

### Format `TASKS/<id>_<slug>.md`

**Frontmatter** :
```markdown
---
title: Implémenter sidebar dynamique
assigned_to: claude_code        # IA actuelle
status: in_progress
handoff_from: null
created: 2026-04-25T10:00:00Z
updated: 2026-04-25T12:30:00Z
context_tokens_used: 42000
---
```

**Status progression** :
- `pending` → `in_progress` → `in_review` → `ready_for_handoff` → `done`

### Format `HANDOFF_<task_id>.md`

Créé par IA qui s'arrête, lu par IA suivante :

```markdown
---
handoff_from: claude_code
handoff_to: comet
date: 2026-04-25T14:00:00Z
---

## État actuel

### Fichiers modifiés/créés
- src/ui/tabs/base_tab.py ✅ (abstract Tab class complet)
- src/ui/tabs/markdown_tab.py 🔄 (80% — renderer md)
- src/ui/sidebar/sidebar_panel.py ⏳ (stub vide)

### Prochaine étape précise
1. Terminer markdown_tab.py (ligne 45 onwards — manque render logic)
2. Implémenter content_view.py (zone droite, select tab)
3. Intégrer dans sidebar_panel.py (layout)
4. Tests : test_markdown_tab.py (80% couverture)

### Pièges identifiés
- CTkScrollableFrame redimensionnement non-réactif → gérer dans layout()
- Frontmatter YAML edge cases (empty sections, special chars) → tester

### Contexte à charger (v2.5.0)
- ROADMAP Phase 11.1 (sidebar objectives)
- ARCHITECTURE section "Contenus dynamiques" + "Loaders"
- Apprentissage : ui/customtkinter_best_practices.md (si existe)

### Tokens utilisés
- Lire doc : 600
- Impl : 2200
- Tests : 800
- Audit doc : 200
- **Total** : ~3800 (sur ~5000 budget)

### Blocages
Aucun — prêt handoff.
```

---

## 🎯 Guidelines par IA

### Claude Code

**Adapter** : `.claude/CLAUDE.md`

**Commandes** : `/start`, `/close`, `/doc`, `/bump_version`

**Particularités** :
- Accès direct projet (filesystem, git)
- Peut exécuter scripts `.tooling/`
- Écriture directe fichiers organes

### Comet (Perplexity)

**Adapter** : `.comet/COMET.md`

**Commandes** : `/start`, `/close`, `/doc` (syntaxe Comet)

**Particularités** :
- Pas d'accès direct filesystem (lire via chat)
- Handoff via pastebin/gist si fichiers volumineux
- Focus : analysis, review, audit

### Antigravity

**Adapter** : `.antigravity/ANTIGRAVITY.md`

**Commandes** : `/start`, `/close`, `/doc` (syntaxe Antigravity)

**Particularités** :
- Peuvent exécuter code (lire output, pas d'accès direct)
- Idéal pour tests + analysis
- Excellente pour audit `/doc`

---

## ✅ Checklist `/close`

- [ ] `/doc` exécuté (v2.6.0+) — pas de warnings majeurs
- [ ] Apprentissages documentés (si nouveau) → fichier + meta.json
- [ ] Tests ≥90% couverture (si v2.5.0+)
- [ ] Commit message normalisé + traçabilité IA
- [ ] Version bumpée si release (`/bump_version`)
- [ ] Tag créé (si release)
- [ ] HANDOFF créé (si passage à IA suivante)

---

## 📊 Token budget recommandé

| Phase | Budget | Durée |
|-------|--------|-------|
| `/start` (lire + charger) | 500-800 | 5 min |
| Implémentation feature | 2000-3000 | 20-40 min |
| Tests (v2.5.0+) | 1000-1500 | 15-20 min |
| `/doc` audit (v2.6.0+) | 500 | 5 min |
| `/close` (doc + commit) | 300 | 5 min |
| **Total/session** | **5000-6500** | **60-90 min** |

**Reset context** : entre phases majeures ou ≥60% max context → handoff.

---

## 🔄 Intégration adapters IA

### Adapter template

```python
# .claude/commands/start.md — Claude Code
/start : [lecture organes] → [charger apprentissages] → [analyser ROADMAP] → [recommander tâches]

# .comet/COMET.md — Comet
/start : même procédure, exécuter via Comet API

# .antigravity/ANTIGRAVITY.md — Antigravity
/start : même procédure, exécuter via Antigravity API
```

Tous lisent **le même WORKFLOW.md** — adapters = syntaxe cible uniquement.

---

**Version** : WORKFLOW.md v1 (v2.6.0+)
**Auteur** : ServOMorph + Claude Code (v2.4.0)
**Dernière MAJ** : 2026-04-25
