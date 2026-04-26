# Changelog

Toutes les modifications notables de **AutoClaude** sont documentées dans ce fichier.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [Unreleased] — branche MAJ

### Corrigé

- **Crash long-run** : cache `_total_on_disk` en mémoire pour éviter la relecture JSON à chaque clic ; pruning des événements au-delà de 365j ; `_keep_on_top` s'arrête proprement si widget détruit (`winfo_exists()`), skip si masqué
- **Détection échouée après premier clic** : état hover du bouton empêchant la re-détection — `move_away()` utilise maintenant un déplacement relatif <50px au lieu d'absolu vers (5,5)
- **Interval=150s sauvegardé** : `settings.json` avait `interval: 150` ce qui ralentissait la détection à 2,5 min — resetté à 0,5s par défaut
- **Lien GitHub** : URL mise à jour vers `https://github.com/ServOMorph/AutoClaude` (était juste `/ServOMorph`)

### Modifié

- **OverlayToggle** : déplacé dans l'UI sous le bouton Activer (avant c'était avant le compteur)
- **Lambda leak dans `_on_autoclick`** : refactorisé pour déléguer à `_refresh_click_ui()` au lieu de créer un lambda par clic

### Ajouté

- **Analytics fenêtrées** : remplacement des 5 périodes vagues (heure/jour/semaine/mois/année) par 5 vues temporelles précises — Aujourd'hui (heure), 7j (jour), 30j (jour), 12m (mois), Tout (année)
- **`daily_totals` persistés** : dict `{"YYYY-MM-DD": count}` stocké dans click_stats.json, jamais purgé — permet l'historique multi-année même si les événements bruts sont limités à 365j
- **Bandeau de statistiques** : dans la fenêtre analyses — Total, Moy/jour actif, Record, Jours actifs
- **Bouton Fermer** : dans la fenêtre analyses (en plus de la croix)

---

## [2.3.0] — 2026-04-25

### Ajouté

- **Overlay flottant always-on-top** (`StatusOverlay`) en bas-gauche, cliquable pour activer/désactiver autoclick sans revenir à la fenêtre principale
- **Overlay draggable** avec persistance de la position (`overlay_x`, `overlay_y` dans settings.json)
- **OverlayToggle** : switch dans l'UI pour afficher/masquer l'overlay
- **Analytics améliorées** : 5 périodes (heure/jour/semaine/mois/année), modes Récent/Tout, navigation Précédent/Suivant (pagination par jour/mois/année), stats chiffrées (total, moy, record, jours actifs), graphes avec labels lisibles
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
