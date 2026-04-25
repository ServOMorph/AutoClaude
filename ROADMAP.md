# 🗺️ ROADMAP AutoClaude

> **Version actuelle** : v2.4.0 (branche `v2.4.0`) • **Cible** : v2.5.0
> **Dernière MAJ** : 2026-04-25
> **Statut global** : Phase 9 (v2.3.0) ✅ • Phase 10 (v2.4.0 infra) 🔄 • Phase 11 (v2.5.0) ⏳

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
| **v2.4.0** | 🔄 | Refacto infra + cycle apprentissage + bump auto |
| **v2.5.0** | ⏳ | Auto-updater + tips + sidebar dynamique |

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

## 🔄 Phase 10 — v2.4.0 : Infrastructure & Cycle d'apprentissage

> Objectif : refondre racine projet, automatiser versioning, instaurer cycle de travail avec mémoire inter-sessions.

### 10.1 — Refactorisation racine (30 min) ✅

| Tâche | Fichier cible | Statut |
|-------|--------------|--------|
| 10.1.1 Créer `DOCS/PLANS_MAJ/`, `build/pyinstaller/`, `.tooling/` | structure | ✅ |
| 10.1.2 Déplacer doc → `DOCS/` (ARCHITECTURE, CHANGELOG, etc.) | `DOCS/` | ✅ |
| 10.1.3 Déplacer specs PyInstaller → `build/pyinstaller/` | `build/` | ✅ |
| 10.1.4 Déplacer outils → `.tooling/` (build.py, audits) | `.tooling/` | ✅ |
| 10.1.5 Conserver `COMET/` (Perplexity) + `COMET/README.md` | `COMET/` | ✅ |
| 10.1.6 Mettre à jour `.gitignore` (build/, dist/, .benchmarks/) | `.gitignore` | ✅ |
| 10.1.7 Section "Intégrations IA" dans `README.md` | `README.md` | ✅ |

### 10.2 — Commande `/bump_version` (5 min) ✅

| Tâche | Fichier cible | Statut |
|-------|--------------|--------|
| 10.2.1 Guide workflow | `.claude/commands/bump_version.md` | ✅ |
| 10.2.2 Script bump | `.tooling/bump_version.py` | ✅ |
| 10.2.3 Script changelog | `.tooling/bump_changelog.py` | ✅ |
| 10.2.4 Config fichiers + patterns | `.tooling/bump_version_files.json` | ✅ |
| 10.2.5 Mode `--analyze` (détection nouveaux fichiers) | — | ✅ |

### 10.3 — Cycle de travail standardisé ✅

| Tâche | Fichier cible | Statut |
|-------|--------------|--------|
| 10.3.1 Commande `/start` (load apprentissages) | `.claude/commands/start.md` | ✅ |
| 10.3.2 Commande `/close` (doc apprentissages + commit) | `.claude/commands/close.md` | ✅ |
| 10.3.3 CLAUDE.md cycle obligatoire + économie tokens | `.claude/CLAUDE.md` | ✅ |

### 10.4 — Système d'apprentissage scalable ✅

| Tâche | Fichier cible | Statut |
|-------|--------------|--------|
| 10.4.1 Structure racine `APPRENTISSAGES/` | `APPRENTISSAGES/` | ✅ |
| 10.4.2 Index `meta.json` (version, count, by_severity) | `APPRENTISSAGES/meta.json` | ✅ |
| 10.4.3 Domains : core, ui, security, bugs_resolved, workflows | sous-dossiers | ✅ |
| 10.4.4 README format apprentissage + bonnes pratiques | `APPRENTISSAGES/README.md` | ✅ |
| 10.4.5 Loader sélection (max 5-7 docs, 3000 tokens) | spec dans CLAUDE.md | ✅ |

### 10.5 — Plan consolidé v2.5.0 ✅

| Tâche | Fichier cible | Statut |
|-------|--------------|--------|
| 10.5.1 Roadmap consolidée | `DOCS/PLANS_MAJ/ROADMAP_v2.5.0.md` | ✅ |
| 10.5.2 Roadmap racine (ce fichier) | `ROADMAP.md` | ✅ |

### Critères de validation v2.4.0

| Critère | Statut |
|---------|--------|
| Racine claire (≤ 7 fichiers) | ✅ |
| `/bump_version` fonctionnel + analyse | ✅ |
| `/start` charge apprentissages | ✅ |
| `/close` documente apprentissages | ✅ |
| `APPRENTISSAGES/meta.json` initialisé | ✅ |
| CLAUDE.md ≤ 60 lignes (économie tokens) | ✅ |
| 3 organes synchronisés (README/ROADMAP/ARCHITECTURE) | ✅ |

---

## ⏳ Phase 11 — v2.5.0 : Auto-updater + Tips + Sidebar

> Objectif : 3 fonctionnalités majeures avec **architecture dynamique** (tout depuis `src/content/`, aucun hardcodé). Durée estimée : 3-4 jours.

### 11.1 — Auto-updater GitHub Releases (1j) ⏳

> 2 exécutables distincts : `AutoClaude.exe` (app) + `AutoClaude_Updater.exe` (15-20 MB)

**Fichiers à créer** :
| Fichier | Rôle |
|---------|------|
| `src/core/update_checker.py` | GitHub API + comparaison versions (`packaging`) |
| `src/ui/components/update_button.py` | Bouton "Vérifier mises à jour" |
| `src/ui/dialogs/update_dialog.py` | Dialog confirmation + progress bar |
| `updater/updater.py` | Standalone : download → kill app → replace → relaunch |
| `updater/updater_config.json` | Config owner, repo, asset_name |
| `updater/AutoClaude_Updater.spec` | PyInstaller spec updater |

**Fichiers à modifier** :
| Fichier | Changement |
|---------|-----------|
| `src/config/constants.py` | +`URL_GITHUB_API`, `UPDATER_CONFIG` |
| `src/config/settings.py` | +`update_check_enabled` (default True) |
| `src/ui/app.py` | +update_button + thread daemon check (2s delay) |
| `requirements.txt` | +`requests>=2.31.0`, `packaging>=24.0` |

**Workflow** : `GitHub API → compare VERSION → dialog → Popen(updater) → app.quit() → updater replace → relaunch`

**Gestion erreurs** : timeout 5s • 404/rate limit silencieux • rollback `.bak` • download partiel (vérif taille > 1MB)

### 11.2 — Tips dynamiques (0.5j) ⏳

| Fichier | Rôle |
|---------|------|
| `src/content/tips/*.md` | Fichiers tips (core, ui, shortcuts, updates) |
| `src/core/tips_loader.py` | Scanner + parser markdown |
| `src/ui/dialogs/tips_dialog.py` | Dialog CTkToplevel : tip aléatoire au démarrage |

**Modifications** :
- `src/config/settings.py` → +`show_tips_on_startup` (default True)
- `src/ui/app.py` → intégrer tips_dialog si setting actif

**Scalabilité** : ajouter `.md` = tip dispo immédiatement, aucun code touché.

### 11.3 — Sidebar dynamique (1.5j) ⏳

**Architecture cible** :
```
src/content/
├── tips/                  → Onglet Tips
├── prompts/               → Onglet Prompts
└── learnings/
    ├── core/              → Sous-onglet
    ├── ui/                → Sous-onglet
    └── security/          → Sous-onglet
```

**Fichiers à créer** :
| Fichier | Rôle |
|---------|------|
| `src/ui/sidebar/sidebar_panel.py` | CTkFrame gauche, nav dynamique |
| `src/ui/sidebar/tab_registry.py` | Scanne `src/content/`, registry |
| `src/ui/sidebar/content_view.py` | Zone droite, contenu actif |
| `src/ui/tabs/base_tab.py` | Classe abstraite (titre, icône, render) |
| `src/ui/tabs/markdown_tab.py` | Renderer .md → CTkScrollableFrame |
| `src/ui/tabs/learning_tab.py` | Sous-onglets depuis sous-dossiers |
| `src/ui/tabs/prompts_tab.py` | Liste prompts + copie rapide |
| `src/ui/tabs/tips_tab.py` | Liste tips + filtre catégorie |

**Scalabilité** : ajouter dossier dans `src/content/` = onglet auto-généré.

### 11.4 — CLAUDE.md contraintes architecture (0.25j) ✅

Section "Architecture dynamique" déjà présente dans [.claude/CLAUDE.md](.claude/CLAUDE.md) :
- ✅ Source unique = `src/content/`
- ✅ Loaders scannent toujours
- ✅ UI auto-générée
- ✅ Anti-patterns documentés

### 11.5 — Build & distribution v2.5.0 ⏳

| Tâche | Statut |
|-------|--------|
| Bump version 2.4.0 → 2.5.0 (`/bump_version`) | ⏳ |
| Build `AutoClaude_v2.5.0.spec` (≈ 120 MB) | ⏳ |
| Build `AutoClaude_Updater.spec` (≈ 15-20 MB) | ⏳ |
| GitHub Release v2.5.0 (assets : app + updater) | ⏳ |
| CHANGELOG v2.5.0 complet | ⏳ |

### Critères de validation v2.5.0

| Critère | Statut |
|---------|--------|
| Auto-updater détecte nouvelle release | ⏳ |
| Updater remplace exe sans corruption | ⏳ |
| App relance après update | ⏳ |
| Tips au démarrage (random depuis `src/content/tips/`) | ⏳ |
| Sidebar liste onglets dynamiquement | ⏳ |
| Sous-onglets `learnings/` auto-générés | ⏳ |
| Ajouter `.md` = feature dispo sans code | ⏳ |
| Aucun contenu hardcodé (audit grep) | ⏳ |

---

## 📊 Résumé global

| Phase | Version | Durée | Statut |
|-------|---------|-------|--------|
| 1-8 | v2.0 | — | ✅ |
| 9 | v2.3.0 | — | ✅ |
| 10.1 (refacto racine) | v2.4.0 | 30 min | ⏳ |
| 10.2 (bump_version) | v2.4.0 | 5 min | ✅ |
| 10.3 (cycle) | v2.4.0 | — | ✅ |
| 10.4 (apprentissage) | v2.4.0 | — | ✅ |
| 10.5 (roadmap) | v2.4.0 | — | ✅ |
| 11.1 (auto-updater) | v2.5.0 | 1j | ⏳ |
| 11.2 (tips) | v2.5.0 | 0.5j | ⏳ |
| 11.3 (sidebar) | v2.5.0 | 1.5j | ⏳ |
| 11.4 (constraints) | v2.5.0 | 0.25j | ✅ |
| 11.5 (build/release) | v2.5.0 | 0.25j | ⏳ |

---

## 🚀 Prochaines étapes (ordre d'exécution)

1. ⏳ **Phase 10.1** : exécuter refacto racine (DOCS/, build/pyinstaller/, .tooling/)
2. ⏳ **Documenter** premiers apprentissages (bugs résolus v2.3.0 → APPRENTISSAGES/bugs_resolved/)
3. ⏳ **Phase 11.1** : implémenter auto-updater
4. ⏳ **Phase 11.2** : implémenter tips
5. ⏳ **Phase 11.3** : implémenter sidebar
6. ⏳ **Phase 11.5** : bump 2.5.0 + build + release

---

## 🔮 Évolutions futures (hors v2.5.0)

- Internationalisation FR/EN
- Personnalisation image cible depuis l'UI
- Profils multiples (images selon contexte)
- Mode "dry-run" (détecter sans cliquer)
- Raccourci global système (activer/désactiver)
- Tests automatisés (pytest)
- Support Linux/macOS

---

## 📂 Documents liés (sources analysées)

| Fichier | Période couverte | Rôle | Cohérence |
|---------|------------------|------|-----------|
| [ARCHIVES/docs_legacy/ROADMAP_v2.3.0_historical.md](ARCHIVES/docs_legacy/ROADMAP_v2.3.0_historical.md) | v1 → v2.3.0 | Historique détaillé phases 1-9 | 📦 Archivé |
| [ARCHIVES/docs_legacy/DEVELOPMENT_PLAN.md](ARCHIVES/docs_legacy/DEVELOPMENT_PLAN.md) | v2.0 (2026-04-23) | Plan initial UI/refacto | 📦 Archivé |
| [ARCHIVES/docs_legacy/PLAN_DE_TRAVAIL.md](ARCHIVES/docs_legacy/PLAN_DE_TRAVAIL.md) | v2.5.0 features | Détails auto-updater + tips + sidebar | 📦 Archivé |
| [ARCHIVES/docs_legacy/ROADMAP_v2.5.0.md](ARCHIVES/docs_legacy/ROADMAP_v2.5.0.md) | v2.4.0 → v2.5.0 | Plan consolidé phases + apprentissage | ✅ Source principale |
| [ARCHIVES/docs_legacy/REFACTOR_PLAN.md](ARCHIVES/docs_legacy/REFACTOR_PLAN.md) | v2.4.0 (refacto racine) | Détails Phases 1-6 + stub Phase 7 | 📦 Archivé |
| [DOCS/ARCHITECTURE.md](DOCS/ARCHITECTURE.md) | — | Architecture technique projet | ✅ |
| [APPRENTISSAGES/README.md](APPRENTISSAGES/README.md) | — | Système d'apprentissage | ✅ |
| [.claude/CLAUDE.md](.claude/CLAUDE.md) | — | Directives Claude Code | ✅ Optimisé tokens |
| [DOCS/CHANGELOG.md](DOCS/CHANGELOG.md) | v1 → v2.3.0 | Historique versions | ✅ |

---

## 🔍 Analyse de cohérence inter-documents

### ✅ Cohérences établies

| Document | Constat |
|----------|---------|
| `DEVELOPMENT_PLAN.md` (v2.0) | 100% des items livrés (Phases 1-8 ✅) → archive historique |
| `DOCS/ROADMAP.md` | Phases 1-9 complètes, statut "v2.3.0 terminée" cohérent |
| `constants.py VERSION = "2.4.0"` | Cohérent avec branche `v2.4.0` et plans en cours |
| `PLAN_DE_TRAVAIL.md` ↔ `ROADMAP_v2.5.0.md` | Mêmes 3 features (updater/tips/sidebar), specs alignées |
| `REFACTOR_PLAN.md` Phases 1-6 ↔ Phase 10.1 ci-dessus | Même contenu, pas de divergence |

### ⚠️ Divergences détectées

| Divergence | Impact | Action |
|------------|--------|--------|
| `PLAN_DE_TRAVAIL.md` et `ROADMAP_v2.5.0.md` se chevauchent (~70%) | Source dupliquée | Conserver `ROADMAP_v2.5.0.md` (consolidé), garder `PLAN_DE_TRAVAIL.md` comme spec technique détaillée |
| `REFACTOR_PLAN.md` ligne ~330 : ref ancien `PLAN_DE_TRAVAIL.md` | Lien existe (DOCS/PLAN_DE_TRAVAIL.md) ✅ | Mais `Phase 7 stub` à supprimer (déjà dans ROADMAP) |
| `DEVELOPMENT_PLAN.md` mentionne window 520×640 | Réalité : 520×860 (overlay v2.3.0) | Document historique, pas de mise à jour nécessaire |
| Aucun document ne couvre Phase 9 (v2.3.0) sauf `DOCS/ROADMAP.md` | OK | Source unique = historique |

### 📌 Hiérarchie clarifiée

```
ROADMAP.md (racine)              ← INDEX MAÎTRE (ce fichier)
│
├── Passé (v1 → v2.3.0)
│   ├── DOCS/ROADMAP.md          ← Historique détaillé phases 1-9
│   ├── DOCS/DEVELOPMENT_PLAN.md ← Plan original v2.0 (archive)
│   └── DOCS/CHANGELOG.md        ← Versions livrées
│
├── Présent (v2.4.0 — en cours)
│   ├── DOCS/REFACTOR_PLAN.md    ← Spec refacto racine (Phase 10.1)
│   └── APPRENTISSAGES/          ← Cycle apprentissage actif
│
└── Futur (v2.5.0 — planifié)
    ├── DOCS/PLANS_MAJ/ROADMAP_v2.5.0.md  ← Plan consolidé
    └── DOCS/PLAN_DE_TRAVAIL.md           ← Spec technique détaillée
```

### 🎯 Recommandations

1. **`DOCS/PLAN_DE_TRAVAIL.md`** : conserver comme **spec technique détaillée** (workflow updater, gestion erreurs, format tips, API tab_registry) — complémentaire à ROADMAP_v2.5.0
2. **`DOCS/REFACTOR_PLAN.md`** : retirer la "Phase 7 stub" (lignes 328+) qui duplique Phase 11 ci-dessus
3. **`DOCS/DEVELOPMENT_PLAN.md`** : marquer comme **archive** (en-tête à ajouter : "📦 Archive — Plan v2.0 livré 2026-04-23")
4. **`DOCS/ROADMAP.md`** : continuer comme historique uniquement, ne plus alimenter pour v2.4.0+

---

**Branche actuelle** : `v2.4.0` • **Version constants.py** : `2.4.0` • **Source de vérité** : ce fichier (ROADMAP.md racine)
