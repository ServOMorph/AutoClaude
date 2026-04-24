# Contribuer à AutoClaude

Merci de votre intérêt pour contribuer à AutoClaude !

## Signaler un bug

1. Vérifier que le bug n'a pas déjà été rapporté dans les [issues](https://github.com/ServOMorph/AutoClaude/issues)
2. Ouvrir une nouvelle issue en utilisant le template **Bug Report**
3. Fournir un maximum de détails (étapes, version, OS, Python)

## Proposer une fonctionnalité

1. Ouvrir une issue **Feature Request**
2. Décrire le problème résolu et la solution proposée
3. Attendre une discussion avant de coder

## Environnement de développement

```bash
git clone https://github.com/ServOMorph/AutoClaude
cd AutoClaude

# Environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou .venv\Scripts\activate  # Windows

# Dépendances
pip install -r requirements.txt
pip install -r requirements-dev.txt
# ou : pip install -e ".[dev]"
```

## Tests

```bash
pytest tests/ -v
pytest tests/ --cov=src --cov-report=term-missing
```

## Style de code

- Python ≥ 3.10
- Format : `black src/ tests/`
- Lint : `ruff check src/ tests/`
- Types : `mypy src/`
- Docstrings obligatoires pour fonctions/classes publiques
- Type hints recommandés

## Processus de Pull Request

1. Fork le repository
2. Créer une branche : `git checkout -b feat/ma-fonctionnalite`
3. Commits au format **Conventional Commits** en français :
   - `feat: ajoute ...`
   - `fix: corrige ...`
   - `docs: met à jour ...`
   - `test: ajoute tests ...`
   - `refactor: réorganise ...`
   - `chore: maintenance ...`
4. Tests : `pytest tests/` doit passer
5. Mettre à jour le `CHANGELOG.md` (section `[Unreleased]`)
6. Push et ouvrir une PR vers `main`

## Code of Conduct

Ce projet adhère au [Code of Conduct](CODE_OF_CONDUCT.md). En participant, vous acceptez de respecter ces règles.

## Questions

Utiliser les [GitHub Discussions](https://github.com/ServOMorph/AutoClaude/discussions) ou ouvrir une issue.

---

Merci pour votre contribution à AutoClaude !
