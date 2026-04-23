# Roadmap AutoClaude v2.0 — Suivi d'avancement

> Dernière mise à jour : 2026-04-23
> Statut global : **Phase 7 terminée** — UI fonctionnelle, Phase 8 (doc) à faire

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
| 8.1 `DOCS/ARCHITECTURE.md` | `DOCS/ARCHITECTURE.md` | ⏳ | Décisions techniques, patterns, dépendances |
| 8.2 `DOCS/SECURITY.md` | `DOCS/SECURITY.md` | ⏳ | Détails `ClaudeMdProtector`, bloc injecté, cas limites |
| 8.3 `DOCS/CHARTE_GRAPHIQUE.md` | `DOCS/CHARTE_GRAPHIQUE.md` | ⏳ | Extraits pertinents palette + typographie |
| 8.4 Réécrire `README.md` | `README.md` | ⏳ | Installation, usage, captures d'écran |
| 8.5 Créer `LICENSE` (MIT) | `LICENSE` | ⏳ | |
| 8.6 Audit secrets / chemins absolus | — | ⏳ | Aucun chemin utilisateur, aucune clé |
| 8.7 `.gitignore` final | `.gitignore` | ⏳ | Vérification avant push public |

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
| README à jour avec instructions + captures d'écran | ⏳ |

---

## Évolutions futures (hors v2.0)

> Non planifiées — consignées pour référence.

- Internationalisation FR/EN
- Personnalisation de l'image cible depuis l'UI
- Statistiques : nombre de clics, uptime
- Profils multiples (images différentes selon contexte)
- Mode "dry-run" : détecter sans cliquer
- Raccourci global système pour activer/désactiver
- Installeur Windows (.exe via PyInstaller)
- Tests automatisés (pytest)
- Support Linux/macOS (doc permissions écran macOS)

---

## Historique des mises à jour

| Date | Modification |
|------|-------------|
| 2026-04-23 | Création de la roadmap — v1 complète, v2.0 planifiée |
| 2026-04-23 | Phases 1→7 complètes — UI v2.0 fonctionnelle |
