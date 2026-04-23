# Charte Graphique — Palette SéréniaTech

## Palette de couleurs

| Rôle | Constante | Hex | Usage |
|------|-----------|-----|-------|
| Fond principal | `COLOR_BG` | `#1a202c` | Arrière-plan fenêtre |
| Fond secondaire | `COLOR_BG_SECONDARY` | `#2d3748` | Cards, sections |
| Primaire | `COLOR_PRIMARY` | `#A5C9CA` | Accents, boutons actifs |
| Succès | `COLOR_SUCCESS` | `#48BB78` | État ON, confirmations |
| Avertissement | `COLOR_WARNING` | `#ED8936` | Bandeau warning, alertes |
| Texte | `COLOR_TEXT` | `#E2E8F0` | Corps de texte |
| Texte discret | `COLOR_TEXT_MUTED` | `#718096` | Labels secondaires |
| Bordure | `COLOR_BORDER` | `#4A5568` | Séparateurs, contours |

## Typographie

**Police préférée** : Space Grotesk  
**Fallback** : Segoe UI (Windows)

La résolution se fait à l'initialisation via `tkinter.font.families()`. Si Space Grotesk n'est pas installée sur le système, le fallback est appliqué automatiquement — aucune erreur levée.

| Style | Taille | Graisse | Fonction CTk |
|-------|--------|---------|--------------|
| Titre | 40 | bold | `theme.font_title()` |
| Sous-titre | 13 | bold | `theme.font_subtitle()` |
| Corps | 12 | normal | `theme.font_body()` |
| Icône/petit | 20 | normal | `theme.font_small()` |

> Les `CTkFont` sont instanciés dans les méthodes des widgets, jamais au niveau module — tkinter doit avoir une root active avant toute création de font.

## Fenêtre

- Dimensions : **520 × 860 px**, non redimensionnable
- Mode : **dark** (`ctk.set_appearance_mode("dark")`)
- Thème de base : `dark-blue`
- Icône : `assets/logo.png`

## Composants

| Composant | Particularité visuelle |
|-----------|----------------------|
| `WarningBanner` | Bordure gauche 4 px couleur `COLOR_WARNING` |
| `ActivateButton` | Forme pill, dot emoji, toggle ON (`COLOR_SUCCESS`) / OFF |
| `Footer` | Lien texte simple, pas de cadre visible |
| `Header` | Logo 120 px, lien `serenia-tech.fr`, titre + slogan |
