---
title: Boucle autoclick — stop_event.wait() vs time.sleep()
category: core
severity: medium
---

## Problème

La boucle autoclick utilisait `time.sleep()` bloquant → ne répondait pas aux événements d'arrêt pendant l'intervalle.

## Solution

Remplacer `time.sleep(interval)` par `stop_event.wait(timeout=interval)` pour permettre un arrêt immédiat.

## Pattern

```python
while not self._stop.is_set():
    # ... détection + clic
    self._stop.wait(timeout=self._interval)  # interruptible
```

## Piège

`time.sleep()` bloquant : ESC prend jusqu'à `interval` secondes pour prendre effet. Ne jamais l'utiliser dans des boucles avec événements d'arrêt.
