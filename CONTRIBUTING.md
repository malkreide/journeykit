# Contributing

Thanks for considering a contribution. JourneyKit is small on purpose; the
bar for new dependencies and new surface is high, the bar for better lints,
better examples and translations is low.

## Setup

```bash
git clone https://github.com/malkreide/journeykit.git
cd journeykit
pip install -e ".[dev]"
pip install -r requirements-lint.txt
```

## Before you open a pull request

```bash
python -m pytest -q
ruff check .
ruff format --check .
python scripts/validate_repo.py .
journeykit lint examples/kindergarteneintritt/journey.json --strict
```

All four must pass. `ruff --version` must match `requirements-lint.txt`.

## What makes a good contribution

- **A new lint** comes with: a code in the right block, a level, a hint that says what to do, a test, and a line in both READMEs. Lints judge the model, not prose quality.
- **A schema change** comes with: schema, `model.py` if it touches claims or references, the viewer, the example journeys, tests, and a note in `docs/konzept.md`. Keep `additionalProperties: false`.
- **A new example** must be synthetic. No real people, addresses, contact data or quotes from real interviews. Quote atoms must appear verbatim in the input files with a locator.
- **Viewer changes** keep it a single file without external resources. Check light and dark mode, a 390 px viewport, and that `pageerror` stays empty.
- **Language**: content in German with Swiss spelling (no ß), identifiers and schema fields in English, READMEs in both languages with the same structure.

## Commit messages

Conventional Commits: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`. Add an entry under `[Unreleased]` in `CHANGELOG.md`.

## Working with Claude Code

`CLAUDE.md` is the entry point. It lists conventions, commands and open items.
