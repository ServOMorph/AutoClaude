# Architecture AutoClaude v2.4.0+

## Vue d'ensemble

```
AutoClaude/
├── run.py                      # Point d'entrée (4 lignes)
├── requirements.txt            # Dépendances Python
├── ROADMAP.md                  # Phases, statuts, priorités (organe)
├── ARCHITECTURE.md             # Structure technique (organe)
├── WORKFLOW.md                 # Cycle /start /close /doc IA-agnostique (organe, v2.6.0+)
├── README.md                   # Mission, features, usage (organe)
├── CHANGELOG.md                # Historique versions
├── assets/
│   ├── yes.png                 # Template détection par défaut
│   └── logo.png                # Branding SéréniaTech
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── constants.py        # Constantes globales (couleurs, paths, URLs, VERSION)
│   │   └── settings.py         # Persistance JSON (~/.autoclaude/settings.json)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── monitors.py         # Énumération moniteurs
│   │   ├── detector.py         # Détection image (template matching)
│   │   ├── clicker.py          # Clic souris
│   │   ├── listener.py         # Écoute clavier/souris (Esc, auto-stop)
│   │   ├── autoclick_service.py# Orchestration thread + événements
│   │   ├── logger.py           # Logs rotatifs + monitoring
│   │   ├── health_monitor.py   # Watchdog stabilité 24h+
│   │   ├── click_stats.py      # Buffering stats + persistence
│   │   ├── doc_analyzer.py     # Analyse cohérence doc (v2.6.0+)
│   │   ├── doc_validator.py    # Règles audit doc (v2.6.0+)
│   │   ├── tasks_loader.py     # Scan TASKS/, parse frontmatter (v2.6.0+)
│   │   └── prompts_loader.py   # Scan src/content/prompts/ (v2.5.0+)
│   ├── integrations/           # Adapters multi-IA (v2.7.0+)
│   │   ├── __init__.py
│   │   ├── base_adapter.py     # Interface abstraite
│   │   ├── claude_code.py      # Adapter Claude Code
│   │   ├── antigravity.py      # Adapter Antigravity
│   │   └── comet.py            # Adapter Comet
│   ├── security/
│   │   ├── __init__.py
│   │   └── claude_md_protector.py  # Injection restrictions .claude/CLAUDE.md
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── theme.py            # Palette SéréniaTech + CTk fonts
│   │   ├── app.py              # Fenêtre principale AutoClaudeApp
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── header.py       # Titre + statut
│   │   │   ├── warning_banner.py# Info/warning banner
│   │   │   ├── activate_button.py# Start/stop autoclick
│   │   │   ├── protection_button.py# Protection CLAUDE.md
│   │   │   ├── footer.py       # Boutons stats + settings
│   │   │   ├── click_counter.py# Affichage + reset compteur
│   │   │   ├── overlay_toggle.py# Toggle overlay flottant
│   │   │   └── update_button.py # Vérifier mises à jour (v2.8.0+)
│   │   ├── dialogs/
│   │   │   ├── __init__.py
│   │   │   ├── folder_picker.py# Sélection dossier projet
│   │   │   ├── analytics_window.py# Graphes analyses clics
│   │   │   ├── tips_dialog.py  # Tips aléatoire démarrage (v2.5.0+)
│   │   │   └── update_dialog.py # Confirmation update (v2.8.0+)
│   │   ├── sidebar/            # Hub dynamique (v2.5.0+)
│   │   │   ├── __init__.py
│   │   │   ├── sidebar_panel.py # CTkFrame gauche, nav
│   │   │   ├── tab_registry.py  # Génère registry depuis src/content/
│   │   │   └── content_view.py  # Zone droite, contenu actif
│   │   ├── tabs/               # Onglets dynamiques (v2.5.0+)
│   │   │   ├── __init__.py
│   │   │   ├── base_tab.py      # Classe abstraite (titre, icône, render)
│   │   │   ├── markdown_tab.py  # Renderer .md → CTkScrollableFrame
│   │   │   ├── learning_tab.py  # Sous-onglets learnings
│   │   │   ├── prompts_tab.py   # Liste prompts + copie rapide
│   │   │   ├── tips_tab.py      # Liste tips + filtre
│   │   │   └── tasks_tab.py     # Liste tâches + assignation IA (v2.7.0+)
│   │   └── overlays/
│   │       ├── __init__.py
│   │       └── status_overlay.py# Indicateur flottant always-on-top
│   └── content/                # Source unique : filesystem-driven (v2.5.0+)
│       ├── tips/               # Tips startup + sidebar (*.md)
│       ├── prompts/            # Bibliothèque prompts inter-IA (*.md)
│       ├── learnings/          # Auto-apprentissages (sous-dossiers : core, ui, security, bugs_resolved, workflows)
│       ├── workflows/          # Workflows réutilisables (v2.6.0+)
│       └── tasks/              # Tâches TASKS/ exposées sidebar (v2.7.0+)
├── .claude/
│   ├── CLAUDE.md               # Directives essentielles + cycle travail
│   └── commands/
│       ├── start.md            # `/start` — analyser + charger apprentissages
│       ├── close.md            # `/close` — documenter apprentissages + commit
│       ├── doc.md              # `/doc` — audit cohérence doc (v2.6.0+)
│       └── bump_version.md     # `/bump_version` — versioning auto
├── .antigravity/               # Adapter Antigravity (v2.6.0+)
│   ├── ANTIGRAVITY.md          # Directives Antigravity-spécifiques
│   └── commands/
│       ├── start.md
│       ├── close.md
│       └── doc.md
├── .comet/                     # Adapter Comet (v2.6.0+)
│   ├── COMET.md                # Directives Comet-spécifiques
│   └── commands/
│       ├── start.md
│       ├── close.md
│       └── doc.md
├── APPRENTISSAGES/             # Système d'apprentissage inter-sessions
│   ├── meta.json               # Index (version, count, domains, severity)
│   ├── README.md               # Format + bonnes pratiques
│   ├── core/
│   ├── ui/
│   ├── security/
│   ├── bugs_resolved/
│   └── workflows/
├── TASKS/                      # Tâches inter-IA + handoff (v2.6.0+)
│   ├── README.md               # Format + workflow handoff
│   └── <id>_<slug>.md          # frontmatter: assigned_to, status, handoff_from, created, updated
├── ARCHIVES/                   # Fichiers obsolètes + searchable index
│   ├── meta.json               # Index : reason, tags, recall_when
│   ├── README.md               # Système d'archivage
│   ├── docs_legacy/
│   ├── specs_pyinstaller/
│   ├── tooling_artifacts/
│   └── old_builds/
├── COMET/                      # Intégration Perplexity (docs générées)
│   └── README.md
├── DOCS/                       # Documentation additionnelle
│   ├── SECURITY.md             # Bonnes pratiques sécurité
│   └── (archived docs moved to ARCHIVES/)
├── .tooling/                   # Outils de développement
│   ├── bump_version.py
│   ├── bump_changelog.py
│   ├── bump_version_files.json
│   ├── archive_search.py
│   └── coverage_report.py      # Rapport couverture tests (v2.5.0+)
├── tests/                      # Suite tests (v2.5.0+)
│   ├── unit/
│   │   ├── test_loaders.py
│   │   ├── test_detector.py
│   │   ├── test_settings.py
│   │   └── (couverture 90%+)
│   ├── integration/
│   │   ├── test_sidebar.py
│   │   ├── test_tasks_handoff.py
│   │   └── (couverture 90%+)
│   ├── ui/
│   │   └── (UI tests mock Tkinter)
│   └── conftest.py             # Fixtures pytest
├── build/
│   └── pyinstaller/            # Specs PyInstaller par version
├── updater/                    # Auto-updater standalone (v2.8.0+)
│   ├── updater.py
│   ├── updater_config.json
│   └── AutoClaude_Updater.spec
├── dist/                       # Builds compilées
├── .gitignore                  # Ignore build/, dist/, .benchmarks/, etc.
├── pytest.ini                  # Config tests (v2.5.0+)
└── LICENSE
```

---

## Flux d'exécution

```
run.py
  └── AutoClaudeApp (CTk)
        ├── SidebarPanel (v2.5.0+)
        │   ├── TabRegistry (scanne src/content/)
        │   └── ContentView (onglets dynamiques)
        │
        ├── AutoclickService.start()
        │   ├── InputListener (thread) ← Esc / auto-stop
        │   ├── HealthMonitor (thread) ← Watchdog 24h+
        │   └── _run() (daemon) ← loop: detector → clicker → stats
        │
        ├── StatusOverlay (Toplevel always-on-top)
        │
        └── ClaudeMdProtector.apply() ← sur demande utilisateur
```

---

## Système d'analyse doc `/doc` (v2.6.0+)

### Workflow `/doc`

```
/doc
  ├── Lire 4 organes (README/ROADMAP/ARCHITECTURE/WORKFLOW)
  ├── DocAnalyzer.scan() → détecte incohérences
  │   ├── Versions désynchronisées (constants.py vs CHANGELOG vs ROADMAP)
  │   ├── Références mortes (fichiers supprimés, liens rompus)
  │   ├── Contenu hardcodé (repéré vs contenu dynamique)
  │   └── Multi-LLM compliance (adapters mentionnés ? WORKFLOW.md partagé ?)
  │
  ├── DocValidator.validate() → applique règles audit
  │   ├── Section requises présentes
  │   ├── Format markdown validé
  │   └── Priorisation warnings (majeur=fail close, mineur=info)
  │
  └── Rapport audit → DOCS/doc_audit_<date>.md
      ├── ✅ Cohérences établies
      ├── ⚠️ Warnings (sections obsolètes, doublon)
      └── 🔧 Propositions (refactor, réorg, optimisations)

Exit code 1 si warnings majeurs → bloquer /close v2.6.0+
```

### Fichiers clés

| Fichier | Rôle |
|---------|------|
| `src/core/doc_analyzer.py` | Scan README/ROADMAP/ARCHITECTURE/WORKFLOW + regex patterns |
| `src/core/doc_validator.py` | Règles validation + scoring warnings |
| `.claude/commands/doc.md` | Procédure `/doc` pour Claude Code |
| `.antigravity/commands/doc.md` | Procédure `/doc` pour Antigravity |
| `.comet/commands/doc.md` | Procédure `/doc` pour Comet |

---

## Contenus dynamiques (v2.5.0+)

### Architecture `src/content/`

Principe : **tout fichier `.md` ajouté = feature dispo** sans code.

```
src/content/
├── tips/
│   ├── core.md                 # Tips détection/clic
│   ├── ui.md                   # Tips interface
│   └── shortcuts.md            # Raccourcis clavier
├── prompts/
│   ├── analyze_code.md         # Prompt réutilisable (ia_target: claude_code)
│   ├── debug_issue.md          # (ia_target: comet)
│   └── refactor_module.md      # (ia_target: antigravity)
├── learnings/
│   ├── core/
│   │   ├── detector_patterns.md
│   │   └── autoclick_optimization.md
│   ├── ui/
│   │   ├── customtkinter_best_practices.md
│   │   └── sidebar_architecture.md
│   ├── security/
│   │   └── claude_md_protection.md
│   ├── bugs_resolved/
│   │   └── 2026_04_25_thread_freeze.md
│   └── workflows/
│       ├── bump_version_process.md
│       └── multi_ia_handoff.md
├── workflows/
│   ├── start.md                # Procédure /start généralisée
│   ├── close.md                # Procédure /close généralisée
│   └── doc.md                  # Procédure /doc généralisée
└── tasks/
    └── (TASKS/ exposés dans sidebar, v2.7.0+)
```

### Loaders

| Fichier | Rôle |
|---------|------|
| `src/core/tips_loader.py` | Scanne `src/content/tips/`, retourne liste tips (titre, contenu, catégorie) |
| `src/core/prompts_loader.py` | Scanne `src/content/prompts/`, retourne liste prompts (title, ia_target, tags, contenu) |
| `src/ui/sidebar/tab_registry.py` | Génère registry onglets depuis sous-dossiers `src/content/` |
| `src/core/tasks_loader.py` | Scanne `TASKS/`, parse frontmatter (status, assigned_to) |

---

## Handoff inter-IA (v2.6.0+)

### Format `TASKS/<id>_<slug>.md`

```markdown
---
title: Implémenter sidebar dynamique
assigned_to: claude_code  # IA actuelle
status: in_progress
handoff_from: null
created: 2026-04-25T10:00:00Z
updated: 2026-04-25T12:30:00Z
context_tokens_used: 42000
next_steps: |
  1. Terminer tab_registry.py (75% fait)
  2. Tests unitaires loaders
  3. /close avec couverture 90%+
---

## Contexte

Sidebar v2.5.0 — scanner src/content/ → onglets dynamiques.

### Fichiers modifiés
- src/ui/sidebar/tab_registry.py (draft 70%)
- tests/unit/test_tab_registry.py (stubs)

### État
- Modules scannent bien
- Rendering en cours

## Handoff à IA-B
```
assigned_to: comet
next_steps:
  1. Finir rendering (ContentView)
  2. Tests intégration
  3. Exécuter /doc audit
```

---

## Session management (v2.7.0+)

### Token budget par phase

Pour chaque IA, adapter le budget context :

| Phase | Recommandé |
|-------|-----------|
| Lire 4 organes + apprentissages | 500-800 tokens |
| Implémenter feature | 2000-3000 tokens |
| Tests (v2.5.0+) | 1000-1500 tokens |
| `/doc` audit (v2.6.0+) | 500 tokens |
| `/close` → apprentissages + commit | 300 tokens |

**Total par session** : ~5000-6500 tokens = 1-2 phases majeures/session.

### Context reset points

Entre phases majeures ou quand context ≈ 60% du max :
- IA-A → **sauve contexte dans `HANDOFF_<task_id>.md`**
- IA-B → reprend avec fichier + `/start` (recharge organes) + continue

### `HANDOFF_<task_id>.md`

Fichier créé par IA qui s'arrête pour faciliter IA suivante :

```markdown
---
handoff_from: claude_code
handoff_to: comet
date: 2026-04-25T14:00:00Z
---

## État actuels

### Fichiers modifiés/créés
- src/ui/tabs/base_tab.py ✅ (abstract Tab class)
- src/ui/tabs/markdown_tab.py 🔄 (80% renderer)
- src/ui/sidebar/sidebar_panel.py ⏳ (stub)

### Prochaine étape précise
1. Terminer markdown_tab.py (ligne 45 onwards)
2. Implémenter content_view.py (intégrer dans sidebar_panel)
3. Tests: test_markdown_tab.py

### Pièges identifiés
- CTkScrollableFrame ne supporte pas la réactivité au redimensionnement → à gérer dans layout()
- Frontmatter YAML → tester avec contenu réel (prompts + learnings)

### Contexte à charger (v2.5.0)
- ROADMAP Phase 11.1 (sidebar)
- ARCHITECTURE section "Contenus dynamiques"
- Apprentissages : core/ui_customtkinter_best_practices.md
```

---

## Tests & Couverture (v2.5.0+)

### Structure

```
tests/
├── unit/                       # Loaders, parsers, utilities
│   ├── test_loaders.py         # TipsLoader, PromptsLoader
│   ├── test_detector.py        # Image matching
│   ├── test_settings.py        # Persistance JSON
│   ├── test_doc_analyzer.py    # Audit cohérence (v2.6.0+)
│   └── ...
├── integration/                # Fluxes multi-modules
│   ├── test_sidebar.py         # TabRegistry + ContentView
│   ├── test_tasks_handoff.py   # Parse frontmatter + assignation (v2.7.0+)
│   ├── test_autoclick_flow.py  # detector → clicker → stats
│   └── ...
├── ui/                         # Composants CTk (mock Tkinter)
│   ├── test_sidebar_panel.py
│   ├── test_tabs_rendering.py
│   └── ...
└── conftest.py                 # Fixtures pytest + mocks
```

### Exigences

- **Min couverture** : 90%+ (v2.5.0+)
- **Fail `/close`** : couverture < 90%
- **Run tests** :
  ```bash
  pytest tests/ --cov=src --cov-report=html --cov-fail-under=90
  ```
- **Rapport** : `.tooling/coverage_report.py` génère synthèse

---

## Adapters multi-IA (v2.7.0+)

### Interface abstraite

```python
# src/integrations/base_adapter.py
class BaseAdapter:
    def __init__(self, project_path: str):
        self.project_path = project_path
    
    def start(self) -> dict:
        """Lance /start, retourne apprentissages chargés"""
        pass
    
    def doc(self) -> dict:
        """Lance /doc audit, retourne rapport"""
        pass
    
    def close(self, learnings: list) -> bool:
        """Exécute /close, documente apprentissages, commit"""
        pass
    
    def spawn_task(self, task_id: str) -> bool:
        """Lance IA sur TASKS/<id>_*.md"""
        pass
```

### Adapters implémentés

| Adapter | Rôle |
|---------|------|
| `claude_code.py` | Lance Claude Code via `.claude/CLAUDE.md` + script shell |
| `comet.py` | API Perplexity Comet (v2.7.0+) |
| `antigravity.py` | API Antigravity (v2.7.0+) |

---

## Décisions techniques

### Détection image — dégradation progressive

`detector.locate()` essaie backends dans l'ordre :

| Priorité | Backend | Condition |
|----------|---------|-----------|
| 1 | Custom module | Présent dans projet |
| 2 | `mss` + `cv2` | Les deux importables |
| 3 | `pyautogui` (multi-monitor) | `screeninfo` disponible |
| 4 | `pyautogui` simple | Fallback minimal |

Absence dépendance optionnelle ne bloque jamais.

### Thread daemon + threading.Event

`AutoclickService` = daemon → VM Python quitte sans rejoindre. Arrêt propre via `Event.set()` testé à chaque itération.

### Séparation UI / service

`AutoClaudeApp` = UI-only. Instancie `AutoclickService` + passes callbacks (`on_click`, `on_stop`) mis à jour via `after()`.

### Persistance paramètres

`src/config/settings.py` lit/écrit `~/.autoclaude/settings.json`. Pas de paths absolus personnels → résolution runtime via `Path.home()`.

### Content scanning

Aucun registry statique. À chaque lancement :
- `tab_registry.scan()` lit `src/content/` filesystem
- Génère onglets dynamiquement
- Ajouter `.md` = feature immédiate (zéro code)

---

## Stabilité & Observabilité

### Logging rotatif

`src/core/logger.py` → fichiers rotatifs `~/.autoclaude/logs/` (10×10MB max). Zéro logs console.

### Health Monitor

Thread daemon vérifiant chaque 60s :
- Mémoire (seuil 300MB → redémarrage)
- Processus crashed (auto-restart service)
- Log file size (rotation manuelle si limite proche)

Permet 24h+ production sans supervision.

### Stats buffering

`src/core/click_stats.py` accumule clics en mémoire (buffer 1000) puis persiste toutes les 5 min ou shutdown. Prévient perte data en crash. `AnalyticsWindow` offre graphes Récent/Tout + pagination.

### Overlay flottant

`src/ui/overlays/status_overlay.py` → Toplevel 100×60px, always-on-top, clickable (toggle autoclick), dynamique (affiche statut + count).

---

## Dépendances

| Lib | Rôle | Obligatoire | Depuis |
|-----|------|-------------|--------|
| `customtkinter` | UI mode sombre | Oui | v2.0 |
| `Pillow` | Logo PNG dans CTk | Oui | v2.0 |
| `pyautogui` | Détection + clic fallback | Oui | v1.0 |
| `pynput` | Listener clavier/souris | Oui | v1.0 |
| `matplotlib` | Graphes analyses | Oui | v2.1 |
| `psutil` | Monitoring mémoire | Oui | v2.3 |
| `opencv-python` | Template matching précis | Non | v1.0 |
| `mss` | Capture multi-moniteur | Non | v1.0 |
| `numpy` | Traitement image cv2 | Non | v1.0 |
| `screeninfo` | Énumération moniteurs | Non | v1.0 |
| `pytest` | Framework tests | Non | v2.5.0 |
| `pytest-cov` | Coverage reports | Non | v2.5.0 |
| `requests` | HTTP GitHub API | Non | v2.8.0 |
| `packaging` | Version comparison | Non | v2.8.0 |
