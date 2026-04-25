---
title: Tips au démarrage — bannière inline > CTkToplevel popup
domain: ui
tags: [customtkinter, tips, popup, inline, overrideredirect, windows]
severity: HIGH
created: 2026-04-25
updated: 2026-04-25
version: 2.4.0
---

## Problème

`CTkToplevel` avec `overrideredirect(True)` pour un dialog de tips cause plusieurs problèmes sur Windows :
- Taille et position incorrectes (winfo_width/height retourne 1 avant rendu complet)
- Fenêtre apparaît hors de l'écran ou trop petite
- Gestion focus/lift fragile

## Solution

Remplacer le popup par une **bannière inline** dans la fenêtre principale :
- Swap dans un container frame fixe (`_banner_slot`)
- Au démarrage : `TipsBanner` dans le slot (remplace `WarningBanner`)
- À la fermeture : `WarningBanner` réinjectée dans le slot
- Zéro CTkToplevel → zéro problème de fenêtrage

## Code pattern

```python
# Dans _build_ui()
self._banner_slot = ctk.CTkFrame(self, fg_color="transparent")
self._banner_slot.pack(fill="x", padx=20, pady=(0, 16))
self._show_banner()

def _show_banner(self):
    for w in self._banner_slot.winfo_children():
        w.destroy()
    if settings.get("show_tips_on_start"):
        TipsBanner(self._banner_slot, on_close=self._show_warning).pack(fill="x")
    else:
        self._show_warning()

def _show_warning(self):
    for w in self._banner_slot.winfo_children():
        w.destroy()
    WarningBanner(self._banner_slot, text=_WARNING_TEXT).pack(fill="x")
```

## Pièges

- `winfo_width/height()` sur le parent retourne 1 si la fenêtre n'est pas encore rendue → `update_idletasks()` nécessaire mais pas suffisant sur Windows
- `after(800, TipsDialog)` : délai arbitraire fragile selon les machines
- Pattern "slot + swap" applicable à tout widget interchangeable dans une UI
