# PLAN v2.5.6 — Crash access violation sur sessions longues (> 1h)

> Statut : **EN ATTENTE DE VALIDATION** (écrire la validation dans `validation.txt`)
> Date : 2026-07-17

---

## 1. Constat (logs)

- Le crash persiste **après** le passage à Python 3.13 / Tk 8.6.15 (fix v2.5.4) :
  les 6 dernières traces de `~/.autoclaude/logs/crash.log` sont sur le runtime `Python313`.
- Dernier crash : **2026-07-16 à 15:16:51**, après ~1h19 de session avec autoclick actif
  (démarrage 13:57:50). Signature identique : `Windows fatal exception: access violation`,
  thread principal dans `tkinter.mainloop`.
- Les snapshots santé confirment qu'il n'y a **aucune fuite** : RSS ~120-160 Mo stable,
  handles ~425 stables, threads stables. Ce n'est pas un problème de ressources.

## 2. Cause racine identifiée (hypothèse forte)

**Des objets Tkinter sont finalisés depuis des threads secondaires**, ce qui corrompt
l'état natif de l'interpréteur Tcl (lié à son thread créateur). La corruption explose
plus tard, aléatoirement, dans `mainloop` → access violation dans `tk86t.dll`,
quelle que soit la version de Tk (8.6.12 **et** 8.6.15 → ce n'est pas le bug de version).

Deux vecteurs dans le code :

### Vecteur A — `gc.collect()` explicite dans le thread HealthMonitor
[health_monitor.py:42](src/core/health_monitor.py#L42) : toutes les 5 min, le thread
`HealthMonitor` exécute `gc.collect()`. Les logs montrent **1000-3000 objets collectés
par tick** pendant les sessions actives. Quand un cycle collecté contient des objets Tk
(`CTkFont` → `tkinter.font.Font`, `Variable`, `CTkImage`/`PhotoImage` — l'UI en crée
partout), leur `__del__` appelle l'interpréteur Tcl **depuis le mauvais thread**.
Ironie : ce `gc.collect()` avait été ajouté pour la stabilité longue durée — il fait
l'inverse.

### Vecteur B — gc *automatique* déclenché dans le thread AutoclickWorker
Le worker alloue massivement toutes les 0,5 s (`numpy` arrays dans `_mss_cv2`,
[detector.py:82-88](src/core/detector.py#L82-L88)). Le gc générationnel de Python se
déclenche dans **le thread qui alloue** — donc quasi toujours dans le worker pendant
une session active. Même effet : finalisation d'objets Tk hors du thread principal.
**Cohérent avec l'observation « ça plante quand l'autoclick tourne longtemps »** :
plus la session active est longue, plus il y a de passes gc dans le mauvais thread.

## 3. Évaluation de l'idée « reset mémoire toutes les 30 min »

Idée : relancer/réinitialiser l'appli périodiquement (sans perdre les stats).

- ✅ Les stats sont persistées (`~/.autoclaude`), un restart ne perd rien.
- ❌ Ne corrige pas la cause : la corruption peut survenir **avant** 30 min (le crash
  du 16/07 aurait pu arriver à 25 min), et un cycle destroy/recreate massif de widgets
  Tk génère justement un pic de finalisations → **augmente** le risque au moment du reset.
- ❌ Un reset in-process ne réinitialise pas l'état natif corrompu de l'interpréteur
  Tcl ; il faudrait tuer le **processus** entier.
- ❌ Interruption de l'autoclick toutes les 30 min (fenêtre de quelques secondes où un
  « Yes » de Claude Code peut être raté), flicker UI, complexité.

**Verdict : pertinente comme filet de sécurité, mais pas comme correctif.** On garde
l'esprit de l'idée sous une forme plus sûre : un **superviseur de relance** qui
redémarre le processus uniquement s'il crashe (étape 3, optionnelle).

## 4. Correctifs proposés

### Étape 1 — Router tout le gc vers le thread principal (correctif racine)
- `run.py` : `gc.disable()` au démarrage (désactive le gc *automatique* ; le comptage
  de références continue de libérer 99 % des objets normalement).
- `app.py` : tâche périodique `self.after(60_000, ...)` qui exécute `gc.collect()`
  **dans le thread principal Tk** toutes les 60 s et logge le nombre d'objets collectés.
  Toutes les finalisations d'objets Tk se font désormais dans le bon thread.
- `health_monitor.py` : supprimer le `gc.collect()` du thread watchdog (le snapshot
  santé reste, il loggera le compteur gc fourni par l'app).

### Étape 2 — Réduire le bruit / risques secondaires
- `detector.py` : `cv2.setNumThreads(1)` — supprime le pool de threads OpenCV
  (~20 threads), source du warning permanent « Threads élevés : 43 (seuil 20) » qui
  pollue les logs. `matchTemplate` sur une image d'écran reste largement assez rapide.
- `health_monitor.py` : seuil threads 20 → 30 (baseline réelle ~21 threads).

### Étape 3 (optionnelle, filet de sécurité) — Superviseur de relance
- Nouveau `supervisor.py` : lance `run.py` en sous-processus ; si le processus meurt
  avec un code de sortie anormal (crash natif), il le relance automatiquement
  (backoff simple, max N relances/heure, log de l'événement).
- Reprend ton idée de « relance » mais **uniquement en cas de crash réel**, sans
  interrompre les sessions saines. Les stats et la position de l'overlay sont déjà
  persistées, la reprise est transparente.
- À toi de dire si tu la veux dans cette version ou plus tard.

### Étape 4 — Versioning & docs
- Bump 2.5.5 → 2.5.6, CHANGELOG, README si superviseur retenu.
- Mise à jour de la mémoire projet (crash signature → cause gc/threads).

## 5. Vérification

1. `pytest` — la suite existante passe.
2. Test manuel court : lancer l'app, vérifier dans `autoclaude.log` les ticks
   `gc (main thread)` et l'absence du gc HealthMonitor.
3. **Test décisif** : session longue ≥ 3 h avec autoclick actif (conditions du crash
   du 16/07). Critère de succès : aucune nouvelle entrée dans `crash.log`
   (noter la taille/date du fichier avant le test).
4. Si étape 3 retenue : tuer le processus manuellement (`taskkill /F`) et vérifier la
   relance automatique + reprise des stats.

## 6. Risques

- `gc.disable()` : si du code crée des cycles massifs entre deux collectes (60 s),
  le RSS peut onduler un peu plus — surveillé par le HealthMonitor existant.
- L'hypothèse gc-thread est la plus probable (elle explique la persistance du crash
  sur Tk 8.6.15, la corrélation avec les sessions actives, et l'absence de fuite),
  mais un crash natif reste difficile à prouver à 100 % avant le test longue durée.
  Le superviseur (étape 3) couvre le cas résiduel.
