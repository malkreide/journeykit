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


def test_no_user_source_is_warn(minimal):
    for src in minimal["sources"]:
        src["kind"] = "internal_document"
    assert "L011" in codes(lint_journey(minimal, today=TODAY), WARN)


def test_case_records_count_as_user_source(minimal):
    minimal["sources"][0]["kind"] = "case_records"
    minimal["sources"][1]["kind"] = "internal_document"
    assert "L011" not in codes(lint_journey(minimal, today=TODAY))


def test_dangling_reference_is_error(minimal):
    minimal["phases"][0]["steps"][0]["thinking"][0]["evidence_refs"] = ["gibt-es-nicht"]
    findings = lint_journey(minimal, today=TODAY)
    assert "L001" in codes(findings, ERROR)


def test_duplicate_id_is_error(minimal):
    minimal["evidence"][1]["id"] = "ev-1"
    assert "L002" in codes(lint_journey(minimal, today=TODAY), ERROR)


def test_dangling_duration_reference_is_error(minimal):
    minimal["phases"][0]["duration_days"] = {"typical": 5, "evidence_refs": ["gibt-es-nicht"]}
    assert "L001" in codes(lint_journey(minimal, today=TODAY), ERROR)


def test_contradictory_duration_is_error(minimal):
    minimal["phases"][0]["duration_days"] = {"typical": 38, "max": 20, "evidence_refs": ["ev-1"]}
    assert "L003" in codes(lint_journey(minimal, today=TODAY), ERROR)
    minimal["phases"][0]["duration_days"] = {"typical": 38, "min": 40, "evidence_refs": ["ev-1"]}
    assert "L003" in codes(lint_journey(minimal, today=TODAY), ERROR)


def test_consistent_duration_is_clean(minimal):
    minimal["phases"][0]["duration_days"] = {
        "typical": 38,
        "min": 38,
        "max": 112,
        "evidence_refs": ["ev-1"],
    }
    findings = lint_journey(minimal, today=TODAY)
    assert {"L001", "L003"}.isdisjoint(codes(findings))


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


def test_audit_transfer_is_not_primary_evidence(minimal):
    # Audit-Übertrag nach SKILL.md: Die Vorlage ist eine Quelle «assumed»,
    # jede übertragene Stelle ein Atom mit Fundstelle. Das darf keine
    # Primärevidenz vortäuschen, auch wenn sich die Vorlage auf Interviews beruft.
    minimal["sources"] = [
        {
            "id": "vorlage",
            "title": "Bestehende Journey Map (Bild)",
            "kind": "internal_document",
            "default_class": "assumed",
            "pii_status": "none",
            "notes": "Nennt zwölf Interviews, legt sie nicht bei.",
        }
    ]
    minimal["evidence"] = [
        {
            "id": f"map-{i}",
            "source_ref": "vorlage",
            "class": "assumed",
            "kind": "document_excerpt",
            "text": text,
            "locator": f"Phase 1, Spalte 1, Zeile {row}",
        }
        for i, (text, row) in enumerate(
            [("Muss ich etwas tun?", "Gedanken"), ("unsicher", "Gefühle"), ("Anruf", "Aktivität")]
        )
    ]
    minimal["persona"]["evidence_refs"] = []
    step = minimal["phases"][0]["steps"][0]
    step["thinking"][0]["evidence_refs"] = ["map-0"]
    step["feeling"]["evidence_refs"] = ["map-1"]
    step["pain_points"][0]["evidence_refs"] = ["map-2"]
    step["recovery_paths"][0]["evidence_refs"] = ["map-2"]
    assert is_valid(minimal)
    findings = lint_journey(minimal, today=TODAY)
    assert "L001" not in codes(findings)
    assert "L010" in codes(findings, ERROR)
    assert {"L011", "L012"} <= codes(findings, WARN)


def _without_experience(journey):
    step = journey["phases"][0]["steps"][0]
    step["thinking"] = []
    step["feeling"] = None
    step["pain_points"] = []
    step["recovery_paths"] = []
    journey["opportunities"][0].pop("linked_pain_points")
    return journey


def test_no_experience_claims_at_all(minimal):
    # Ohne jede Erlebnis-Aussage gibt es keine Quote – L010 meldet die Leere selbst.
    f = lint_journey(_without_experience(minimal), today=TODAY)
    hit = [x for x in f if x.code == "L010"]
    assert len(hit) == 1 and hit[0].level == WARN
    assert hit[0].message.startswith("Keine einzige Erlebnis-Aussage")
    minimal["meta"]["status"] = "hypothesis"
    assert "L010" in codes(lint_journey(minimal, today=TODAY), INFO)


def test_no_breakdown_is_error_unless_hypothesis(minimal):
    minimal["phases"][0]["steps"][0]["pain_points"][0]["type"] = "friction"
    minimal["opportunities"][0]["linked_pain_points"] = ["pp-1"]
    assert "L020" in codes(lint_journey(minimal, today=TODAY), ERROR)
    minimal["meta"]["status"] = "hypothesis"
    assert "L020" in codes(lint_journey(minimal, today=TODAY), WARN)


def test_no_breakdown_in_to_be_concept_is_info(minimal):
    minimal["phases"][0]["steps"][0]["pain_points"][0]["type"] = "friction"
    minimal["opportunities"][0]["linked_pain_points"] = ["pp-1"]
    minimal["scenario"]["perspective"] = "to_be"
    hit = [f for f in lint_journey(minimal, today=TODAY) if f.code == "L020"]
    assert [f.level for f in hit] == [INFO]
    assert hit[0].message.startswith("Soll-Konzept ohne Breakdown")
    minimal["scenario"]["perspective"] = "as_is"
    assert "L020" in codes(lint_journey(minimal, today=TODAY), ERROR)


def test_breakdown_without_recovery_warns(minimal):
    minimal["phases"][0]["steps"][0]["recovery_paths"] = []
    assert "L022" in codes(lint_journey(minimal, today=TODAY), WARN)


def test_counterpart_change_without_transition_is_info(minimal):
    first = minimal["phases"][0]["steps"][0]
    first["channel"] = "web"
    first["counterpart"] = "Gemeinde"
    second = {
        "id": "step-1-2",
        "name": "Link zum Kanton",
        "action": "Die Persona folgt dem Link zur kantonalen Website.",
        "channel": "web",
        "counterpart": "Kanton",
        "feeling": None,
    }
    minimal["phases"][0]["steps"].append(second)
    f = lint_journey(minimal, today=TODAY)
    hit = [x for x in f if x.code == "L023"]
    assert len(hit) == 1 and hit[0].level == INFO
    assert "«Gemeinde» → «Kanton»" in hit[0].message
    second["counterpart"] = " gemeinde "  # gleiche Stelle, nur anders geschrieben
    assert "L023" not in codes(lint_journey(minimal, today=TODAY))
    second["counterpart"] = "Kanton"
    second["is_transition"] = True
    assert "L023" not in codes(lint_journey(minimal, today=TODAY))
    second["is_transition"] = False
    second["channel"] = "phone"  # Kanal- und Stellenwechsel: eine Meldung, nicht zwei
    hit = [x for x in lint_journey(minimal, today=TODAY) if x.code == "L023"]
    assert len(hit) == 1 and "web → phone" in hit[0].message


def test_static_map_rules(minimal):
    del minimal["meta"]["owner"]
    del minimal["meta"]["review_cycle_days"]
    minimal["meta"]["next_review"] = "2020-01-01"
    f = lint_journey(minimal, today=TODAY)
    assert {"L030", "L031", "L032"} <= codes(f, WARN)


def test_missing_date_is_info(minimal):
    assert "L035" not in codes(lint_journey(minimal, today=TODAY))
    del minimal["meta"]["created"]
    assert "L035" not in codes(lint_journey(minimal, today=TODAY))  # updated genügt
    del minimal["meta"]["updated"]
    assert "L035" in codes(lint_journey(minimal, today=TODAY), INFO)


def test_severe_pain_point_without_owner_or_opportunity(minimal):
    pp = minimal["phases"][0]["steps"][0]["pain_points"][0]
    del pp["owner"]
    minimal["opportunities"] = []
    f = lint_journey(minimal, today=TODAY)
    assert "L033" in codes(f, WARN)
    assert "L060" in codes(f, WARN)


def test_missing_end_state_is_info(minimal):
    minimal["scenario"]["end_state"] = "Das Kind ist angemeldet."
    assert "L053" not in codes(lint_journey(minimal, today=TODAY))
    minimal["scenario"]["end_state"] = "  "
    assert "L053" in codes(lint_journey(minimal, today=TODAY), INFO)
    del minimal["scenario"]["end_state"]
    assert "L053" in codes(lint_journey(minimal, today=TODAY), INFO)


def test_missing_trigger_is_info(minimal):
    minimal["scenario"]["trigger"] = "Ein Hinweis aus dem Bekanntenkreis."
    assert "L054" not in codes(lint_journey(minimal, today=TODAY))
    minimal["scenario"]["trigger"] = " "
    assert "L054" in codes(lint_journey(minimal, today=TODAY), INFO)
    del minimal["scenario"]["trigger"]
    assert "L054" in codes(lint_journey(minimal, today=TODAY), INFO)


def test_opportunity_without_anchor(minimal):
    opp = minimal["opportunities"][0]
    del opp["linked_pain_points"]
    assert "L064" not in codes(lint_journey(minimal, today=TODAY))  # phase_ref genügt
    del opp["phase_ref"]
    f = lint_journey(minimal, today=TODAY)
    assert "L064" in codes(f, WARN)
    assert next(x for x in f if x.code == "L064").message.endswith("opp-1.")
    minimal["meta"]["status"] = "hypothesis"
    assert "L064" in codes(lint_journey(minimal, today=TODAY), INFO)
    opp["step_ref"] = "step-1-1"
    assert "L064" not in codes(lint_journey(minimal, today=TODAY))  # step_ref genügt


def test_opportunity_step_ref_integrity(minimal):
    opp = minimal["opportunities"][0]
    opp["step_ref"] = "gibt-es-nicht"
    hit = [f for f in lint_journey(minimal, today=TODAY) if f.code == "L001"]
    assert [f.message for f in hit] == [
        "Chance «opp-1» verweist auf unbekannten Schritt «gibt-es-nicht»."
    ]
    minimal["phases"].append(
        {
            "id": "phase-2",
            "name": "Danach",
            "steps": [{"id": "step-2-1", "name": "Nachfragen", "action": "Ruft an."}],
        }
    )
    opp["step_ref"] = "step-2-1"  # phase_ref bleibt phase-1
    hit = [f for f in lint_journey(minimal, today=TODAY) if f.code == "L001"]
    assert [f.message for f in hit] == [
        "Chance «opp-1»: Schritt «step-2-1» liegt nicht in Phase «phase-1»."
    ]
    del opp["phase_ref"]
    assert "L001" not in codes(lint_journey(minimal, today=TODAY))


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
