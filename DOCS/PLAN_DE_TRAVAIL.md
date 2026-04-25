# PLAN DE TRAVAIL — AutoClaude v2.5.0

## Contexte

Suite à la v2.4.0 (overlay + stabilité), on va implémenter 3 fonctionnalités
majeures en une phase coordonnée. Tout repose sur un principe central :
**tout contenu est dynamique** — l'UI se construit depuis les fichiers du projet,
aucun contenu hardcodé.

---

## Fonctionnalité 1 — Auto-updater GitHub Releases

### Architecture : 2 exécutables

```
AutoClaude_v2.5.0.exe       ← App principale
AutoClaude_Updater.exe       ← Updater standalone (15-20 MB)
```

### Fichiers à créer

```
src/core/update_checker.py         ← GitHub API, comparaison versions
src/ui/components/update_button.py ← Bouton "Vérifier mises à jour"
src/ui/dialogs/update_dialog.py    ← Dialog CTk + progress, lance updater
updater/
  updater.py                        ← Standalone : download → remplace → relance
  updater_config.json               ← owner, repo, asset_name, install_dir
  AutoClaude_Updater.spec           ← PyInstaller spec updater
```

### Fichiers à modifier

```
src/config/constants.py   ← +URL_GITHUB_API
src/config/settings.py    ← +update_check_enabled (default: True)
src/ui/app.py             ← +update_button + check auto thread daemon 2s
requirements.txt          ← +requests>=2.31.0, packaging>=24.0
```

### Workflow updater

```
App démarre → Thread (2s) → GitHub API → compare VERSION
  └─ Dispo → update_dialog → OK → Popen(updater.exe) → app.quit()
               └─ Updater : download .tmp → kill app → rename → relance
```

### Gestion erreurs

- Réseau absent → silencieux (log only)
- 404 / JSON malformé → None
- Download partiel → checksum, garde .bak pour rollback
- Process qui ne quitte pas → timeout 10s + kill

### updater_config.json

```json
{
  "owner": "ServOMorph",
  "repo": "AutoClaude",
  "asset_name": "AutoClaude_v{version}.exe",
  "app_exe_name": "AutoClaude_v{version}.exe",
  "install_dir": "."
}
```

### GitHub Release format

- Tag : `v2.5.0`
- Assets : `AutoClaude_v2.5.0.exe` + `AutoClaude_Updater.exe`

---

## Fonctionnalité 2 — Tips dynamiques au démarrage

### Principe : 100% depuis fichiers

```
src/content/tips/
  core.md          ← Tips sur la détection/clic
  ui.md            ← Tips sur l'interface
  shortcuts.md     ← Tips sur les raccourcis
  updates.md       ← Tips sur les mises à jour
  # Ajouter un .md = ajouter des tips automatiquement
```

### Format d'un fichier .md de tips

```markdown
# Nom de la catégorie

## tip_id_1
**Titre du tip**
Corps du tip sur une ou plusieurs lignes.

## tip_id_2
**Autre tip**
Contenu.
```

### Fichiers à créer

```
src/content/tips/               ← Dossier de contenu (dynamique)
  core.md
  ui.md
  shortcuts.md
src/core/tips_loader.py         ← Lit tous les .md de src/content/tips/, parse
src/ui/dialogs/tips_dialog.py   ← Dialog CTkToplevel : tip aléatoire au démarrage
```

### Fichiers à modifier

```
src/config/settings.py   ← +show_tips_on_startup (default: True)
src/ui/app.py            ← Appeler tips_dialog si setting activé
```

### tips_loader.py API

```python
def load_all_tips() -> list[dict]:
    """Scanne src/content/tips/*.md, retourne list de {id, title, body, category}"""

def get_random_tip() -> dict:
    """Retourne un tip aléatoire parmi tous les .md chargés"""
```

### Scalabilité

- Ajouter un fichier .md dans `src/content/tips/` = tips disponibles immédiatement
- Aucun changement de code requis

---

## Fonctionnalité 3 — Menu latéral dynamique (Sidebar)

### Principe : UI auto-générée depuis dossiers + fichiers

```
src/content/
  tips/            ← Onglet "Tips" auto-généré
  prompts/         ← Onglet "Prompts" auto-généré
  learnings/       ← Onglet "Apprentissages" auto-généré
    core/          ← Sous-onglet "Core"
    ui/            ← Sous-onglet "UI"
    security/      ← Sous-onglet "Sécurité"
    # Ajouter un dossier = nouveau sous-onglet Apprentissages
  # Ajouter un dossier = nouvel onglet Sidebar
```

### Architecture sidebar

```
src/ui/sidebar/
  sidebar_panel.py     ← CTkFrame gauche, génère dynamiquement les boutons d'onglets
  tab_registry.py      ← Scanne src/content/, construit la registry des onglets
  content_view.py      ← Zone droite, affiche le contenu de l'onglet actif

src/ui/tabs/
  base_tab.py          ← Classe abstraite : titre, icône, render(parent) -> CTkFrame
  markdown_tab.py      ← Renderer générique : .md → CTkScrollableFrame + labels
  learning_tab.py      ← Extend base_tab : sous-onglets depuis sous-dossiers
  prompts_tab.py       ← Extend base_tab : liste prompts avec copie rapide
  tips_tab.py          ← Extend base_tab : liste tips avec filtre catégorie
```

### tab_registry.py

```python
def scan_content_dir() -> list[TabConfig]:
    """
    Scanne src/content/. Pour chaque dossier :
      - Crée un TabConfig(name=dossier, icon=dossier/icon.png si dispo, tab_class=...)
      - Associe la classe d'onglet selon le nom (learnings→LearningTab, prompts→PromptsTab...)
      - Fallback : MarkdownTab pour tout dossier inconnu
    """
```

### Sidebar dynamique

```python
# sidebar_panel.py
def build_nav(registry: list[TabConfig]):
    """Pour chaque onglet en registry : crée un CTkButton dans le nav gauche"""

def refresh():
    """Rescanne + rebuild nav (appelé si contenu modifié)"""
```

### Format learning (sous-onglets par dossier)

```
src/content/learnings/
  core/
    detector.md
    clicker.md
  ui/
    theme.md
    components.md
  security/
    claude_md_protector.md
```

→ Onglet "Apprentissages" → TabView avec onglets "Core", "UI", "Sécurité"
→ Ajouter dossier `tests/` → onglet "Tests" apparaît automatiquement

### Format prompts

```
src/content/prompts/
  debug.md         ← Prompts de debug
  features.md      ← Prompts de dev
  analysis.md      ← Prompts d'analyse
```

→ Liste affichée avec bouton "Copier" à droite de chaque prompt

---

## Contrainte transversale : tout dynamique

**Règle** : Aucun contenu (tips, prompts, apprentissages) hardcodé dans le code.
Tout est lu depuis `src/content/`. Ajouter un fichier = fonctionnalité dispo.

Patterns imposés :
- Loaders : scannent dossiers, pas de liste statique
- UI : se reconstruit depuis la registry, pas de widgets hardcodés
- Settings : driven par fichiers de config JSON, pas de constantes UI

---

## Fichiers à modifier dans CLAUDE.md

```
## Architecture dynamique (OBLIGATOIRE)

- Tout contenu (tips, prompts, apprentissages) : dans src/content/
- Ajouter un fichier .md = contenu disponible immédiatement, sans code
- Ajouter un dossier dans src/content/ = nouvel onglet Sidebar
- Loaders : toujours scanner les dossiers, jamais de liste statique
- UI : générée depuis fichiers/registry, jamais hardcodée
```

---

## Intégration dans REFACTOR_PLAN.md

Ajouter **Phase 7** (après Phase 6 / commit) :

```markdown
## Phase 7 : Fonctionnalités majeures v2.5.0 (3-4j)

### 7.1 — Auto-updater (1j)
Checklist des fichiers à créer/modifier (voir PLAN_DE_TRAVAIL.md #1)

### 7.2 — Tips dynamiques au démarrage (0.5j)
Checklist + créer src/content/tips/ avec fichiers .md initiaux

### 7.3 — Sidebar + menu dynamique (1.5j)
Checklist + créer src/content/ architecture + loaders + sidebar

### 7.4 — Mise à jour CLAUDE.md (0.25j)
Contrainte "tout dynamique" + section Architecture dynamique
```

---

## Dépendances à ajouter

```
requests>=2.31.0    ← auto-updater
packaging>=24.0     ← comparaison versions
mistune>=3.0.0      ← parsing Markdown pour tips/prompts/learnings (optionnel)
```

---

## Vérification

1. Auto-updater : mock release v2.4.1 → app v2.4.0 voit la mise à jour
2. Tips : ajouter `src/content/tips/test.md` → tip apparaît au démarrage
3. Sidebar : ajouter `src/content/custom/` → onglet "Custom" apparaît dans sidebar
4. Learning : ajouter `src/content/learnings/tests/` → sous-onglet "Tests" auto
