# AutoClaude

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Tests](https://github.com/ServOMorph/AutoClaude/actions/workflows/tests.yml/badge.svg)](https://github.com/ServOMorph/AutoClaude/actions/workflows/tests.yml)
[![Version](https://img.shields.io/badge/version-2.4.0-blue.svg)](https://github.com/ServOMorph/AutoClaude/releases)

> **Centre de commande multi-IA** — orchestrez Claude Code, Comet, Antigravity et d'autres LLM sur un seul projet avec un workflow unifié, des contenus dynamiques et un système de handoff automatisé.

AutoClaude offre une interface graphique CustomTkinter (mode sombre) pour :
- **Gérer plusieurs IA** via adapters (`/start` `/close` `/doc` identiques pour tous)
- **Détecter et cliquer** automatiquement sur boutons récurrents (Claude Code, confirmation utilisateur)
- **Partager prompts/tips/learnings** : bibliothèque centralisée, scannable, extensible
- **Suivre tâches** entre IA (handoff automatisé, assignation, historique)
- **Auditer cohérence** doc avec `/doc` (multi-LLM compliance, propositions d'amélioration)

> Développé par [SéréniaTech](https://serenia-tech.fr) · [GitHub](https://github.com/ServOMorph)

---

## 🚀 Fonctionnalités

### Core
- **Détection d'image par template matching** (OpenCV + mss, fallback pyautogui)
- **Support multi-moniteur** → adaptation seamless
- **Dégradation progressive** : absence dépendance optionnelle = app continue

### Automation
- **Autoclick** : détecte + clique boutons récurrents Claude Code
- **Overlay flottant** : indicateur always-on-top (on/off), contrôlable depuis n'importe quelle app
- **Arrêt sécurisé** : Esc, fermeture fenêtre, mouvement souris (auto-stop mode)

### Multi-IA (v2.5.0+)
- **Workflow IA-agnostique** : `/start` `/close` `/doc` `/bump_version` identiques pour Claude Code, Comet, Antigravity
- **Adapters** : traduction syntaxe LLM cible ↔ workflow unifié
- **Handoff automatisé** : IA-A → IA-B via `TASKS/<id>.md` (frontmatter : status, assignation, contexte)
- **Session management** : token budget par phase, context reset points, `HANDOFF_*` entre agents

### Contenu dynamique (v2.5.0+)
- **Sidebar centrale** : onglets auto-générés depuis `src/content/{tips,prompts,learnings,workflows}/`
- **Bibliothèque prompts** : copie rapide, partageable inter-IA
- **Tips** : affichage startup + onglet sidebar, extensible sans code
- **Learnings** : sous-dossiers auto-générés (core, ui, security, bugs_resolved, workflows)

### Analyse & qualité (v2.6.0+)
- **Commande `/doc`** : audit cohérence README/ROADMAP/ARCHITECTURE/WORKFLOW
- **Vérification multi-LLM** : détecte si doc est adaptée orchestration multi-IA
- **Propositions améliorations** : rapport audit, fail `/close` si warnings majeurs
- **Couverture tests** : 90%+ depuis v2.5.0, audit avant chaque release

### Opérations
- **Compteur de clics** : historique persisté, analyses graphiques (Récent/Tout, par heure/jour/semaine/mois/année)
- **Logs rotatifs** : `~/.autoclaude/logs/` (rotation auto 10×10MB)
- **Health monitor** : watchdog stabilité 24h+, redémarrage auto, gestion mémoire
- **Protections Claude Code** : injection restrictions `.claude/CLAUDE.md` (sécurité projet)
- **Bump version auto** : `/bump_version` met à jour VERSION + CHANGELOG + tous fichiers références
- **Système d'apprentissage** : `APPRENTISSAGES/` inter-sessions, max 5-7 docs par session (3000 tokens)

---

## 📥 Installation

### Option 1 : Exécutable Windows (simplest)

Télécharge `AutoClaude_v2.4.0.exe` depuis les [releases](https://github.com/ServOMorph/AutoClaude/releases) et double-clique. Aucune dépendance Python requise.

### Option 2 : Depuis le code source

```bash
# Cloner le dépôt
git clone https://github.com/ServOMorph/AutoClaude.git
cd AutoClaude

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python run.py
```

### Dépendances (installation depuis source)

**Obligatoires**

| Package | Rôle |
|---------|------|
| `pyautogui` | Détection et clic d'image (fallback) |
| `pynput` | Écoute clavier/souris |
| `customtkinter` | Interface graphique |
| `Pillow` | Affichage des images |
| `matplotlib` | Graphes d'analyse |
| `psutil` | Monitoring mémoire/stabilité |

**Optionnelles** (meilleures performances)

| Package | Rôle |
|---------|------|
| `opencv-python` | Template matching haute précision |
| `mss` | Capture multi-moniteur rapide |
| `numpy` | Traitement d'image (requis OpenCV) |
| `screeninfo` | Énumération des moniteurs |
| `requests` | HTTP GitHub API (auto-updater v2.8.0+) |
| `packaging` | Version comparison (auto-updater v2.8.0+) |

---

## 🖥️ Interface

![AutoClaude UI](assets/ui-screenshot.png)

---

## 📖 Utilisation

```bash
# Lancer l'interface graphique
python run.py
```

### Fonctionnalités UI

1. **Activer/désactiver autoclick** — bouton bleu/rouge central
2. **Sélectionner projet** — dossier à protéger
3. **Protéger/retirer protection** — injecter restrictions `CLAUDE.md`
4. **Compteur clics** — affichage temps réel + reset
5. **Analyses graphiques** — navigation Récent/Tout, stats chiffrées, tendances
6. **Overlay flottant** — toggle ON/OFF depuis n'importe quelle app
7. **Sidebar dynamique** (v2.5.0+) — onglets tips/prompts/learnings + recherche

### Indicateur flottant

Petit badge en bas à gauche de l'écran, toujours au-dessus :
- 🔵 **Bleu — AutoClaude OFF** : autoclick inactif
- 🔴 **Rouge — AutoClaude ON** : autoclick actif

Clic → bascule ON/OFF sans revenir fenêtre principale.

### Analyses

- **5 périodes** : Heure, Jour, Semaine, Mois, Année
- **Mode Récent** (défaut) : fenêtre glissante 24h/30j/12 semaines/12 mois
- **Mode Tout** : historique complet, pagination
- **Stats** : total, moyenne/jour actif, record, jours actifs

### Arrêt

- Touche **Esc** — arrête autoclick
- **Fermeture fenêtre** — arrêt propre du thread
- **Mouvement souris** — si mode auto-stop actif

---

## 🎯 Image cible

Par défaut, AutoClaude cherche `assets/yes.png`. Remplace ce fichier par un screenshot du bouton à automatiser (PNG, JPG, BMP).

---

## 🔐 Protection Claude Code

Le bouton **Protéger** injecte un bloc de restrictions dans `.claude/CLAUDE.md` du projet sélectionné. Ce bloc est lu par Claude Code au démarrage et contraint le comportement IA au périmètre du projet.

Voir [DOCS/SECURITY.md](DOCS/SECURITY.md) pour détails.

---

## 🤝 Organes de communication entre IA

AutoClaude utilise **4 fichiers à la racine** comme source de vérité unique pour toute IA collaborant sur le projet (Claude Code, Perplexity/Comet, Antigravity, etc.) :

| Fichier | Rôle | Public |
|---------|------|--------|
| **[README.md](README.md)** | Vue d'ensemble : mission, features, usage | Utilisateurs + IA |
| **[ROADMAP.md](ROADMAP.md)** | Phases, statuts, priorités, versions | IA + contributeurs |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | Structure technique, décisions, dépendances | IA + développeurs |
| **[WORKFLOW.md](WORKFLOW.md)** | Cycle `/start` `/close` `/doc` IA-agnostique | Tous les adapters IA |

### Workflow unifié

```
/start
  ├─ Lire 4 organes (README/ROADMAP/ARCHITECTURE/WORKFLOW)
  └─ Charger apprentissages (APPRENTISSAGES/meta.json)

Travail
  ├─ Implémenter selon ROADMAP
  └─ Tests (v2.5.0+)

/doc (avant /close — v2.6.0+)
  ├─ Analyser cohérence 4 organes
  ├─ Vérifier multi-LLM compliance
  └─ Proposer fixes

/close
  ├─ Documenter apprentissages (APPRENTISSAGES/)
  ├─ Commit message normalisé
  └─ Tag version
```

Tout IA (Claude Code, Comet, Antigravity) suit le même workflow. Les adapters (`.claude/`, `.comet/`, `.antigravity/`) traduisent vers syntaxe LLM cible.

### 📚 Système d'apprentissage inter-sessions

[APPRENTISSAGES/](APPRENTISSAGES/) stocke la mémoire accumulée entre sessions IA :
- **Format** : fichiers `.md` avec métadonnées (domain, severity, tags)
- **Domains** : core, ui, security, bugs_resolved, workflows
- **Sélection** : max 5-7 docs HIGH/MEDIUM par session (3000 tokens)
- **Cycle** : `/start` charge → travail → `/close` documente si nouveau

Voir [APPRENTISSAGES/README.md](APPRENTISSAGES/README.md).

### 🗃️ Archives & historique

[ARCHIVES/](ARCHIVES/) conserve fichiers obsolètes avec index searchable :
- **Catégories** : docs_legacy, specs_pyinstaller, tooling_artifacts, old_builds
- **Métadonnées** : reason, tags, recall_when
- **Recherche** : `python .tooling/archive_search.py <query>`

Rien n'est perdu. Voir [ARCHIVES/README.md](ARCHIVES/README.md).

---

## Logs & stabilité

AutoClaude est conçu pour tourner en continu. Logs disponibles dans `~/.autoclaude/logs/autoclaude.log` (rotation auto, 5 Mo × 3 fichiers). En cas de crash, consultez ce fichier en priorité.

---

## Architecture générale

```
src/core/       détection, clic, listener, autoclick_service, logger, health monitor, /doc analyzer
src/ui/         CustomTkinter app, composants, dialogs, overlays, sidebar dynamique
src/integrations/ adapters Claude Code, Comet, Antigravity (v2.7.0+)
src/config/     constantes, persistance JSON, settings
src/content/    source unique : tips/, prompts/, learnings/, tasks/, workflows/
assets/         yes.png (target), logo.png
.claude/        CLAUDE.md (directives), commandes (/start, /close, /doc, /bump_version)
APPRENTISSAGES/ système d'apprentissage inter-sessions
TASKS/          tâches inter-IA + handoff (v2.6.0+)
ARCHIVES/       fichiers obsolètes + index
```

Voir [ARCHITECTURE.md](ARCHITECTURE.md) pour détails techniques.

---

## 🌌 Intégration multi-IA — Comet, Antigravity, etc.

AutoClaude peut être orchestré par plusieurs IA via adapters standardisés.

### Workflow multi-IA

1. **IA-A (Claude Code)** : lit README/ROADMAP/ARCHITECTURE/WORKFLOW → exécute `/start` → travaille → `/doc` audit → `/close`
2. **IA-B (Comet)** : reprend via `HANDOFF_<task_id>.md` → mêmes 4 organes → mêmes commandes (syntaxe adaptée) → handoff à IA-C
3. **IA-C (Antigravity)** : continue, tâche escalade si nécessaire

**Advantage** : une seule source de vérité, cycle unifié, continuité garantie.

Voir [WORKFLOW.md](WORKFLOW.md) pour détails. Adapters spécifiques dans `.claude/`, `.comet/`, `.antigravity/`.

---

## 🧪 Tests & Qualité

À partir de **v2.5.0** :
- **Couverture tests** : minimum 90%+ (fail `/close` si <90%)
- **Audit `/doc`** : avant chaque commit (v2.6.0+), propositions automatiques

Exécuter tests :
```bash
pytest tests/ --cov=src --cov-report=html
```

---

## Licence

MIT — voir [LICENSE](LICENSE)

---

Projet réalisé par ServOMorph avec Claude Code pour SérénIA Tech :
https://serenia-tech.fr/

Date : 25 avril 2026 (v2.4.0)

---

## Contribuer

Les contributions sont les bienvenues ! Consulter [CONTRIBUTING.md](CONTRIBUTING.md) pour démarrer.
