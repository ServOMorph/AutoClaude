---
title: pytest — Patcher des constantes importées statiquement
domain: bugs_resolved
tags: [pytest, mocking, patching, imports, content_loader]
severity: HIGH
created: 2026-04-25
updated: 2026-04-25
version: 2.4.0
---

## Problème

`monkeypatch.setattr("config.constants.CONTENT_DIR", temp_dir)` ne fonctionne pas quand le module à tester fait un import statique :

```python
# content_loader.py
from src.config.constants import CONTENT_DIR  # ← résolu à l'import
```

Le patching de la source ne change pas la variable locale déjà résolue dans le module cible.

## Solution

Patcher au point d'utilisation dans le module testé, pas à la source :

```python
# ✅ Correct — patcher dans le module qui l'utilise
with patch("src.core.content_loader.CONTENT_DIR", temp_dir):
    result = load_tips()

# ❌ Ne fonctionne pas — patche la source mais trop tard
monkeypatch.setattr("config.constants.CONTENT_DIR", temp_dir)
```

## Pièges

- `monkeypatch.setattr("module.variable")` ne fonctionne que si `module.variable` est une référence mutable (attribut d'objet ou module)
- Les constantes `Path` importées par `from ... import X` créent une copie locale → patcher la source n'affecte pas les copies
- `patch("path.to.module.CONST", value)` est la façon correcte avec `unittest.mock.patch`
- Idem pour les mocks de `Path` : `MagicMock(spec=Path)` → les attributs read-only peuvent bloquer `monkeypatch.setattr`
