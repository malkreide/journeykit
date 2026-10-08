"""Lint-Meldungen je Sprache: Vollständigkeit, Platzhalter, Aufrufe in lint.py.

Die Regeln liefern nur IDs und Werte; Text und Hinweis stehen in
``lint_messages.py``. Geprüft wird, dass jede Sprache dieselben Meldungen mit
denselben Platzhaltern hat und dass jeder ``c.add``-Aufruf in ``lint.py`` eine
vorhandene Meldung mit genau deren Platzhaltern füllt – so fällt ein Tippfehler
auf, bevor eine selten ausgelöste Regel zur Laufzeit scheitert.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

import pytest

from journeykit.cli import main
from journeykit.lint import _PII_PATTERNS, lint_journey
from journeykit.lint_messages import LANGUAGES, MESSAGES, PII_LABELS, SUMMARY, resolve_language
from journeykit.render import UI_LANGUAGES, render_html

LINT_PY = Path(__file__).resolve().parents[1] / "src" / "journeykit" / "lint.py"
# Argumente von _Collector.add, die keine Platzhalter sind
_ADD_ARGS = {"code", "level", "antipattern", "path", "msg"}


def _placeholders(text: str) -> set[str]:
    return set(re.findall(r"\{(\w+)\}", text))


def _calls() -> list[tuple[int, str, set[str]]]:
    """(Zeile, Meldungs-ID, übergebene Platzhalter) für jeden c.add-Aufruf in lint.py."""
    out = []
    for node in ast.walk(ast.parse(LINT_PY.read_text(encoding="utf-8"))):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "add"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "c"
        ):
            continue
        kwargs = {k.arg: k.value for k in node.keywords}
        msg = kwargs.get("msg")
        msg_id = msg.value if isinstance(msg, ast.Constant) else node.args[0].value
        out.append((node.lineno, msg_id, set(kwargs) - _ADD_ARGS))
    return out


def test_languages_match_viewer():
    assert set(LANGUAGES) == set(UI_LANGUAGES)


@pytest.mark.parametrize("lang", [x for x in LANGUAGES if x != "de"])
def test_same_messages_and_placeholders_as_german(lang):
    de, other = MESSAGES["de"], MESSAGES[lang]
    assert set(de) == set(other), set(de) ^ set(other)
    for key, (msg, hint) in de.items():
        assert _placeholders(msg) == _placeholders(other[key][0]), key
        assert _placeholders(hint) == _placeholders(other[key][1]), key
        assert bool(hint) == bool(other[key][1]), f"{key}: Hinweis nur in einer Sprache"
    assert set(PII_LABELS["de"]) == set(PII_LABELS[lang]) == {k for k, _ in _PII_PATTERNS}
    assert _placeholders(SUMMARY["de"]) == _placeholders(SUMMARY[lang])


@pytest.mark.parametrize("lang", LANGUAGES)
def test_messages_are_filled_and_swiss_spelling(lang):
    for key, (msg, hint) in MESSAGES[lang].items():
        assert msg.strip(), key
        assert "ß" not in msg + hint, key


def test_french_typography():
    for key, (msg, hint) in MESSAGES["fr"].items():
        for text in (msg, hint):
            assert not re.search(r" [:;?!]", text), f"{key}: normales Leerzeichen vor Satzzeichen"
            assert "« " not in text and " »" not in text, (
                f"{key}: Guillemets ohne geschütztes Leerzeichen"
            )


def test_every_call_uses_an_existing_message_with_its_placeholders():
    calls = _calls()
    assert len(calls) > 40, "AST-Muster greift nicht mehr"
    problems = []
    for line, msg_id, given in calls:
        if msg_id not in MESSAGES["de"]:
            problems.append(f"lint.py:{line}: Meldung {msg_id} fehlt")
            continue
        msg, hint = MESSAGES["de"][msg_id]
        wanted = _placeholders(msg) | _placeholders(hint)
        if given != wanted:
            problems.append(f"lint.py:{line}: {msg_id} erwartet {wanted}, bekommt {given}")
    assert not problems, problems


def test_every_message_is_used():
    used = {msg_id for _, msg_id, _ in _calls()}
    assert set(MESSAGES["de"]) - used == set()


def test_lint_in_french(minimal):
    minimal["phases"][0]["steps"][0]["pain_points"][0]["type"] = "friction"
    fr = lint_journey(minimal, lang="fr")
    de = lint_journey(minimal)
    assert [f.code for f in fr] == [f.code for f in de]
    l020 = next(f for f in fr if f.code == "L020")
    assert l020.message.startswith("Aucun irritant") and l020.hint


def test_unknown_language_is_rejected(minimal):
    with pytest.raises(ValueError):
        lint_journey(minimal, lang="it")


def test_language_follows_meta_language(minimal):
    assert resolve_language(minimal) == "de"
    minimal["meta"]["language"] = "fr"
    assert resolve_language(minimal) == "fr"
    assert resolve_language(minimal, "de") == "de"
    minimal["meta"]["language"] = "rm"
    assert resolve_language(minimal) == "de"


def test_cli_lint_lang(tmp_path, minimal, capsys):
    src = tmp_path / "j.json"
    src.write_text(json.dumps(minimal), encoding="utf-8")
    main(["lint", str(src), "--lang", "fr"])
    out = capsys.readouterr().out
    assert "erreur(s)" in out and "remarque(s)" in out


def test_render_uses_ui_language_for_findings(minimal):
    minimal["scenario"].pop("scope_exclusions", None)
    assert "Aucune exclusion de périmètre" in render_html([minimal], lang="fr")
    assert "Kein expliziter Scope-Ausschluss" in render_html([minimal])
