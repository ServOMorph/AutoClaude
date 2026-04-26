"""Configuration debug — À modifier pour tester le comportement du compteur."""

DEBUG_COMPTEUR = True  # Mettez à True pour afficher les cercles rouges de debug au clique

# Cooldown après chaque clic (en secondes)
# Augmentez si le bouton n'a pas assez de temps pour disparaître
# Diminuez pour une détection plus rapide
COOLDOWN_DURATION = 4.0

# Seuil de confiance pour la détection d'image (0.0 à 1.0)
# Plus haut = plus strict (moins de faux positifs)
# Plus bas = plus permissif (risque de fausses détections)
# Défaut ancien: 0.8 (trop permissif sur bleu)
# Recommandé: 0.90-0.95 pour YES button strict
CONFIDENCE_THRESHOLD = 0.90
