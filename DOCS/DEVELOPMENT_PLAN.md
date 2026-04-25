# Plan de développement — AutoClaude v2.0

> Transformation du script mono-fichier en application desktop moderne avec UI CustomTkinter, respectant la charte graphique SéréniaTech (mode sombre), avec gestion de la sécurité projet via CLAUDE.md.

---

## Vue d'ensemble

AutoClaude v2.0 est une application desktop qui automatise les clics sur un bouton "Yes" détecté à l'écran, pensée pour aider à valider automatiquement les prompts de Claude Code. L'application ajoute une couche de sécurité en permettant à l'utilisateur d'injecter des restrictions dans le fichier `.claude/CLAUDE.md` de son projet, afin d'empêcher Claude Code de modifier des fichiers en dehors du périmètre projet.

### Objectifs principaux

- Passer d'un script CLI mono-fichier à une application GUI structurée
- Proposer une interface moderne en mode sombre (charte SéréniaTech)
- Séparer proprement les responsabilités (UI / core / sécurité / config)
- Préparer le projet pour une publication GitHub publique
- Ajouter un module de protection automatique via `.claude/CLAUDE.md`

---

## Nouvelle structure du projet

```
AutoClaude/
├── run.py                          # Point d'entrée (lance l'UI)
├── requirements.txt                # Dépendances mises à jour (+ customtkinter, Pillow)
├── README.md                       # Doc utilisateur
├── LICENSE                         # MIT (projet public)
├── .gitignore
│
├── src/                            # Code source
│   ├── __init__.py
│   │
│   ├── core/                       # Logique métier (ancien run.py éclaté)
│   │   ├── __init__.py
│   │   ├── detector.py             # Détection d'image (mss, cv2, pyautogui)
│   │   ├── clicker.py              # Gestion des clics
│   │   ├── monitors.py             # Multi-écran (screeninfo, mss)
│   │   ├── listener.py             # Écoute clavier/souris (pynput)
│   │   └── autoclick_service.py    # Orchestrateur (start/stop, thread)
│   │
│   ├── ui/                         # Interface CustomTkinter
│   │   ├── __init__.py
│   │   ├── app.py                  # Classe principale CTk
│   │   ├── theme.py                # Couleurs/fonts SéréniaTech
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── header.py           # Logo + titre + liens
│   │   │   ├── activate_button.py  # Bouton Activer/Désactiver
│   │   │   ├── protection_button.py # Bouton Protection
│   │   │   ├── warning_banner.py   # Mention d'avertissement
│   │   │   └── footer.py           # Liens site + GitHub
│   │   └── dialogs/
│   │       ├── __init__.py
│   │       └── folder_picker.py    # Wrapper filedialog
│   │
│   ├── security/                   # Module sécurité
│   │   ├── __init__.py
│   │   └── claude_md_protector.py  # Ajoute restrictions dans CLAUDE.md
│   │
│   └── config/                     # Configuration
│       ├── __init__.py
│       ├── constants.py            # Chemins, defaults, URLs
│       └── settings.py             # Persistance (JSON dans ~/.autoclaude)
│
├── assets/                         # Ressources
│   ├── yes.png                     # Template de détection
│   └── logo.png                    # Logo SéréniaTech (placeholder si absent)
│
├── DOCS/                           # Documentation dev
│   ├── DEVELOPMENT_PLAN.md         # Ce plan
│   ├── ARCHITECTURE.md             # Décisions techniques
│   ├── SECURITY.md                 # Détails de la protection CLAUDE.md
│   └── CHARTE_GRAPHIQUE.md         # Extraits pertinents pour devs
│
└── tests/                          # Tests (optionnel v1)
    └── __init__.py
```

---

## Design (Mode sombre harmonieux)

### Palette

Inspirée de la charte graphique SéréniaTech, adaptée au mode sombre :

| Rôle | Couleur | Hex |
|------|---------|-----|
| Fond principal | bg-dark | `#1a202c` |
| Fond secondaire | bg-alt-dark | `#2d3748` |
| Fond tertiaire | bg-dark-3 | `#4a5568` |
| Accent primary | Primary | `#A5C9CA` |
| Accent hover | Primary Light | `#B9DDDE` |
| Accent action | Primary Dark | `#7DA1A2` |
| Texte principal | text-dark | `#e2e8f0` |
| Texte secondaire | text-muted-dark | `#cbd5e0` |
| Success (activé) | Success | `#48BB78` |
| Warning (bannière) | Warning | `#ED8936` |
| Error (désactivé) | Error | `#F56565` |

### Typographie

- **Titres** : Space Grotesk (fallback : Segoe UI)
- **Corps** : Inter (fallback : Segoe UI)
- Chargement via `customtkinter.CTkFont`

### Fenêtre principale

- Dimensions : 520 × 640 px
- Non redimensionnable (`resizable(False, False)`)
- Bords arrondis modernes (CustomTkinter gère cela automatiquement)
- Icône de fenêtre : logo SéréniaTech

---

## Composants UI détaillés

### 1. Header

- Logo SéréniaTech (80 px de haut) centré
- **Titre** : `AutoClaude` — Space Grotesk 3xl (30px), bold, Primary Light
- Lien cliquable : `https://serenia-tech.fr` (ouvre navigateur via `webbrowser.open`)
- Slogan discret : *"L'innovation au service de votre sérénité numérique"*

### 2. Warning Banner

Carte orange (Warning) avec icône d'avertissement :

```
⚠️ Attention : si vous utilisez cet outil, pensez à ajouter dans
.claude/CLAUDE.md de votre projet l'interdiction de sortir du dossier.
Utilisez le bouton Protection ci-dessous pour le faire automatiquement.
```

- Fond : `#ED8936` à 15% d'opacité
- Bordure gauche : 4 px solid `#ED8936`
- Texte : `#e2e8f0`

### 3. Activate Button (toggle)

| État | Label | Couleur | Action |
|------|-------|---------|--------|
| OFF | `▶ Activer` | `#48BB78` (Success) | Démarre `AutoclickService` |
| ON | `■ Désactiver` | `#F56565` (Error) | Arrête `AutoclickService` |

- Forme : pill-shaped (border-radius élevé)
- Padding généreux (16 × 32)
- Petit indicateur d'état à côté (dot vert/rouge)
- Le service tourne dans un thread daemon pour ne pas geler l'UI

### 4. Protection Button

- Label : `🛡 Configurer la protection projet`
- Style secondary : fond transparent, bordure Primary, texte Primary Light
- Action au clic :
  1. Ouvre `filedialog.askdirectory()` pour choisir le dossier projet
  2. Valide que le chemin existe
  3. Appelle `ClaudeMdProtector.apply(project_path)`
  4. Affiche un toast/dialog de succès ou d'erreur

### 5. Footer

- 🌐 [serenia-tech.fr](https://serenia-tech.fr) (cliquable)
- 💻 [github.com/ServOMorph](https://github.com/ServOMorph) (cliquable)
- Mention version : `v2.0` en très petit, texte muted
- Liens : Primary Light, underline on hover

---

## Module Sécurité : `ClaudeMdProtector`

**Emplacement** : `src/security/claude_md_protector.py`

### Logique

1. Reçoit `project_path` (dossier sélectionné par l'utilisateur)
2. Crée `.claude/` s'il n'existe pas (`Path.mkdir(exist_ok=True)`)
3. Ouvre `.claude/CLAUDE.md` (crée si absent)
4. Vérifie la présence du bloc de restriction via marqueurs :
   - `<!-- AUTOCLAUDE_GUARD_START -->`
   - `<!-- AUTOCLAUDE_GUARD_END -->`
5. Si absent : ajoute le bloc à la fin du fichier
6. Si présent : propose de le remplacer (confirmation UI)

### Bloc injecté

```markdown
<!-- AUTOCLAUDE_GUARD_START -->
## Restrictions de sécurité (injectées par AutoClaude)

**Périmètre strict** : Tu ne dois JAMAIS lire, modifier, créer ou supprimer
des fichiers en dehors de ce dossier projet (`{project_path}`).

Interdictions absolues :
- Accès aux dossiers système (`C:\Windows`, `/etc`, `/usr`, etc.)
- Accès aux dossiers utilisateur autres que le projet (Documents, Desktop...)
- Exécution de commandes affectant des chemins hors projet
- Utilisation de chemins absolus pointant ailleurs
- Symlinks ou `..` pour échapper au périmètre

Toute opération doit utiliser des chemins relatifs à la racine du projet.

Injecté par AutoClaude v2.0 — https://serenia-tech.fr
<!-- AUTOCLAUDE_GUARD_END -->
```

### API

```python
class ClaudeMdProtector:
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.claude_dir = project_path / ".claude"
        self.claude_md = self.claude_dir / "CLAUDE.md"

    def apply(self) -> tuple[bool, str]:
        """Retourne (success, message)."""

    def is_already_protected(self) -> bool:
        """Vérifie la présence du bloc."""

    def remove_protection(self) -> bool:
        """Supprime le bloc (pour maintenance)."""
```

---

## Refactoring du code existant

### `run.py` actuel → éclaté en

| Ancien emplacement | Nouveau fichier | Responsabilité |
|--------------------|-----------------|----------------|
| `locate_image_*` | `src/core/detector.py` | Détection d'image (chaîne de fallbacks) |
| `click_*` | `src/core/clicker.py` | Exécution des clics |
| `get_all_monitors` | `src/core/monitors.py` | Énumération multi-écran |
| `on_press`, `on_mouse_move` | `src/core/listener.py` | Callbacks clavier/souris |
| boucle `main()` | `src/core/autoclick_service.py` | Orchestration + threading |

### Nouveau `run.py` (racine, 10 lignes max)

```python
"""AutoClaude - Point d'entrée principal."""
from src.ui.app import AutoClaudeApp


def main():
    app = AutoClaudeApp()
    app.mainloop()


if __name__ == "__main__":
    main()
```

### `AutoclickService`

Classe avec cycle de vie propre :

```python
class AutoclickService:
    def __init__(self, image_path: Path, poll_interval: float = 0.5):
        ...

    def start(self) -> None:
        """Lance la détection dans un thread daemon."""

    def stop(self) -> None:
        """Arrête proprement le thread via Event."""

    def is_running(self) -> bool:
        ...
```

---

## Dépendances ajoutées

`requirements.txt` mis à jour :

```
# Dépendances principales
pyautogui>=0.9.53
pynput>=1.7.6

# Interface graphique
customtkinter>=5.2.2
Pillow>=10.0.0

# Optionnel : meilleure détection multi-écran et performance
mss>=9.0.1
opencv-python>=4.8.0
numpy>=1.24.0
screeninfo>=0.8.1
```

---

## Étapes d'implémentation

1. **Setup structure** : créer l'arborescence + tous les `__init__.py`
2. **Config** : `src/config/constants.py` (URLs, chemins assets, couleurs hex)
3. **Theme** : `src/ui/theme.py` (mapping charte → CustomTkinter)
4. **Core refacto** : éclater le `run.py` actuel en 5 modules `core/`
5. **Service** : implémenter `AutoclickService` threadé
6. **Security** : implémenter `ClaudeMdProtector` + tests manuels
7. **UI components** : header, warning, activate_button, protection_button, footer
8. **Dialogs** : `folder_picker.py` (wrapper `filedialog.askdirectory`)
9. **App** : assemblage dans `AutoClaudeApp(ctk.CTk)`
10. **run.py** : point d'entrée minimal
11. **Docs** : finaliser `ARCHITECTURE.md`, `SECURITY.md`, `CHARTE_GRAPHIQUE.md`
12. **README** : réécriture pour publication publique (captures d'écran)
13. **Cleanup** : `.gitignore`, `LICENSE` (MIT), vérif secrets

---

## Points d'attention

- **Threading** : l'autoclick DOIT tourner hors du thread UI. Utiliser `threading.Thread(daemon=True)` et un `threading.Event` pour l'arrêt propre.
- **Arrêt propre** : flag `stop_event` partagé entre service et UI. Vérifier qu'à la fermeture de la fenêtre, le thread s'arrête bien.
- **Chemin image** : `assets/yes.png` résolu dynamiquement via `Path(__file__).parent.parent / "assets" / "yes.png"`.
- **Logo manquant** : fallback texte si `assets/logo.png` absent (ne pas crasher).
- **Fonts CustomTkinter** : vérifier que Space Grotesk/Inter sont installées sinon fallback automatique à "Segoe UI".
- **Public GitHub** : aucun chemin utilisateur en dur, aucune clé/secret, pas de chemin absolu Windows-only.
- **Pynput sur Linux** : nécessite `python3-tk` et un serveur X (non bloquant pour v1 Windows-first).
- **Permission écran** : sur macOS, nécessite l'autorisation "Enregistrement d'écran" (documenter dans README).

---

## Critères de validation

- [ ] L'app lance avec `python run.py` en moins de 2 secondes
- [ ] Mode sombre respecté, couleurs de la charte appliquées
- [ ] Bouton Activer/Désactiver bascule correctement l'autoclick
- [ ] Détection et clics fonctionnent comme dans la v1 CLI
- [ ] Bouton Protection modifie/crée bien `.claude/CLAUDE.md` dans le dossier choisi
- [ ] Les liens `serenia-tech.fr` et `github.com/ServOMorph` s'ouvrent dans le navigateur
- [ ] Aucun freeze de l'UI pendant l'autoclick
- [ ] Fermeture de fenêtre arrête proprement le thread (pas de zombie)
- [ ] La touche Esc arrête l'autoclick (comportement conservé de v1)
- [ ] Structure prête pour publication GitHub publique (pas de chemins absolus personnels)
- [ ] README à jour avec instructions d'installation et captures d'écran

---

## Évolutions futures (hors v2.0)

- Internationalisation (FR/EN)
- Personnalisation de l'image cible depuis l'UI
- Statistiques : nombre de clics, uptime
- Profils multiples (images différentes selon le contexte)
- Mode "dry-run" : détecter sans cliquer (debug)
- Raccourci global système pour activer/désactiver
- Installeur Windows (.exe via PyInstaller)
- Tests automatisés (pytest)

---
K
*Document rédigé le 2026-04-23 — AutoClaude v2.0*
