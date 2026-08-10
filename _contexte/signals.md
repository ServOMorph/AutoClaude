# Signals — autoclaude   (MAJ 2026-08-10)

## Actions ouvertes
- [P1] Confirmer sur une session longue (plusieurs heures, badges + autoclick actifs) que
  plus aucun crash access violation ne se produit (ni model_badge, ni autoclick_service/screeninfo).
  fait quand: une session de plusieurs heures se termine sans que session.lock persiste au
  prochain démarrage (pas de warning "session précédente terminée anormalement") et sans
  nouvelle entrée dans crash.log.
  réf: run.py (sentinelle session.lock, marqueur horodaté crash.log), src/core/detector.py,
  src/core/monitors.py, src/core/autoclick_service.py
- [P2] Corriger l'incohérence de version dans pyproject.toml (affiche 2.5.6 alors que
  src/config/constants.py et CHANGELOG.md sont à 2.5.12).
  fait quand: pyproject.toml affiche la même version que constants.py.
  réf: pyproject.toml, src/config/constants.py

## Contexte chaud
- Analyse de ~/.autoclaude/logs/crash.log (13 sessions v2.5.10) : le correctif tk86t.dll/
  model_badge (throttle 4s + geometry conditionnel, session 2026-07-19) tient — aucune fault
  dans model_badge.py sur ces sessions. Mais l'app a continué à crasher, cette fois dans le
  thread AutoclickWorker : double moteur de capture GDI (mss+cv2 puis pyautogui/screeninfo)
  empilés à chaque tick (0.5s), avec screeninfo interrogé en boucle serrée depuis un thread
  secondaire — signature classique de corruption mémoire différée (site de fault natif variable
  d'un crash à l'autre : screeninfo, matchTemplate, time.sleep).
- Correctif appliqué cette session (cache TTL 30s sur get_all_monitors, suppression du fallback
  pyautogui/screeninfo quand mss+cv2 disponible) mais non confirmé en conditions réelles longue
  durée — seuls les tests unitaires valident le comportement. À rouvrir si nouvelle fault dans
  crash.log malgré le correctif, y compris avec un site natif différent.

## Dernière session (2026-08-10)
Publication de la release GitHub v2.5.12 (absente jusqu'ici — seul un exe périmé v2.5.0 était
disponible). Premier build livré cassé : PyInstaller construit sans erreur bloquante même quand
une dépendance manque dans l'environnement de build (`customtkinter` absent), l'utilisateur a
eu un `ModuleNotFoundError` au lancement. Corrigé : dépendances installées (`pip install -r
requirements.txt`), rebuild propre, vérification du fichier de warnings PyInstaller (aucune
dépendance Windows manquante), test de lancement, asset remplacé sur la release existante
(`gh release upload --clobber`).

## Décisions prises
- Publication release v2.5.12 : tag git + asset `AutoClaude.exe` sur GitHub Releases.
- Procédure de build validée : toujours `pip install -r requirements.txt` avant `python
  build.py`, et contrôler `build/AutoClaude/warn-AutoClaude.txt` (grep sur les modules du
  projet) avant de publier un exe.
- Pas de bump de version (CHANGELOG/constants.py) cette session : aucun changement de code
  applicatif, uniquement publication et correction du build/release.

## Livrables produits ou modifiés
- Tag git `v2.5.12` (poussé sur origin)
- Release GitHub v2.5.12 : `AutoClaude.exe` (74 MB), fonctionnel après remplacement de l'asset
- gh CLI installé et authentifié sur la machine locale

## Hypothèses validées / invalidées
- INVALIDE : un build PyInstaller sans erreur de sortie signifie un exe fonctionnel -> faux,
  les modules manquants ne sont que des warnings non bloquants.
- VALIDE : après installation des dépendances et rebuild, l'exe se lance sans
  ModuleNotFoundError et sans dépendance Windows manquante dans les warnings.
- EN ATTENTE : le correctif crash access violation (2.5.11, cache moniteurs + suppression
  fallback) n'a toujours pas été confirmé par une session longue réelle.

## Prochaine étape exacte
Corriger l'incohérence de version pyproject.toml (2.5.6) vs constants.py (2.5.12). Puis
lancer une session longue (plusieurs heures, badges + autoclick actifs) et vérifier crash.log :
absence de nouvelle entrée toutes causes confondues (model_badge et autoclick_service).

## Question bloquante pour la session suivante
Aucune
