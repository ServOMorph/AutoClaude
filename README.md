# AutoClaude — Automatiseur de clics GUI

Script Python qui détecte et clique automatiquement sur un bouton spécifique apparaissant à l'écran.

## Utilisation

### Installation

```bash
# Installation minimale (pyautogui seul)
pip install pyautogui pynput

# Installation complète (meilleure détection multi-écran)
pip install -r requirements.txt
```

### Exécution basique

```bash
# Utilise yes.png dans le répertoire courant par défaut
python run.py
```

### Options CLI

```bash
# Spécifier un autre chemin d'image
python run.py --image /chemin/vers/image.png

# Configurer l'intervalle de polling (en secondes)
python run.py --interval 1.0

# Arrêt au premier mouvement souris/clavier (sauf Esc)
python run.py --auto-stop
```

### Variables d'environnement

```bash
# Configurer le chemin par défaut
export AUTOCLAUDE_IMAGE_PATH=/chemin/vers/yes.png
python run.py
```

## Fonctionnalités

- ✅ Détection d'image par template matching
- ✅ Gestion multi-écran
- ✅ Fallbacks automatiques (pyautogui, opencv, mss)
- ✅ Arrêt sécurisé (Esc, Ctrl+C, mouvement souris)
- ✅ Logs clairs et informatifs

## Arrêt

- **Esc** : Arrête le script
- **Ctrl+C** : Arrête le script
- **Mouvement souris** (si `--auto-stop`) : Arrête le script

## Architecture

Le script utilise un pattern de **dégradation progressive** :

1. **Priorité 1** : Module custom `outils/image_finder` (si disponible)
2. **Priorité 2** : OpenCV + mss (haute précision, multi-écran)
3. **Priorité 3** : screeninfo + pyautogui
4. **Priorité 4** : pyautogui seul (fallback minimal)

Chaque méthode est testée indépendamment. L'absence d'une dépendance optionnelle ne bloque jamais l'exécution.

## Dépendances

### Obligatoires
- `pyautogui` : Détection et clic d'image
- `pynput` : Écoute clavier/souris

### Optionnelles
- `opencv-python` : Meilleure détection par template matching
- `mss` : Capture d'écran multi-moniteur
- `numpy` : Traitement d'images (dépendance d'OpenCV)
- `screeninfo` : Énumération des moniteurs

## Exemples

```bash
# Détecter et cliquer sur yes.png toutes les 0.5s
python run.py

# Utiliser une image personnalisée, arrêter au premier mouvement
python run.py --image button.png --auto-stop

# Intervalle plus court (100ms)
python run.py --interval 0.1
```

## Cas d'usage

- Automatisation de validations répétitives
- Tests UI automatisés
- Workflows d'acceptation de popups
- Tâches d'interaction GUI sans API

## Notes

- L'image `yes.png` doit être en format PNG/JPG/BMP
- Les coordonnées détectées sont le centre de l'image
- Tous les fallbacks sont testés silencieusement (logs seulement au démarrage)
