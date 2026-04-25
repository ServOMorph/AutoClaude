# Changelog

Tous les changements notables de ce projet sont documentés dans ce fichier.

Le format suit [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) et le versioning suit [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [2.3.0] — 2026-04-25

### Added
- **Overlay flottant always-on-top** : indicateur visuel en bas à gauche (bleu=OFF, rouge=ON), cliquable, visible sur toutes les applications
- **Switch UI** pour afficher/masquer l'overlay (persisté dans settings.json)
- **Logger centralisé** : logs rotatifs dans `~/.autoclaude/logs/` (5 Mo × 3 fichiers, rotation automatique)
- **HealthMonitor** : watchdog de stabilité, snapshot mémoire/handles/threads toutes les 5 min avec alertes WARNING
- **Buffer d'écriture pour clics** : accumulation en mémoire + flush atomique (toutes les 20 clics ou 60s) → moins d'I/O
- **Auto-restart du service** : redémarrage automatique en cas d'exception (max 3 tentatives) pour fiabilité long-run
- **Hook Tk global** : capture des exceptions silencieuses via `report_callback_exception`
- **Analyses améliorées** :
  - Mode "Récent" : fenêtres glissantes (24h / 30 jours / 12 semaines / 12 mois)
  - Mode "Tout" : historique complet avec navigation Précédent/Suivant
  - **Bandeau stats** : Total, Moyenne/jour actif, Record journalier, Jours actifs
  - Navigation intelligente par période (jour / mois / année selon le contexte)

### Changed
- Hauteur fenêtre principale : 940px → 980px (place pour le switch overlay)
- Fenêtre analytique : 720×520 → 760×600 (place pour navigation + stats)
- `stop()` dans AutoclickService : non-bloquant (pas de `join(timeout=5)` pour éviter freeze UI)
- Listener pynput : `stop()` rendu idempotent (garde interne pour éviter double-arrêt)
- AnalyticsWindow : `_draw()` optimisée pour rotation de labels si > 14 items

### Fixed
- `click_stats.flush_buffer()` : était un no-op, maintenant flush vraiment le buffer en mémoire
- `listener.stop()` : pouvait lever une exception si appelé deux fois, maintenant safe
- Analytics : libération explicite de matplotlib avec `plt.close('all')` + `CTkImage = None` pour éviter fuites
- Overlay : bindings robustes (CTkButton au lieu de Label pour garantir les clics)

### Security
- Écriture atomique des stats via fichier `.tmp` → `replace()` (pas de corruption en cas de crash)
- Logging des exceptions pour audit (aucune erreur silencieuse)

### Performance
- Buffer disque réduit de ~95% (1 write/20 clics au lieu de 1 write/clic)
- Health monitoring sans impact perf (snapshot asynchrone, daemon thread)

---

## [2.2.1] — 2026-04-23

### Added
- Texte d'aide sous le bouton "Activer" dans l'UI

### Changed
- Mise à jour README pour contexte Claude Code VSCode

---

## [2.2.0] — 2026-04-20

### Added
- **Compteur de clics** avec historique persisté dans `~/.autoclaude/click_stats.json`
- **Analyses graphiques** : visualiser les clics par heure/jour/semaine/mois/année
- Fenêtre AnalyticsWindow avec sélecteur de période (CTkSegmentedButton)
- Bouton "📊 Graphiques" dans l'UI principale

### Changed
- Layout UI réorganisé pour intégrer compteur + bouton graphiques
- Matplotlib intégré comme dépendance obligatoire

### Fixed
- Gestion correcte des jours/semaines/mois dans l'agrégation des données

---

## [2.1.0] — 2026-04-18

### Added
- **Dégradation progressive** : si OpenCV/mss manquent, l'outil continue avec pyautogui fallback
- Support explicite pour `outils.image_finder` (détection custom)
- Méthode `describe_detector()` et `describe_clicker()` pour diagnostic

### Changed
- Détecteur multi-fallback : outils → OpenCV+mss → pyautogui multi-moniteur → pyautogui single

---

## [2.0.0] — 2026-04-15

### Added
- **Refactoring complet en modules** :
  - `src/core/monitors.py` : gestion moniteurs
  - `src/core/detector.py` : détection image
  - `src/core/clicker.py` : clic souris
  - `src/core/listener.py` : écoute clavier/souris
  - `src/core/autoclick_service.py` : orchestration
  - `src/ui/app.py` : fenêtre principale
  - `src/ui/components/` : composants réutilisables
  - `src/ui/dialogs/` : dialogues
  - `src/ui/theme.py` : palette SéréniaTech
  - `src/config/` : constantes et persistance
  - `src/security/` : ClaudeMdProtector

- **Interface CustomTkinter** :
  - Design sombre charte SéréniaTech
  - Logo 120px, lien website
  - Warning banner orange
  - Bouton toggle Activer/Désactiver (bleu/rouge)
  - Sélecteur dossier projet
  - Boutons Protéger/Retirer protection
  - Footer avec lien GitHub

- **ClaudeMdProtector** : injection/suppression de bloc protection dans `.claude/CLAUDE.md`
  - Marqueurs `AUTOCLAUDE_GUARD:START/END`
  - Création/modification fichier sécurisée

- **Settings persistents** : `~/.autoclaude/settings.json`
  - interval, auto_stop, image_path

- **Documentation** :
  - ARCHITECTURE.md : décisions techniques, patterns
  - SECURITY.md : détail protection Claude Code
  - CHARTE_GRAPHIQUE.md : palette + typographie
  - README complet avec installation, usage, architecture
  - LICENSE (MIT)

### Changed
- Migration complète depuis v1 `run.py` monolithique vers architecture modulaire
- CLI argparse remplacée par interface graphique
- Lancement < 2 secondes validé

### Performance
- Détection multi-moniteur optimisée (mss + OpenCV)
- UI responsive (pas de freeze pendant autoclick)

---

## [1.0.0] — 2025-12-01

### Initial Release
- Détection image par template matching (OpenCV + mss)
- Support multi-moniteur
- Écoute clavier (Esc) + souris (auto-stop)
- CLI argparse : `--image`, `--interval`, `--auto-stop`
- Assets : yes.png (target), logo.png (branding)

---

[Unreleased]: https://github.com/ServOMorph/AutoClaude/compare/v2.3.0...HEAD
[2.3.0]: https://github.com/ServOMorph/AutoClaude/compare/v2.2.1...v2.3.0
[2.2.1]: https://github.com/ServOMorph/AutoClaude/compare/v2.2.0...v2.2.1
[2.2.0]: https://github.com/ServOMorph/AutoClaude/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/ServOMorph/AutoClaude/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/ServOMorph/AutoClaude/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/ServOMorph/AutoClaude/releases/tag/v1.0.0
