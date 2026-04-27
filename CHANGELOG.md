# Changelog

Toutes les modifications notables de **AutoClaude** sont documentées dans ce fichier.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Unreleased]

### Corrigé

### Ajouté

---

## [2.4.6] — 2026-04-27

### Corrigé

- **FlashIndicator CTkToplevel crash** : changé en `tk.Toplevel` pur pour éviter les erreurs RGBA (`#ffffff22`) sur systèmes où customtkinter échoue. `DEBUG_COMPTEUR=True` fonctionne maintenant sans crash.

---

## [2.4.5] — 2026-04-27

### Corrigé

- **Crash long-run (sessions de plusieurs heures)** : suite de fixes ciblés sur l'accumulation de ressources Win32/GDI :
  - **`FlashIndicator` réutilisable** : un seul `CTkToplevel` partagé pour tous les flashs au lieu d'en créer/détruire un par clic. Évite la fuite progressive de HWND et de références dans `AppearanceModeTracker`/`ScalingTracker` de customtkinter sur sessions longues.
  - **`_keep_on_top` paresseux** : ne fait plus d'appel `lift()`/`-topmost` quand l'overlay est masqué (`winfo_viewable()`), et passe l'intervalle de 2s → 5s. Économise des milliers d'appels Win32 inutiles par session.
  - **Instance `mss` persistante** : le détecteur partage une seule instance MSS au lieu d'en allouer/désallouer une à chaque détection (toutes les 0.5s). Évite la fragmentation du pool de GDI handles. En cas d'erreur, l'instance est jetée et recréée au prochain appel.
  - **`gc.collect()` périodique** : forcé toutes les 5min par le HealthMonitor. Tk/customtkinter laissent traîner des références circulaires (callbacks `after`, widget→master) que le GC cyclique de Python ne récupère pas immédiatement.
  - **Polling 1s du compteur supprimé** : `ClickCounter._schedule_refresh` était redondant (déjà rafraîchi par `_refresh_click_ui` après chaque clic). Économise 3600 appels `after()` par heure.

---

## [2.4.4] — 2026-04-26

### Corrigé

- **Debug circle timing** : cercle rouge dessiné AVANT le clic au lieu d'après. Permet de vérifier visuellement la position cible avant exécution du clic.

---

## [2.4.3] — 2026-04-26

### Ajouté

- **Configuration fine-tuning** : variables `CONFIDENCE_THRESHOLD`, `PRE_CLICK_DELAY`, `COOLDOWN_DURATION`, `DEBUG_COMPTEUR` maintenant tuneables dans `config.py` sans toucher au code
- **Documentation des problèmes connus** : guide complet pour comptage imprécis, faux positifs, non-détection avec solutions

### Modifié

- **Detection strictness configurable** : `CONFIDENCE_THRESHOLD` (défaut 0.90) remplace hardcoded 0.8, réduit faux positifs sur bleu
- **Pre-click stabilization** : ajouté `PRE_CLICK_DELAY` (défaut 1.0s) après détection avant clic, assure bouton prêt
- **README expansion** : tableau de config, troubleshooting, exemples pratiques

---

## [2.4.2] — 2026-04-26

### Corrigé

- **Re-clic fantôme après disparition du bouton** : le bouton s'affichait encore pendant la boucle suivante et était re-cliqué à une position désormais vide. Ajouté cooldown de 3 secondes après chaque clic — pendant ce délai, la détection est ignorée. Permet au bouton de complètement disparaître avant relance de la détection.

---

## [2.4.1] — 2026-04-26

### Corrigé

- **Double-click bug — sleep duration insufficient** : v2.4.0 utilisait `sleep(1.0)` post-clic, mais Claude Code met >1.2s à traiter et fermer le bouton. Augmenté à `sleep(2.0)`. Root cause validée en production : 1.0s = button still visible, detected again → 2nd click on stale position.

---

## [2.4.0] — 2026-04-26

### Corrigé

- **Double-click bug** : compteur comptait 2x les clics — `sleep(0.4)` après clic insuffisant pour laisser bouton disparaître. Passé à `sleep(1.0)` post-clic. Root cause: 0.4s sleep + 280ms locate() = 680ms, but button stays visible >700ms
- **Crash long-run** : cache `_total_on_disk` en mémoire pour éviter la relecture JSON à chaque clic ; pruning des événements au-delà de 365j ; `_keep_on_top` s'arrête proprement si widget détruit (`winfo_exists()`)
- **Détection échouée après premier clic** : état hover du bouton empêchant la re-détection — `move_away()` utilise maintenant un déplacement relatif <50px
- **Interval=150s sauvegardé** : `settings.json` avait `interval: 150` ce qui ralentissait la détection — resetté à 0,5s par défaut
- **Lien GitHub** : URL mise à jour vers `https://github.com/ServOMorph/AutoClaude`
- **Version logging** : logs affichaient "vAutoClaude" au lieu de "v2.4.0" — importé VERSION constant correctement

### Ajouté

- **Tests unitaires** : 42 tests (`test_click_stats.py` 12 tests + `test_status_overlay.py` 9 tests), isolation via fixture tmp_path
- **Analytics fenêtrées** : 5 vues temporelles — Aujourd'hui, 7j, 30j, 12m, Tout
- **`daily_totals` persistés** : dict multi-année dans click_stats.json, jamais purgé
- **Bandeau de statistiques** : Total, Moy/jour actif, Record, Jours actifs
- **Bouton Fermer** : dans la fenêtre analyses

### Modifié

- **requirements.txt** : psutil ajouté (dépendance obligatoire Health Monitor)
- **ROADMAP.md** : déplacé de DOCS/ → racine, Phase 10-11 expansion documentée
- **README.md** : analytics périodes correctes, date mise à jour, assets harmonisés
- **OverlayToggle** : déplacé sous le bouton Activer
- **Lambda leak** : refactorisé `_on_autoclick` pour éviter lambdas par clic

---

## [2.3.0] — 2026-04-25

### Ajouté

- **Overlay flottant always-on-top** (`StatusOverlay`) en bas-gauche, cliquable pour activer/désactiver autoclick sans revenir à la fenêtre principale
- **Overlay draggable** avec persistance de la position (`overlay_x`, `overlay_y` dans settings.json)
- **OverlayToggle** : switch dans l'UI pour afficher/masquer l'overlay
- **Analytics améliorées** : sélecteur 5 périodes (Aujourd'hui/7j/30j/12m/Tout), stats chiffrées (total, moyenne, record, jours actifs), graphes avec labels lisibles et couleurs hiérarchisées
- **Logger centralisé** (`src/core/logger.py`) : rotation 5 Mo × 3 fichiers dans `~/.autoclaude/logs/`
- **Health Monitor** (`src/core/health_monitor.py`) : snapshot psutil toutes les 5 min (RSS, handles, threads), alertes si dépassement seuils
- **Auto-restart service** (`_run_with_restart`) : jusqu'à 3 tentatives de redémarrage sur exception inattendue
- **Buffer click_stats** : flush every 20 clics ou 60s (I/O −95% vs read-write à chaque clic)
- **Listener idempotence** : guard `_started` pour éviter double-démarrage (`InputListener.start()`)
- **Hook `report_callback_exception`** : log audit des exceptions Tk silencieuses au lieu de crash
- **Libération matplotlib** : `plt.close()` + `CTkImage = None` + handler destroy à la fermeture analytics
- **PyInstaller build** : `AutoClaude_v2.3.0.exe` (120 Mo), release GitHub, notes complètes

---

## [2.0.0] — 2026-04-23

### Ajouté

- **Architecture modulaire** : `src/core/` (détection, clic, listener, service), `src/ui/` (app, composants, dialogs, overlays), `src/security/` (ClaudeMdProtector), `src/config/` (constantes, settings)
- **Interface CustomTkinter** : mode sombre, charte graphique SéréniaTech (couleurs, typographie)
- **Composants UI** : Header (logo + lien website), WarningBanner, ActivateButton (pill-shaped toggle), ProtectionButton (Protéger/Retirer), ClickCounter (compteur + reset), Footer
- **ClaudeMdProtector** : injection de restrictions dans `.claude/CLAUDE.md` du projet sélectionné (marqueurs `AUTOCLAUDE_GUARD:START/END`)
- **Persistance settings** : fichier JSON `~/.autoclaude/settings.json` pour interval, auto_stop, overlay_x/y, etc.
- **Compteur de clics** : affichage temps réel + reset confirm dialog
- **Point d'entrée minimal** : `run.py` réduit à 4 lignes (import + mainloop)

### Modifié

- **Refactoring v1** : `run.py` monolith éclaté en modules cohérents (core + ui + security)

---

## [1.0.0] — 2026-04-23

Version initiale — CLI-based autoclick tool.

### Ajouté

- **Détection d'image** : template matching multi-moniteur via mss + OpenCV, fallback pyautogui
- **Clic automatique** : pyautogui.click + module `outils/` (integration avec custom scripts)
- **Input listeners** : clavier ESC (pynput) pour arrêt, souris `--auto-stop` (déplacement > 50px)
- **CLI argparse** : flags `--image`, `--interval`, `--auto-stop`
- **Gestion moniteurs** : `get_all_monitors()` pour multi-écran

---

[Unreleased]: https://github.com/ServOMorph/AutoClaude/compare/v2.3.0...HEAD
[2.3.0]: https://github.com/ServOMorph/AutoClaude/compare/v2.0.0...v2.3.0
[2.0.0]: https://github.com/ServOMorph/AutoClaude/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/ServOMorph/AutoClaude/releases/tag/v1.0.0
