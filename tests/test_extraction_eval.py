"""Testsatz für die Extraktion: Fälle, Gold, Schablone und Scorer passen zusammen.

Die CI ruft kein Modell auf. Sie prüft, dass jeder Fall vollständig ist, dass die
Prompt-Schablone aus evidenz.md mit den Werten der Fälle gefüllt werden kann,
dass die Referenz-Extraktion jedes Falls die volle Punktzahl ohne Regelverstoss
erreicht und dass der Scorer typische Fehler einer Extraktion erkennt.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

import pytest

from journeykit.lint import _PII_PATTERNS

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "eval_extraction", ROOT / "scripts" / "eval_extraction.py"
)
ev = importlib.util.module_from_spec(_spec)
sys.modules["eval_extraction"] = ev
_spec.loader.exec_module(ev)

CASES = ev.load_cases()


def _reference(case) -> list[dict]:
    return json.loads((case.path / "reference.json").read_text(encoding="utf-8"))


def _rules(result) -> set[str]:
    return {rule for _, rule, _ in result.violations}


def _failed_fields(result) -> set[tuple[str, str]]:
    return {(key, name) for key, name, ok, _, _ in result.fields if not ok}


def test_cases_are_discovered():
    assert {c.id for c in CASES} >= {
        "interview",
        "anfragen",
        "prozessdokument",
        "statistik",
        "workshop",
        "interview-hort",
        "befragung",
        "beschwerde",
    }


def test_template_placeholders_are_filled_by_every_case():
    tmpl = ev.template()
    assert "{prefix}" in tmpl and "{source_id}" in tmpl
    for case in CASES:
        missing = ev.placeholders(tmpl) - set(ev.template_values(case))
        assert not missing, (case.id, missing)
        prompt = ev.render_prompt(case, tmpl)
        assert case.input_text.strip().splitlines()[-1] in prompt
        assert "{" not in prompt.split("Quelle «")[0], "ungefüllter Platzhalter"


@pytest.mark.parametrize("case", CASES, ids=lambda c: c.id)
def test_reference_extraction_scores_perfectly(case):
    result = ev.score_case(case, _reference(case))
    assert result.recall == 1.0, result.missing
    assert result.field_accuracy == 1.0, _failed_fields(result)
    assert not result.violations, result.violations


@pytest.mark.parametrize("case", CASES, ids=lambda c: c.id)
def test_inputs_are_synthetic_and_free_of_contact_data(case):
    text = case.input_text
    assert not [label for label, rx in _PII_PATTERNS if rx.search(text)]
    assert "synthetisch" in text or case.input_name.endswith(".csv")


def test_gold_keys_are_unique_and_required_atoms_exist():
    for case in CASES:
        keys = [g["key"] for g in case.expected["atoms"]]
        assert len(keys) == len(set(keys)), case.id
        assert any(g.get("required") for g in case.expected["atoms"]), case.id


def _interview():
    case = next(c for c in CASES if c.id == "interview")
    return case, _reference(case)


def test_scorer_detects_typical_extraction_errors():
    case, atoms = _interview()
    bad = copy.deepcopy(atoms)
    bad[0]["text"] = "Ich kannte die Frist von vierzehn Tagen nicht."  # umformuliert
    bad[1].pop("locator")  # Fundstelle fehlt
    bad[2]["emotion_hint"]["explicit"] = False  # ausdrückliche Angst als abgeleitet
    bad[4]["signal"] = "friction"  # Aufgeben ist ein Breakdown
    bad[6]["text"] = bad[6]["text"].replace("[…]", "Frau Roth,")  # erfundener Name im Zitat
    bad[7]["source_ref"] = "int-1"
    bad.append(
        {**bad[3], "id": "u1-10", "kind": "metric", "text": "Heimatschein: neun Tage"}
    )  # doppelt
    bad.append(
        {**bad[8], "id": "u1-11", "text": "Wie sind Sie dann vorgegangen?", "locator": "[01:30]"}
    )  # Frage der interviewenden Person
    result = ev.score_case(case, bad)
    assert {
        "wörtlich",
        "fundstelle",
        "personendaten",
        "source_ref",
        "aufgeteilt",
        "keine-evidenz",
    } <= _rules(result)
    assert ("angst-busse", "emotion") in _failed_fields(result)
    assert ("upload-aufgegeben", "signal") in _failed_fields(result)
    assert "frist-unbekannt" in result.missing, "umformuliertes Zitat darf nicht als Treffer zählen"


def test_scorer_checks_units_and_counts():
    case = next(c for c in CASES if c.id == "statistik")
    atoms = _reference(case)
    median = next(a for a in atoms if a["locator"] == "bearbeitungsdauer_median")
    median.update(value=8, unit="Kalendertage")  # umgerechnet statt wie in der Quelle
    result = ev.score_case(case, atoms + copy.deepcopy(atoms))
    assert ("dauer-median", "unit") in _failed_fields(result)
    assert ("dauer-median", "value") in _failed_fields(result)
    assert {"anzahl", "id"} <= _rules(result)


def test_verbatim_allows_elision_and_bracketed_replacements():
    source = "Meine Nachbarin, Frau Roth, hat mir gezeigt, welche Unterlagen ich kopieren muss."
    assert ev.is_verbatim("Meine Nachbarin, [Name], hat mir gezeigt …", source)
    assert ev.is_verbatim(
        "«Meine Nachbarin […] hat mir gezeigt, welche Unterlagen ich kopieren muss.»", source
    )
    assert not ev.is_verbatim("Meine Nachbarin hat mir die Unterlagen gezeigt.", source)


def test_candidate_parsing_tolerates_fences_and_wrapper():
    assert ev.parse_candidate('```json\n[{"id": "x-1"}]\n```') == [{"id": "x-1"}]
    assert ev.parse_candidate('{"atoms": [{"id": "x-1"}]}') == [{"id": "x-1"}]


def test_cli_prompts_and_score(tmp_path, capsys):
    assert ev.main(["prompts", "-o", str(tmp_path / "p")]) == 0
    assert len(list((tmp_path / "p").glob("*.prompt.md"))) == len(CASES)
    cand = tmp_path / "c"
    cand.mkdir()
    for case in CASES:
        (cand / f"{case.id}.json").write_text(
            (case.path / "reference.json").read_text(encoding="utf-8"), encoding="utf-8"
        )
    assert ev.main(["score", str(cand), "-o", str(tmp_path / "r.md")]) == 0
    assert "| **gesamt** |" in (tmp_path / "r.md").read_text(encoding="utf-8")


def test_recorded_runs_still_score_as_reported():
    """Die abgelegten Läufe bleiben mit dem aktuellen Scorer reproduzierbar."""
    runs = ROOT / "skill" / "user-journey" / "evals" / "extraction" / "runs"
    for run in sorted(p for p in runs.iterdir() if p.is_dir()):
        title = (run / "bericht.md").read_text(encoding="utf-8").splitlines()[0][2:]
        # ältere Läufe kennen spätere Fälle nicht; sie werden nur über ihre eigenen bewertet
        results = ev.score_run(run, CASES)
        assert results, run.name
        assert ev.report_markdown(results, title) == (run / "bericht.md").read_text(
            encoding="utf-8"
        ), run.name


def _case(case_id):
    case = next(c for c in CASES if c.id == case_id)
    return case, _reference(case)


def _atom(atoms, locator):
    return next(a for a in atoms if a["locator"] == locator)


def test_scorer_separates_duration_from_deadline_and_others_feelings():
    case, atoms = _case("interview-hort")
    _atom(atoms, "[04:30]")["value"] = 2  # Frist statt erlebter Dauer
    _atom(atoms, "[08:15]")["emotion_hint"] = {"valence": -2, "label": "traurig", "explicit": True}
    _atom(atoms, "[10:02]").pop("contradicts")
    _atom(atoms, "[07:38]")["text"] = _atom(atoms, "[07:38]")["text"].replace(
        "[Name]", "Frau Brunner"
    )
    result = ev.score_case(case, atoms)
    assert {
        ("bescheid-sieben-wochen", "value"),
        ("sohn-geweint", "emotion"),
        ("mittagessen-unbekannt", "contradicts"),
    } <= _failed_fields(result)
    assert "personendaten" in _rules(result)


def test_scorer_checks_n_units_and_negative_wording_in_surveys():
    case, atoms = _case("befragung")
    _atom(atoms, "F4")["signal"] = "positive"  # 64 % Zustimmung zu «zu lang»
    _atom(atoms, "F8")["text"] = "Eltern mit anderer Erstsprache: 36 % Zustimmung"  # ohne n
    _atom(atoms, "F1")["unit"] = "Prozent"
    result = ev.score_case(case, atoms)
    assert {
        ("f4-wartezeit", "signal"),
        ("f8-erstsprache", "text_has"),
        ("f1-frist", "unit"),
    } <= _failed_fields(result)


def test_unit_accepts_a_list_of_spellings():
    case, atoms = _case("interview-hort")
    for unit in ("CHF", "Franken pro Betreuungstag", "chf/tag"):
        _atom(atoms, "[09:26]")["unit"] = unit
        assert ("beitrag-23", "unit") not in _failed_fields(ev.score_case(case, atoms)), unit
    _atom(atoms, "[09:26]")["unit"] = "Tage"
    assert ("beitrag-23", "unit") in _failed_fields(ev.score_case(case, atoms))


def test_scorer_reads_irony_and_numbers_in_complaints():
    case, atoms = _case("beschwerde")
    _atom(atoms, "Zeile 14")["signal"] = "positive"  # Ironie
    _atom(atoms, "Zeile 10")["value"] = "1'236"  # Tausendertrennzeichen statt Zahl
    atoms.append(
        {**_atom(atoms, "Zeile 15"), "id": "bes-14", "text": "Sandra Imhof", "locator": "Zeile 20"}
    )
    result = ev.score_case(case, atoms)
    assert {("ironie", "signal"), ("mahnung-voll", "value")} <= _failed_fields(result)
    assert "personendaten" in _rules(result)


def test_bundle_holds_evidenz_and_prompt(tmp_path):
    case = CASES[0]
    bundle = ev.render_bundle(case)
    assert bundle.startswith("# Evidenz") and "# Auftrag" in bundle
    assert bundle.endswith(ev.render_prompt(case))
    # Schablone aus einer anderen evidenz.md
    other = tmp_path / "evidenz.md"
    other.write_text(
        ev.EVIDENZ_MD.read_text(encoding="utf-8").replace("Du extrahierst", "Extrahiere"),
        encoding="utf-8",
    )
    assert ev.main(["prompts", "-o", str(tmp_path / "p"), "--evidenz", str(other), "--bundle"]) == 0
    prompt = (tmp_path / "p" / f"{case.id}.prompt.md").read_text(encoding="utf-8")
    assert prompt.startswith("Extrahiere")
    assert (tmp_path / "p" / f"{case.id}.bundle.md").exists()


def test_compare_lists_runs_templates_and_missed_atoms(tmp_path):
    for name in ("a-1", "a-2", "b-1"):
        (tmp_path / name).mkdir()
        for case in CASES:
            atoms = _reference(case)
            if name == "b-1" and case.id == "interview-hort":
                atoms = [a for a in atoms if a["locator"] != "[02:58]"]  # Dritte übersehen
                _atom(atoms, "[04:30]")["value"] = 5
            (tmp_path / name / f"{case.id}.json").write_text(json.dumps(atoms), encoding="utf-8")
    (tmp_path / "a-2" / "befragung.json").unlink()  # Fall fehlt im Lauf
    out = tmp_path / "vergleich.md"
    assert (
        ev.main(["compare", *(str(tmp_path / n) for n in ("a-1", "a-2", "b-1")), "-o", str(out)])
        == 0
    )
    md = out.read_text(encoding="utf-8")
    assert "| a | 2 | 100% | 100% | 0.0 |" in md, "Schablone a: zwei Läufe, beide perfekt"
    assert "| interview-hort | schwiegermutter | ✓ | ✓ | – |" in md
    assert "| interview-hort | bescheid-sieben-wochen | ✓ | ✓ | value |" in md
    assert "| befragung | 12/12 · 69/69 · 0 | · | 12/12 · 69/69 · 0 |" in md
