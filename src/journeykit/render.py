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
# Sprachen der Viewer-Oberfläche (Block «jk-i18n» in viewer.html); die Lint-Meldungen
# im Tab «Prüfung» folgen derselben Sprache. Die Inhalte der Journey bleiben, wie sie sind.
UI_LANGUAGES = ("de", "fr")


def ui_language(journeys: list[dict[str, Any]], lang: str | None = None) -> str:
    """Sprache der Oberfläche: ausdrücklich gewählt, sonst die der ersten Journey, sonst Deutsch."""
    if lang is not None:
        if lang not in UI_LANGUAGES:
            raise ValueError(
                f"Keine Viewer-Oberfläche für «{lang}» – verfügbar: {', '.join(UI_LANGUAGES)}."
            )
        return lang
    meta_lang = journeys[0].get("meta", {}).get("language")
    return meta_lang if meta_lang in UI_LANGUAGES else "de"


def viewer_template() -> str:
    return resources.files("journeykit").joinpath("viewer/viewer.html").read_text(encoding="utf-8")


def _safe_json(data: Any) -> str:
    # </script> in Nutzertexten darf das Script-Tag nicht beenden.
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def render_html(
    journeys: list[dict[str, Any]],
    findings: list[list[Finding]] | None = None,
    title: str | None = None,
    lang: str | None = None,
) -> str:
    """HTML für eine oder mehrere Journeys (mehrere = Multi-Persona-Vergleich)."""
    if not journeys:
        raise ValueError("Mindestens eine Journey nötig.")
    ui_lang = ui_language(journeys, lang)
    if findings is None:
        findings = [lint_journey(j, lang=ui_lang) for j in journeys]
    payload = {
        "generator": f"journeykit {__version__}",
        "generated": date.today().isoformat(),
        "title": title or journeys[0]["meta"]["title"],
        "lang": ui_lang,
        "journeys": journeys,
        "findings": [[f.as_dict() for f in fs] for fs in findings],
    }
    html = viewer_template()
    if PLACEHOLDER not in html:
        raise RuntimeError("Viewer-Template ohne Datenplatzhalter.")
    return html.replace(PLACEHOLDER, _safe_json(payload), 1)
