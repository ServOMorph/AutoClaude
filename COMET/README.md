# 🌌 COMET — Initialisation Perplexity

Ce dossier contient les fichiers d'initialisation pour **Perplexity via Comet**, permettant à Perplexity (autre IA) de comprendre et travailler sur le projet AutoClaude.

## 📄 Fichiers

| Fichier | Rôle | Usage |
|---------|------|-------|
| `PROMPT_PERPLEXITY.txt` | Instructions système | Charger dans Perplexity pour contextualiser |
| `ARCHITECTURE_AutoClaude.md` | Structure du projet | Référence architecture générale |
| `CODE_BUNDLE_AutoClaude.md` | Bundle code complet | Contexte complet pour Perplexity |

## 🚀 Utilisation

### Intégration Perplexity

1. **Copier le contenu** de `PROMPT_PERPLEXITY.txt`
2. **Charger dans Perplexity** comme system prompt ou contexte initial
3. **Référencer** `ARCHITECTURE_AutoClaude.md` si besoin d'architecture spécifique
4. **Utiliser** `CODE_BUNDLE_AutoClaude.md` pour accès code complet

### Avec Comet

Si tu utilises Comet (plateforme Perplexity) :
- Créer un "dossier de projet" dans Comet
- Uploader/referencer ces fichiers comme contexte persistant
- Perplexity pourra répondre sur AutoClaude avec compréhension du projet

## 🔄 Régénération

Ces fichiers sont **auto-générés**. Pas de modification manuelle recommandée.

Si besoin de mise à jour :
```bash
# Régénérer architecture
python build.py --analyze

# Copier les outputs dans COMET/
```

## 📌 Note

Ce dossier est **optionnel** mais utile pour :
- Déléguer travail à une autre IA
- Avoir un contexte persistant Perplexity/Comet
- Documenter architecture pour tiers parties

Ne pas inclure dans `.gitignore` — c'est une ressource du projet.

---

**Créé** : v2.4.0  
**Dernière update** : 2026-04-25
