"""Texte der Kommandozeile je Sprache: Vollständigkeit, Hilfe, Meldungen, Gerüst."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from journeykit.cli import _early_lang, build_parser, main, scaffold
from journeykit.cli_texts import ENV_LANG, TEXTS
from journeykit.lint_messages import LANGUAGES
from journeykit.validate import validate_journey

CLI_PY = Path(__file__).resolve().parents[1] / "src" / "journeykit" / "cli.py"


def _placeholders(text: str) -> set[str]:
    return set(re.findall(r"\{(\w+)\}", text))


def _all_help(lang: str) -> str:
    parser = build_parser(lang)
    sub = next(a for a in parser._actions if a.dest == "command")
    return "\n".join([parser.format_help(), *(p.format_help() for p in sub.choices.values())])


@pytest.fixture(autouse=True)
def _no_env_language(monkeypatch):
    monkeypatch.delenv(ENV_LANG, raising=False)


@pytest.mark.parametrize("lang", [x for x in LANGUAGES if x != "de"])
def test_same_keys_and_placeholders_as_german(lang):
    assert set(TEXTS["de"]) == set(TEXTS[lang])
    wrong = [k for k, v in TEXTS["de"].items() if _placeholders(v) != _placeholders(TEXTS[lang][k])]
    assert not wrong, wrong


def test_french_typography():
    for key, value in TEXTS["fr"].items():
        assert not re.search(r" [:;?!]", value), key


def test_keys_used_in_cli_exist_and_all_are_used():
    code = CLI_PY.read_text(encoding="utf-8")
    used = set(re.findall(r'_text\(\s*\w+,\s*"([\w.]+)"', code))
    used |= {f"help.{k}" for k in re.findall(r'\bh\("(\w+)"\)', code)}
    used |= {f"scaffold.{k}" for k in re.findall(r'\bt\("(\w+)"\)', code)}
    assert used == set(TEXTS["de"]), set(TEXTS["de"]) ^ used


def test_french_help_has_no_german_text():
    out = _all_help("fr")
    leftovers = [v for k, v in TEXTS["de"].items() if k.startswith("help.") and v in out]
    assert not leftovers, leftovers
    assert "Contrôle méthodologique" in out


def test_early_language_from_argument_or_environment(monkeypatch):
    assert _early_lang(["lint", "x.json", "--lang", "fr"]) == "fr"
    assert _early_lang(["lint", "--lang=fr", "x.json"]) == "fr"
    assert _early_lang(["lint", "x.json"]) == "de"
    monkeypatch.setenv(ENV_LANG, "fr")
    assert _early_lang(["lint", "x.json"]) == "fr"
    assert _early_lang(["lint", "x.json", "--lang", "de"]) == "de"
    monkeypatch.setenv(ENV_LANG, "it")
    assert _early_lang([]) == "de"


def test_scaffold_in_french_is_valid():
    j = scaffold("x-y", "Titre", "Persona", "Rôle", "Objectif", lang="fr")
    assert validate_journey(j) == []
    assert j["meta"]["language"] == "fr"
    assert j["phases"][0]["steps"][0]["action"].startswith("TODO\u00a0: que fait")


def test_new_follows_environment(tmp_path, monkeypatch):
    out = tmp_path / "n.json"
    monkeypatch.setenv(ENV_LANG, "fr")
    argv = ["new", "x-y", "--title", "T1", "--persona", "P", "--role", "R", "--goal", "Z"]
    assert main([*argv, "-o", str(out)]) == 0
    assert json.loads(out.read_text(encoding="utf-8"))["meta"]["language"] == "fr"


def test_validate_messages_follow_journey_language(tmp_path, minimal, capsys):
    src = tmp_path / "j.json"
    minimal["meta"]["language"] = "fr"
    src.write_text(json.dumps(minimal), encoding="utf-8")
    assert main(["validate", str(src)]) == 0
    assert "conforme au schéma" in capsys.readouterr().out
    assert main(["validate", str(src), "--lang", "de"]) == 0
    assert "schema-valide" in capsys.readouterr().out
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"schema_version": "1.0"}), encoding="utf-8")
    with pytest.raises(SystemExit):
        main(["lint", str(bad), "--lang", "fr"])
    assert "erreur(s) de schéma" in capsys.readouterr().err


def test_written_message_follows_output_language(tmp_path, minimal, capsys):
    src = tmp_path / "j.json"
    src.write_text(json.dumps(minimal), encoding="utf-8")
    main(["export", str(src), "--format", "audit", "--lang", "fr", "-o", str(tmp_path / "a.md")])
    assert "écrit" in capsys.readouterr().err
