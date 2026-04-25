---
title: CTkLabel bind(<Button-1>) non fiable sur Windows avec overrideredirect
domain: bugs_resolved
tags: [customtkinter, windows, overlay, click, overrideredirect]
severity: HIGH
created: 2026-04-25
updated: 2026-04-25
version: 2.4.0
---

## Problème

`CTkLabel.bind("<Button-1>", handler)` ne déclenche pas systématiquement le handler sur Windows quand la fenêtre a `overrideredirect(True)`.

Le clic atterrit sur le widget interne `tk.Label` (encapsulé dans le Frame CTkLabel) qui ne propage pas l'événement au parent Frame. Résultat : l'overlay semblait non-cliquable en état OFF.

## Solution

Remplacer `CTkLabel` + `bind()` par `CTkButton` avec `fg_color="transparent"` et `command=handler`. Le `command=` de CTkButton est natif Tkinter et fiable dans tous les contextes.

## Code pattern

```python
# ❌ Non fiable sur Windows + overrideredirect
label = ctk.CTkLabel(self, text="● OFF")
label.bind("<Button-1>", self._handle_click)

# ✅ Fiable
btn = ctk.CTkButton(
    self, text="● OFF",
    fg_color="transparent",
    hover_color="#ffffff22",
    corner_radius=0,
    border_width=0,
    command=self._handle_click,
)
```

## Pièges

- `self.bind("<Button-1>", ...)` sur le Toplevel fonctionne parfois mais pas toujours avec `overrideredirect(True)` sur Windows
- Ne pas swallow les exceptions dans le handler (`except: pass`) — masque les vrais bugs
- CTkButton supporte `configure(text=...)` comme CTkLabel → drop-in replacement
