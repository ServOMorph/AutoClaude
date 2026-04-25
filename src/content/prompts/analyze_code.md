---
title: Analyse de code
ia_target: claude_code
tags: review,quality,security
---

Analyse ce fichier :

```python
[COLLER LE CODE ICI]
```

Vérifie :
1. Sécurité (injection, exposition données, OWASP top 10)
2. Performance (N+1, boucles inutiles, mémoire)
3. SRP (1 responsabilité par fichier, max 500L)
4. Tests manquants ou insuffisants

Retourne : liste bullets, sévérité (HIGH/MEDIUM/LOW), fix suggéré.
