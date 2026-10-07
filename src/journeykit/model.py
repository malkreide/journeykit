"""Leichtgewichtige Sicht auf eine Journey: Indizes und Iteratoren.

Keine Klassenhierarchie, keine Validierung - das Schema ist die Wahrheit.
Dieses Modul beantwortet die Fragen, die Lints, Export und Viewer gemeinsam
stellen: Welche Aussagen gibt es, worauf stützen sie sich, was ist primär?
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

PRIMARY_CLASSES = frozenset({"observed", "reported"})
EVIDENCE_CLASSES = ("observed", "reported", "assumed")


@dataclass(frozen=True)
class Claim:
    """Eine belegbare Aussage irgendwo in der Journey."""

    path: str  # JSON-Pointer-ähnlich, z. B. phases[0].steps[2].thinking[1]
    kind: str  # persona, scenario, step, thinking, feeling, pain_point, edge_case, recovery, opportunity
    text: str
    evidence_refs: tuple[str, ...]
    phase_id: str | None = None
    step_id: str | None = None


@dataclass
class JourneyIndex:
    journey: dict[str, Any]
    evidence: dict[str, dict[str, Any]] = field(default_factory=dict)
    sources: dict[str, dict[str, Any]] = field(default_factory=dict)
    phases: dict[str, dict[str, Any]] = field(default_factory=dict)
    steps: dict[str, dict[str, Any]] = field(default_factory=dict)
    pain_points: dict[str, dict[str, Any]] = field(default_factory=dict)
    opportunities: dict[str, dict[str, Any]] = field(default_factory=dict)
    step_phase: dict[str, str] = field(default_factory=dict)
    pain_point_step: dict[str, str] = field(default_factory=dict)

    @classmethod
    def build(cls, journey: dict[str, Any]) -> JourneyIndex:
        idx = cls(journey=journey)
        for atom in journey.get("evidence", []):
            idx.evidence[atom["id"]] = atom
        for src in journey.get("sources", []):
            idx.sources[src["id"]] = src
        for phase in journey.get("phases", []):
            idx.phases[phase["id"]] = phase
            for step in phase.get("steps", []):
                idx.steps[step["id"]] = step
                idx.step_phase[step["id"]] = phase["id"]
                for pp in step.get("pain_points", []):
                    idx.pain_points[pp["id"]] = pp
                    idx.pain_point_step[pp["id"]] = step["id"]
        for opp in journey.get("opportunities", []):
            idx.opportunities[opp["id"]] = opp
        return idx

    # -- Evidenz ---------------------------------------------------------

    def classes_of(self, refs: list[str] | tuple[str, ...]) -> set[str]:
        """Evidenzklassen hinter einer Referenzliste (unbekannte IDs werden ignoriert)."""
        out: set[str] = set()
        for ref in refs:
            atom = self.evidence.get(ref)
            if atom:
                out.add(atom["class"])
        return out

    def has_primary(self, refs: list[str] | tuple[str, ...]) -> bool:
        return bool(self.classes_of(refs) & PRIMARY_CLASSES)

    def evidence_summary(self) -> dict[str, int]:
        counts = dict.fromkeys(EVIDENCE_CLASSES, 0)
        for atom in self.evidence.values():
            counts[atom["class"]] = counts.get(atom["class"], 0) + 1
        counts["total"] = len(self.evidence)
        return counts

    # -- Aussagen --------------------------------------------------------

    def claims(self) -> Iterator[Claim]:
        j = self.journey
        persona = j.get("persona", {})
        yield Claim(
            "persona", "persona", persona.get("name", ""), tuple(persona.get("evidence_refs", []))
        )
        scenario = j.get("scenario", {})
        yield Claim(
            "scenario",
            "scenario",
            scenario.get("goal", ""),
            tuple(scenario.get("evidence_refs", [])),
        )
        for pi, phase in enumerate(j.get("phases", [])):
            for si, step in enumerate(phase.get("steps", [])):
                base = f"phases[{pi}].steps[{si}]"
                ids = dict(phase_id=phase["id"], step_id=step["id"])
                yield Claim(
                    base,
                    "step",
                    step.get("action", ""),
                    tuple(step.get("evidence_refs", [])),
                    **ids,
                )
                for ti, th in enumerate(step.get("thinking", [])):
                    yield Claim(
                        f"{base}.thinking[{ti}]",
                        "thinking",
                        th["text"],
                        tuple(th.get("evidence_refs", [])),
                        **ids,
                    )
                feeling = step.get("feeling")
                if feeling:
                    yield Claim(
                        f"{base}.feeling",
                        "feeling",
                        feeling.get("label", str(feeling.get("valence"))),
                        tuple(feeling.get("evidence_refs", [])),
                        **ids,
                    )
                for ppi, pp in enumerate(step.get("pain_points", [])):
                    yield Claim(
                        f"{base}.pain_points[{ppi}]",
                        "pain_point",
                        pp["text"],
                        tuple(pp.get("evidence_refs", [])),
                        **ids,
                    )
                for ei, ec in enumerate(step.get("edge_cases", [])):
                    yield Claim(
                        f"{base}.edge_cases[{ei}]",
                        "edge_case",
                        ec["text"],
                        tuple(ec.get("evidence_refs", [])),
                        **ids,
                    )
                for ri, rp in enumerate(step.get("recovery_paths", [])):
                    yield Claim(
                        f"{base}.recovery_paths[{ri}]",
                        "recovery",
                        rp["path"],
                        tuple(rp.get("evidence_refs", [])),
                        **ids,
                    )
        for oi, opp in enumerate(j.get("opportunities", [])):
            yield Claim(
                f"opportunities[{oi}]",
                "opportunity",
                opp["hmw"],
                tuple(opp.get("evidence_refs", [])),
                phase_id=opp.get("phase_ref"),
            )

    def all_refs(self) -> Iterator[tuple[str, str]]:
        """(pfad, evidence_id) für jede Referenz - für Dangling-Checks."""
        for claim in self.claims():
            for ref in claim.evidence_refs:
                yield claim.path, ref
        for pi, phase in enumerate(self.journey.get("phases", [])):
            for ref in (phase.get("duration_days") or {}).get("evidence_refs", []):
                yield f"phases[{pi}].duration_days", ref
            for ki, kpi in enumerate(phase.get("kpis", [])):
                if kpi.get("source_ref"):
                    yield f"phases[{pi}].kpis[{ki}].source_ref", kpi["source_ref"]
            for si, step in enumerate(phase.get("steps", [])):
                for ki, kpi in enumerate(step.get("kpis", [])):
                    if kpi.get("source_ref"):
                        yield f"phases[{pi}].steps[{si}].kpis[{ki}].source_ref", kpi["source_ref"]

    # -- Kennzahlen über die Journey ---------------------------------------

    def step_count(self) -> int:
        return len(self.steps)

    def breakdowns(self) -> list[dict[str, Any]]:
        return [pp for pp in self.pain_points.values() if pp.get("type") == "breakdown"]

    def opportunity_for_pain_point(self, pain_point_id: str) -> list[dict[str, Any]]:
        return [
            o
            for o in self.opportunities.values()
            if pain_point_id in o.get("linked_pain_points", [])
        ]


def priority_quadrant(opp: dict[str, Any]) -> str | None:
    """Impact/Effort-Quadrant einer Chance; None, wenn Scores fehlen."""
    impact = opp.get("user_impact")
    value = opp.get("public_value")
    effort = opp.get("effort")
    if impact is None or effort is None:
        return None
    combined = impact + (value if value is not None else impact)
    high_value = combined >= 6  # Mittelwert >= 3 von 5
    low_effort = effort <= 2
    if high_value and low_effort:
        return "quick_win"
    if high_value and not low_effort:
        return "big_bet"
    if not high_value and low_effort:
        return "fill_in"
    return "skip"
