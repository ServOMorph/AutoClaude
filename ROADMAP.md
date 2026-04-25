# 🗺️ ROADMAP AutoClaude

> **Version actuelle** : v2.4.0 (branche `v2.4.0`) • **Cible** : v2.5.0
> **Dernière MAJ** : 2026-04-25
> **Statut global** : Phase 10 (v2.4.0) ✅ • Phase 11 (v2.5.0) ⏳

---

## 🎯 Vision

> **AutoClaude = Centre de commande multi-IA** (Claude Code, Comet, Antigravity, et d'autres)
>
> L'autoclick est un module parmi d'autres. Le cœur du projet : une interface scalable et dynamique pour orchestrer plusieurs IA sur un projet, avec un **workflow IA-agnostique** partagé (même `/start` `/close` `/doc` quel que soit le LLM), des contenus pilotés par fichiers, et un système de handoff entre agents.

---

## Légende

| Symbole | Signification |
|---------|---------------|
| ✅ | Terminé |
| 🔄 | En cours |
| ⏳ | Planifié |
| ❌ | Bloqué / annulé |

---

## 📚 Vue d'ensemble

| Version | Statut | Thème principal |
|---------|--------|-----------------|
| v1.x | ✅ | CLI base : détection + clic + listener |
| v2.0 | ✅ | UI CustomTkinter + sécurité CLAUDE.md |
| v2.1-2.2 | ✅ | Stats, analyses, polish |
| **v2.3.0** | ✅ | Overlay flottant + stabilité long-run (24h+) |
| **v2.4.0** | ✅ | Refacto infra + cycle apprentissage + bump auto |
| **v2.5.0** | ⏳ | Hub UI dynamique (sidebar + prompts + tips) + tests 90% |
| **v2.6.0** | ⏳ | Workflow IA-agnostique + `/doc` + session management |
| **v2.7.0** | ⏳ | Connecteurs IA (Comet, Antigravity, CC) + routeur tâches + tests |
| **v2.8.0** | ⏳ | Auto-updater + polish distribution + final tests |

---

## ✅ Phases historiques (v1 → v2.3.0)

Détails complets dans [ARCHIVES/docs_legacy/ROADMAP_v2.3.0_historical.md](ARCHIVES/docs_legacy/ROADMAP_v2.3.0_historical.md).

| Phase | Version | Livrables | Statut |
|-------|---------|-----------|--------|
| 1 — Setup & Config | v2.0 | `src/`, constants, settings, requirements | ✅ |
| 2 — Core (refacto v1) | v2.0 | monitors, detector, clicker, listener, autoclick_service | ✅ |
| 3 — Sécurité | v2.0 | `ClaudeMdProtector` + marqueurs GUARD | ✅ |
| 4 — UI Theme | v2.0 | Palette SéréniaTech + polices | ✅ |
| 5 — Composants UI | v2.0 | Header, banner, buttons, footer, dialogs | ✅ |
| 6 — App principale | v2.0 | `AutoClaudeApp` 520×860px | ✅ |
| 7 — Point d'entrée | v2.0 | `run.py` 4 lignes, lancement < 2s | ✅ |
| 8 — Doc & Publication | v2.0 | ARCHITECTURE, SECURITY, CHARTE, README, LICENSE | ✅ |
| 9 — Overlay + Stabilité | **v2.3.0** | Overlay always-on-top, logger, health monitor, auto-restart, buffer stats, idempotence listener, GitHub Release | ✅ |

---

## ✅ Phase 10 — v2.4.0 : Infrastructure & Cycle d'apprentissage

> Objectif : refondre racine projet, automatiser versioning, instaurer cycle de travail avec mémoire inter-sessions.

| Sous-phase | Livrables | Statut |
|-----------|-----------|--------|
| 10.1 — Refactorisation racine | `DOCS/`, `build/pyinstaller/`, `.tooling/`, `.gitignore` MAJ | ✅ |
| 10.2 — `/bump_version` | Script bump + changelog + config fichiers + mode `--analyze` | ✅ |
| 10.3 — Cycle standardisé | `/start`, `/close`, `CLAUDE.md` cycle + économie tokens | ✅ |
| 10.4 — Système d'apprentissage | `APPRENTISSAGES/` + `meta.json` + domains + README | ✅ |
| 10.5 — Roadmap consolidée | `ROADMAP.md` racine cohérente | ✅ |

### Critères v2.4.0 ✅

- Racine claire (≤ 7 fichiers hors doc)
- `/bump_version` fonctionnel
- `/start` charge apprentissages, `/close` documente
- `APPRENTISSAGES/meta.json` initialisé
- 3 organes synchronisés (README/ROADMAP/ARCHITECTURE)

---

## ⏳ Phase 11 — v2.5.0 : Hub UI dynamique + Tests

> Objectif : interface centrale scalable — tout contenu depuis `src/content/`, aucun hardcodé. Couverture tests 90%.
> Durée estimée : 4-5 jours.

### 11.1 — Sidebar dynamique (1.5j) ⏳

**Architecture** :
```
src/content/
├── tips/           → Onglet Tips (1 onglet sidebar)
├── prompts/        → Onglet Prompts (bibliothèque inter-IA)
└── learnings/
    ├── core/       → Sous-onglet
    ├── ui/         → Sous-onglet
    └── security/   → Sous-onglet
```

| Fichier | Rôle |
|---------|------|
| `src/ui/sidebar/sidebar_panel.py` | CTkFrame gauche, nav dynamique |
| `src/ui/sidebar/tab_registry.py` | Scanne `src/content/`, génère registry |
| `src/ui/sidebar/content_view.py` | Zone droite, contenu actif |
| `src/ui/tabs/base_tab.py` | Classe abstraite (titre, icône, render) |
| `src/ui/tabs/markdown_tab.py` | Renderer `.md` → CTkScrollableFrame |
| `src/ui/tabs/learning_tab.py` | Sous-onglets depuis sous-dossiers |
| `src/ui/tabs/prompts_tab.py` | Liste prompts + copie rapide |
| `src/ui/tabs/tips_tab.py` | Liste tips + filtre catégorie |

**Scalabilité** : ajouter dossier `src/content/` = onglet auto-généré.

### 11.2 — Bibliothèque de prompts (0.5j) ⏳

| Fichier | Rôle |
|---------|------|
| `src/content/prompts/*.md` | Prompts partagés inter-IA (frontmatter : title, ia_target, tags) |
| `src/core/prompts_loader.py` | Scanner + parser markdown |

**Usage** : copie rapide depuis sidebar → coller dans Claude Code / Comet / Antigravity.

### 11.3 — Tips au démarrage (0.5j) ⏳

> Tips = onglet sidebar **ET** dialog optionnel au démarrage (pas de feature séparée)

| Fichier | Rôle |
|---------|------|
| `src/content/tips/*.md` | Fichiers tips (core, ui, shortcuts) |
| `src/core/tips_loader.py` | Scanner + parser markdown |
| `src/ui/dialogs/tips_dialog.py` | Dialog CTkToplevel : tip aléatoire au démarrage |

### 11.4 — Tests unitaires + intégration (1.5j) ⏳

| Fichier | Couverture |
|---------|-----------|
| `tests/unit/` | Loaders, parsers, tab_registry (détection contenu) |
| `tests/integration/` | Sidebar rendering, navigation onglets |
| `tests/ui/` | CTkFrame interaction (mock Tkinter) |
| `.tooling/coverage_report.py` | Rapport couverture + fail <90% |
| `pytest.ini` | Config tests + min coverage 90% |

**Exigence** : `/close` v2.5.0 échoue si couverture < 90%.

### 11.5 — Documentation cohérence multi-LLM (0.5j) ⏳

Exécuter `/doc` sur le projet :
- Vérifier README, ROADMAP, ARCHITECTURE cohérence
- Vérifier optimisation multi-LLM (README mention center command ? adaptable par IA ?)
- Proposer améliorations

### 11.6 — Build & commit v2.5.0 (0.25j) ⏳

| Tâche | Statut |
|-------|--------|
| Exécuter `/doc` — vérifier cohérence | ⏳ |
| Tests couverture ≥90% | ⏳ |
| Bump 2.4.0 → 2.5.0 (`/bump_version`) | ⏳ |
| `/close` — documenter apprentissages | ⏳ |
| GitHub commit + tag v2.5.0 | ⏳ |

### Critères v2.5.0

| Critère | Statut |
|---------|--------|
| Sidebar liste onglets dynamiquement depuis `src/content/` | ⏳ |
| Sous-onglets `learnings/` auto-générés | ⏳ |
| Prompts copiables depuis sidebar | ⏳ |
| Tips au démarrage (random depuis `src/content/tips/`) | ⏳ |
| Ajouter `.md` = feature dispo sans code | ⏳ |
| Tests couverture 90%+ | ⏳ |
| `/doc` valide cohérence multi-LLM | ⏳ |

---

## ⏳ Phase 12 — v2.6.0 : Workflow IA-agnostique + `/doc` intégré

> Objectif : que Comet, Antigravity, Claude Code suivent exactement le même cycle, avec `/doc` automatisé en fin de session.
> Durée estimée : 3 jours.

### 12.1 — Commande `/doc` (1j) ⏳

**Purpose** : analyse + amélioration doc automatique multi-LLM.

| Fichier | Rôle |
|---------|------|
| `.claude/commands/doc.md` | Procédure `/doc` — lire, auditer, proposer |
| `src/core/doc_analyzer.py` | Script : scan fichiers organes, vérifier cohérence |
| `src/core/doc_validator.py` | Règles : sections requises, format, multi-LLM compliance |

**Workflow `/doc`** :
1. Lire README/ROADMAP/ARCHITECTURE/WORKFLOW
2. Chercher incohérences (ref mortes, versions désynchronisées, contenu hardcodé)
3. Auditer optimisation multi-LLM (language agnostique ? adapters mentionnés ?)
4. Proposer fichier `DOCS/doc_audit_<date>.md` avec :
   - ✅ Cohérences établies
   - ⚠️ Warnings (sections obsolètes, doublon)
   - 🔧 Propositions (refactor, réorg)

**Exécution** :
```bash
python -m src.core.doc_analyzer --check README.md ROADMAP.md ARCHITECTURE.md WORKFLOW.md
# Sortie : rapport + exit code 1 si warnings > 0 (peut bloquer `/close`)
```

### 12.2 — `WORKFLOW.md` (4ème organe) (0.5j) ⏳

Nouveau fichier racine décrivant le cycle de travail **sans référence à un LLM spécifique** :
- Lire README/ROADMAP/ARCHITECTURE/WORKFLOW au démarrage
- Charger apprentissages (`APPRENTISSAGES/meta.json`)
- Format de rapport de session
- Documenter apprentissages au close
- Committer avec message normalisé

### 12.3 — Adapters IA (0.5j) ⏳

| Dossier | Contenu |
|---------|---------|
| `.claude/commands/` | `/start`, `/close`, `/doc`, `/bump_version` |
| `.antigravity/commands/` | Équivalents pour Antigravity |
| `.comet/commands/` | Équivalents pour Comet |

Tous lisent `WORKFLOW.md` comme source de vérité. Adapters = traduction vers syntaxe IA cible uniquement.

### 12.4 — Format tâche normalisé (1j) ⏳

```
TASKS/
├── <id>_<slug>.md       frontmatter: assigned_to, status, handoff_from, created, updated
└── README.md            format + workflow handoff
```

**Cycle handoff** : IA-A termine → écrit résultat dans `TASKS/<id>.md` → status = `done` → IA-B reprend avec contexte.

### 12.5 — Integration `/doc` dans cycle (0.5j) ⏳

Mettre à jour CLAUDE.md :
```
3️⃣ /close :
   - Exécuter `/doc` — vérifier cohérence
   - Si warnings : proposer fixes avant commit
   - Documenter apprentissages
   - Committer avec message normalisé
```

Comet/Antigravity font pareil dans `.comet/COMET.md`, `.antigravity/ANTIGRAVITY.md`.

### Critères v2.6.0

| Critère | Statut |
|---------|--------|
| `/doc` command fonctionnel + audit report | ⏳ |
| `WORKFLOW.md` racine (4ème organe) | ⏳ |
| `.antigravity/` + `.comet/` avec commandes `/start` `/close` `/doc` | ⏳ |
| Format `TASKS/<id>.md` défini + README | ⏳ |
| CLAUDE.md référence WORKFLOW.md + `/doc` dans `/close` | ⏳ |
| `/doc` appelé avant chaque commit (v2.6 → suite) | ⏳ |

---

## ⏳ Phase 13 — v2.7.0 : Connecteurs IA + Routeur + Tests

> Objectif : UI gestion tâches inter-IA. Couverture tests 90%+.
> Durée estimée : 4-5 jours.

### 13.1 — Adapters code (1j) ⏳

| Fichier | Rôle |
|---------|------|
| `src/integrations/base_adapter.py` | Interface abstraite |
| `src/integrations/claude_code.py` | Adapter Claude Code |
| `src/integrations/antigravity.py` | Adapter Antigravity |
| `src/integrations/comet.py` | Adapter Comet |

### 13.2 — Onglet "Tâches" sidebar (1.5j) ⏳

| Fichier | Rôle |
|---------|------|
| `src/content/tasks/` | Tâches TASKS/ exposées dans sidebar |
| `src/ui/tabs/tasks_tab.py` | Liste tâches + statut + assignation IA |
| `src/core/tasks_loader.py` | Scanne `TASKS/`, parse frontmatter |

### 13.3 — Tests + `/doc` validation (1.5j) ⏳

| Fichier | Couverture |
|---------|-----------|
| `tests/unit/integrations/` | Adapters (spawn, communicate) |
| `tests/integration/tasks/` | Handoff IA-à-IA, parsing frontmatter |
| `tests/ui/tasks_tab/` | Rendering tâches, assignation |

**Avant `/close` v2.7.0** :
- Couverture ≥90%
- `/doc` audit sans warnings (ou fixes committed)

### 13.4 — Session management optimization (1j) ⏳

Pour chaque IA, documenter :
- **Token budget par phase** (lire doc=500, implém=2000, tests=1000, close=500)
- **Context reset points** (entre phases majeures)
- **Handoff format** : ce qu'IA-A laisse à IA-B pour continuer
  ```
  HANDOFF_<task_id>.md :
  - Contexte chargé au `/start` de IA-B
  - Où on en est (phase, fichiers modifiés)
  - Prochaine étape explicite
  ```

### 13.5 — Commit & close v2.7.0 (0.25j) ⏳

Workflow strict :
1. `/doc` audit (fail si warnings majeurs)
2. Tests ≥90% (fail si <90%)
3. `/close` — apprentissages + commit
4. Tag version sur GitHub

### Critères v2.7.0

| Critère | Statut |
|---------|--------|
| 3+ adapters IA opérationnels | ⏳ |
| Onglet Tâches dans sidebar | ⏳ |
| Handoff IA-à-IA via `TASKS/` + `HANDOFF_*` | ⏳ |
| Tests couverture 90%+ | ⏳ |
| `/doc` appelé avant chaque commit | ⏳ |

---

## ⏳ Phase 14 — v2.8.0 : Auto-updater + Polish + Final Tests

> Objectif : livraison autonome. Couverture tests 90%+. Audit `/doc` zéro warning.
> Durée estimée : 2-3 jours.

### 14.1 — Auto-updater (1j) ⏳

> 2 exécutables distincts : `AutoClaude.exe` (app) + `AutoClaude_Updater.exe` (15-20 MB)

| Fichier | Rôle |
|---------|------|
| `src/core/update_checker.py` | GitHub API + comparaison versions |
| `src/ui/components/update_button.py` | Bouton "Vérifier mises à jour" |
| `src/ui/dialogs/update_dialog.py` | Dialog confirmation + progress bar |
| `updater/updater.py` | Standalone : download → kill app → replace → relaunch |

### 14.2 — Final tests + `/doc` audit (0.75j) ⏳

**Tests** : couverture 90%+ incluant updater
**Audit** : `/doc` sans warnings majeurs

### 14.3 — Deuxième Overlay (0.5j) ⏳

> Overlay complémentaire (design à finaliser — inspiré projet "Bot ou pas Bot")

| Fichier | Rôle |
|---------|------|
| `src/ui/overlays/secondary_overlay.py` | Nouvel overlay flottant (stats/contrôles/info) |
| `src/ui/app.py` | Instanciation + gestion lifecycle |
| `tests/ui/test_secondary_overlay.py` | Tests rendering + interactions |

**À définir** : fonctionnalités (stats temps réel, contrôles, info supplémentaires)

### 14.4 — Build & release (0.5j) ⏳

| Tâche | Statut |
|-------|--------|
| `/doc` audit final (fix warnings) | ⏳ |
| Tests couverture ≥90% | ⏳ |
| Bump 2.7.0 → 2.8.0 (`/bump_version`) | ⏳ |
| `/close` + commit | ⏳ |
| GitHub Release v2.8.0 (app + updater) | ⏳ |

---

## 📊 Résumé global

| Phase | Version | Thème | Durée | Tests | Statut |
|-------|---------|-------|-------|-------|--------|
| 1-8 | v2.0 | Base | — | — | ✅ |
| 9 | v2.3.0 | Overlay + stabilité | — | — | ✅ |
| 10 | v2.4.0 | Infra + cycle | — | — | ✅ |
| 11 | v2.5.0 | Hub UI + tests | 4-5j | 90% | ⏳ |
| 12 | v2.6.0 | Workflow `/doc` | 3j | — | ⏳ |
| 13 | v2.7.0 | Connecteurs + tests | 4-5j | 90% | ⏳ |
| 14 | v2.8.0 | Auto-updater + final | 2-3j | 90% | ⏳ |

---

## 🔄 Intégration `/doc` dans workflow

À partir de **v2.6.0**, chaque session :

```
/start
  ├─ Lire README/ROADMAP/ARCHITECTURE/WORKFLOW
  └─ Charger apprentissages

Travail
  ├─ Implémenter
  └─ Tests

/doc (avant /close)
  ├─ Analyser cohérence
  ├─ Vérifier multi-LLM compliance
  └─ Proposer fixes → commit si nécessaire

/close
  ├─ Documenter apprentissages
  ├─ Commit message normalisé
  └─ Tag version
```

**Fréquence** : `/doc` systématique avant `/close` dès v2.6.0.

---

## 🚀 Prochaines étapes (ordre d'exécution)

1. ⏳ **Phase 11.1-11.3** : sidebar + prompts + tips
2. ⏳ **Phase 11.4** : tests 90%+
3. ⏳ **Phase 11.5** : `/doc` audit initial
4. ⏳ **Phase 11.6** : commit v2.5.0
5. ⏳ **Phase 12.1** : implémenter `/doc` command
6. ⏳ **Phase 12.2-12.5** : WORKFLOW.md + adapters + intégration
7. ⏳ **Phase 13** : connecteurs IA + tests
8. ⏳ **Phase 14** : auto-updater + final tests

---

## 🔮 Évolutions futures (hors v2.8.0)

- Internationalisation FR/EN (auditer avec `/doc`)
- Personnalisation image cible depuis l'UI
- Profils multiples (images selon contexte)
- Mode "dry-run" (détecter sans cliquer)
- Raccourci global système
- Support Linux/macOS
- Intégrations additionnelles (Claude 4.7, autres IA)

---

**Branche actuelle** : `v2.4.0` • **Version constants.py** : `2.4.0` • **Source de vérité** : ce fichier (ROADMAP.md racine)
