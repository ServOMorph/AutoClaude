# Roadmap AutoClaude v2.0 — Suivi d'avancement

> Dernière mise à jour : 2026-04-26
> Statut global : **Phase 9 (v2.3.0) terminée** — **Phase 10 (préparation merge) en cours** — Phase 11 planifiée

---

## Légende

| Symbole | Signification |
|---------|---------------|
| ✅ | Terminé |
| 🔄 | En cours |
| ⏳ | Planifié, pas encore démarré |
| ❌ | Bloqué / annulé |

---

## Statut de la v1 (base de départ)

| Fonctionnalité | Statut | Notes |
|----------------|--------|-------|
| Détection image multi-moniteur (mss + cv2) | ✅ | `run.py:104-127` |
| Détection image fallback pyautogui | ✅ | `run.py:129-162` |
| Détection image module `outils/` | ✅ | `run.py:164-182` |
| Clic pyautogui + module `outils/` | ✅ | `run.py:195-217` |
| Listener clavier Esc (pynput) | ✅ | `run.py:219-229` |
| Listener souris `--auto-stop` (pynput) | ✅ | `run.py:231-243` |
| CLI argparse (`--image`, `--interval`, `--auto-stop`) | ✅ | `run.py:336-358` |
| Gestion des moniteurs (`get_all_monitors`) | ✅ | `run.py:87-102` |
| `yes.png` template par défaut | ✅ | racine du projet |
| `Logo.png` branding SéréniaTech | ✅ | racine du projet |

---

## Phase 1 — Setup & Config ✅

> Objectif : poser la structure de fichiers et la configuration sans logique applicative.

| Tâche | Fichier cible | Statut | Notes |
|-------|--------------|--------|-------|
| 1.1 Créer arborescence `src/` + sous-dossiers | `src/` | ✅ | `core/`, `ui/components/`, `ui/dialogs/`, `security/`, `config/` |
| 1.2 Créer tous les `__init__.py` | `src/**/__init__.py` | ✅ | |
| 1.3 Déplacer assets dans `assets/` | `assets/yes.png`, `assets/logo.png` | ✅ | |
| 1.4 `src/config/constants.py` | `src/config/constants.py` | ✅ | URLs, chemins assets, couleurs hex, version, dimensions fenêtre |
| 1.5 `src/config/settings.py` | `src/config/settings.py` | ✅ | Persistance JSON dans `~/.autoclaude/settings.json` |
| 1.6 Mettre à jour `requirements.txt` | `requirements.txt` | ✅ | Ajout `customtkinter>=5.2.2`, `Pillow>=10.0.0` |
| 1.7 Créer `.gitignore` complet | `.gitignore` | ✅ | `.autoclaude/`, `__pycache__/`, `*.pyc`, etc. |

---

## Phase 2 — Core (refactoring v1) ✅

> Objectif : éclater `run.py` en modules cohérents sans casser le comportement existant.

| Tâche | Fichier cible | Statut | Notes |
|-------|--------------|--------|-------|
| 2.1 `src/core/monitors.py` | `src/core/monitors.py` | ✅ | `get_all_monitors()` |
| 2.2 `src/core/detector.py` | `src/core/detector.py` | ✅ | `locate()`, `has_detector()`, `describe_detector()` |
| 2.3 `src/core/clicker.py` | `src/core/clicker.py` | ✅ | `click()`, `has_clicker()`, `describe_clicker()` |
| 2.4 `src/core/listener.py` | `src/core/listener.py` | ✅ | Classe `InputListener` avec `threading.Event` |
| 2.5 `src/core/autoclick_service.py` | `src/core/autoclick_service.py` | ✅ | `AutoclickService.start/stop/is_running` |
| 2.6 Vérification comportement identique v1 | — | ✅ | Imports validés, 1 moniteur détecté |

### Détail `AutoclickService`

```
start()  → lance thread daemon
stop()   → signal stop_event
is_running() → bool
```

---

## Phase 3 — Sécurité ✅

> Objectif : implémenter `ClaudeMdProtector` — module indépendant, testable isolément.

| Tâche | Fichier cible | Statut | Notes |
|-------|--------------|--------|-------|
| 3.1 `src/security/claude_md_protector.py` | `src/security/claude_md_protector.py` | ✅ | Marqueurs `AUTOCLAUDE_GUARD:START/END` |
| 3.2 Méthode `apply()` | — | ✅ | Crée/modifie le fichier, ajoute `---` avant le bloc si fichier existant |
| 3.3 Méthode `is_already_protected()` | — | ✅ | Vérifie présence des marqueurs START/END |
| 3.4 Méthode `remove_protection()` | — | ✅ | Supprime le bloc entre marqueurs, efface le fichier si vide |
| 3.5 Test manuel | — | ✅ | Testé sur dossier tmp + projet réel |

---

## Phase 4 — UI Theme ✅

> Objectif : définir la charte graphique CustomTkinter avant de coder les composants.

| Tâche | Fichier cible | Statut | Notes |
|-------|--------------|--------|-------|
| 4.1 `src/ui/theme.py` | `src/ui/theme.py` | ✅ | Palette SéréniaTech → constantes CTk |
| 4.2 Validation palette couleurs | — | ✅ | bg `#1a202c`, primary `#A5C9CA`, success `#48BB78`, etc. |
| 4.3 Définition polices (Space Grotesk / fallback Segoe UI) | — | ✅ | `CTkFont` avec fallback automatique, instanciables après root |

---

## Phase 5 — Composants UI ✅

> Objectif : construire chaque composant CustomTkinter indépendamment.

| Tâche | Fichier cible | Statut | Notes |
|-------|--------------|--------|-------|
| 5.1 `src/ui/components/header.py` | `src/ui/components/header.py` | ✅ | Logo 120px + lien serenia-tech.fr + titre + slogan |
| 5.2 `src/ui/components/warning_banner.py` | `src/ui/components/warning_banner.py` | ✅ | Bordure gauche 4px orange |
| 5.3 `src/ui/components/activate_button.py` | `src/ui/components/activate_button.py` | ✅ | Toggle ON/OFF pill-shaped, dot emoji |
| 5.4 `src/ui/components/protection_button.py` | `src/ui/components/protection_button.py` | ✅ | Boutons Protéger + Retirer protection, label statut |
| 5.5 `src/ui/components/footer.py` | `src/ui/components/footer.py` | ✅ | Lien GitHub cliquable (texte simple, pas de cadre) |
| 5.6 `src/ui/dialogs/folder_picker.py` | `src/ui/dialogs/folder_picker.py` | ✅ | Wrapper `filedialog.askdirectory()` |

---

## Phase 6 — App principale ✅

> Objectif : assembler tous les composants dans la fenêtre principale.

| Tâche | Fichier cible | Statut | Notes |
|-------|--------------|--------|-------|
| 6.1 `src/ui/app.py` | `src/ui/app.py` | ✅ | Classe `AutoClaudeApp(ctk.CTk)`, 520×860px, non redimensionnable |
| 6.2 Assemblage des composants | — | ✅ | Header, warning, activate, folder picker, protection, footer |
| 6.3 Binding Esc → stop service | — | ✅ | |
| 6.4 Hook fermeture fenêtre → stop thread | — | ✅ | `protocol("WM_DELETE_WINDOW", ...)` |
| 6.5 Icône de fenêtre | — | ✅ | `assets/logo.png` via `CTk.iconbitmap` |

---

## Phase 7 — Point d'entrée ✅

> Objectif : remplacer `run.py` par un point d'entrée minimal.

| Tâche | Fichier cible | Statut | Notes |
|-------|--------------|--------|-------|
| 7.1 Réécrire `run.py` (≤10 lignes) | `run.py` | ✅ | 4 lignes |
| 7.2 Vérification lancement `python run.py` < 2s | — | ✅ | 0.56s mesuré |

---

## Phase 8 — Documentation & Publication

> Objectif : préparer la publication GitHub publique.

| Tâche | Fichier cible | Statut | Notes |
|-------|--------------|--------|-------|
| 8.1 `DOCS/ARCHITECTURE.md` | `DOCS/ARCHITECTURE.md` | ✅ | Décisions techniques, patterns, dépendances |
| 8.2 `DOCS/SECURITY.md` | `DOCS/SECURITY.md` | ✅ | Détails `ClaudeMdProtector`, bloc injecté, cas limites |
| 8.3 `DOCS/CHARTE_GRAPHIQUE.md` | `DOCS/CHARTE_GRAPHIQUE.md` | ✅ | Extraits pertinents palette + typographie |
| 8.4 Réécrire `README.md` | `README.md` | ✅ | Installation, usage, architecture |
| 8.5 Créer `LICENSE` (MIT) | `LICENSE` | ✅ | |
| 8.6 Audit secrets / chemins absolus | — | ✅ | Aucun chemin utilisateur, aucune clé |
| 8.7 `.gitignore` final | `.gitignore` | ✅ | Vérifié — complet |

---

## Critères de validation globaux

| Critère | Statut |
|---------|--------|
| `python run.py` lance en < 2 secondes | ✅ |
| Mode sombre respecté, couleurs charte appliquées | ✅ |
| Bouton Activer/Désactiver bascule correctement l'autoclick | ✅ |
| Détection et clics fonctionnent comme en v1 CLI | ✅ |
| Bouton Protection crée/modifie `.claude/CLAUDE.md` | ✅ |
| Lien `github.com/ServOMorph` s'ouvre | ✅ |
| Aucun freeze UI pendant l'autoclick | ✅ |
| Fermeture fenêtre arrête proprement le thread (pas de zombie) | ✅ |
| Touche Esc arrête l'autoclick | ✅ |
| Aucun chemin absolu personnel, aucun secret dans le code | ✅ |
| README à jour avec instructions + captures d'écran | ✅ |

---

## Phase 9 — v2.3.0 Overlay + Stabilité ✅

> Objectif : overlay flottant always-on-top + stabilité long-run (24h+ sans crash).

| Tâche | Fichier cible | Statut | Notes |
|-------|--------------|--------|-------|
| 9.1 Logger centralisé | `src/core/logger.py` | ✅ | Rotation 5 Mo × 3, `~/.autoclaude/logs/` |
| 9.2 Health Monitor | `src/core/health_monitor.py` | ✅ | Snapshot psutil toutes les 5 min, alertes RSS/handles/threads |
| 9.3 Auto-restart service | `src/core/autoclick_service.py` | ✅ | Max 3 tentatives, `stop()` non-bloquant |
| 9.4 Buffer click_stats | `src/core/click_stats.py` | ✅ | Flush atomique, réduction I/O ~95% |
| 9.5 Listener idempotence | `src/core/listener.py` | ✅ | Guard `_started` pour éviter double-démarrage |
| 9.6 Libération matplotlib | `src/ui/dialogs/analytics_window.py` | ✅ | `plt.close()` + `CTkImage = None` + destroy handler |
| 9.7 Hook Tk exception | `src/ui/app.py` | ✅ | `report_callback_exception` pour audit |
| 9.8 StatusOverlay Toplevel | `src/ui/overlays/status_overlay.py` | ✅ | Always-on-top, bas-gauche, cliquable (CTkButton) |
| 9.9 OverlayToggle switch | `src/ui/components/overlay_toggle.py` | ✅ | Persisté dans settings.json |
| 9.10 Analyses améliorées | `src/ui/dialogs/analytics_window.py` | ✅ | Mode Récent/Tout + navigation + bandeau stats |
| 9.11 Version bump 2.3.0 | `src/config/constants.py`, `pyproject.toml` | ✅ | Partout : VERSION, height, specs |
| 9.12 Build PyInstaller | `AutoClaude_v2.3.0.spec` | ✅ | Exe 120 MB, prêt distribution |
| 9.13 GitHub Release v2.3.0 | GitHub | ✅ | Exe upload, notes complet |
| 9.14 CHANGELOG complet | `CHANGELOG.md` | ✅ | v1.0.0 → v2.3.0, Keep a Changelog format |

### Critères v2.3.0

| Critère | Statut |
|---------|--------|
| Overlay visible bas-gauche, cliquable | ✅ |
| Overlay reste topmost (refresh 2s) | ✅ |
| Stop() non-bloquant < 100ms | ✅ |
| Click stats write < 20 clics | ✅ |
| Health monitor < 1% CPU | ✅ |
| Analyses Récent/Tout mode | ✅ |
| Analyses navigation Précédent/Suivant | ✅ |
| Stats banner (total, moy, record, actifs) | ✅ |
| Exe téléchargeable 120 MB | ✅ |
| Release GitHub publiée | ✅ |
| 24h test sans crash | ✅ (validé en logs) |

---

## Phase 10 — Préparation merge sur main 🔄

> Objectif : préparer le merge de la branche MAJ sur main — cohérence doc/code, tests, fixes pré-merge.

### Blocages critiques (doivent être corrigés avant merge)

| Tâche | Statut | Subtâches | Critère acceptation |
|-------|--------|-----------|-------------------|
| 10.1 Corriger `requirements.txt` — ajouter `psutil` | ⏳ | 1. Ouvrir `requirements.txt`<br/>2. Vérifier présence `psutil>=5.9.0`<br/>3. Si manquant, ajouter dans liste obligatoire<br/>4. Tester `pip install -r requirements.txt` | Installation depuis source réussit sans erreur dépendance |
| 10.2 Fixer log version (app.py:65) | ⏳ | 1. Ouvrir `src/ui/app.py` ligne 65<br/>2. Importer `VERSION` depuis `src.config.constants`<br/>3. Remplacer `APP_NAME` par `VERSION` dans le log<br/>4. Tester logs — vérifier "v2.3.0" au lieu de "vAutoClaude" | Logs affichent "v2.3.0" correctement |
| 10.3 Mettre à jour README — périodes analytics | ✅ | Corriger "Heure/Jour/Semaine/Mois/Année" → "Aujourd'hui/7j/30j/12m/Tout" + clarifier Mode Récent/Tout | README cohérent avec code |
| 10.4 Valider/clarifier Mode Récent/Tout | 🔄 | 1. Vérifier `src/ui/dialogs/analytics_window.py` — les deux modes existent-ils?<br/>2. Si oui: ✅ fonctionnalité complete<br/>3. Si non: clarifier README (retirer mentions Mode Tout si absent) | CHANGELOG et README alignés avec features présentes |

### Recommandations (avant merge idéalement)

| Tâche | Statut | Subtâches | Priorité |
|-------|--------|-----------|----------|
| 10.5 Ajouter tests unitaires | ⏳ | 1. Créer `tests/test_click_stats.py` — test `aggregate_windowed()`<br/>2. Créer `tests/test_analytics.py` — test `daily_totals` persistence<br/>3. Créer `tests/test_overlay.py` — test StatusOverlay drag et position save/load<br/>4. Exécuter `pytest` pour vérifier couverture | Tous les tests passent, couverture >70% |
| 10.6 Nettoyer TODO comments | ⏳ | 1. Grep: `grep -r "TODO" src/` → lister 74 entrées<br/>2. Remplacer docstrings génériques par descriptions spécifiques<br/>3. Identifier et supprimer les TODOs obsolètes<br/>4. Laisser seulement les vrais blocages pour futures phases | Aucun "TODO" ou "FIXME" vague dans le code |
| 10.7 Mettre à jour date README | ✅ | Changer "25 avril" → "26 avril 2026" | README affiche bonne date |
| 10.8 Harmoniser noms assets dans doc | ⏳ | 1. Vérifier fichiers réels dans `assets/` (ls -la assets/)<br/>2. Réconcilier refs dans README + docs<br/>3. Si logo.png et Icone AutoClaude.png dupliqués: garder un seul nom uniforme<br/>4. Mettre à jour toutes les refs | Nomenclature cohérente partout |

### Critères d'acceptation merge

| Critère | Statut | Notes |
|---------|--------|-------|
| Tous les bloquants (10.1–10.4) corrigés | 🔄 | 10.3 ✅, 10.4 en cours |
| Tests unitaires existants | ⏳ | Recommandé — permet CI futur |
| README cohérent avec le code | 🔄 | 10.3/10.7 ✅ |
| CHANGELOG à jour jusqu'à la date du merge | ⏳ | À finaliser lors du merge |
| Version pyproject/constants/badges synchronisées | ✅ | v2.3.0 partout |
| Pas de chemin absolu personnel dans le code | ✅ | Audit complet, aucun trouvé |
| Pas de secrets (clés, tokens) visibles | ✅ | Audit complet, aucun trouvé |

---

## Phase 11 — Post-merge : Amélioration continu ⏳

> Objectif (après merge main) : stabiliser, documenter, et préparer futures versions.

| Tâche | Statut | Objectif | Délivrables |
|-------|--------|---------|-------------|
| 11.1 Configurer CI/CD GitHub | ⏳ | Tests auto sur chaque PR, linting, couverture | `.github/workflows/tests.yml` |
| 11.2 Ajouter badges CI à README | ⏳ | Visibilité status build + couverture | Badges dans header README |
| 11.3 Audit de sécurité complet | ⏳ | Vérifier dépendances (pip audit), injections possibles | Rapport audit_security.md |
| 11.4 Documenter API interne | ⏳ | Générer docstrings valides pour Sphinx | `docs/api/` avec HTML buildable |
| 11.5 Tester sur Python 3.11 + 3.12 | ⏳ | Vérifier compatibilité declared (3.10+) | Passage tests sur 3.11 et 3.12 |
| 11.6 Support macOS basique | ⏳ | Alerter sur permissions écran, tester mouse listener | Marquer comme "expérimental macOS" |
| 11.7 Refactoring logger | ⏳ | Consolider logique version + exception hook | Moins de dépendances circulaires |
| 11.8 Release v2.4.0 | ⏳ | Bump version, CHANGELOG, exe PyInstaller | Tag + release GitHub |

### Post-merge quick wins

Réalisables rapidement si ressources disponibles après merge :
- Ajouter favicon dans la fenêtre (CTk supporte `.ico`)
- Optim mémoire : lazy-load matplotlib si analytics jamais utilisées
- Cacher périodiquement les événements click_stats (compacter JSON tous les 7j)
- Dark mode / light mode toggle dans UI (CustomTkinter supporte)

---

## Évolutions futures (backlog)

> Non planifiées — consignées pour référence après v2.4.0.

- Internationalisation FR/EN
- Personnalisation de l'image cible depuis l'UI (image picker)
- Profils multiples (images différentes selon contexte actif)
- Mode "dry-run" : détecter sans cliquer (useful pour validation avant activation)
- Raccourci global système pour activer/désactiver (sans revenir à fenêtre principale)
- Tests de performance : mesurer latence détection → clic
- Support Linux/macOS production-ready (actuellement expérimental)

---

## Historique des mises à jour

| Date | Modification |
|------|-------------|
| 2026-04-23 | Création de la roadmap — v1 complète, v2.0 planifiée |
| 2026-04-23 | Phases 1→7 complètes — UI v2.0 fonctionnelle |
| 2026-04-23 | Phase 8 complète — ARCHITECTURE, SECURITY, CHARTE_GRAPHIQUE, README, LICENSE |
| 2026-04-25 | Phase 9 complète — v2.3.0 publiée (overlay + analyses + stabilité long-run) |
| 2026-04-26 | Fixes crash long-run — cache total click_stats, pruning events 365j, _keep_on_top robuste, _on_autoclick sans lambda leak |
| 2026-04-26 | Refactoring racine du projet + analytics refactoring + Phase 10 (préparation merge) — 8 tâches bloquantes/recommandées identifiées |
| 2026-04-26 | Phase 10 expansion — README updated, ROADMAP moved to root, Phase 11 backlog + CI/CD planning |
