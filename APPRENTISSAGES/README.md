# 📚 Système d'apprentissage AutoClaude

Répertoire centralisé pour documenter patterns, bugs résolus et workflows découverts.

## Structure

```
APPRENTISSAGES/
├── meta.json              ← Index centralisé (version, count, tags)
├── core/                  ← Patterns : détection, clic, listener
├── ui/                    ← Patterns : CustomTkinter, theme, components
├── security/              ← Sécurité : protection, permissions
├── bugs_resolved/         ← Bugs résolus (datés)
└── workflows/             ← Workflows : versioning, build, update
```

## Cycle d'apprentissage

### 📖 Chargement (`/start`)
1. startV2.md charge apprentissages pertinents depuis APPRENTISSAGES/
2. Sélectionne TOP 5-7 docs (HIGH severity + domaine détecté)
3. Intègre dans contexte des prompts (max 3000 tokens)

### 📝 Documentation (`/close`)
1. Si bug résolu ou pattern découvert :
   - Créer `APPRENTISSAGES/<domain>/<topic>.md`
   - Ajouter métadonnées : title, domain, tags, severity, created
   - Mettre à jour `meta.json` : incrementer count, ajouter dans by_severity
2. Format compact (< 500 tokens, réutilisable)

## Format d'un apprentissage

```markdown
---
title: "Détection d'image multi-moniteur avec OpenCV"
domain: "core"
tags: ["detection", "opencv", "mss", "performance"]
severity: "high"
created: "2024-04-25"
updated: "2024-04-25"
version: "v2.4.0"
---

## Problème

Détection inefficace sur multi-moniteur avec OpenCV seul.

## Solution

Combiner mss (capture rapide) + cv2 (template matching).
- OpenCV seul : 400ms
- mss + cv2 : 100ms (4x plus rapide)

## Code pattern

\`\`\`python
import mss
import cv2

def locate(image_path, threshold=0.8):
    with mss.mss() as sct:
        for monitor in sct.monitors[1:]:
            screenshot = sct.grab(monitor)
            # ... cv2.matchTemplate
\`\`\`

## Pièges à éviter

- ❌ Charger image à chaque itération (I/O)
- ❌ Seuil trop bas (faux positifs) ou haut (missed detections)
- ✅ Mettre en cache l'image
- ✅ Seuil 0.8 pour balance
```

## Domaines

| Domaine | Sévérité | Exemples |
|---------|----------|----------|
| **core** | HIGH | Détection multi-moniteur, clic fiable, listener idempotent |
| **ui** | MEDIUM | CustomTkinter patterns, theme system, component architecture |
| **security** | HIGH | CLAUDE.md protection, file permissions, path handling |
| **bugs_resolved** | VARIES | Thread freeze (HIGH), API rate limit (MEDIUM), etc. |
| **workflows** | MEDIUM | Bump version automation, auto-updater, PyInstaller |

## Sévérité

- **HIGH** : Critical patterns / bugs that caused issues
- **MEDIUM** : Useful patterns / good practices learned
- **LOW** : Optional tips / nice-to-know facts

## Meta.json

Fichier index (petit, toujours chargé) pour filtrage rapide :
- `version` : version du projet (comparé au /start)
- `domains` : count par domaine
- `by_severity` : liste fichiers (permet de charger TOP N sans scanner)

## Scalabilité

- ✅ Ajouter `.md` = apprentissage auto-découvrable
- ✅ Meta.json = filtrage rapide, pas de scan disque complet
- ✅ Limite tokens (max 3000) → contexte pas saturé
- ✅ Compact (< 500 tokens/doc) → réutilisable

## Bonnes pratiques

- ✅ Documenter **après résolution** (pattern frais, contexte clair)
- ✅ Inclure **code patterns** (réutilisable immédiatement)
- ✅ Lister **pièges** (évite mêmes erreurs futures)
- ✅ Limiter à **un topic par fichier** (focalisé, testable)
- ❌ Ne pas mélanger plusieurs bugs dans un doc
- ❌ Ne pas laisser apprentissage "en brouillon"

---

Voir `.claude/CLAUDE.md` section "Système d'apprentissage" pour les détails d'intégration.
