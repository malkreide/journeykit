from __future__ import annotations

from journeykit import load_schema
from journeykit.cli import scaffold
from journeykit.validate import is_valid, validate_journey


def test_schema_is_draft_2020_12():
    assert load_schema()["$schema"].endswith("2020-12/schema")


def test_scaffold_is_valid():
    j = scaffold("x-y", "Titel", "Persona", "Rolle", "Ziel")
    assert validate_journey(j) == []


def test_examples_are_valid(example_journey, example_second_persona, example_hypothesis):
    for j in (example_journey, example_second_persona, example_hypothesis):
        assert validate_journey(j) == [], j["meta"]["id"]


def test_missing_required_block_fails(minimal):
    del minimal["persona"]
    errors = validate_journey(minimal)
    assert errors and "persona" in errors[0].message


def test_additional_properties_rejected(minimal):
    minimal["phases"][0]["steps"][0]["emotion"] = "happy"
    assert not is_valid(minimal)


def test_evidence_class_enum(minimal):
    minimal["evidence"][0]["class"] = "guessed"
    errors = validate_journey(minimal)
    assert any("guessed" in e.message for e in errors)


def test_feeling_null_allowed(minimal):
    minimal["phases"][0]["steps"][0]["feeling"] = None
    assert is_valid(minimal)


def test_valence_range(minimal):
    minimal["phases"][0]["steps"][0]["feeling"]["valence"] = 3
    assert not is_valid(minimal)


def test_id_pattern(minimal):
    minimal["phases"][0]["id"] = "Phase 1"
    assert not is_valid(minimal)


def test_publication_channel_and_case_records_kind(minimal):
    minimal["phases"][0]["steps"][0]["channel"] = "publication"
    minimal["sources"][0]["kind"] = "case_records"
    assert is_valid(minimal)


def test_performed_by(minimal):
    step = minimal["phases"][0]["steps"][0]
    step["performed_by"] = {
        "kind": "intermediary",
        "role": "Installationsfirma",
        "mandate": "formal",
    }
    assert is_valid(minimal)
    step["performed_by"] = {"kind": "persona"}
    assert is_valid(minimal)


def test_performed_by_requires_role_and_mandate_for_third_parties(minimal):
    step = minimal["phases"][0]["steps"][0]
    step["performed_by"] = {"kind": "shared", "role": "Nachbarin"}
    assert not is_valid(minimal)
    step["performed_by"] = {"kind": "persona", "role": "Persona selbst"}
    assert not is_valid(minimal)
    step["performed_by"] = {"kind": "authority", "role": "Bauamt", "mandate": "formal"}
    assert not is_valid(minimal)


def test_duration_days(minimal):
    phase = minimal["phases"][0]
    phase["duration_days"] = {
        "typical": 38,
        "min": 14,
        "max": 112,
        "basis": "Median",
        "evidence_refs": ["ev-1"],
    }
    assert is_valid(minimal)


def test_duration_days_requires_evidence_and_positive_typical(minimal):
    phase = minimal["phases"][0]
    phase["duration_days"] = {"typical": 38}
    assert not is_valid(minimal)
    phase["duration_days"] = {"typical": 38, "evidence_refs": []}
    assert not is_valid(minimal)
    phase["duration_days"] = {"typical": 0, "evidence_refs": ["ev-1"]}
    assert not is_valid(minimal)
    phase["duration_days"] = {"typical": 3, "unit": "weeks", "evidence_refs": ["ev-1"]}
    assert not is_valid(minimal)
