---
title: CustomTkinter — bonnes pratiques layout et scrolling
category: ui
severity: medium
---

## CTkScrollableFrame redimensionnement

`CTkScrollableFrame` n'est pas réactif au redimensionnement de la fenêtre parent par défaut.

## Solution

Passer `fill="both", expand=True` lors du pack + fixer `width` explicitement dans le constructeur.

## Pattern

```python
# Correct
scroll = ctk.CTkScrollableFrame(parent, fg_color="transparent")
scroll.pack(fill="both", expand=True)

# Incorrect — bloque le redimensionnement
scroll = ctk.CTkScrollableFrame(parent, width=400, height=300)
scroll.pack()
```

## Fontes

- `theme.font_body()` : corps standard (12px)
- `theme.font_subtitle()` : titres sections (13px bold)
- `ctk.CTkFont(size=N, weight="bold")` : inline custom

## Piège

`pack()` et `grid()` ne peuvent pas être mixés dans le même conteneur parent.
