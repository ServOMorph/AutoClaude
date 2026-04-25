---
name: dynamic-content
description: "Dynamic content architecture for AutoClaude. Use when: implementing content loaders (tips, prompts, learnings), creating filesystem-driven UI components, building sidebar registries, implementing markdown parsing from src/content/, extending content types without code changes. DO NOT USE: for hardcoding UI content, creating static content lists."
applyTo: ["src/content/**/*.md", "src/ui/sidebar/**/*.py", "src/ui/tabs/**/*.py"]
---

# Dynamic Content Architecture — AutoClaude v2.5.0+

> **Principe** : Tout contenu depuis \\src/content/\\ — aucun hardcodé. UI auto-générée.

Zéro : \\	ips = [{'id': '...', 'title': '...'}]\\
Oui : \\def load_all_tips() -> list\\

---

## Structure src/content/

\\\
src/content/
├── tips/                        # Tips startup + sidebar
│   ├── getting_started.md
│   ├── best_practices.md
│   └── troubleshooting.md
├── prompts/                     # Bibliothèque prompts inter-IA
│   ├── code_review.md
│   ├── documentation.md
│   └── optimization.md
├── learnings/                   # Auto-apprentissages (sous-dossiers domains)
│   ├── core/
│   ├── ui/
│   └── security/
├── workflows/                   # Workflows réutilisables (v2.6.0+)
│   └── session_management.md
└── tasks/                       # Tâches assignées IA (v2.7.0+)
    └── TASKS/
\\\

---

## Frontmatter format

Tous .md avec optional frontmatter YAML (optional si pas de metadata) :

\\\yaml
---
title: Titre complet
domain: core|ui|security|bugs_resolved|workflows
tags: [tag1, tag2, tag3]
severity: HIGH|MEDIUM|LOW    # Pour learnings uniquement
created: 2026-04-25
updated: 2026-04-25
version: 2.4.0
---

# Contenu markdown ci-dessous
\\\

---

## Loaders pattern

Créer \\src/content/loaders/*.py\\ :

\\\python
\"\"\"Loaders pour src/content/ — scan FS, retour data structures.\"\"\"
from pathlib import Path
from typing import List, Dict

def load_all_tips() -> List[Dict]:
    \"\"\"Scan src/content/tips/*.md, retourne liste structures.\"\"\"
    content_dir = Path(__file__).parent / "tips"
    tips = []
    
    for md_file in content_dir.glob("*.md"):
        data = parse_frontmatter(md_file)
        tips.append({
            "id": md_file.stem,
            "title": data.get("title", md_file.stem.replace("_", " ")),
            "tags": data.get("tags", []),
            "content": md_file.read_text(encoding="utf-8"),
        })
    
    return tips

def parse_frontmatter(path: Path) -> Dict:
    \"\"\"Parse YAML frontmatter si présent, sinon retourne {}.\"\"\"
    import yaml
    text = path.read_text(encoding="utf-8")
    
    if text.startswith("---"):
        # Extrait section entre --- markers
        parts = text.split("---", 2)
        if len(parts) >= 2:
            try:
                return yaml.safe_load(parts[1]) or {}
            except:
                return {}
    
    return {}
\\\

---

## UI Components pattern

UI composants consomment loaders :

\\\python
\"\"\"src/ui/tabs/tips_tab.py — affiche tips dynamiquement.\"\"\"
from src.content.loaders import load_all_tips
import customtkinter as ctk

class TipsTab(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Charger depuis filesystem
        self.tips = load_all_tips()
        
        # Générer UI
        for tip in self.tips:
            self.add_tip_widget(tip)
    
    def add_tip_widget(self, tip_data):
        label = ctk.CTkLabel(
            self,
            text=tip_data['title'],
            text_color='white'
        )
        label.pack(padx=10, pady=5)
\\\

---

## Sidebar Registry pattern

Tab registry auto-génère depuis sous-dossiers :

\\\python
\"\"\"src/ui/sidebar/tab_registry.py — génère registry depuis structure.\"\"\"
from pathlib import Path

def build_registry() -> Dict:
    \"\"\"Scan src/content/, retourne registry onglets.\"\"\"
    content_dir = Path(__file__).parent.parent.parent / "content"
    
    registry = {}
    
    # Parcourir domaines
    for domain_dir in (content_dir / "learnings").iterdir():
        if domain_dir.is_dir():
            registry[f"learnings_{domain_dir.name}"] = {
                "label": domain_dir.name.replace("_", " ").title(),
                "icon": "📚",
                "path": domain_dir,
            }
    
    return registry
\\\

---

## Anti-patterns

❌ \\	ips_list = [{"id": "intro", "title": "Introduction", ...}]\\

✅ \\	ips = load_all_tips()\\ (scan FS)

❌ Hardcoder sidebar onglets dans app.py

✅ Générer depuis tab_registry.build_registry()

❌ Copier contenu .md multiple endroits

✅ Source unique src/content/, loaders partagés

---

## Extension patterns

Ajouter nouveau type contenu = **ajouter .md fichier** :

`
src/content/templates/        # ← Nouveau type
├── email_draft.md
├── pr_template.md
└── issue_template.md
`

Créer loader :

\\\python
def load_all_templates() -> List[Dict]:
    template_dir = Path(__file__).parent / "templates"
    return [
        {
            "name": f.stem,
            "content": f.read_text(),
            "meta": parse_frontmatter(f)
        }
        for f in template_dir.glob("*.md")
    ]
\\\

UI auto-adapt sans modifications ! 

---

## Checklist implémentation

- [ ] Loaders dans src/content/loaders/*.py
- [ ] Frontmatter YAML parsable (optionnel)
- [ ] UI composants consomment loaders
- [ ] Tab registry généré depuis FS
- [ ] Ajouter .md = feature (extensibilité)
- [ ] Tests 90%+ couverture loaders
- [ ] Zero hardcoding contenu UI
