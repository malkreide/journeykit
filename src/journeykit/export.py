"""Exporte aus dem Journey-Modell: Story Map, Massnahmenliste, Audit-Report.

Alle Exporte sind Text (Markdown oder CSV), damit sie in Tickets, Notion,
Wikis oder Protokolle wandern können - dort, wo Massnahmen tatsächlich leben.
Die Texte stehen je Sprache in ``export_texts.py`` (``lang`` = "de" oder "fr").
"""

from __future__ import annotations

import csv
import io
from typing import Any

from .export_texts import QUADRANT_LABELS, text
from .lint import ERROR, INFO, PRIMARY_SOURCE_KINDS, WARN, Finding, summarize
from .lint_messages import ANTIPATTERN_LABELS, check_language
from .model import JourneyIndex, Verdict, priority_quadrant, propose_verdict


def _texts(lang: str):
    check_language(lang)
    return lambda key, **params: text(lang, key, **params)


def _opps_by_phase(idx: JourneyIndex) -> dict[str | None, list[dict[str, Any]]]:
    out: dict[str | None, list[dict[str, Any]]] = {}
    for opp in idx.opportunities.values():
        out.setdefault(idx.opportunity_anchor(opp)[0], []).append(opp)
    return out


def _rank(opp: dict[str, Any]) -> tuple[int, int]:
    order = {"quick_win": 0, "big_bet": 1, "fill_in": 2, "skip": 3, None: 4}
    return order[priority_quadrant(opp)], -(opp.get("user_impact") or 0)


def story_map_markdown(journey: dict[str, Any], lang: str = "de") -> str:
    """Patton-Story-Map: Phasen horizontal (Backbone), Stories vertikal priorisiert, MVP-Linie."""
    t = _texts(lang)
    idx = JourneyIndex.build(journey)
    by_phase = _opps_by_phase(idx)
    lines = [t("storymap.title", title=journey["meta"]["title"]), ""]
    persona = journey["persona"]
    lines.append(
        t(
            "storymap.persona",
            name=persona["name"],
            role=persona["role"],
            goal=journey["scenario"]["goal"],
        )
    )
    lines.append("")
    lines.append(t("storymap.backbone"))
    lines.append("")
    lines.append("| " + " | ".join(p["name"] for p in journey["phases"]) + " |")
    lines.append("|" + "---|" * len(journey["phases"]))
    lines.append(
        "| "
        + " | ".join("<br>".join(f"• {s['name']}" for s in p["steps"]) for p in journey["phases"])
        + " |"
    )
    lines.append("")
    lines.append(t("storymap.stories"))
    lines.append("")
    for phase in journey["phases"]:
        opps = sorted(by_phase.get(phase["id"], []), key=_rank)
        lines.append(f"### {phase['name']}")
        if not opps:
            lines.append(t("storymap.no_opps"))
            lines.append("")
            continue
        for opp in opps:
            q = priority_quadrant(opp)
            tag = f" `{QUADRANT_LABELS[lang][q]}`" if q else ""
            lines.append(f"**{opp['hmw']}**{tag}")
            for story in opp.get("stories", []):
                mark = "✅" if story.get("mvp") else "◻️"
                lines.append(f"- {mark} {story['text']}")
            if not opp.get("stories"):
                lines.append(t("storymap.no_stories"))
            lines.append("")
    unassigned = by_phase.get(None, [])
    if unassigned:
        lines.append(t("storymap.no_phase"))
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


def opportunities_markdown(journey: dict[str, Any], lang: str = "de") -> str:
    """Priorisierungsmatrix: Chancen nach Quadrant."""
    t = _texts(lang)
    idx = JourneyIndex.build(journey)
    lines = [t("opps.title", title=journey["meta"]["title"]), ""]
    lines.append(t("opps.header"))
    lines.append("|---|---|---|---|---|---|---|---|")
    for opp in sorted(idx.opportunities.values(), key=_rank):
        q = priority_quadrant(opp)
        lines.append(
            f"| {QUADRANT_LABELS[lang].get(q, '–')} | {opp['hmw']} | {opp.get('user_impact', '–')} | {opp.get('public_value', '–')} | {opp.get('effort', '–')} | {', '.join(opp.get('linked_pain_points', [])) or '–'} | {opp.get('owner', '–')} | {opp.get('status', '–')} |"
        )
    lines.append("")
    lines.append(t("opps.legend"))
    return "\n".join(lines)


def _audit_diagnosis(meta: dict[str, Any], scenario: dict[str, Any], t) -> list[str]:
    lines = [t("audit.diagnosis"), ""]
    if scenario.get("perspective") == "to_be":
        lines += [t("audit.diagnosis_to_be"), ""]
    diagnosis = meta.get("diagnosis")
    if not diagnosis:
        return lines + [t("audit.diagnosis_missing", map_type=meta["map_type"]), ""]
    lines += [diagnosis["rationale"], ""]
    extra = [
        t("audit.diagnosis_alternative", alternative=alt)
        for alt in diagnosis.get("alternatives_considered", [])
    ]
    if diagnosis.get("backstage_documented_in"):
        extra.append(t("audit.diagnosis_backstage", ref=diagnosis["backstage_documented_in"]))
    return lines + (extra + [""] if extra else [])


def _audit_verdict(v: Verdict, t) -> list[str]:
    lines = [t("audit.verdict"), ""]
    if v.kind == "poster":
        labels = {
            "owner": t("audit.missing_owner"),
            "review": t("audit.missing_review"),
            "anchored_opportunity": t("audit.missing_anchored_opportunity"),
        }
        lines.append(t("audit.verdict_poster", missing=", ".join(labels[m] for m in v.missing)))
    elif v.kind == "hypothesis":
        labels = {
            "no_experience": t("audit.reason_no_experience"),
            "low_primary": t("audit.reason_low_primary", pct=v.primary_pct),
            "status_hypothesis": t("audit.reason_status_hypothesis"),
            "breakdown_without_recovery": t(
                "audit.reason_breakdown_without_recovery", n=v.breakdowns_without_recovery
            ),
        }
        reasons = ", ".join(labels[r] for r in v.reasons if r != "to_be")
        if "to_be" in v.reasons:
            # Ein Soll-Konzept ist nicht «noch nicht belegt», sondern nicht belegbar.
            also = " " + t("audit.verdict_also", reasons=reasons) if reasons else ""
            lines.append(t("audit.verdict_to_be") + also)
        else:
            lines.append(t("audit.verdict_hypothesis", reasons=reasons))
    else:
        lines.append(t("audit.verdict_robust", pct=v.primary_pct))
    return lines + ["", t("audit.verdict_note"), ""]


def _audit_next_steps(
    v: Verdict,
    findings: list[Finding],
    t,
    relayed: int = 0,
    source_request: dict[str, Any] | None = None,
    limit: int = 3,
) -> list[str]:
    """Die schwersten Befunde, je Anti-Pattern einer.

    Davor, in dieser Reihenfolge: die Rückfrage nach den Quellen, wenn Zitate nur aus
    zweiter Hand vorliegen (mit dem Rohmaterial werden sie Primärevidenz), und bei einer
    Hypothese ohne Plan der Plan.
    """
    lines: list[str] = []
    n = 0
    if relayed:
        n += 1
        if source_request:
            lines.append(
                t("audit.step_source_request", n=n, q=relayed, text=source_request["text"])
            )
        else:
            lines.append(t("audit.step_source_request_new", n=n, q=relayed))
    if v.kind == "hypothesis" and not v.has_research_plan:
        n += 1
        lines.append(t("audit.step_plan", n=n))
    rank = {ERROR: 0, WARN: 1, INFO: 2}
    seen: set[str] = set()
    for f in sorted(findings, key=lambda f: rank.get(f.level, 3)):
        if n >= limit:
            break
        if f.antipattern in seen:
            continue
        seen.add(f.antipattern)
        n += 1
        lines.append(t("audit.step", n=n, code=f.code, message=f.message))
        if f.hint:
            lines.append(f"   - → {f.hint}")
    return [t("audit.next_steps"), ""] + (lines or [t("audit.no_steps")]) + [""]


def audit_markdown(journey: dict[str, Any], findings: list[Finding], lang: str = "de") -> str:
    """Audit-Report: Diagnose, Urteilsvorschlag, nächste Schritte, Evidenzlage, Befunde je Anti-Pattern.

    Die Befunde kommen fertig formuliert; für einen französischen Report
    ``lint_journey(journey, lang="fr")`` übergeben.
    """
    t = _texts(lang)
    idx = JourneyIndex.build(journey)
    meta = journey["meta"]
    ev = idx.evidence_summary()
    counts = summarize(findings)
    lines = [t("audit.title", title=meta["title"]), ""]
    lines.append(
        t("audit.meta", version=meta["version"], status=meta["status"], map_type=meta["map_type"])
    )
    if meta.get("synthetic"):
        lines.append("")
        lines.append(t("audit.synthetic"))
    lines.append("")
    lines += _audit_diagnosis(meta, journey["scenario"], t)
    verdict = propose_verdict(idx)
    lines += _audit_verdict(verdict, t)
    # Zitate aus zweiter Hand: Die Quelle schreibt sie Nutzenden zu, ist selbst aber keine
    # Nutzerquelle (z. B. eine übernommene Map). Die Klasse bleibt an der Quelle.
    relayed = sum(
        1
        for a in idx.evidence.values()
        if a["kind"] == "quote"
        and a["class"] == "assumed"
        and idx.sources.get(a["source_ref"], {}).get("kind") not in PRIMARY_SOURCE_KINDS
    )
    source_request = next(
        (
            q
            for q in journey.get("open_questions", [])
            if q.get("proposed_method") == "source_request"
        ),
        None,
    )
    lines += _audit_next_steps(verdict, findings, t, relayed, source_request)
    lines.append(t("audit.evidence"))
    lines.append("")
    kinds = ", ".join(sorted({s["kind"] for s in idx.sources.values()})) or "–"
    lines.append(t("audit.sources", n=len(idx.sources), kinds=kinds))
    lines.append(
        t(
            "audit.atoms",
            total=ev["total"],
            observed=ev["observed"],
            reported=ev["reported"],
            assumed=ev["assumed"],
        )
    )
    if relayed:
        lines.append(t("audit.relayed_quotes", n=relayed))
    experience = [c for c in idx.claims() if c.kind in {"thinking", "feeling", "pain_point"}]
    backed = sum(1 for c in experience if idx.has_primary(c.evidence_refs))
    if experience:
        pct = f"{backed / len(experience) * 100:.0f}"
        lines.append(t("audit.experience", backed=backed, n=len(experience), pct=pct))
    else:
        lines.append(t("audit.experience_none"))
    lines.append(
        t(
            "audit.counts",
            breakdowns=len(idx.breakdowns()),
            pain_points=len(idx.pain_points),
            opps=len(idx.opportunities),
        )
    )
    lines.append("")
    lines.append(
        t(
            "audit.findings",
            errors=counts["ERROR"],
            warnings=counts["WARN"],
            infos=counts["INFO"],
        )
    )
    lines.append("")
    by_ap: dict[str, list[Finding]] = {}
    for f in findings:
        by_ap.setdefault(f.antipattern, []).append(f)
    for ap, label in ANTIPATTERN_LABELS[lang].items():
        items = by_ap.get(ap)
        if not items:
            continue
        lines.append(f"### {label}")
        lines.append("")
        for f in items:
            where = f" (`{f.path}`)" if f.path else ""
            lines.append(
                t("audit.finding", level=f.level, code=f.code, where=where, message=f.message)
            )
            if f.hint:
                lines.append(f"  - → {f.hint}")
        lines.append("")
    if not findings:
        lines.append(t("audit.no_findings"))
        lines.append("")
    oq = journey.get("open_questions", [])
    if oq:
        lines.append(t("audit.open_questions"))
        lines.append("")
        for q in oq:
            method = (
                t("audit.method", method=q["proposed_method"]) if q.get("proposed_method") else ""
            )
            # Fundort: der Schritt, sonst die Phase; ein unbekannter Verweis bleibt stumm (L001 meldet ihn)
            target = idx.steps.get(q.get("step_ref", "")) or idx.phases.get(q.get("phase_ref", ""))
            at = t("audit.oq_at", name=target["name"]) if target else ""
            lines.append(f"- {at}{q['text']}{method}")
        lines.append("")
    return "\n".join(lines)
