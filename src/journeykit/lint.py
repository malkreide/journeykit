"""Methodische Lints: die fünf Fallstricke als prüfbare Regeln.

Jede Regel trägt einen Code, eine Stufe (ERROR, WARN, INFO), das Anti-Pattern,
das sie adressiert, und einen Hinweis, was zu tun ist. Meldung und Hinweis
stehen je Sprache in ``lint_messages.py``. Die Regeln urteilen
über das Modell, nicht über den Text - sie können nicht erkennen, ob ein Zitat
gut gewählt ist, aber sie erkennen, ob es fehlt.

Stufen:
    ERROR  Die Journey ist methodisch nicht belastbar oder technisch kaputt.
    WARN   Ein Fallstrick ist wahrscheinlich; vor dem Teilen klären.
    INFO   Hinweis, der beim nächsten Review helfen kann.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date
from typing import Any

from .lint_messages import ANTIPATTERN_LABELS, PII_LABELS, check_language, render_message
from .model import PRIMARY_CLASSES, JourneyIndex

ERROR, WARN, INFO = "ERROR", "WARN", "INFO"
LEVEL_ORDER = {ERROR: 0, WARN: 1, INFO: 2}

ANTIPATTERNS = ANTIPATTERN_LABELS["de"]

PRIMARY_SOURCE_KINDS = frozenset(
    {
        "interview",
        "survey",
        "diary_study",
        "observation",
        "ticket_export",
        "inquiry_log",
        "analytics",
        "case_records",
        "complaint",
    }
)

COMMERCIAL_KPI_TERMS = (
    "conversion",
    "churn",
    "revenue",
    "umsatz",
    "clv",
    "lifetime value",
    "cac",
    "acquisition cost",
    "cart",
    "warenkorb",
    "upsell",
    "arpu",
)

# Schlüssel → PII_LABELS in lint_messages.py
_PII_PATTERNS = (
    ("email", re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")),
    ("phone", re.compile(r"(?<!\d)(\+41|0041|0)\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}(?!\d)")),
    ("ahv", re.compile(r"756\.\d{4}\.\d{4}\.\d{2}")),
)


@dataclass(frozen=True)
class Finding:
    code: str
    level: str
    antipattern: str
    message: str
    path: str = ""
    hint: str = ""

    def as_dict(self) -> dict[str, str]:
        return asdict(self)

    def format(self, with_hint: bool = True) -> str:
        where = f" @ {self.path}" if self.path else ""
        hint = f"\n      → {self.hint}" if self.hint and with_hint else ""
        return f"[{self.level}] {self.code}{where}: {self.message}{hint}"

    def __str__(self) -> str:
        return self.format()


class _Collector:
    def __init__(self, lang: str = "de") -> None:
        self.lang = lang
        self.findings: list[Finding] = []

    def add(
        self,
        code: str,
        level: str,
        antipattern: str,
        path: str = "",
        msg: str | None = None,
        **params: Any,
    ) -> None:
        """Befund mit Meldung ``msg`` (Standard: der Code) aus lint_messages.py."""
        message, hint = render_message(self.lang, msg or code, **params)
        self.findings.append(Finding(code, level, antipattern, message, path, hint))


def _shortlist(ids: list[str], limit: int) -> str:
    return ", ".join(ids[:limit]) + ("…" if len(ids) > limit else "")


# ---------------------------------------------------------------------------
# Regeln
# ---------------------------------------------------------------------------


def _rule_integrity(idx: JourneyIndex, c: _Collector) -> None:
    j = idx.journey
    # Doppelte IDs über alle Namensräume - eine ID soll genau ein Ding bezeichnen.
    seen: Counter[str] = Counter()
    for phase in j.get("phases", []):
        seen[phase["id"]] += 1
        for step in phase.get("steps", []):
            seen[step["id"]] += 1
            for pp in step.get("pain_points", []):
                seen[pp["id"]] += 1
    for key in ("opportunities", "evidence", "sources"):
        seen.update(item["id"] for item in j.get(key, []))
    for dup, n in seen.items():
        if n > 1:
            c.add("L002", ERROR, "integrity", id=dup, n=n)

    for path, ref in idx.all_refs():
        if ref not in idx.evidence and ref not in idx.sources:
            c.add("L001", ERROR, "integrity", path, msg="L001.ref", ref=ref)
    for atom in idx.evidence.values():
        if atom["source_ref"] not in idx.sources:
            c.add(
                "L001",
                ERROR,
                "integrity",
                f"evidence[{atom['id']}]",
                msg="L001.source",
                atom=atom["id"],
                source=atom["source_ref"],
            )
        for other in atom.get("contradicts", []):
            if other not in idx.evidence:
                c.add(
                    "L001",
                    ERROR,
                    "integrity",
                    f"evidence[{atom['id']}]",
                    msg="L001.contradicts",
                    atom=atom["id"],
                    other=other,
                )
    for oi, opp in enumerate(j.get("opportunities", [])):
        for pp in opp.get("linked_pain_points", []):
            if pp not in idx.pain_points:
                c.add(
                    "L001",
                    ERROR,
                    "integrity",
                    f"opportunities[{oi}]",
                    msg="L001.opp_pain_point",
                    opp=opp["id"],
                    pp=pp,
                )
        if opp.get("phase_ref") and opp["phase_ref"] not in idx.phases:
            c.add(
                "L001",
                ERROR,
                "integrity",
                f"opportunities[{oi}]",
                msg="L001.opp_phase",
                opp=opp["id"],
                phase=opp["phase_ref"],
            )
    for qi, q in enumerate(j.get("open_questions", [])):
        if q.get("phase_ref") and q["phase_ref"] not in idx.phases:
            c.add(
                "L001",
                ERROR,
                "integrity",
                f"open_questions[{qi}]",
                msg="L001.question_phase",
                phase=q["phase_ref"],
            )
        if q.get("step_ref") and q["step_ref"] not in idx.steps:
            c.add(
                "L001",
                ERROR,
                "integrity",
                f"open_questions[{qi}]",
                msg="L001.question_step",
                step=q["step_ref"],
            )
    for pi, phase in enumerate(j.get("phases", [])):
        dd = phase.get("duration_days")
        if not dd:
            continue
        lo, typ, hi = dd.get("min"), dd["typical"], dd.get("max")
        if (lo is not None and lo > typ) or (hi is not None and hi < typ):
            c.add(
                "L003",
                ERROR,
                "integrity",
                f"phases[{pi}].duration_days",
                phase=phase["id"],
                min=lo,
                typical=typ,
                max=hi,
            )


def _rule_inside_out(idx: JourneyIndex, c: _Collector) -> None:
    j = idx.journey
    status = j["meta"]["status"]
    experience = [cl for cl in idx.claims() if cl.kind in {"thinking", "feeling", "pain_point"}]
    if experience:
        unsupported = [cl for cl in experience if not idx.has_primary(cl.evidence_refs)]
        ratio = len(unsupported) / len(experience)
        if ratio == 1.0 and status != "hypothesis":
            c.add(
                "L010",
                ERROR,
                "inside_out",
                msg="L010.none",
                n=len(experience),
            )
        elif ratio >= 0.5:
            level = INFO if status == "hypothesis" else WARN
            c.add(
                "L010",
                level,
                "inside_out",
                msg="L010.most",
                unsupported=len(unsupported),
                n=len(experience),
                pct=f"{ratio * 100:.0f}",
            )
    kinds = {s["kind"] for s in idx.sources.values()}
    if idx.sources and not (kinds & PRIMARY_SOURCE_KINDS):
        c.add(
            "L011",
            INFO if status == "hypothesis" else WARN,
            "inside_out",
            "sources",
        )
    persona = j["persona"]
    primary_refs = [
        r
        for r in persona.get("evidence_refs", [])
        if idx.evidence.get(r, {}).get("class") in PRIMARY_CLASSES
    ]
    if len(primary_refs) < 3 and not persona.get("is_hypothesis"):
        c.add(
            "L012",
            WARN,
            "inside_out",
            "persona",
            name=persona["name"],
            n=len(primary_refs),
        )


def _rule_happy_path(idx: JourneyIndex, c: _Collector) -> None:
    status = idx.journey["meta"]["status"]
    if not idx.breakdowns():
        c.add(
            "L020",
            WARN if status == "hypothesis" else ERROR,
            "happy_path",
        )
    for pi, phase in enumerate(idx.journey["phases"]):
        pains = sum(len(s.get("pain_points", [])) for s in phase["steps"])
        edges = sum(len(s.get("edge_cases", [])) for s in phase["steps"])
        if pains == 0 and edges == 0:
            c.add(
                "L021",
                WARN,
                "happy_path",
                f"phases[{pi}]",
                phase=phase["name"],
            )
        for si, step in enumerate(phase["steps"]):
            has_breakdown = any(pp.get("type") == "breakdown" for pp in step.get("pain_points", []))
            if has_breakdown and not step.get("recovery_paths"):
                c.add(
                    "L022",
                    WARN,
                    "happy_path",
                    f"phases[{pi}].steps[{si}]",
                    step=step["name"],
                )
    # Kanalwechsel ohne Markierung als Übergang
    prev_channel: str | None = None
    for pi, phase in enumerate(idx.journey["phases"]):
        for si, step in enumerate(phase["steps"]):
            ch = step.get("channel")
            if prev_channel and ch and ch != prev_channel and not step.get("is_transition"):
                c.add(
                    "L023",
                    INFO,
                    "happy_path",
                    f"phases[{pi}].steps[{si}]",
                    from_channel=prev_channel,
                    to_channel=ch,
                    step=step["name"],
                )
            if ch:
                prev_channel = ch


def _rule_static_map(idx: JourneyIndex, c: _Collector, today: date) -> None:
    meta = idx.journey["meta"]
    if meta.get("status") == "archived":
        return
    if not meta.get("owner"):
        c.add("L030", WARN, "static_map", "meta")
    if not meta.get("review_cycle_days"):
        c.add("L031", WARN, "static_map", "meta")
    nxt = meta.get("next_review")
    if nxt:
        try:
            if date.fromisoformat(nxt) < today:
                c.add("L032", WARN, "static_map", "meta.next_review", date=nxt)
        except ValueError:
            pass
    for pid, pp in idx.pain_points.items():
        if (pp.get("severity") or 0) >= 4 and not pp.get("owner"):
            c.add(
                "L033",
                WARN,
                "static_map",
                f"pain_points[{pid}]",
                pp=pid,
                severity=pp["severity"],
            )
    no_status = [o["id"] for o in idx.opportunities.values() if not o.get("status")]
    if no_status:
        c.add(
            "L034",
            INFO,
            "static_map",
            "opportunities",
            n=len(no_status),
            ids=_shortlist(no_status, 5),
        )


def _rule_empathy(idx: JourneyIndex, c: _Collector) -> None:
    steps = list(idx.steps.values())
    if not steps:
        return
    no_feeling = [s for s in steps if not s.get("feeling")]
    no_thinking = [s for s in steps if not s.get("thinking")]
    if len(no_feeling) / len(steps) >= 0.5:
        c.add(
            "L040",
            WARN,
            "empathy_vacuum",
            missing=len(no_feeling),
            n=len(steps),
        )
    if len(no_thinking) / len(steps) >= 0.5:
        c.add(
            "L041",
            WARN,
            "empathy_vacuum",
            missing=len(no_thinking),
            n=len(steps),
        )
    unbacked = 0
    derived = 0
    for s in steps:
        f = s.get("feeling")
        if not f:
            continue
        refs = f.get("evidence_refs", [])
        if not refs:
            unbacked += 1
            continue
        explicit = any(
            (idx.evidence.get(r, {}).get("emotion_hint") or {}).get("explicit") for r in refs
        )
        if not explicit:
            derived += 1
    if unbacked:
        c.add("L042", INFO, "empathy_vacuum", n=unbacked)
    if derived:
        c.add("L043", INFO, "evidence", n=derived)


def _rule_overcomplexity(idx: JourneyIndex, c: _Collector) -> None:
    phases = idx.journey["phases"]
    if len(phases) > 8:
        c.add("L050", WARN, "overcomplexity", "phases", n=len(phases))
    if idx.step_count() > 30:
        c.add("L051", WARN, "overcomplexity", "phases", n=idx.step_count())
    if not idx.journey["scenario"].get("scope_exclusions"):
        c.add("L052", INFO, "overcomplexity", "scenario")


def _rule_micro_disconnect(idx: JourneyIndex, c: _Collector) -> None:
    status = idx.journey["meta"]["status"]
    if not idx.opportunities:
        c.add(
            "L060",
            INFO if status == "hypothesis" else WARN,
            "micro_disconnect",
        )
        return
    for pid, pp in idx.pain_points.items():
        if (pp.get("severity") or 0) >= 4 and not idx.opportunity_for_pain_point(pid):
            c.add("L061", WARN, "micro_disconnect", f"pain_points[{pid}]", pp=pid)
    unscored = [
        o["id"]
        for o in idx.opportunities.values()
        if o.get("user_impact") is None or o.get("effort") is None
    ]
    if unscored:
        c.add("L062", INFO, "micro_disconnect", "opportunities", n=len(unscored))
    no_stories = [o["id"] for o in idx.opportunities.values() if not o.get("stories")]
    if no_stories and len(no_stories) == len(idx.opportunities):
        c.add("L063", INFO, "micro_disconnect", "opportunities")


def _rule_blueprint(idx: JourneyIndex, c: _Collector) -> None:
    meta = idx.journey["meta"]
    if not meta.get("diagnosis"):
        c.add("L070", WARN, "blueprint", "meta")
    backstage = sum(len(s.get("backstage_notes", [])) for s in idx.steps.values())
    if idx.step_count() and backstage > idx.step_count():
        c.add("L071", WARN, "blueprint", notes=backstage, n=idx.step_count())
    if meta.get("map_type") not in {"user_journey", "customer_journey"}:
        c.add("L072", INFO, "blueprint", "meta.map_type", map_type=meta.get("map_type"))
    delegated = [
        s for s in idx.steps.values() if (s.get("performed_by") or {}).get("kind") == "intermediary"
    ]
    if idx.step_count() and len(delegated) / idx.step_count() > 0.5:
        c.add(
            "L073",
            INFO,
            "blueprint",
            "phases",
            delegated=len(delegated),
            n=idx.step_count(),
        )


def _rule_privacy(idx: JourneyIndex, c: _Collector) -> None:
    for sid, src in idx.sources.items():
        if src.get("pii_status") == "contains_pii":
            c.add("L080", ERROR, "privacy", f"sources[{sid}]", source=sid)
    for aid, atom in idx.evidence.items():
        for key, pattern in _PII_PATTERNS:
            if pattern.search(atom.get("text", "")):
                c.add(
                    "L081",
                    WARN,
                    "privacy",
                    f"evidence[{aid}]",
                    atom=aid,
                    what=PII_LABELS[c.lang][key],
                )
                break


def _rule_kpi(idx: JourneyIndex, c: _Collector) -> None:
    kpis: list[tuple[str, dict[str, Any]]] = []
    for pi, phase in enumerate(idx.journey["phases"]):
        kpis += [(f"phases[{pi}].kpis", k) for k in phase.get("kpis", [])]
        for si, step in enumerate(phase["steps"]):
            kpis += [(f"phases[{pi}].steps[{si}].kpis", k) for k in step.get("kpis", [])]
    if not kpis:
        c.add("L090", INFO, "kpi")
        return
    for path, k in kpis:
        name = k.get("name", "").lower()
        if any(term in name for term in COMMERCIAL_KPI_TERMS):
            c.add("L091", INFO, "kpi", path, name=k["name"])
    leading = [k for _, k in kpis if k.get("indicator_type") == "leading"]
    if not leading:
        c.add("L092", INFO, "kpi")


def _rule_evidence_quality(idx: JourneyIndex, c: _Collector) -> None:
    used = {ref for _, ref in idx.all_refs()}
    unused = [aid for aid in idx.evidence if aid not in used]
    if unused:
        c.add(
            "L100",
            INFO,
            "evidence",
            "evidence",
            n=len(unused),
            ids=_shortlist(unused, 6),
        )
    contradictions = [a for a in idx.evidence.values() if a.get("contradicts")]
    for a in contradictions:
        c.add(
            "L101",
            INFO,
            "evidence",
            f"evidence[{a['id']}]",
            atom=a["id"],
            others=", ".join(a["contradicts"]),
        )
    no_locator = [
        a["id"] for a in idx.evidence.values() if a["class"] != "assumed" and not a.get("locator")
    ]
    if no_locator:
        c.add(
            "L102",
            INFO,
            "evidence",
            "evidence",
            n=len(no_locator),
        )


# ---------------------------------------------------------------------------
# Einstieg
# ---------------------------------------------------------------------------


def lint_journey(
    journey: dict[str, Any], today: date | None = None, lang: str = "de"
) -> list[Finding]:
    """Alle Befunde, sortiert nach Stufe und Code. Setzt eine schema-valide Journey voraus.

    ``lang`` wählt die Sprache von Meldung und Hinweis (``lint_messages.LANGUAGES``).
    """
    today = today or date.today()
    idx = JourneyIndex.build(journey)
    c = _Collector(check_language(lang))
    _rule_integrity(idx, c)
    _rule_inside_out(idx, c)
    _rule_happy_path(idx, c)
    _rule_static_map(idx, c, today)
    _rule_empathy(idx, c)
    _rule_overcomplexity(idx, c)
    _rule_micro_disconnect(idx, c)
    _rule_blueprint(idx, c)
    _rule_privacy(idx, c)
    _rule_kpi(idx, c)
    _rule_evidence_quality(idx, c)
    return sorted(c.findings, key=lambda f: (LEVEL_ORDER[f.level], f.code, f.path))


def summarize(findings: list[Finding]) -> dict[str, int]:
    counts = Counter(f.level for f in findings)
    return {ERROR: counts.get(ERROR, 0), WARN: counts.get(WARN, 0), INFO: counts.get(INFO, 0)}


def worst_level(findings: list[Finding]) -> str | None:
    if not findings:
        return None
    return min(findings, key=lambda f: LEVEL_ORDER[f.level]).level
