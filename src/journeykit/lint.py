"""Methodische Lints: die fünf Fallstricke als prüfbare Regeln.

Jede Regel trägt einen Code, eine Stufe (ERROR, WARN, INFO), das Anti-Pattern,
das sie adressiert, und einen Hinweis, was zu tun ist. Die Regeln urteilen
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

from .model import PRIMARY_CLASSES, JourneyIndex

ERROR, WARN, INFO = "ERROR", "WARN", "INFO"
LEVEL_ORDER = {ERROR: 0, WARN: 1, INFO: 2}

ANTIPATTERNS = {
    "integrity": "Referenzen und IDs",
    "inside_out": "Inside-Out Bias (Annahmen statt Nutzerevidenz)",
    "happy_path": "Happy Path Bias (keine Breakdowns, keine Recovery)",
    "static_map": "Static Map Trap (keine Verantwortung, kein Review)",
    "empathy_vacuum": "Empathie-Vakuum (Klicks ohne Gedanken und Gefühle)",
    "overcomplexity": "Überkomplexität (zu viele Phasen, kein Scope)",
    "micro_disconnect": "Micro-Level Disconnect (keine Übersetzung in Massnahmen)",
    "blueprint": "Service Blueprint statt User Journey",
    "privacy": "Personendaten",
    "kpi": "Kennzahlen",
    "evidence": "Evidenzqualität",
}

PRIMARY_SOURCE_KINDS = frozenset(
    {
        "interview",
        "survey",
        "diary_study",
        "observation",
        "ticket_export",
        "inquiry_log",
        "analytics",
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

_PII_PATTERNS = (
    ("E-Mail-Adresse", re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")),
    ("Telefonnummer", re.compile(r"(?<!\d)(\+41|0041|0)\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}(?!\d)")),
    ("AHV-Nummer", re.compile(r"756\.\d{4}\.\d{4}\.\d{2}")),
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
    def __init__(self) -> None:
        self.findings: list[Finding] = []

    def add(
        self, code: str, level: str, antipattern: str, message: str, path: str = "", hint: str = ""
    ) -> None:
        self.findings.append(Finding(code, level, antipattern, message, path, hint))


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
            c.add(
                "L002",
                ERROR,
                "integrity",
                f"ID «{dup}» wird {n}-mal vergeben.",
                hint="IDs eindeutig machen; sie sind Referenzziele.",
            )

    for path, ref in idx.all_refs():
        if ref not in idx.evidence and ref not in idx.sources:
            c.add(
                "L001", ERROR, "integrity", f"Referenz «{ref}» zeigt auf kein Evidenz-Atom.", path
            )
    for atom in idx.evidence.values():
        if atom["source_ref"] not in idx.sources:
            c.add(
                "L001",
                ERROR,
                "integrity",
                f"Evidenz «{atom['id']}» verweist auf unbekannte Quelle «{atom['source_ref']}».",
                f"evidence[{atom['id']}]",
            )
        for other in atom.get("contradicts", []):
            if other not in idx.evidence:
                c.add(
                    "L001",
                    ERROR,
                    "integrity",
                    f"Evidenz «{atom['id']}» widerspricht unbekanntem Atom «{other}».",
                    f"evidence[{atom['id']}]",
                )
    for oi, opp in enumerate(j.get("opportunities", [])):
        for pp in opp.get("linked_pain_points", []):
            if pp not in idx.pain_points:
                c.add(
                    "L001",
                    ERROR,
                    "integrity",
                    f"Chance «{opp['id']}» verweist auf unbekannten Pain Point «{pp}».",
                    f"opportunities[{oi}]",
                )
        if opp.get("phase_ref") and opp["phase_ref"] not in idx.phases:
            c.add(
                "L001",
                ERROR,
                "integrity",
                f"Chance «{opp['id']}» verweist auf unbekannte Phase «{opp['phase_ref']}».",
                f"opportunities[{oi}]",
            )
    for qi, q in enumerate(j.get("open_questions", [])):
        if q.get("phase_ref") and q["phase_ref"] not in idx.phases:
            c.add(
                "L001",
                ERROR,
                "integrity",
                f"Offene Frage verweist auf unbekannte Phase «{q['phase_ref']}».",
                f"open_questions[{qi}]",
            )
        if q.get("step_ref") and q["step_ref"] not in idx.steps:
            c.add(
                "L001",
                ERROR,
                "integrity",
                f"Offene Frage verweist auf unbekannten Schritt «{q['step_ref']}».",
                f"open_questions[{qi}]",
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
                f"Keine der {len(experience)} Erlebnis-Aussagen (Denken, Fühlen, Pain Points) stützt sich auf Nutzerevidenz.",
                hint="meta.status auf «hypothesis» setzen und einen Erhebungsplan unter open_questions festhalten - oder Interviews, Befragungen, Anfragen auswerten.",
            )
        elif ratio >= 0.5:
            level = INFO if status == "hypothesis" else WARN
            c.add(
                "L010",
                level,
                "inside_out",
                f"{len(unsupported)} von {len(experience)} Erlebnis-Aussagen ({ratio:.0%}) ohne Primärevidenz (beobachtet/berichtet).",
                hint="Im Viewer den Filter «nur Primärevidenz» einschalten: Was dann übrig bleibt, ist die belegte Journey.",
            )
    kinds = {s["kind"] for s in idx.sources.values()}
    if idx.sources and not (kinds & PRIMARY_SOURCE_KINDS):
        c.add(
            "L011",
            INFO if status == "hypothesis" else WARN,
            "inside_out",
            "Quellenregister enthält keine Nutzerquelle (Interview, Befragung, Anfragen, Analytics, Beobachtung).",
            "sources",
            hint="Mindestens eine Quelle, in der Nutzende selbst zu Wort kommen oder gemessen werden.",
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
            f"Persona «{persona['name']}» stützt sich auf {len(primary_refs)} Primärevidenz(en).",
            "persona",
            hint="Weniger als drei unabhängige Belege: persona.is_hypothesis = true setzen oder Evidenz nachreichen.",
        )


def _rule_happy_path(idx: JourneyIndex, c: _Collector) -> None:
    status = idx.journey["meta"]["status"]
    if not idx.breakdowns():
        c.add(
            "L020",
            WARN if status == "hypothesis" else ERROR,
            "happy_path",
            "Kein einziger Pain Point vom Typ «breakdown»: Die Journey kennt keinen Punkt, an dem sie scheitert.",
            hint="Wo weichen Nutzende aus - Anruf, Beschwerde, Nichthandeln? Das ist der Breakdown. Anfragen- und Beschwerdedaten zeigen ihn.",
        )
    for pi, phase in enumerate(idx.journey["phases"]):
        pains = sum(len(s.get("pain_points", [])) for s in phase["steps"])
        edges = sum(len(s.get("edge_cases", [])) for s in phase["steps"])
        if pains == 0 and edges == 0:
            c.add(
                "L021",
                WARN,
                "happy_path",
                f"Phase «{phase['name']}»: keine Reibung, kein Edge Case.",
                f"phases[{pi}]",
                hint="Entweder ist die Phase wirklich reibungslos (dann Evidenz dafür anfügen) oder sie wurde aus Innensicht beschrieben.",
            )
        for si, step in enumerate(phase["steps"]):
            has_breakdown = any(pp.get("type") == "breakdown" for pp in step.get("pain_points", []))
            if has_breakdown and not step.get("recovery_paths"):
                c.add(
                    "L022",
                    WARN,
                    "happy_path",
                    f"Schritt «{step['name']}» hat einen Breakdown, aber keinen Recovery-Pfad.",
                    f"phases[{pi}].steps[{si}]",
                    hint="Wie kommt die Persona zurück in die Journey? Falls heute gar nicht: recovery_paths mit exists=false als Soll-Pfad festhalten.",
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
                    f"Kanalwechsel {prev_channel} → {ch} bei «{step['name']}» ist nicht als Übergang markiert.",
                    f"phases[{pi}].steps[{si}]",
                    hint="Übergangspunkte sind die häufigsten Reibungsstellen; is_transition = true und gezielt nach Evidenz suchen.",
                )
            if ch:
                prev_channel = ch


def _rule_static_map(idx: JourneyIndex, c: _Collector, today: date) -> None:
    meta = idx.journey["meta"]
    if meta.get("status") == "archived":
        return
    if not meta.get("owner"):
        c.add(
            "L030",
            WARN,
            "static_map",
            "Keine verantwortliche Rolle (meta.owner).",
            "meta",
            hint="Ohne Owner wird die Journey zum Poster. Rolle und Funktionsadresse eintragen.",
        )
    if not meta.get("review_cycle_days"):
        c.add(
            "L031",
            WARN,
            "static_map",
            "Kein Review-Rhythmus (meta.review_cycle_days).",
            "meta",
            hint="Zum Beispiel 180 Tage, gekoppelt an die nächste Erhebung oder den Jahreszyklus.",
        )
    nxt = meta.get("next_review")
    if nxt:
        try:
            if date.fromisoformat(nxt) < today:
                c.add(
                    "L032",
                    WARN,
                    "static_map",
                    f"Review-Termin {nxt} ist überschritten.",
                    "meta.next_review",
                )
        except ValueError:
            pass
    for pid, pp in idx.pain_points.items():
        if (pp.get("severity") or 0) >= 4 and not pp.get("owner"):
            c.add(
                "L033",
                WARN,
                "static_map",
                f"Schwerer Pain Point «{pid}» (Severity {pp['severity']}) ohne Owner.",
                f"pain_points[{pid}]",
            )
    no_status = [o["id"] for o in idx.opportunities.values() if not o.get("status")]
    if no_status:
        c.add(
            "L034",
            INFO,
            "static_map",
            f"{len(no_status)} Chance(n) ohne Status: {', '.join(no_status[:5])}{'…' if len(no_status) > 5 else ''}.",
            "opportunities",
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
            f"{len(no_feeling)} von {len(steps)} Schritten ohne Gefühlslage.",
            hint="Lücken sind ehrlich - aber wenn mehr als die Hälfte fehlt, fehlt die Nutzerperspektive. Interviews nach Emotionen pro Schritt auswerten.",
        )
    if len(no_thinking) / len(steps) >= 0.5:
        c.add(
            "L041",
            WARN,
            "empathy_vacuum",
            f"{len(no_thinking)} von {len(steps)} Schritten ohne Gedanken/Fragen der Persona.",
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
        c.add(
            "L042",
            INFO,
            "empathy_vacuum",
            f"{unbacked} Emotionspunkt(e) ohne Beleg - werden im Viewer als Annahme gezeichnet.",
            hint="Emoji-Kurven aus Workshop-Bauchgefühl sind Pseudo-Präzision. Belegen oder als Hypothese stehen lassen.",
        )
    if derived:
        c.add(
            "L043",
            INFO,
            "evidence",
            f"{derived} Emotionspunkt(e) sind aus Evidenz abgeleitet, nicht ausdrücklich geäussert (emotion_hint.explicit fehlt).",
        )


def _rule_overcomplexity(idx: JourneyIndex, c: _Collector) -> None:
    phases = idx.journey["phases"]
    if len(phases) > 8:
        c.add(
            "L050",
            WARN,
            "overcomplexity",
            f"{len(phases)} Phasen - mehr als acht lassen sich kaum noch lesen.",
            "phases",
            hint="Szenario enger fassen oder in zwei Journeys teilen.",
        )
    if idx.step_count() > 30:
        c.add(
            "L051",
            WARN,
            "overcomplexity",
            f"{idx.step_count()} Schritte - das ist ein User Flow, keine Journey.",
            "phases",
            hint="Schritte auf Erlebnis-Ebene zusammenfassen; UI-Pfade gehören in einen User Flow.",
        )
    if not idx.journey["scenario"].get("scope_exclusions"):
        c.add(
            "L052",
            INFO,
            "overcomplexity",
            "Kein expliziter Scope-Ausschluss (scenario.scope_exclusions).",
            "scenario",
            hint="Was bewusst nicht abgedeckt ist, schützt die Journey vor dem Stammbaum-Effekt.",
        )


def _rule_micro_disconnect(idx: JourneyIndex, c: _Collector) -> None:
    status = idx.journey["meta"]["status"]
    if not idx.opportunities:
        c.add(
            "L060",
            INFO if status == "hypothesis" else WARN,
            "micro_disconnect",
            "Keine Chancen (opportunities) abgeleitet.",
            hint="Eine Map ohne Handlungsableitung ist ein Poster. Pro Frustrationstal mindestens eine How-might-we-Frage.",
        )
        return
    for pid, pp in idx.pain_points.items():
        if (pp.get("severity") or 0) >= 4 and not idx.opportunity_for_pain_point(pid):
            c.add(
                "L061",
                WARN,
                "micro_disconnect",
                f"Schwerer Pain Point «{pid}» ohne verknüpfte Chance.",
                f"pain_points[{pid}]",
            )
    unscored = [
        o["id"]
        for o in idx.opportunities.values()
        if o.get("user_impact") is None or o.get("effort") is None
    ]
    if unscored:
        c.add(
            "L062",
            INFO,
            "micro_disconnect",
            f"{len(unscored)} Chance(n) ohne Impact/Effort-Score - keine Priorisierung möglich.",
            "opportunities",
        )
    no_stories = [o["id"] for o in idx.opportunities.values() if not o.get("stories")]
    if no_stories and len(no_stories) == len(idx.opportunities):
        c.add(
            "L063",
            INFO,
            "micro_disconnect",
            "Keine Chance hat User Stories - die Story Map bleibt leer.",
            "opportunities",
            hint="journeykit export --format storymap zeigt, was ankommt.",
        )


def _rule_blueprint(idx: JourneyIndex, c: _Collector) -> None:
    meta = idx.journey["meta"]
    if not meta.get("diagnosis"):
        c.add(
            "L070",
            WARN,
            "blueprint",
            "Keine Eingangsdiagnose (meta.diagnosis): Warum ist das eine User Journey und kein Service Blueprint?",
            "meta",
        )
    backstage = sum(len(s.get("backstage_notes", [])) for s in idx.steps.values())
    if idx.step_count() and backstage > idx.step_count():
        c.add(
            "L071",
            WARN,
            "blueprint",
            f"{backstage} Back-Stage-Notizen bei {idx.step_count()} Schritten.",
            hint="Das Interesse liegt offenbar hinter der Sichtbarkeitslinie. Service Blueprint anlegen und in meta.diagnosis.backstage_documented_in verweisen.",
        )
    if meta.get("map_type") not in {"user_journey", "customer_journey"}:
        c.add(
            "L072",
            INFO,
            "blueprint",
            f"map_type = {meta.get('map_type')}: Erlebnis-Lints gelten nur eingeschränkt.",
            "meta.map_type",
        )


def _rule_privacy(idx: JourneyIndex, c: _Collector) -> None:
    for sid, src in idx.sources.items():
        if src.get("pii_status") == "contains_pii":
            c.add(
                "L080",
                ERROR,
                "privacy",
                f"Quelle «{sid}» enthält Personendaten (pii_status = contains_pii).",
                f"sources[{sid}]",
                hint="Vor dem Teilen anonymisieren oder pseudonymisieren; nur die Ablage referenzieren, nicht das Material.",
            )
    for aid, atom in idx.evidence.items():
        for label, pattern in _PII_PATTERNS:
            if pattern.search(atom.get("text", "")):
                c.add(
                    "L081",
                    WARN,
                    "privacy",
                    f"Evidenz «{aid}» enthält möglicherweise eine {label}.",
                    f"evidence[{aid}]",
                )
                break


def _rule_kpi(idx: JourneyIndex, c: _Collector) -> None:
    kpis: list[tuple[str, dict[str, Any]]] = []
    for pi, phase in enumerate(idx.journey["phases"]):
        kpis += [(f"phases[{pi}].kpis", k) for k in phase.get("kpis", [])]
        for si, step in enumerate(phase["steps"]):
            kpis += [(f"phases[{pi}].steps[{si}].kpis", k) for k in step.get("kpis", [])]
    if not kpis:
        c.add(
            "L090",
            INFO,
            "kpi",
            "Keine Kennzahlen hinterlegt.",
            hint="Pro Phase mindestens eine Outcome-Kennzahl (Erledigungsquote, Rückfragen, Durchlaufzeit) - sonst lässt sich Wirkung nicht zeigen.",
        )
        return
    for path, k in kpis:
        name = k.get("name", "").lower()
        if any(term in name for term in COMMERCIAL_KPI_TERMS):
            c.add(
                "L091",
                INFO,
                "kpi",
                f"Kennzahl «{k['name']}» ist kommerziell geprägt.",
                path,
                hint="In Verwaltungsbegriffe übersetzen (Conversion → Anteil erledigter Anliegen, Churn → Ausweichen in Workarounds oder Beschwerden); Original in commercial_equivalent festhalten.",
            )
    leading = [k for _, k in kpis if k.get("indicator_type") == "leading"]
    if not leading:
        c.add(
            "L092",
            INFO,
            "kpi",
            "Nur Spätindikatoren (lagging) - kein Frühwarnsignal.",
            hint="Aufwand pro Anliegen oder Rückfragequote pro Schritt sind Frühindikatoren.",
        )


def _rule_evidence_quality(idx: JourneyIndex, c: _Collector) -> None:
    used = {ref for _, ref in idx.all_refs()}
    unused = [aid for aid in idx.evidence if aid not in used]
    if unused:
        c.add(
            "L100",
            INFO,
            "evidence",
            f"{len(unused)} Evidenz-Atom(e) werden nirgends referenziert: {', '.join(unused[:6])}{'…' if len(unused) > 6 else ''}.",
            "evidence",
            hint="Nicht synthetisiertes Material - entweder einordnen oder bewusst als «ausserhalb Scope» markieren.",
        )
    contradictions = [a for a in idx.evidence.values() if a.get("contradicts")]
    for a in contradictions:
        c.add(
            "L101",
            INFO,
            "evidence",
            f"Evidenz «{a['id']}» widerspricht {', '.join(a['contradicts'])}.",
            f"evidence[{a['id']}]",
            hint="Widersprüche gehören in die Journey (z. B. als Edge Case oder offene Frage), nicht geglättet.",
        )
    no_locator = [
        a["id"] for a in idx.evidence.values() if a["class"] != "assumed" and not a.get("locator")
    ]
    if no_locator:
        c.add(
            "L102",
            INFO,
            "evidence",
            f"{len(no_locator)} Primärevidenz(en) ohne Fundstelle (locator).",
            "evidence",
            hint="Ohne Fundstelle lässt sich ein Zitat nicht nachprüfen.",
        )


# ---------------------------------------------------------------------------
# Einstieg
# ---------------------------------------------------------------------------


def lint_journey(journey: dict[str, Any], today: date | None = None) -> list[Finding]:
    """Alle Befunde, sortiert nach Stufe und Code. Setzt eine schema-valide Journey voraus."""
    today = today or date.today()
    idx = JourneyIndex.build(journey)
    c = _Collector()
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
