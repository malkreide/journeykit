from __future__ import annotations

from datetime import date

from journeykit.lint import ERROR, INFO, WARN, lint_journey, summarize, worst_level
from journeykit.validate import is_valid

TODAY = date(2026, 10, 5)


def codes(findings, level=None):
    return {f.code for f in findings if level is None or f.level == level}


def test_minimal_fixture_is_clean(minimal):
    assert is_valid(minimal)
    findings = lint_journey(minimal, today=TODAY)
    assert codes(findings, ERROR) == set()
    assert codes(findings, WARN) == set(), [str(f) for f in findings if f.level == WARN]


def test_dangling_reference_is_error(minimal):
    minimal["phases"][0]["steps"][0]["thinking"][0]["evidence_refs"] = ["gibt-es-nicht"]
    findings = lint_journey(minimal, today=TODAY)
    assert "L001" in codes(findings, ERROR)


def test_duplicate_id_is_error(minimal):
    minimal["evidence"][1]["id"] = "ev-1"
    assert "L002" in codes(lint_journey(minimal, today=TODAY), ERROR)


def test_all_assumed_with_validated_status_is_error(minimal):
    for atom in minimal["evidence"]:
        atom["class"] = "assumed"
    minimal["meta"]["status"] = "validated"
    findings = lint_journey(minimal, today=TODAY)
    assert "L010" in codes(findings, ERROR)


def test_all_assumed_with_hypothesis_status_is_info(minimal):
    for atom in minimal["evidence"]:
        atom["class"] = "assumed"
    minimal["meta"]["status"] = "hypothesis"
    findings = lint_journey(minimal, today=TODAY)
    assert "L010" in codes(findings, INFO)
    assert "L010" not in codes(findings, ERROR)


def test_no_breakdown_is_error_unless_hypothesis(minimal):
    minimal["phases"][0]["steps"][0]["pain_points"][0]["type"] = "friction"
    minimal["opportunities"][0]["linked_pain_points"] = ["pp-1"]
    assert "L020" in codes(lint_journey(minimal, today=TODAY), ERROR)
    minimal["meta"]["status"] = "hypothesis"
    assert "L020" in codes(lint_journey(minimal, today=TODAY), WARN)


def test_breakdown_without_recovery_warns(minimal):
    minimal["phases"][0]["steps"][0]["recovery_paths"] = []
    assert "L022" in codes(lint_journey(minimal, today=TODAY), WARN)


def test_static_map_rules(minimal):
    del minimal["meta"]["owner"]
    del minimal["meta"]["review_cycle_days"]
    minimal["meta"]["next_review"] = "2020-01-01"
    f = lint_journey(minimal, today=TODAY)
    assert {"L030", "L031", "L032"} <= codes(f, WARN)


def test_severe_pain_point_without_owner_or_opportunity(minimal):
    pp = minimal["phases"][0]["steps"][0]["pain_points"][0]
    del pp["owner"]
    minimal["opportunities"] = []
    f = lint_journey(minimal, today=TODAY)
    assert "L033" in codes(f, WARN)
    assert "L060" in codes(f, WARN)


def test_empathy_vacuum(minimal):
    step = minimal["phases"][0]["steps"][0]
    step["feeling"] = None
    step["thinking"] = []
    f = lint_journey(minimal, today=TODAY)
    assert {"L040", "L041"} <= codes(f, WARN)


def test_feeling_without_evidence_is_info(minimal):
    minimal["phases"][0]["steps"][0]["feeling"]["evidence_refs"] = []
    assert "L042" in codes(lint_journey(minimal, today=TODAY), INFO)


def test_blueprint_smell(minimal):
    del minimal["meta"]["diagnosis"]
    minimal["phases"][0]["steps"][0]["backstage_notes"] = ["a", "b", "c"]
    f = lint_journey(minimal, today=TODAY)
    assert {"L070", "L071"} <= codes(f, WARN)


def _all_steps(journey):
    return [s for p in journey["phases"] for s in p["steps"]]


def test_mostly_delegated_steps_are_info(minimal):
    actor = {"kind": "intermediary", "role": "Installationsfirma", "mandate": "formal"}
    for s in _all_steps(minimal):
        s["performed_by"] = dict(actor)
    assert "L073" in codes(lint_journey(minimal, today=TODAY), INFO)


def test_half_delegated_steps_are_not_flagged(minimal):
    first = minimal["phases"][0]["steps"][0]
    second = {"id": "zweiter-schritt", "name": "Zweiter Schritt", "action": "Die Persona wartet."}
    minimal["phases"][0]["steps"].append(second)
    first["performed_by"] = {
        "kind": "intermediary",
        "role": "Installationsfirma",
        "mandate": "formal",
    }
    second["performed_by"] = {"kind": "shared", "role": "Nachbarin", "mandate": "informal"}
    assert "L073" not in codes(
        lint_journey(minimal, today=TODAY), INFO
    )  # 1 von 2 ist nicht mehr als die Hälfte


def test_pii(minimal):
    minimal["sources"][0]["pii_status"] = "contains_pii"
    minimal["evidence"][1]["text"] = "Rufen Sie mich an: 044 123 45 67"
    f = lint_journey(minimal, today=TODAY)
    assert "L080" in codes(f, ERROR)
    assert "L081" in codes(f, WARN)


def test_commercial_kpi_hint(minimal):
    minimal["phases"][0]["kpis"] = [
        {"name": "Conversion Rate", "category": "outcome", "indicator_type": "lagging"}
    ]
    f = lint_journey(minimal, today=TODAY)
    assert {"L091", "L092"} <= codes(f, INFO)


def test_unused_and_contradicting_evidence_are_info(minimal):
    minimal["evidence"][3]["contradicts"] = ["ev-1"]
    f = lint_journey(minimal, today=TODAY)
    assert "L100" in codes(f, INFO)  # ev-4 wird nirgends referenziert
    assert "L101" in codes(f, INFO)


def test_workshop_hypothesis_shows_inside_out_as_info(example_hypothesis):
    f = lint_journey(example_hypothesis, today=TODAY)
    assert summarize(f)[ERROR] == 0
    assert "L010" in codes(f, INFO)


def test_worst_level():
    assert worst_level([]) is None
    f = lint_journey(
        {
            "meta": {"status": "draft", "map_type": "user_journey"},
            "persona": {"name": "x", "evidence_refs": []},
            "scenario": {},
            "phases": [],
            "sources": [],
            "evidence": [],
            "opportunities": [],
        },
        today=TODAY,
    )
    assert worst_level(f) in {ERROR, WARN}
