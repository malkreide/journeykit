from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from journeykit.cli import scaffold

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_DIR = ROOT / "examples" / "kindergarteneintritt"


@pytest.fixture(scope="session")
def example_journey() -> dict:
    return json.loads((EXAMPLE_DIR / "journey.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def example_second_persona() -> dict:
    return json.loads((EXAMPLE_DIR / "journey-berufstaetig.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def example_hypothesis() -> dict:
    return json.loads((EXAMPLE_DIR / "workshop-hypothese.json").read_text(encoding="utf-8"))


@pytest.fixture
def minimal() -> dict:
    """Kleine, schema-valide Journey mit einer Quelle und einem Primärbeleg - zum Mutieren in Tests."""
    j = scaffold("test-journey", "Testjourney", "Testperson", "Elternteil", "Ziel erreichen")
    j["meta"]["status"] = "draft"
    j["sources"] = [
        {
            "id": "int-1",
            "title": "Interview 1",
            "kind": "interview",
            "default_class": "reported",
            "pii_status": "anonymised",
            "n": 1,
        },
        {
            "id": "doc-1",
            "title": "Prozessdokument",
            "kind": "internal_document",
            "default_class": "assumed",
            "pii_status": "none",
        },
    ]
    j["evidence"] = [
        {
            "id": "ev-1",
            "source_ref": "int-1",
            "class": "reported",
            "kind": "quote",
            "text": "Ich wusste nicht, was ich tun muss.",
            "locator": "Zeile 3",
            "emotion_hint": {"valence": -1, "label": "unsicher", "explicit": True},
        },
        {
            "id": "ev-2",
            "source_ref": "int-1",
            "class": "reported",
            "kind": "quote",
            "text": "Dann habe ich angerufen.",
            "locator": "Zeile 5",
        },
        {
            "id": "ev-3",
            "source_ref": "int-1",
            "class": "reported",
            "kind": "quote",
            "text": "Am Ende hat es geklappt.",
            "locator": "Zeile 9",
        },
        {
            "id": "ev-4",
            "source_ref": "doc-1",
            "class": "assumed",
            "kind": "document_excerpt",
            "text": "Alle erhalten den Brief rechtzeitig.",
        },
    ]
    j["persona"]["evidence_refs"] = ["ev-1", "ev-2", "ev-3"]
    j["persona"]["is_hypothesis"] = False
    step = j["phases"][0]["steps"][0]
    step["name"] = "Brief erhalten"
    step["action"] = "Die Persona erhält einen Brief."
    step["channel"] = "letter"
    step["thinking"] = [{"text": "Muss ich etwas tun?", "evidence_refs": ["ev-1"]}]
    step["feeling"] = {"valence": -1, "label": "unsicher", "evidence_refs": ["ev-1"]}
    step["pain_points"] = [
        {
            "id": "pp-1",
            "text": "Brief unklar",
            "type": "breakdown",
            "severity": 4,
            "owner": "Kommunikation",
            "status": "open",
            "evidence_refs": ["ev-1", "ev-2"],
        },
    ]
    step["recovery_paths"] = [
        {"trigger": "Brief unklar", "path": "Anruf", "evidence_refs": ["ev-2"]}
    ]
    j["opportunities"] = [
        {
            "id": "opp-1",
            "hmw": "Wie könnten wir den Brief klarer machen?",
            "linked_pain_points": ["pp-1"],
            "phase_ref": "phase-1",
            "user_impact": 4,
            "public_value": 3,
            "effort": 2,
            "status": "open",
            "stories": [{"text": "Als Elternteil möchte ich …", "mvp": True}],
        },
    ]
    j["scenario"]["scope_exclusions"] = ["Privatschulen"]
    j["meta"]["diagnosis"] = {"rationale": "Front-Stage-Erleben der Eltern."}
    return copy.deepcopy(j)
