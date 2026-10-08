"""Testsatz für die Extraktion: Prompts erzeugen und Extraktionen gegen das Gold bewerten.

Prüft die Prompt-Schablone in ``skill/user-journey/references/evidenz.md``. Jeder
Fall unter ``skill/user-journey/evals/extraction/cases/<fall>/`` hat

- ``input.*``       die Quelle (synthetisch),
- ``case.json``     die Werte für die Schablone und die Regeln des Falls,
- ``expected.json`` das Gold: Atome, die eine gute Extraktion enthalten muss,
- ``reference.json`` eine von Hand erstellte korrekte Extraktion (Selbsttest).

Ablauf::

    python scripts/eval_extraction.py prompts -o /tmp/prompts      # gefüllte Prompts
    # je Fall den Prompt an ein Modell geben, Antwort als <fall>.json speichern
    python scripts/eval_extraction.py score /tmp/antworten -o bericht.md

Entwicklerwerkzeug – Ausgaben nur deutsch. Keine Abhängigkeit von einem LLM:
Das Skript bewertet, es extrahiert nicht.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from journeykit import load_schema
from journeykit.lint import _PII_PATTERNS

ROOT = Path(__file__).resolve().parents[1]
CASES_DIR = ROOT / "skill" / "user-journey" / "evals" / "extraction" / "cases"
EVIDENZ_MD = ROOT / "skill" / "user-journey" / "references" / "evidenz.md"
TEMPLATE_HEADING = "## Prompt-Schablone für die Extraktion"


# -- Fälle und Schablone ------------------------------------------------------


@dataclass
class Case:
    id: str
    path: Path
    config: dict[str, Any]
    expected: dict[str, Any]
    input_name: str
    input_text: str

    @property
    def rules(self) -> dict[str, Any]:
        return self.config.get("rules", {})


def load_cases(cases_dir: Path = CASES_DIR) -> list[Case]:
    out = []
    for d in sorted(p for p in cases_dir.iterdir() if (p / "case.json").exists()):
        config = json.loads((d / "case.json").read_text(encoding="utf-8"))
        expected = json.loads((d / "expected.json").read_text(encoding="utf-8"))
        text = (d / config["input"]).read_text(encoding="utf-8")
        out.append(Case(d.name, d, config, expected, config["input"], text))
    return out


def template(evidenz_md: Path = EVIDENZ_MD) -> str:
    """Den Codeblock unter «Prompt-Schablone für die Extraktion» – die Schablone, wie sie im Skill steht."""
    text = evidenz_md.read_text(encoding="utf-8")
    after = text.split(TEMPLATE_HEADING, 1)[1]
    m = re.search(r"```\n(.*?)```", after, re.S)
    if not m:
        raise ValueError("Keine Prompt-Schablone in evidenz.md gefunden.")
    return m.group(1)


def placeholders(tmpl: str) -> set[str]:
    return set(re.findall(r"\{(\w+)\}", tmpl))


def template_values(case: Case) -> dict[str, str]:
    c = case.config
    known = "; ".join(f"{a['id']}: «{a['text']}»" for a in c.get("known_atoms", [])) or "keine"
    return {
        "title": c["title"],
        "kind": c["kind"],
        "class": c["class"],
        "source_id": c["source_id"],
        "phasen": ", ".join(c["phases"]),
        "persona": c["persona"],
        "bekannte_atome": known,
        "prefix": c["prefix"],
    }


def render_prompt(case: Case, tmpl: str | None = None) -> str:
    tmpl = template() if tmpl is None else tmpl
    prompt = tmpl.format(**template_values(case))
    return f"{prompt}\nQuelle «{case.input_name}»:\n\n```\n{case.input_text}```\n"


# -- Bewertung -----------------------------------------------------------------


def _norm(text: str) -> str:
    text = text.replace(" ", " ").replace(" ", " ")
    return re.sub(r"\s+", " ", text).strip()


def _strip_quotes(text: str) -> str:
    return text.strip().strip("«»\"„“”'").strip()


def is_verbatim(quote: str, source: str) -> bool:
    """Zitat steht wörtlich in der Quelle.

    Erlaubt sind Auslassungen («…», «...») und Ersetzungen in eckigen Klammern
    («[Name]», «[…]») – so verlangt es evidenz.md für Personendaten in Zitaten.
    """
    haystack = _norm(source)
    pos = 0
    for part in re.split(r"\[[^\]]*\]|…|\.\.\.", _strip_quotes(_norm(quote))):
        part = part.strip(" ,;")
        if not part:
            continue
        found = haystack.find(part, pos)
        if found < 0:
            return False
        pos = found + len(part)
    return True


def _numbers(atom: dict[str, Any]) -> set[float]:
    out: set[float] = set()
    value = atom.get("value")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        out.add(float(value))
    elif isinstance(value, str):
        out |= {float(x.replace(",", ".")) for x in re.findall(r"\d+(?:[.,]\d+)?", value)}
    out |= {
        float(x.replace(",", ".")) for x in re.findall(r"\d+(?:[.,]\d+)?", atom.get("text", ""))
    }
    return out


def matches(gold: dict[str, Any], atom: dict[str, Any]) -> bool:
    """Gold-Atom gefunden: Textbaustein in text oder locator, bei Messwerten auch der Wert."""
    text = _norm(f"{atom.get('text', '')} {atom.get('locator') or ''}").casefold()
    ok = False
    for alt in gold["match"]:
        parts = [alt] if isinstance(alt, str) else alt
        if all(p.casefold() in text for p in parts):
            ok = True
            break
    if ok and gold.get("value_any"):
        ok = bool(_numbers(atom) & {float(v) for v in gold["value_any"]})
    return ok


def _emotion_ok(rule: str, atom: dict[str, Any]) -> bool:
    hint = atom.get("emotion_hint")
    if rule == "any":
        return True
    if rule == "none":
        return not hint
    if rule == "not_explicit":
        return not hint or hint.get("explicit") is not True
    if rule in ("explicit_negative", "explicit_positive"):
        if not hint or hint.get("explicit") is not True:
            return False
        valence = hint.get("valence", 0)
        return valence < 0 if rule == "explicit_negative" else valence > 0
    raise ValueError(f"unbekannte Emotionsregel {rule}")


def field_checks(gold: dict[str, Any], atom: dict[str, Any]) -> list[tuple[str, bool, Any, Any]]:
    """(Feld, ok, erwartet, erhalten) für jedes Feld, das das Gold vorgibt."""
    out = []
    for name in ("kind", "class", "signal"):
        if name in gold:
            out.append((name, atom.get(name) in gold[name], gold[name], atom.get(name)))
    if "locator" in gold:
        loc = (atom.get("locator") or "").casefold()
        ok = bool(loc) and any(x.casefold() in loc for x in gold["locator"])
        out.append(("locator", ok, gold["locator"], atom.get("locator")))
    if "emotion" in gold:
        out.append(
            (
                "emotion",
                _emotion_ok(gold["emotion"], atom),
                gold["emotion"],
                atom.get("emotion_hint"),
            )
        )
    if "value" in gold:
        try:
            ok = float(atom.get("value")) == float(gold["value"])
        except (TypeError, ValueError):
            ok = False
        out.append(("value", ok, gold["value"], atom.get("value")))
    if "unit" in gold:
        ok = _norm(str(atom.get("unit", ""))).casefold() == gold["unit"].casefold()
        out.append(("unit", ok, gold["unit"], atom.get("unit")))
    if "contradicts" in gold:
        ok = set(gold["contradicts"]) <= set(atom.get("contradicts", []))
        out.append(("contradicts", ok, gold["contradicts"], atom.get("contradicts", [])))
    return out


@dataclass
class CaseResult:
    case: str
    n_atoms: int
    required: int
    found_required: int
    missing: list[str] = field(default_factory=list)
    fields: list[tuple[str, str, bool, Any, Any]] = field(default_factory=list)
    violations: list[tuple[str, str, str]] = field(default_factory=list)
    unmatched: list[str] = field(default_factory=list)

    @property
    def recall(self) -> float:
        return self.found_required / self.required if self.required else 1.0

    @property
    def field_accuracy(self) -> float:
        return sum(1 for f in self.fields if f[2]) / len(self.fields) if self.fields else 1.0


_ATOM_VALIDATOR = None


def _atom_errors(atom: dict[str, Any]) -> list[str]:
    global _ATOM_VALIDATOR
    if _ATOM_VALIDATOR is None:
        schema = load_schema()
        _ATOM_VALIDATOR = Draft202012Validator(
            {"$ref": "#/$defs/evidence_atom", "$defs": schema["$defs"]}
        )
    return [e.message for e in _ATOM_VALIDATOR.iter_errors(atom)]


def rule_violations(case: Case, atoms: list[dict[str, Any]]) -> list[tuple[str, str, str]]:
    """(Atom-ID, Regel, Detail) – Verstösse gegen die Regeln aus evidenz.md und die des Falls."""
    c, rules, out = case.config, case.rules, []
    n = len(atoms)
    if not rules.get("atoms_min", 0) <= n <= rules.get("atoms_max", 10**6):
        out.append(
            (
                "–",
                "anzahl",
                f"{n} Atome, erwartet {rules.get('atoms_min')}–{rules.get('atoms_max')}",
            )
        )
    ids = [a.get("id", "?") for a in atoms]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        out.append((dup, "id", "doppelt vergeben"))
    for a in atoms:
        aid = a.get("id", "?")
        for err in _atom_errors(a):
            out.append((aid, "schema", err))
        if not str(aid).startswith(f"{c['prefix']}-"):
            out.append((aid, "id", f"Präfix «{c['prefix']}-» fehlt"))
        if a.get("source_ref") != c["source_id"]:
            out.append((aid, "source_ref", f"«{a.get('source_ref')}» statt «{c['source_id']}»"))
        if a.get("class") != c["class"]:
            out.append((aid, "klasse", f"{a.get('class')} statt {c['class']}"))
        if rules.get("kinds") and a.get("kind") not in rules["kinds"]:
            out.append((aid, "art", f"{a.get('kind')} – erlaubt: {', '.join(rules['kinds'])}"))
        text = a.get("text", "")
        if a.get("kind") == "quote" and not is_verbatim(text, case.input_text):
            out.append((aid, "wörtlich", "Zitat steht so nicht in der Quelle"))
        if rules.get("locator_required") and not (a.get("locator") or "").strip():
            out.append((aid, "fundstelle", "locator fehlt"))
        hits = [t for t in rules.get("pii_terms", []) if t.casefold() in text.casefold()]
        hits += [label for label, rx in _PII_PATTERNS if rx.search(text)]
        if hits:
            out.append((aid, "personendaten", ", ".join(hits)))
        for f in rules.get("forbidden", []):
            if _norm(f["text"]).casefold() in _norm(text).casefold():
                out.append((aid, "keine-evidenz", f["why"]))
        hint = a.get("emotion_hint")
        if rules.get("no_emotion") and hint:
            out.append((aid, "emotion", "emotion_hint in einer Quelle ohne Gefühlsäusserungen"))
        if rules.get("no_explicit_emotion") and hint and hint.get("explicit") is True:
            out.append((aid, "emotion", "explicit true, obwohl niemand ein Gefühl äussert"))
    if rules.get("one_atom_per_locator"):
        by_loc: dict[str, list[str]] = {}
        for a in atoms:
            loc = _norm(a.get("locator") or "")
            if loc:
                by_loc.setdefault(loc, []).append(a.get("id", "?"))
        for loc, group in by_loc.items():
            if len(group) > 1:
                out.append(
                    (
                        ", ".join(group),
                        "aufgeteilt",
                        f"eine Aussage ({loc}) auf {len(group)} Atome verteilt",
                    )
                )
    obs = rules.get("observations")
    if obs:
        pattern = re.compile(obs["locator_pattern"])
        k = sum(
            1
            for a in atoms
            if a.get("kind") == "observation" and pattern.search(a.get("locator") or "")
        )
        if not obs["min"] <= k <= obs["max"]:
            out.append(
                (
                    "–",
                    "einzelfälle",
                    f"{k} Einzelfälle mit Ticket-ID, erwartet {obs['min']}–{obs['max']}",
                )
            )
    return out


def score_case(case: Case, atoms: list[dict[str, Any]]) -> CaseResult:
    gold = case.expected["atoms"]
    res = CaseResult(case.id, len(atoms), sum(1 for g in gold if g.get("required")), 0)
    used: set[int] = set()
    for g in gold:
        # unter den passenden Atomen das mit den meisten erfüllten Feldern – nicht einfach das erste
        candidates = [i for i, a in enumerate(atoms) if i not in used and matches(g, a)]
        hit = max(
            candidates,
            key=lambda i: (sum(ok for _, ok, _, _ in field_checks(g, atoms[i])), -i),
            default=None,
        )
        if hit is None:
            if g.get("required"):
                res.missing.append(g["key"])
            continue
        used.add(hit)
        if g.get("required"):
            res.found_required += 1
        res.fields += [(g["key"], *check) for check in field_checks(g, atoms[hit])]
    res.unmatched = [a.get("id", "?") for i, a in enumerate(atoms) if i not in used]
    res.violations = rule_violations(case, atoms)
    return res


def parse_candidate(text: str) -> list[dict[str, Any]]:
    """JSON-Array der Atome; Codezäune und ein umschliessendes Objekt {"atoms": [...]} werden toleriert."""
    m = re.search(r"```(?:json)?\s*\n(.*?)```", text, re.S)
    data = json.loads(m.group(1) if m else text)
    if isinstance(data, dict):
        data = data.get("atoms", [])
    if not isinstance(data, list):
        raise ValueError("Erwartet ein JSON-Array von Atomen.")
    return data


# -- Bericht ---------------------------------------------------------------------


def report_markdown(results: list[CaseResult], title: str = "Extraktion gegen Gold") -> str:
    lines = [f"# {title}", ""]
    lines.append("| Fall | Atome | Pflicht-Atome gefunden | Feldtreue | Regelverstösse |")
    lines.append("|---|---|---|---|---|")
    for r in results:
        lines.append(
            f"| {r.case} | {r.n_atoms} | {r.found_required}/{r.required} ({r.recall:.0%}) "
            f"| {sum(1 for f in r.fields if f[2])}/{len(r.fields)} ({r.field_accuracy:.0%}) | {len(r.violations)} |"
        )
    req = sum(r.required for r in results)
    found = sum(r.found_required for r in results)
    fld = sum(len(r.fields) for r in results)
    ok = sum(1 for r in results for f in r.fields if f[2])
    vio = sum(len(r.violations) for r in results)
    lines.append(
        f"| **gesamt** | {sum(r.n_atoms for r in results)} | {found}/{req} ({found / req if req else 1:.0%}) "
        f"| {ok}/{fld} ({ok / fld if fld else 1:.0%}) | {vio} |"
    )
    for r in results:
        problems = [f for f in r.fields if not f[2]]
        if not (r.missing or problems or r.violations):
            continue
        lines += ["", f"## {r.case}", ""]
        if r.missing:
            lines.append(f"- **Fehlende Pflicht-Atome:** {', '.join(r.missing)}")
        for key, name, _, want, got in problems:
            lines.append(f"- **{key}** – {name}: erwartet {want}, erhalten {got}")
        for aid, rule, detail in r.violations:
            lines.append(f"- Regel **{rule}** ({aid}): {detail}")
    return "\n".join(lines) + "\n"


# -- Kommandozeile -------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("prompts", help="Gefüllte Prompts je Fall schreiben")
    s.add_argument("-o", "--output", required=True)
    s = sub.add_parser("score", help="Extraktionen (<fall>.json) gegen das Gold bewerten")
    s.add_argument("candidates")
    s.add_argument("-o", "--output")
    s.add_argument("--title", default="Extraktion gegen Gold")
    args = p.parse_args(argv)

    cases = load_cases()
    if args.cmd == "prompts":
        out = Path(args.output)
        out.mkdir(parents=True, exist_ok=True)
        for case in cases:
            (out / f"{case.id}.prompt.md").write_text(render_prompt(case), encoding="utf-8")
        print(f"{len(cases)} Prompts geschrieben: {out}", file=sys.stderr)
        return 0

    results = []
    for case in cases:
        f = Path(args.candidates) / f"{case.id}.json"
        if not f.exists():
            print(f"fehlt: {f}", file=sys.stderr)
            continue
        results.append(score_case(case, parse_candidate(f.read_text(encoding="utf-8"))))
    report = report_markdown(results, args.title)
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
    else:
        sys.stdout.write(report)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
