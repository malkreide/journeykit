"""Exporte aus dem Journey-Modell: Story Map, Massnahmenliste, Audit-Report.

Alle Exporte sind Text (Markdown oder CSV), damit sie in Tickets, Notion,
Wikis oder Protokolle wandern können - dort, wo Massnahmen tatsächlich leben.
"""

from __future__ import annotations

import csv
import io
from typing import Any

from .lint import ANTIPATTERNS, Finding, summarize
from .model import JourneyIndex, priority_quadrant

QUADRANT_LABELS = {
    "quick_win": "Quick Win",
    "big_bet": "Big Bet",
    "fill_in": "Nebenbei",
    "skip": "Zurückstellen",
}


def _opps_by_phase(idx: JourneyIndex) -> dict[str | None, list[dict[str, Any]]]:
    out: dict[str | None, list[dict[str, Any]]] = {}
    for opp in idx.opportunities.values():
        phase = opp.get("phase_ref")
        if not phase and opp.get("linked_pain_points"):
            step = idx.pain_point_step.get(opp["linked_pain_points"][0])
            phase = idx.step_phase.get(step) if step else None
        out.setdefault(phase, []).append(opp)
    return out


def _rank(opp: dict[str, Any]) -> tuple[int, int]:
    order = {"quick_win": 0, "big_bet": 1, "fill_in": 2, "skip": 3, None: 4}
    return order[priority_quadrant(opp)], -(opp.get("user_impact") or 0)


def story_map_markdown(journey: dict[str, Any]) -> str:
    """Patton-Story-Map: Phasen horizontal (Backbone), Stories vertikal priorisiert, MVP-Linie."""
    idx = JourneyIndex.build(journey)
    by_phase = _opps_by_phase(idx)
    lines = [f"# Story Map: {journey['meta']['title']}", ""]
    lines.append(
        f"Persona: **{journey['persona']['name']}** ({journey['persona']['role']}) · Ziel: {journey['scenario']['goal']}"
    )
    lines.append("")
    lines.append("## Backbone (Nutzeraktivitäten)")
    lines.append("")
    lines.append("| " + " | ".join(p["name"] for p in journey["phases"]) + " |")
    lines.append("|" + "---|" * len(journey["phases"]))
    lines.append(
        "| "
        + " | ".join("<br>".join(f"• {s['name']}" for s in p["steps"]) for p in journey["phases"])
        + " |"
    )
    lines.append("")
    lines.append("## Stories je Phase (oben = wichtigste; ✅ = MVP-Schnitt)")
    lines.append("")
    for phase in journey["phases"]:
        opps = sorted(by_phase.get(phase["id"], []), key=_rank)
        lines.append(f"### {phase['name']}")
        if not opps:
            lines.append("_Keine Chancen abgeleitet._")
            lines.append("")
            continue
        for opp in opps:
            q = priority_quadrant(opp)
            tag = f" `{QUADRANT_LABELS[q]}`" if q else ""
            lines.append(f"**{opp['hmw']}**{tag}")
            for story in opp.get("stories", []):
                mark = "✅" if story.get("mvp") else "◻️"
                lines.append(f"- {mark} {story['text']}")
            if not opp.get("stories"):
                lines.append("- _(noch keine Stories)_")
            lines.append("")
    unassigned = by_phase.get(None, [])
    if unassigned:
        lines.append("### Ohne Phasenbezug")
        for opp in unassigned:
            lines.append(f"- {opp['hmw']}")
        lines.append("")
    return "\n".join(lines)


def actions_csv(journey: dict[str, Any]) -> str:
    """Massnahmenliste: ein Pain Point pro Zeile mit Owner, Status, Evidenzlage und verknüpften Chancen."""
    idx = JourneyIndex.build(journey)
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=";", lineterminator="\n")
    w.writerow(
        [
            "phase",
            "step",
            "pain_point_id",
            "type",
            "severity",
            "frequency",
            "text",
            "workaround",
            "owner",
            "status",
            "evidence_primary",
            "evidence_assumed",
            "opportunities",
        ]
    )
    for phase in journey["phases"]:
        for step in phase["steps"]:
            for pp in step.get("pain_points", []):
                classes = [
                    idx.evidence[r]["class"]
                    for r in pp.get("evidence_refs", [])
                    if r in idx.evidence
                ]
                primary = sum(1 for c in classes if c in ("observed", "reported"))
                assumed = sum(1 for c in classes if c == "assumed")
                opps = ", ".join(o["id"] for o in idx.opportunity_for_pain_point(pp["id"]))
                w.writerow(
                    [
                        phase["name"],
                        step["name"],
                        pp["id"],
                        pp["type"],
                        pp.get("severity", ""),
                        pp.get("frequency", ""),
                        pp["text"],
                        pp.get("workaround", ""),
                        pp.get("owner", ""),
                        pp.get("status", ""),
                        primary,
                        assumed,
                        opps,
                    ]
                )
    return buf.getvalue()


def opportunities_markdown(journey: dict[str, Any]) -> str:
    """Priorisierungsmatrix: Chancen nach Quadrant."""
    idx = JourneyIndex.build(journey)
    lines = [f"# Chancen und Priorisierung: {journey['meta']['title']}", ""]
    lines.append(
        "| Quadrant | Chance | Impact | Public Value | Aufwand | Pain Points | Owner | Status |"
    )
    lines.append("|---|---|---|---|---|---|---|---|")
    for opp in sorted(idx.opportunities.values(), key=_rank):
        q = priority_quadrant(opp)
        lines.append(
            f"| {QUADRANT_LABELS.get(q, '–')} | {opp['hmw']} | {opp.get('user_impact', '–')} | {opp.get('public_value', '–')} | {opp.get('effort', '–')} | {', '.join(opp.get('linked_pain_points', [])) or '–'} | {opp.get('owner', '–')} | {opp.get('status', '–')} |"
        )
    lines.append("")
    lines.append(
        "Quadranten: Quick Win = hoher Wert, Aufwand ≤ 2 · Big Bet = hoher Wert, Aufwand ≥ 3 · Nebenbei = geringer Wert, geringer Aufwand · Zurückstellen = geringer Wert, hoher Aufwand."
    )
    return "\n".join(lines)


def audit_markdown(journey: dict[str, Any], findings: list[Finding]) -> str:
    """Audit-Report: Evidenzlage, Befunde je Anti-Pattern, nächste Schritte."""
    idx = JourneyIndex.build(journey)
    meta = journey["meta"]
    ev = idx.evidence_summary()
    counts = summarize(findings)
    lines = [f"# Audit: {meta['title']}", ""]
    lines.append(
        f"Version {meta['version']} · Status `{meta['status']}` · Typ `{meta['map_type']}`"
    )
    if meta.get("synthetic"):
        lines.append("")
        lines.append("> Synthetisches Beispiel: Quellen und Evidenz sind erfunden.")
    lines.append("")
    lines.append("## Evidenzlage")
    lines.append("")
    lines.append(
        f"- Quellen: {len(idx.sources)} ({', '.join(sorted({s['kind'] for s in idx.sources.values()})) or '–'})"
    )
    lines.append(
        f"- Evidenz-Atome: {ev['total']} · beobachtet {ev['observed']} · berichtet {ev['reported']} · angenommen {ev['assumed']}"
    )
    experience = [c for c in idx.claims() if c.kind in {"thinking", "feeling", "pain_point"}]
    backed = sum(1 for c in experience if idx.has_primary(c.evidence_refs))
    if experience:
        lines.append(
            f"- Erlebnis-Aussagen mit Primärevidenz: {backed}/{len(experience)} ({backed / len(experience):.0%})"
        )
    lines.append(
        f"- Breakdowns: {len(idx.breakdowns())} · Pain Points gesamt: {len(idx.pain_points)} · Chancen: {len(idx.opportunities)}"
    )
    lines.append("")
    lines.append(
        f"## Befunde: {counts['ERROR']} Fehler · {counts['WARN']} Warnungen · {counts['INFO']} Hinweise"
    )
    lines.append("")
    by_ap: dict[str, list[Finding]] = {}
    for f in findings:
        by_ap.setdefault(f.antipattern, []).append(f)
    for ap, label in ANTIPATTERNS.items():
        items = by_ap.get(ap)
        if not items:
            continue
        lines.append(f"### {label}")
        lines.append("")
        for f in items:
            where = f" (`{f.path}`)" if f.path else ""
            lines.append(f"- **{f.level}** {f.code}{where}: {f.message}")
            if f.hint:
                lines.append(f"  - → {f.hint}")
        lines.append("")
    if not findings:
        lines.append("Keine Befunde.")
        lines.append("")
    oq = journey.get("open_questions", [])
    if oq:
        lines.append("## Offene Fragen")
        lines.append("")
        for q in oq:
            method = f" _(Methode: {q['proposed_method']})_" if q.get("proposed_method") else ""
            lines.append(f"- {q['text']}{method}")
        lines.append("")
    return "\n".join(lines)
