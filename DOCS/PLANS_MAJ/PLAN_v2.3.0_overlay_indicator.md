# Plan v2.3.0 — Overlay d'état autoclick global + Stabilité

> Branche cible : `V2.3.0`
> Base : `main` (v2.2.1)
> Date rédaction : 2026-04-24

---

## 1. Objectifs

### 1.1 Overlay d'état autoclick

Ajouter un **indicateur visuel flottant** affiché :

- En bas à gauche de l'écran
- **Toujours au-dessus de toutes les fenêtres** (always-on-top)
- **Visible sur tous les bureaux virtuels Windows** (tous les espaces de travail)
- Reflétant en temps réel l'état ON/OFF de l'autoclick

L'utilisateur doit pouvoir **activer/désactiver l'affichage** de cet overlay depuis l'UI principale (un switch dans la fenêtre AutoClaude). Le choix est **persisté** dans `settings.json`.

### 1.2 Stabilité long-run (critique)

**Problème constaté** : l'application **crashe au bout d'un long moment de fonctionnement** (plusieurs heures d'autoclick continu).

**Objectif v2.3.0** : identifier la cause racine et garantir une stabilité de **24h+ sans crash ni fuite mémoire**. Voir la Phase 8 dédiée ci-dessous.

---

## 2. Contraintes techniques

| Contrainte | Solution retenue |
|-----------|------------------|
| Always-on-top | `Toplevel.attributes("-topmost", True)` (Tk natif) |
| Sans bordure / sans décoration | `Toplevel.overrideredirect(True)` |
| Transparence partielle | `Toplevel.attributes("-alpha", 0.85)` |
| Visible sur tous les bureaux virtuels Windows | **Win32 API** via `ctypes` — `SetWindowPos` + `WS_EX_TOOLWINDOW` + `WS_EX_TOPMOST`. Pour l'affichage cross-desktop, utiliser `IVirtualDesktopManager` (COM) pour « épingler » la fenêtre (ou fallback : re-topmost périodique via `after`) |
| Pas de clic-through (l'overlay doit rester cliquable pour toggle rapide) | Par défaut cliquable. Option configurable `overlay_click_through` (fallback future) |
| Monitor cible (le principal) | `winfo_screenwidth()` / `winfo_screenheight()` pour positionner bas-gauche du moniteur principal |
| Aucun freeze UI | `Toplevel` géré dans le même thread Tk que `AutoClaudeApp` — rafraîchissement via `after()` |

### Notes cross-desktop Windows

Windows 10/11 : pour qu'une fenêtre apparaisse sur **tous** les bureaux virtuels, il faut interroger l'API COM `IVirtualDesktopManager` (`MoveWindowToDesktop` n'est pas suffisant — il faut marquer la fenêtre comme « partagée »). Plusieurs approches :

1. **Approche minimale (recommandée v2.3.0)** — ne pas gérer explicitement les bureaux virtuels. Une fenêtre `topmost` sans bordure apparaît sur le bureau où elle a été créée uniquement. **Documenter la limitation** et fournir un fallback : recréer la fenêtre sur le bureau actif via une écoute de focus global (phase 2).
2. **Approche avancée (v2.3.1 ou plus tard)** — utiliser `pyvda` (package Python `virtual-desktop-accessor`) pour épingler la fenêtre à tous les bureaux. Ajoute une dépendance optionnelle.

**Décision v2.3.0** : implémenter l'approche 1 (simple `topmost`), et ajouter dans le plan futur l'approche 2 si le besoin se confirme à l'usage.

---

## 3. Arborescence cible (diff)

```
src/
├── ui/
│   ├── components/
│   │   ├── overlay_toggle.py          [NOUVEAU] switch on/off dans l'UI principale
│   │   └── ...
│   ├── overlays/                      [NOUVEAU dossier]
│   │   ├── __init__.py
│   │   └── status_overlay.py          [NOUVEAU] fenêtre Toplevel flottante
│   └── app.py                         [MODIFIÉ] instancie l'overlay, bind on_toggle
├── config/
│   └── constants.py                   [MODIFIÉ] constantes overlay (taille, offset, couleurs)
```

Aucune nouvelle dépendance externe en v2.3.0 (Tk natif suffit).

---

## 4. Découpage par phases

### Phase 1 — Configuration (pré-requis)

**Fichier** : `src/config/constants.py`

Ajouter :
```python
# Overlay
OVERLAY_WIDTH = 180
OVERLAY_HEIGHT = 44
OVERLAY_MARGIN = 16            # distance aux bords de l'écran
OVERLAY_ALPHA = 0.9
OVERLAY_COLOR_ACTIVE = "#E53838"     # rouge (aligné ActivateButton)
OVERLAY_COLOR_INACTIVE = "#3886E5"   # bleu (aligné ActivateButton)
OVERLAY_TEXT_COLOR = "#FFFFFF"
```

**Fichier** : `src/config/settings.py`

Ajouter dans `_DEFAULTS` :
```python
"overlay_enabled": True,
```

**Critère de validation** : `settings.get("overlay_enabled")` retourne `True` par défaut, et la valeur persistée dans `~/.autoclaude/settings.json` quand modifiée.

---

### Phase 2 — Overlay Toplevel (fenêtre flottante)

**Fichier** : `src/ui/overlays/__init__.py` (vide)

**Fichier** : `src/ui/overlays/status_overlay.py`

Classe `StatusOverlay(ctk.CTkToplevel)` :

**Responsabilités** :
- Création d'une fenêtre sans bordure, topmost, semi-transparente
- Positionnement bas-gauche du moniteur principal (via `winfo_screenwidth/height`)
- Label affichant l'état : `"● AutoClaude OFF"` (bleu) / `"● AutoClaude ON"` (rouge)
- Méthode `set_active(state: bool)` appelée depuis `app.py`
- Méthode `show()` / `hide()` pour l'activation/désactivation
- Méthode `destroy_overlay()` sur fermeture app
- Clic sur l'overlay → callback optionnel `on_click` (pour toggler l'autoclick directement — QOL)
- Drag déplacement (optionnel v2.3.0 — garder simple) : **non implémenté**, position figée

**API** :
```python
class StatusOverlay(ctk.CTkToplevel):
    def __init__(self, master, on_click: callable = None): ...
    def set_active(self, state: bool) -> None: ...
    def show(self) -> None: ...
    def hide(self) -> None: ...
```

**Détails d'implémentation** :
- `self.overrideredirect(True)` → pas de barre de titre
- `self.attributes("-topmost", True)` → toujours au-dessus
- `self.attributes("-alpha", OVERLAY_ALPHA)` → transparence
- Re-application périodique de `-topmost` via `self.after(2000, self._keep_on_top)` pour contrer le vol de focus par certaines apps
- `self.attributes("-toolwindow", True)` (Windows uniquement) → n'apparaît pas dans Alt+Tab ni dans la barre des tâches

**Piège connu** (mémoire CTkFont) : instancier `CTkFont` **dans la méthode widget**, jamais au module-level.

**Critère de validation** :
- L'overlay apparaît bas-gauche du moniteur principal
- Reste visible au-dessus du navigateur / VSCode
- `set_active(True)` change la couleur en rouge + texte "ON"
- `hide()` rend la fenêtre invisible, `show()` la rétablit

---

### Phase 3 — Switch UI dans la fenêtre principale

**Fichier** : `src/ui/components/overlay_toggle.py`

Classe `OverlayToggle(ctk.CTkFrame)` :
- Un `CTkSwitch` libellé **"Afficher l'indicateur flottant"**
- État initial lu depuis `settings.get("overlay_enabled")`
- `on_change(enabled: bool)` → callback passé par `AutoClaudeApp`
- Persiste automatiquement via `settings.set("overlay_enabled", enabled)`

**Intégration** dans `src/ui/app.py` :
- Placer le switch sous le `row` compteur/graphiques, avant `quit_btn`
- Callback `_on_overlay_toggle(enabled)` → `self._overlay.show()` ou `self._overlay.hide()`

**Critère de validation** :
- Toggle le switch → l'overlay apparaît/disparaît instantanément
- Fermer puis rouvrir l'app → l'état est restauré depuis `settings.json`

---

### Phase 4 — Intégration dans `AutoClaudeApp`

**Fichier** : `src/ui/app.py`

Modifications :

1. Import : `from src.ui.overlays.status_overlay import StatusOverlay`
2. Dans `__init__` (après `_build_ui`) :
   ```python
   self._overlay = StatusOverlay(self, on_click=self._activate_btn._toggle)
   if settings.get("overlay_enabled"):
       self._overlay.show()
   else:
       self._overlay.hide()
   ```
3. Dans `_on_toggle(active)` → relayer à l'overlay :
   ```python
   self._overlay.set_active(active)
   ```
4. Dans `_on_service_stopped` :
   ```python
   self.after(0, lambda: (self._activate_btn.set_active(False), self._overlay.set_active(False)))
   ```
5. Dans `_on_close` → `self._overlay.destroy()` avant `self.destroy()`

**Critère de validation** :
- Activer l'autoclick via l'UI → overlay passe rouge "ON"
- Appui Esc → overlay repasse bleu "OFF"
- Clic sur l'overlay → toggle l'autoclick (raccourci)

---

### Phase 5 — Ajustement hauteur fenêtre principale

La hauteur actuelle (`WINDOW_HEIGHT = 940`) peut nécessiter un ajustement mineur pour intégrer le switch sans compression visuelle.

**Fichier** : `src/config/constants.py`

```python
WINDOW_HEIGHT = 980  # +40px pour le switch overlay
```

**Critère de validation** : UI reste lisible, aucun chevauchement de widgets.

---

### Phase 6 — Documentation & tests manuels

**Fichiers à créer/modifier** :

- `DOCS/ARCHITECTURE.md` → ajouter section "Overlay flottant" (structure + choix Tk natif)
- `README.md` → mentionner la fonctionnalité dans "Fonctionnalités"
- `docs/ROADMAP.md` → nouvelle section "Phase 9 — v2.3.0 Overlay" avec toutes les cases cochées

**Checklist tests manuels** :

- [ ] Overlay visible bas-gauche moniteur principal
- [ ] Reste topmost au-dessus de Chrome, VSCode, explorateur
- [ ] Couleur/texte change avec l'état autoclick
- [ ] Clic sur overlay → toggle autoclick
- [ ] Switch UI → overlay apparaît/disparaît
- [ ] Fermeture app → overlay se ferme proprement (pas de fenêtre fantôme)
- [ ] Esc → autoclick off + overlay OFF
- [ ] Paramètre `overlay_enabled` persisté correctement
- [ ] Multi-moniteur : overlay reste sur le principal (comportement attendu v2.3.0)

---

### Phase 8 — Stabilité & résilience long-run (CRITIQUE)

**Contexte** : l'application crashe après plusieurs heures d'exécution continue. Cause non identifiée à ce stade. Cette phase doit **diagnostiquer, corriger et instrumenter** pour garantir un fonctionnement 24h+ sans crash.

#### 8.1 Diagnostic — hypothèses à vérifier

| Hypothèse | Zone suspectée | Méthode de validation |
|-----------|---------------|------------------------|
| Fuite mémoire OpenCV/mss (captures non libérées) | `src/core/detector.py` | Suivi `psutil.Process().memory_info().rss` toutes les 30s pendant 1h — courbe stable ou croissante ? |
| Fuite handles Tk (widgets créés dans la boucle Analytics) | `src/ui/dialogs/analytics_window.py`, matplotlib | Compter `len(self.winfo_children())` au fil du temps |
| Accumulation buffer `click_stats` non flush | `src/core/click_stats.py` | Lire le code et vérifier la taille du buffer en cours |
| Thread autoclick zombie après stop/start répétés | `src/core/autoclick_service.py` | `threading.enumerate()` avant/après cycles ON/OFF |
| Listener pynput non stoppé proprement | `src/core/listener.py` | Compter les listeners actifs après N cycles |
| Exception silencieuse dans la boucle `_run` | `AutoclickService._run` | Ajouter un `try/except` global avec logging |
| Saturation file d'événements Tk (`after` sans garbage collect) | `src/ui/app.py` | Auditer tous les `self.after(...)` |
| Handle Windows GDI épuisé (screenshots non libérés) | `mss`, `pyautogui.screenshot` | Observer `handle_count` via `psutil` |
| Crash `matplotlib` backend après N figures | `analytics_window.py` | Vérifier `plt.close('all')` après chaque graphe |

#### 8.2 Instrumentation — logging & monitoring

**Fichier** : `src/core/logger.py` **[NOUVEAU]**

Logger centralisé avec rotation :
```python
# Logs dans ~/.autoclaude/logs/autoclaude.log (rotation 5MB × 3 fichiers)
import logging
from logging.handlers import RotatingFileHandler
```

Logs à émettre :
- `INFO` : démarrage app, start/stop service, toggle overlay, compteur clic tous les N
- `WARNING` : détection échouée N fois consécutives, handle count anormal
- `ERROR` : toute exception capturée
- Uptime + memoire loggés toutes les 5 minutes

**Fichier** : `src/core/health_monitor.py` **[NOUVEAU]**

Watchdog interne lancé au démarrage :
- Snapshot `psutil` toutes les 5 min → log (RSS memory, handle count, thread count)
- Alerte WARNING si RSS > 500 Mo ou handles > 5000 ou threads > 20
- Expose un accesseur `get_health_snapshot()` (utilisable plus tard dans l'UI)

#### 8.3 Corrections — robustesse du cœur autoclick

**Fichier** : `src/core/autoclick_service.py`

- Wrapper global `try/except Exception` dans `_run()` avec log de l'exception et **auto-restart** (max 3 tentatives consécutives avant arrêt définitif)
- Garantir `join(timeout=5)` du thread dans `stop()` pour éviter les zombies
- Vérifier que `_stop_event.clear()` est bien appelé avant restart

**Fichier** : `src/core/detector.py`

- Libérer explicitement les captures (`sct.close()` ou contexte `with` pour `mss`)
- Libérer les arrays numpy après template matching (`del img; del screenshot`)
- Si `cv2` lève une exception, logger et retourner `None` au lieu de propager

**Fichier** : `src/core/listener.py`

- Vérifier que `pynput.Listener.stop()` est idempotent et que l'ancien listener est bien détruit avant d'en créer un nouveau

**Fichier** : `src/core/click_stats.py`

- Auditer le buffer : flush périodique (toutes les 60s) + flush systématique sur `stop()`
- Limiter la taille max en mémoire (garde-fou anti-explosion)

**Fichier** : `src/ui/dialogs/analytics_window.py`

- Appeler `plt.close('all')` à la fermeture de la fenêtre
- `figure.canvas.get_tk_widget().destroy()` explicite avant `destroy()` de la Toplevel

**Fichier** : `src/ui/app.py`

- Wrapper `try/except` autour des callbacks `after(...)` sensibles
- Hook global `Tk.report_callback_exception` pour logger toute exception Tk au lieu de crasher

#### 8.4 Tests de stabilité

**Fichier** : `tests/stability/test_longrun.py` **[NOUVEAU]**

Script manuel exécuté hors CI (trop long) :
- Lance AutoClaude en mode headless (autoclick actif sur image factice)
- Tourne 6h
- Log memoire/handles toutes les 5 min
- Vérifie à la fin : RSS final < 1.5 × RSS initial, aucune exception dans les logs

**Checklist manuelle** :
- [ ] 1h d'autoclick continu → pas de crash, RSS stable
- [ ] 100 cycles ON/OFF rapides → aucun thread zombie
- [ ] Ouvrir/fermer Analytics 50 fois → handles GDI stables
- [ ] Laisser l'app tourner une nuit (8h+) → encore vivante au matin
- [ ] Vérifier les logs : aucun ERROR/CRITICAL

#### 8.5 Documentation

**Fichier** : `DOCS/STABILITY.md` **[NOUVEAU]**

Documenter :
- Localisation des logs (`~/.autoclaude/logs/`)
- Comment interpréter un snapshot santé
- Procédure de report de crash (quels logs joindre)
- Historique des causes racines identifiées (post-mortem)

**Critère de validation Phase 8** :
- Test 24h sans crash validé
- Logs exploitables et non bruyants
- Tous les `try/except` ont un log ERROR (pas de `pass` silencieux)
- Aucune régression de perf mesurable vs v2.2.1

---

### Phase 7 — Packaging

**Fichier** : `AutoClaude_v2.2.1.spec` → renommer en `AutoClaude_v2.3.0.spec`

Vérifier que le dossier `src/ui/overlays/` est bien inclus (normalement automatique via `hiddenimports` ou collection `src`).

**Fichier** : `pyproject.toml` → version `2.2.1` → `2.3.0`

**Fichier** : `src/config/constants.py` → `VERSION = "2.3.0"`

**Fichier** : `README.md` → badge version 2.3.0 + nom exe dans « Option 1 »

---

## 5. Limites connues de v2.3.0 (à documenter)

- L'overlay n'apparaît **que sur le bureau virtuel où l'app a été lancée**. Changer de bureau Windows → l'overlay ne suit pas. Solution prévue en v2.3.1 via `pyvda` (optionnel).
- L'overlay est positionné sur le **moniteur principal uniquement**. Pas d'option multi-moniteur en v2.3.0.
- Pas de drag : position figée bas-gauche.

---

## 6. Évolutions futures (v2.3.1+)

- Support cross-desktop Windows (dépendance optionnelle `pyvda`)
- Drag & drop pour repositionner l'overlay
- Choix du moniteur cible (menu déroulant)
- Tailles d'overlay configurables (petit/moyen/grand)
- Mode « compact icône » (juste le point coloré, pas de texte)

---

## 7. Ordre d'exécution recommandé

1. **Créer la branche** : `git checkout -b V2.3.0`
2. **Phase 8 en priorité** (stabilité) — diagnostic + instrumentation logging avant toute autre chose, pour pouvoir détecter d'éventuelles régressions introduites par l'overlay
3. Phase 1 (constants + settings)
4. Phase 2 (overlay toplevel standalone — testable avec un petit script de démo)
5. Phase 3 (switch UI)
6. Phase 4 (intégration app)
7. Phase 5 (ajustement hauteur)
8. Phase 8 — corrections suite au diagnostic + tests longs
9. Phase 6 (tests manuels + doc)
10. Phase 7 (packaging + version bump)
11. Commit + push branche + merge sur `main` après validation (incluant test 24h)

---

## 8. Risques & mitigations

| Risque | Probabilité | Mitigation |
|--------|-------------|-----------|
| `overrideredirect(True)` + `topmost` comportement étrange sur certains drivers | Faible | Fallback : garder la barre de titre si overrideredirect échoue |
| `CTkToplevel` + `alpha` bug de rendu sur Windows | Moyen | Tester rapidement en Phase 2 ; fallback `tk.Toplevel` natif si bug |
| Overlay vole le focus clavier | Faible | `-toolwindow` + ne pas appeler `focus_set()` |
| Persistence du switch non synchronisée | Faible | Écrire `settings.set(...)` dans le callback du switch |

---

## 9. Critères de succès globaux

- [ ] `python run.py` reste < 2s au démarrage
- [ ] L'overlay s'affiche correctement sans modifier le comportement existant de l'autoclick
- [ ] Aucun freeze ni flicker lors du toggle
- [ ] Le switch UI persiste son état entre deux lancements
- [ ] Tests manuels Phase 6 tous validés
- [ ] **Test stabilité 24h sans crash validé** (Phase 8)
- [ ] **RSS memoire stable sur 6h d'autoclick continu** (Phase 8)
- [ ] **Logs exploitables, aucun ERROR silencieux** (Phase 8)
- [ ] Version bumpée à 2.3.0 partout (VERSION, pyproject.toml, README)
- [ ] Documentation à jour (ARCHITECTURE, ROADMAP, README, STABILITY)
