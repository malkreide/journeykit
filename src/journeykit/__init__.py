"""JourneyKit: evidence-based User Journeys for public administration.

Modell vor Darstellung. Eine Journey ist eine JSON-Datei nach
``schema/journey.schema.json``; HTML, Story Map, Audit-Report und Diff werden
daraus erzeugt. Alles, was die Journey behauptet, verweist auf Evidenz-Atome.
"""

from __future__ import annotations

import json
from importlib import resources
from pathlib import Path
from typing import Any

__version__ = "0.1.0"

SCHEMA_VERSION = "1.0"


def schema_path() -> Path:
    """Pfad der mitgelieferten Schema-Datei."""
    return Path(str(resources.files("journeykit").joinpath("schema/journey.schema.json")))


def load_schema() -> dict[str, Any]:
    with schema_path().open(encoding="utf-8") as fh:
        return json.load(fh)


def load_journey(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as fh:
        return json.load(fh)
