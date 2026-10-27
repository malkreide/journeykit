"""Exporte aus dem Journey-Modell: Story Map, Massnahmenliste, Audit-Report, Evidenz-Heatmap.

Alle Exporte sind Text (Markdown, CSV oder SVG), damit sie in Tickets, Notion,
Wikis, Protokolle oder Berichte wandern können - dort, wo Massnahmen tatsächlich leben.
Die Texte stehen je Sprache in ``export_texts.py`` (``lang`` = "de" oder "fr").
"""

from __future__ import annotations

import csv
import io
from datetime import date
from typing import Any
from xml.sax.saxutils import escape, quoteattr

from . import __version__
from .export_texts import QUADRANT_LABELS, STATUS_LABELS, text
from .lint import ERROR, INFO, PRIMARY_SOURCE_KINDS, WARN, Finding, summarize
from .lint_messages import ANTIPATTERN_LABELS, check_language
from .model import EVIDENCE_CLASSES, JourneyIndex, Verdict, priority_quadrant, propose_verdict


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


# Aussagearten der Heatmap, in der Reihenfolge der Zeilen – dieselben wie im Viewer
HEATMAP_KINDS = ("step", "thinking", "feeling", "pain_point", "edge_case", "recovery")


def evidence_heatmap(journey: dict[str, Any]) -> list[dict[str, Any]]:
    """Belege je Schritt und Aussageart, gezählt wie die Heatmap im Viewer.

    Je Zelle: Zahl der Aussagen und der Referenzen je Evidenzklasse (jede Referenz
    zählt, auch wenn zwei Aussagen dasselbe Atom nennen; unbekannte IDs zählen nicht,
    L001 meldet sie). Eine Zeile pro Schritt und Art, auch ohne Aussage – das Raster
    bleibt vollständig, damit eine Lücke als Lücke sichtbar ist.
    """
    idx = JourneyIndex.build(journey)
    cells: dict[tuple[str, str], dict[str, int]] = {}
    for claim in idx.claims():
        if claim.kind not in HEATMAP_KINDS:
            continue
        cell = cells.setdefault(
            (claim.step_id, claim.kind), dict.fromkeys(("n", *EVIDENCE_CLASSES), 0)
        )
        cell["n"] += 1
        for ref in claim.evidence_refs:
            atom = idx.evidence.get(ref)
            if atom:
                cell[atom["class"]] += 1
    rows = []
    for phase in journey["phases"]:
        for step in phase["steps"]:
            for kind in HEATMAP_KINDS:
                c = cells.get((step["id"], kind), dict.fromkeys(("n", *EVIDENCE_CLASSES), 0))
                rows.append(
                    {
                        "phase_id": phase["id"],
                        "phase": phase["name"],
                        "step_id": step["id"],
                        "step": step["name"],
                        "kind": kind,
                        "statements": c["n"],
                        "primary": c["observed"] + c["reported"],
                        **{k: c[k] for k in EVIDENCE_CLASSES},
                    }
                )
    return rows


def heatmap_csv(journey: dict[str, Any]) -> str:
    """Evidenz-Heatmap als Tabelle: eine Zeile pro Schritt und Aussageart, für Excel oder Pivot."""
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=";", lineterminator="\n")
    cols = [
        "phase_id",
        "phase",
        "step_id",
        "step",
        "kind",
        "statements",
        "primary",
        *EVIDENCE_CLASSES,
    ]
    w.writerow(cols[:6] + [f"evidence_{c}" for c in cols[6:]])
    for row in evidence_heatmap(journey):
        w.writerow([row[c] for c in cols])
    return buf.getvalue()


# Farben der hellen Viewer-Tokens: das Bild landet in Berichten und auf Papier
_SVG = {
    "bg": "#ffffff",
    "ink": "#1d1c1a",
    "ink2": "#5a5853",
    "ink3": "#8a877f",
    "phase": "#e3eaf4",
    "observed": (31, 122, 140),
    "gap": "#9c9a93",
}
_FONT = '"Segoe UI", system-ui, -apple-system, Helvetica, Arial, sans-serif'


def _wrap(s: str, width: int, max_lines: int) -> list[str]:
    """Zeilenumbruch nach Zeichenzahl; ein zu langes Wort wird mit «-» getrennt.

    Auf Papier gibt es keinen Tooltip, deshalb trennen statt abschneiden
    («Kreisschulbehör-» / «de»). Erst was über ``max_lines`` hinausgeht, endet mit «…».
    """
    lines: list[str] = []
    for word in s.split():
        while len(word) > width:
            cut = min(width - 1, len(word) - 4)  # nicht «Informationsanla-» / «ss»
            lines.append(word[:cut] + "-")
            word = word[cut:]
        if lines and not lines[-1].endswith("-") and len(lines[-1]) + 1 + len(word) <= width:
            lines[-1] += " " + word
        else:
            lines.append(word)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: width - 1].rstrip(" -") + "…"
    return lines


def _shade(primary: int) -> tuple[str, str]:
    """Füllung und Schriftfarbe einer Zelle: wie ``color-mix`` im Viewer (15 % + 18 % je Beleg, höchstens 85 %)."""
    share = min(15 + primary * 18, 85) / 100
    fill = "#" + "".join(f"{round(c * share + 255 * (1 - share)):02x}" for c in _SVG["observed"])
    return fill, "#ffffff" if primary >= 3 else _SVG["ink"]


def heatmap_svg(journey: dict[str, Any], lang: str = "de", today: date | None = None) -> str:
    """Evidenz-Heatmap als eigenständiges SVG: Schritte nach Phasen × Aussagearten.

    Ohne Schriften oder Bilder von aussen, damit das Bild in geschlossenen Netzen,
    in Word, PowerPoint und auf Papier gleich aussieht.
    """
    t = _texts(lang)
    meta = journey["meta"]
    rows = evidence_heatmap(journey)
    steps = [s for p in journey["phases"] for s in p["steps"]]
    pad, label_w, cell_w, cell_h, gap = 24, 130, 100, 46, 4
    col = cell_w + gap
    grid_x = pad + label_w
    width = max(grid_x + len(steps) * col - gap + pad, 640)
    out: list[str] = []
    y = pad + 18
    out.append(
        f'<text x="{pad}" y="{y}" font-size="18" font-weight="600" fill="{_SVG["ink"]}">{escape(t("heatmap.title", title=meta["title"]))}</text>'
    )
    y += 22
    sub = t(
        "heatmap.subtitle",
        persona=journey["persona"]["name"],
        version=meta["version"],
        status=STATUS_LABELS[lang].get(meta["status"], meta["status"]),
    )
    out.append(f'<text x="{pad}" y="{y}" font-size="12" fill="{_SVG["ink2"]}">{escape(sub)}</text>')
    if meta.get("synthetic"):
        y += 18
        out.append(
            f'<text x="{pad}" y="{y}" font-size="12" font-style="italic" fill="{_SVG["ink3"]}">{escape(t("heatmap.synthetic"))}</text>'
        )
    # Phasen über ihren Schritten
    y += 18
    i = 0
    for phase in journey["phases"]:
        span = len(phase["steps"])
        if span:
            x, w = grid_x + i * col, span * col - gap
            name = _wrap(phase["name"], max(int(w / 6.5), 4), 1)[0]
            out.append(
                f'<g><title>{escape(phase["name"])}</title><rect x="{x}" y="{y}" width="{w}" height="24" rx="4" fill="{_SVG["phase"]}"/>'
            )
            out.append(
                f'<text x="{x + w / 2}" y="{y + 16}" font-size="11.5" font-weight="600" text-anchor="middle" fill="{_SVG["ink"]}">{escape(name)}</text></g>'
            )
        i += span
    # Schrittnamen, bis drei Zeilen
    y += 24 + 14
    for i, step in enumerate(steps):
        cx = grid_x + i * col + cell_w / 2
        tspans = "".join(
            f'<tspan x="{cx}" dy="{0 if k == 0 else 13}">{escape(line)}</tspan>'
            for k, line in enumerate(_wrap(step["name"], 18, 3))
        )
        out.append(
            f'<text y="{y}" font-size="10" text-anchor="middle" fill="{_SVG["ink"]}"><title>{escape(step["name"])}</title>{tspans}</text>'
        )
    y += 3 * 13 + 6
    # Raster: eine Zeile je Aussageart
    by_cell = {(r["step_id"], r["kind"]): r for r in rows}
    labels = {
        "step": t("heatmap.kind_step"),
        "thinking": t("heatmap.kind_thinking"),
        "feeling": t("heatmap.kind_feeling"),
        "pain_point": t("heatmap.kind_pain_point"),
        "edge_case": t("heatmap.kind_edge_case"),
        "recovery": t("heatmap.kind_recovery"),
    }
    for kind in HEATMAP_KINDS:
        label = labels[kind]
        out.append(
            f'<text x="{pad}" y="{y + cell_h / 2 + 4}" font-size="12" font-weight="600" fill="{_SVG["ink2"]}">{escape(label)}</text>'
        )
        for i, step in enumerate(steps):
            r = by_cell[(step["id"], kind)]
            x, cx, cy = grid_x + i * col, grid_x + i * col + cell_w / 2, y + cell_h / 2
            if not r["statements"]:
                out.append(
                    f'<text x="{cx}" y="{cy + 4}" font-size="13" text-anchor="middle" fill="{_SVG["ink3"]}">·</text>'
                )
                continue
            tip = t(
                "heatmap.cell",
                kind=label,
                step=step["name"],
                primary=r["primary"],
                assumed=r["assumed"],
                n=r["statements"],
            )
            g = [f"<g><title>{escape(tip)}</title>"]
            if r["primary"]:
                fill, ink = _shade(r["primary"])
                g.append(
                    f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" rx="6" fill="{fill}"/>'
                )
            else:
                ink = _SVG["gap"]
                g.append(
                    f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{cell_w - 1}" height="{cell_h - 1}" rx="6" fill="none" stroke="{_SVG["gap"]}" stroke-dasharray="4 3"/>'
                )
            num_y = cy + (0 if r["assumed"] else 5)
            g.append(
                f'<text x="{cx}" y="{num_y}" font-size="13" font-weight="{600 if r["primary"] else 400}" text-anchor="middle" fill="{ink}">{r["primary"] or "–"}</text>'
            )
            if r["assumed"]:
                g.append(
                    f'<text x="{cx}" y="{cy + 15}" font-size="10" text-anchor="middle" fill="{ink}">{escape(t("heatmap.assumed_short", n=r["assumed"]))}</text>'
                )
            out.append("".join(g) + "</g>")
        y += cell_h + gap
    # Legende und Herkunft
    y += 14
    for line in _wrap(t("heatmap.legend"), max(int((width - 2 * pad) / 6), 40), 4):
        out.append(
            f'<text x="{pad}" y="{y}" font-size="11" fill="{_SVG["ink2"]}">{escape(line)}</text>'
        )
        y += 15
    stamp = (today or date.today()).isoformat()
    out.append(
        f'<text x="{pad}" y="{y + 4}" font-size="10" fill="{_SVG["ink3"]}">{escape(t("heatmap.generated", generator=f"journeykit {__version__}", date=stamp))}</text>'
    )
    height = y + 4 + pad
    title = t("heatmap.title", title=meta["title"])
    head = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'font-family={quoteattr(_FONT)} role="img" aria-label={quoteattr(title)}>'
        f"<title>{escape(title)}</title>"
        f'<rect width="{width}" height="{height}" fill="{_SVG["bg"]}"/>'
    )
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + head + "\n" + "\n".join(out) + "\n</svg>\n"


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


def _number(x: float) -> str:
    """820.0 → «820», 35.5 → «35.5»; keine Exponentialschreibweise bei grossen Beträgen."""
    return str(int(x)) if isinstance(x, float) and x.is_integer() else str(x)


def _audit_costs(idx: JourneyIndex, t) -> list[str]:
    """Kostentabelle (ADR-0007), ohne Summe – Alternativen und bedingte Kosten lassen sich nicht addieren."""
    rows = list(idx.costs())
    if not rows:
        return []
    periods = {
        "once": t("audit.period_once"),
        "month": t("audit.period_month"),
        "semester": t("audit.period_semester"),
        "year": t("audit.period_year"),
    }
    classes = {
        "observed": t("audit.class_observed"),
        "reported": t("audit.class_reported"),
        "assumed": t("audit.class_assumed"),
    }
    lines = [t("audit.costs"), "", t("audit.costs_header"), "|---|---|---|---|---|---|"]
    for _, step, cost in rows:
        lo, hi = cost.get("min", cost["amount"]), cost.get("max", cost["amount"])
        amount = f"{_number(cost['amount'])} {cost.get('currency', 'CHF')}"
        if lo != hi:
            amount += f" ({_number(lo)}–{_number(hi)})"
        found = idx.classes_of(cost["evidence_refs"])
        evidence = ", ".join(classes[c] for c in EVIDENCE_CLASSES if c in found) or "–"
        cells = [step["name"], cost["label"], amount, periods[cost["period"]]]
        cells += [cost.get("paid_to", "–"), evidence]
        lines.append("| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |")
    return lines + ["", t("audit.costs_note"), ""]


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
    # Breakdowns an Übergängen, mit dem Anteil der Übergänge an allen Schritten als
    # Vergleich: Ist fast jeder Schritt ein Übergang, sagt «alle an Übergängen» wenig.
    breakdowns = idx.breakdowns()
    if breakdowns:
        transitions = {sid for sid, step in idx.steps.items() if step.get("is_transition")}
        lines.append(
            t(
                "audit.transitions",
                at=sum(1 for pp in breakdowns if idx.pain_point_step[pp["id"]] in transitions),
                breakdowns=len(breakdowns),
                transitions=len(transitions),
                steps=idx.step_count(),
            )
        )
    # Ursachenketten (ADR-0008): Folgen mit bekannter Ursache, davon über Phasen hinweg
    caused = {pid: idx.root_causes(pid) for pid in idx.pain_points}
    chains = [pid for pid, causes in caused.items() if causes]
    if chains:
        phase_of = {pid: idx.step_phase[idx.pain_point_step[pid]] for pid in idx.pain_points}
        cross = sum(
            1
            for pid in chains
            if any(
                phase_of[c] != phase_of[pid]
                for c in idx.pain_points[pid]["caused_by"]
                if c in idx.pain_points
            )
        )
        lines.append(t("audit.chains", n=len(chains), cross=cross))
    lines.append("")
    lines += _audit_costs(idx, t)
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
