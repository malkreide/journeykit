"""Sprachen der Viewer-Oberfläche: Vollständigkeit der Texte und Wahl der Sprache.

Die Texte stehen als JSON im Block «jk-i18n» von viewer.html. Geprüft wird, dass
jede Sprache dieselben Schlüssel und Platzhalter hat, dass jeder Schlüssel, den
der Code benutzt, existiert, und dass jeder Enum-Wert des Schemas eine
Beschriftung hat – damit eine Schemaerweiterung die Übersetzung nicht still
überholt.
"""

from __future__ import annotations

import json
import re

import pytest

from journeykit import load_schema
from journeykit.cli import main
from journeykit.lint import ANTIPATTERNS
from journeykit.render import UI_LANGUAGES, render_html, ui_language, viewer_template

# Schema-Enum (Pfad unter $defs) → Abschnitt im Sprachblock
ENUM_LABELS = {
    ("evidence_class",): "classes",
    ("channel",): "channels",
    ("status",): "ppStatus",
    ("meta", "properties", "status"): "status",
    ("meta", "properties", "map_type"): "mapType",
    ("pain_point", "properties", "frequency"): "freq",
    ("kpi", "properties", "category"): "kpiCat",
    ("source", "properties", "kind"): "srcKinds",
    ("source", "properties", "pii_status"): "pii",
    ("evidence_atom", "properties", "kind"): "kinds",
    ("performed_by", "properties", "mandate"): "mandate",
}
# Bewusst leer in einer Sprache: der Hinweis, dass Lint-Meldungen deutsch sind
MAY_BE_EMPTY = {("de", "ui.auditLangNote")}


def _i18n() -> dict:
    html = viewer_template()
    m = re.search(r'<script type="application/json" id="jk-i18n">(.*?)</script>', html, re.S)
    assert m, "Sprachblock jk-i18n fehlt"
    return json.loads(m.group(1))


def _flat(d: dict, prefix: str = "") -> dict[str, str]:
    out: dict[str, str] = {}
    for k, v in d.items():
        if isinstance(v, dict):
            out.update(_flat(v, f"{prefix}{k}."))
        else:
            out[f"{prefix}{k}"] = v
    return out


def _placeholders(text: str) -> set[str]:
    return set(re.findall(r"\{(\w+)\}", text))


I18N = _i18n()


def test_every_ui_language_has_a_text_block():
    assert set(I18N) == set(UI_LANGUAGES)


@pytest.mark.parametrize("lang", [x for x in UI_LANGUAGES if x != "de"])
def test_same_keys_and_placeholders_as_german(lang):
    de, other = _flat(I18N["de"]), _flat(I18N[lang])
    assert set(de) == set(other), set(de) ^ set(other)
    wrong = [k for k in de if _placeholders(de[k]) != _placeholders(other[k])]
    assert not wrong, wrong


@pytest.mark.parametrize("lang", UI_LANGUAGES)
def test_texts_are_filled_and_swiss_spelling(lang):
    flat = _flat(I18N[lang])
    empty = [k for k, v in flat.items() if not v and (lang, k) not in MAY_BE_EMPTY]
    assert not empty, empty
    assert not [k for k, v in flat.items() if "ß" in v]


@pytest.mark.parametrize("lang", UI_LANGUAGES)
def test_schema_enums_have_labels(lang):
    defs = load_schema()["$defs"]
    missing = []
    for path, section in ENUM_LABELS.items():
        node = defs
        for part in path:
            node = node[part]
        missing += [f"{section}.{v}" for v in node["enum"] if v not in I18N[lang][section]]
    missing += [f"antipatterns.{a}" for a in ANTIPATTERNS if a not in I18N[lang]["antipatterns"]]
    assert not missing, missing


def test_keys_used_in_code_exist():
    html = viewer_template()
    code = html[html.index("const DATA =") :]
    ui = I18N["de"]["ui"]
    used = set(re.findall(r'\b(?:t|lbl)\("(\w+)"', code))
    used |= set(re.findall(r'data-i18n(?:-title|-aria)?="(\w+)"', html))
    plural = set(re.findall(r'\btn\("(\w+)"', code))
    missing = sorted(k for k in used if k not in ui)
    missing += sorted(
        f"{k}_one/_other" for k in plural if f"{k}_one" not in ui or f"{k}_other" not in ui
    )
    assert not missing, missing
    assert len(used) > 100, "Muster für Schlüssel greift nicht mehr"


def test_ui_language_follows_meta_language(minimal):
    assert ui_language([minimal]) == "de"
    minimal["meta"]["language"] = "fr"
    assert ui_language([minimal]) == "fr"
    minimal["meta"]["language"] = "it"
    assert ui_language([minimal]) == "de", "ohne italienische Oberfläche gilt Deutsch"
    assert ui_language([minimal], "fr") == "fr"
    with pytest.raises(ValueError):
        ui_language([minimal], "it")


def test_render_embeds_language(minimal):
    assert '"lang": "de"' in render_html([minimal])
    assert '"lang": "fr"' in render_html([minimal], lang="fr")


def test_cli_render_lang(tmp_path, minimal):
    src = tmp_path / "j.json"
    src.write_text(json.dumps(minimal), encoding="utf-8")
    out = tmp_path / "j.html"
    assert main(["render", str(src), "-o", str(out), "--lang", "fr"]) == 0
    assert '"lang": "fr"' in out.read_text(encoding="utf-8")
