"""Vertrag für alle Beispiele unter examples/*/ – gilt für jedes neue Beispiel ohne Zusatzcode.

Ein Beispiel ist ein Verzeichnis mit einer journey.json. Geprüft wird, was CLAUDE.md
für Beispiele verlangt: schema-valide, synthetisch, journey.json ohne ERROR und WARN,
Zitat-Atome wörtlich im Input, keine Kontaktangaben im Rohmaterial.
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

import pytest

from journeykit.lint import _PII_PATTERNS, ERROR, WARN, lint_journey
from journeykit.validate import validate_journey

ROOT = Path(__file__).resolve().parents[1]
# wie in der CI festgepinnt, damit Review-Termine der Beispiele die Tests nicht altern lassen
TODAY = date(2026, 10, 5)
EXAMPLE_DIRS = sorted(p.parent for p in (ROOT / "examples").glob("*/journey.json"))
JOURNEY_FILES = sorted(f for d in EXAMPLE_DIRS for f in d.glob("*.json"))
INPUT_FILES = sorted(f for d in EXAMPLE_DIRS for f in (d / "input").glob("*") if f.is_file())


def _rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


def _norm(text: str) -> str:
    """Zeilenumbrüche und Mehrfach-Leerzeichen sind kein inhaltlicher Unterschied."""
    return re.sub(r"\s+", " ", text).strip()


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_examples_are_discovered():
    assert EXAMPLE_DIRS, "kein Beispiel unter examples/*/journey.json gefunden"


@pytest.mark.parametrize("path", JOURNEY_FILES, ids=_rel)
def test_example_is_schema_valid(path):
    errors = validate_journey(_load(path))
    assert not errors, [str(e) for e in errors]


@pytest.mark.parametrize("path", JOURNEY_FILES, ids=_rel)
def test_example_is_marked_synthetic(path):
    assert _load(path)["meta"].get("synthetic") is True


@pytest.mark.parametrize("path", JOURNEY_FILES, ids=_rel)
def test_example_has_no_lint_errors(path):
    errors = [str(f) for f in lint_journey(_load(path), today=TODAY) if f.level == ERROR]
    assert not errors, errors


@pytest.mark.parametrize("path", [d / "journey.json" for d in EXAMPLE_DIRS], ids=_rel)
def test_example_main_journey_has_no_warnings(path):
    warnings = [str(f) for f in lint_journey(_load(path), today=TODAY) if f.level == WARN]
    assert not warnings, warnings


@pytest.mark.parametrize("path", JOURNEY_FILES, ids=_rel)
def test_example_quotes_are_verbatim_in_input(path):
    journey = _load(path)
    locations = {s["id"]: s.get("location") for s in journey["sources"]}
    problems = []
    for atom in journey["evidence"]:
        if atom["kind"] != "quote":
            continue
        location = locations.get(atom["source_ref"])
        if not location:
            problems.append(f"{atom['id']}: Quelle {atom['source_ref']} ohne location")
            continue
        raw = (path.parent / location).read_text(encoding="utf-8")
        # CSV maskiert Anführungszeichen im Feld als ""
        haystack = _norm(raw.replace('""', '"'))
        if _norm(atom["text"]) not in haystack:
            problems.append(f"{atom['id']}: nicht wörtlich in {location}")
    assert not problems, problems


@pytest.mark.parametrize("path", INPUT_FILES, ids=_rel)
def test_example_input_has_no_contact_data(path):
    text = path.read_text(encoding="utf-8")
    hits = [label for label, rx in _PII_PATTERNS if rx.search(text)]
    assert not hits, hits
