"""HTML-Rendering: Journey-Modell(e) in den eigenständigen Viewer injizieren.

Der Viewer (``viewer/viewer.html``) ist eine Single-File-App ohne externe
Abhängigkeiten. Der Renderer ersetzt genau einen Platzhalter durch die Daten:
eine Liste von Journeys (eine pro Persona) plus Lint-Befunde und Metadaten.
"""

from __future__ import annotations

import json
from datetime import date
from importlib import resources
from typing import Any

from . import __version__
from .lint import Finding, lint_journey

PLACEHOLDER = "/*__JOURNEYKIT_DATA__*/null"


def viewer_template() -> str:
    return resources.files("journeykit").joinpath("viewer/viewer.html").read_text(encoding="utf-8")


def _safe_json(data: Any) -> str:
    # </script> in Nutzertexten darf das Script-Tag nicht beenden.
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def render_html(
    journeys: list[dict[str, Any]],
    findings: list[list[Finding]] | None = None,
    title: str | None = None,
) -> str:
    """HTML für eine oder mehrere Journeys (mehrere = Multi-Persona-Vergleich)."""
    if not journeys:
        raise ValueError("Mindestens eine Journey nötig.")
    if findings is None:
        findings = [lint_journey(j) for j in journeys]
    payload = {
        "generator": f"journeykit {__version__}",
        "generated": date.today().isoformat(),
        "title": title or journeys[0]["meta"]["title"],
        "journeys": journeys,
        "findings": [[f.as_dict() for f in fs] for fs in findings],
    }
    html = viewer_template()
    if PLACEHOLDER not in html:
        raise RuntimeError("Viewer-Template ohne Datenplatzhalter.")
    return html.replace(PLACEHOLDER, _safe_json(payload), 1)
