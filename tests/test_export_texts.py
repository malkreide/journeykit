"""Exporte je Sprache: Vollständigkeit der Texte und französische Ausgabe.

Die Texte stehen in ``export_texts.py``; ``export.py`` greift nur über
Schlüssel darauf zu. Geprüft wird die Parität der Sprachen, dass jeder
verwendete Schlüssel existiert und dass ein französischer Export keine
deutschen Textbausteine mehr enthält.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from journeykit.cli import main
from journeykit.export import (
    audit_markdown,
    opportunities_markdown,
    story_map_markdown,
)
from journeykit.export_texts import QUADRANT_LABELS, TEXTS
from journeykit.lint import ANTIPATTERNS, lint_journey
from journeykit.lint_messages import ANTIPATTERN_LABELS, LANGUAGES

EXPORT_PY = Path(__file__).resolve().parents[1] / "src" / "journeykit" / "export.py"


def _placeholders(text: str) -> set[str]:
    return set(re.findall(r"\{(\w+)\}", text))


def _exports(journey: dict, lang: str) -> str:
    findings = lint_journey(journey, lang=lang)
    return "\n".join(
        [
            story_map_markdown(journey, lang=lang),
            opportunities_markdown(journey, lang=lang),
            audit_markdown(journey, findings, lang=lang),
        ]
    )


@pytest.mark.parametrize("lang", [x for x in LANGUAGES if x != "de"])
def test_same_keys_and_placeholders_as_german(lang):
    assert set(TEXTS["de"]) == set(TEXTS[lang])
    wrong = [k for k, v in TEXTS["de"].items() if _placeholders(v) != _placeholders(TEXTS[lang][k])]
    assert not wrong, wrong
    assert set(QUADRANT_LABELS["de"]) == set(QUADRANT_LABELS[lang])
    assert set(ANTIPATTERN_LABELS[lang]) == set(ANTIPATTERNS)


def test_french_typography():
    for key, value in TEXTS["fr"].items():
        assert not re.search(r" [:;?!]", value), key
        assert "« " not in value and " »" not in value, key


def test_keys_used_in_export_exist_and_all_are_used():
    used = set(re.findall(r'\bt\(\s*"([\w.]+)"', EXPORT_PY.read_text(encoding="utf-8")))
    assert used, "Muster für Schlüssel greift nicht mehr"
    assert used == set(TEXTS["de"]), set(TEXTS["de"]) ^ used


def test_french_export_has_no_german_template_text(example_journey):
    out = _exports(example_journey, "fr")
    leftovers = []
    for key, de in TEXTS["de"].items():
        for part in re.split(r"\{\w+\}", de):
            part = part.strip(" #-|>_*()·:")
            if len(part) >= 6 and part not in TEXTS["fr"][key] and part in out:
                leftovers.append(f"{key}: {part!r}")
    for ap, label in ANTIPATTERNS.items():
        if label != ANTIPATTERN_LABELS["fr"][ap] and label in out:
            leftovers.append(f"antipattern {ap}")
    assert not leftovers, leftovers
    assert "## État des preuves" in out and "## Constats" in out


def test_unknown_language_is_rejected(example_journey):
    with pytest.raises(ValueError):
        story_map_markdown(example_journey, lang="it")


def test_cli_export_lang(tmp_path, minimal):
    src = tmp_path / "j.json"
    src.write_text(json.dumps(minimal), encoding="utf-8")
    out = tmp_path / "a.md"
    assert main(["export", str(src), "--format", "audit", "--lang", "fr", "-o", str(out)]) == 0
    assert "## État des preuves" in out.read_text(encoding="utf-8")
    minimal["meta"]["language"] = "fr"
    src.write_text(json.dumps(minimal), encoding="utf-8")
    assert main(["export", str(src), "--format", "storymap", "-o", str(out)]) == 0
    assert "Colonne vertébrale" in out.read_text(encoding="utf-8")
