---
title: Tips essentiels AutoClaude
category: core
---

## Détection d'image

- Image cible : `assets/yes.png` — remplace par screenshot du bouton à détecter
- Résolution : évite les screenshots flous ou redimensionnés
- Fond : le bouton doit avoir un fond visuel distinct
- Multi-moniteur : activé automatiquement si `mss` + `screeninfo` installés

## Autoclick

- Intervalle : 0.5s (défaut) — ajustable dans settings
- Auto-stop : désactive après mouvement souris (mode prudent)
- ESC : arrêt immédiat depuis n'importe quelle app
- Overlay flottant : indicateur toujours visible, clic = toggle ON/OFF

## Performance

- OpenCV + mss : détection ~40ms (optimal)
- Fallback pyautogui : ~150ms (sans dépendances optionnelles)
- Health monitor : watchdog 60s → redémarre si crash ou RAM > 300MB
