"""Diff zweier Journey-Versionen: Was hat sich am Modell geändert?

Gegen die Static Map Trap: Neue Evidenz soll die Journey verändern, und die
Veränderung soll sichtbar sein - nicht als neue Datei, sondern als Delta.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .model import JourneyIndex


@dataclass
class JourneyDiff:
    old_version: str
    new_version: str
    added_steps: list[str] = field(default_factory=list)
    removed_steps: list[str] = field(default_factory=list)
    added_pain_points: list[str] = field(default_factory=list)
    removed_pain_points: list[str] = field(default_factory=list)
    changed_pain_point_status: list[tuple[str, str | None, str | None]] = field(
        default_factory=list
    )
    added_opportunities: list[str] = field(default_factory=list)
    removed_opportunities: list[str] = field(default_factory=list)
    changed_opportunity_status: list[tuple[str, str | None, str | None]] = field(
        default_factory=list
    )
    feeling_changes: list[tuple[str, int | None, int | None]] = field(default_factory=list)
    evidence_delta: dict[str, int] = field(default_factory=dict)
    added_sources: list[str] = field(default_factory=list)

    def is_empty(self) -> bool:
        return not any(
            [
                self.added_steps,
                self.removed_steps,
                self.added_pain_points,
                self.removed_pain_points,
                self.changed_pain_point_status,
                self.added_opportunities,
                self.removed_opportunities,
                self.changed_opportunity_status,
                self.feeling_changes,
                any(self.evidence_delta.values()),
                self.added_sources,
            ]
        )


def diff_journeys(old: dict[str, Any], new: dict[str, Any]) -> JourneyDiff:
    a, b = JourneyIndex.build(old), JourneyIndex.build(new)
    d = JourneyDiff(old["meta"]["version"], new["meta"]["version"])
    d.added_steps = sorted(set(b.steps) - set(a.steps))
    d.removed_steps = sorted(set(a.steps) - set(b.steps))
    d.added_pain_points = sorted(set(b.pain_points) - set(a.pain_points))
    d.removed_pain_points = sorted(set(a.pain_points) - set(b.pain_points))
    for pid in sorted(set(a.pain_points) & set(b.pain_points)):
        s_old, s_new = a.pain_points[pid].get("status"), b.pain_points[pid].get("status")
        if s_old != s_new:
            d.changed_pain_point_status.append((pid, s_old, s_new))
    d.added_opportunities = sorted(set(b.opportunities) - set(a.opportunities))
    d.removed_opportunities = sorted(set(a.opportunities) - set(b.opportunities))
    for oid in sorted(set(a.opportunities) & set(b.opportunities)):
        s_old, s_new = a.opportunities[oid].get("status"), b.opportunities[oid].get("status")
        if s_old != s_new:
            d.changed_opportunity_status.append((oid, s_old, s_new))
    for sid in sorted(set(a.steps) & set(b.steps)):
        f_old = (a.steps[sid].get("feeling") or {}).get("valence")
        f_new = (b.steps[sid].get("feeling") or {}).get("valence")
        if f_old != f_new:
            d.feeling_changes.append((sid, f_old, f_new))
    ea, eb = a.evidence_summary(), b.evidence_summary()
    d.evidence_delta = {
        k: eb.get(k, 0) - ea.get(k, 0) for k in ("observed", "reported", "assumed", "total")
    }
    d.added_sources = sorted(set(b.sources) - set(a.sources))
    return d


def diff_markdown(d: JourneyDiff) -> str:
    lines = [f"# Änderungen {d.old_version} → {d.new_version}", ""]
    if d.is_empty():
        lines.append("Keine Modelländerungen.")
        return "\n".join(lines)

    def section(title: str, items: list[str]) -> None:
        if items:
            lines.append(f"## {title}")
            lines.extend(f"- {i}" for i in items)
            lines.append("")

    ev = d.evidence_delta
    if any(ev.values()):
        lines.append("## Evidenz")
        lines.append(
            f"- gesamt {ev['total']:+d} · beobachtet {ev['observed']:+d} · berichtet {ev['reported']:+d} · angenommen {ev['assumed']:+d}"
        )
        lines.append("")
    section("Neue Quellen", d.added_sources)
    section("Neue Schritte", d.added_steps)
    section("Entfernte Schritte", d.removed_steps)
    section("Neue Pain Points", d.added_pain_points)
    section("Entfernte Pain Points", d.removed_pain_points)
    section(
        "Pain-Point-Status",
        [f"{p}: {o or '–'} → {n or '–'}" for p, o, n in d.changed_pain_point_status],
    )
    section("Neue Chancen", d.added_opportunities)
    section("Entfernte Chancen", d.removed_opportunities)
    section(
        "Chancen-Status",
        [f"{p}: {o or '–'} → {n or '–'}" for p, o, n in d.changed_opportunity_status],
    )
    section(
        "Emotionale Kurve",
        [
            f"{s}: {o if o is not None else '–'} → {n if n is not None else '–'}"
            for s, o, n in d.feeling_changes
        ],
    )
    return "\n".join(lines)
