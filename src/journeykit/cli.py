"""Kommandozeile: validate · lint · render · export · diff · new · schema."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from . import SCHEMA_VERSION, __version__, load_journey, load_schema
from .diff import diff_journeys, diff_markdown
from .export import actions_csv, audit_markdown, opportunities_markdown, story_map_markdown
from .lint import ERROR, INFO, WARN, lint_journey, summarize
from .lint_messages import LANGUAGES, SUMMARY, resolve_language
from .render import UI_LANGUAGES, render_html
from .validate import validate_journey


def _write(text: str, out: str | None) -> None:
    if out:
        Path(out).write_text(text, encoding="utf-8")
        print(f"geschrieben: {out}", file=sys.stderr)
    else:
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")


def _load_valid(path: str) -> dict:
    journey = load_journey(path)
    errors = validate_journey(journey)
    if errors:
        print(f"{path}: {len(errors)} Schema-Fehler", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        sys.exit(2)
    return journey


# -- Befehle -----------------------------------------------------------------


def cmd_validate(args: argparse.Namespace) -> int:
    rc = 0
    for path in args.files:
        errors = validate_journey(load_journey(path))
        if errors:
            rc = 2
            print(f"✗ {path}: {len(errors)} Schema-Fehler")
            for e in errors:
                print(f"  {e}")
        else:
            print(f"✓ {path}: schema-valide")
    return rc


def cmd_lint(args: argparse.Namespace) -> int:
    today = date.fromisoformat(args.today) if args.today else None
    worst = 0
    for path in args.files:
        journey = _load_valid(path)
        lang = resolve_language(journey, args.lang)
        findings = lint_journey(journey, today=today, lang=lang)
        counts = summarize(findings)
        if args.format == "json":
            print(
                json.dumps(
                    {"file": path, "summary": counts, "findings": [f.as_dict() for f in findings]},
                    ensure_ascii=False,
                    indent=2,
                )
            )
        else:
            print(
                SUMMARY[lang].format(
                    path=path, errors=counts[ERROR], warnings=counts[WARN], infos=counts[INFO]
                )
            )
            seen_codes: set[str] = set()
            for f in findings:
                if f.level == "INFO" and args.quiet:
                    continue
                # Hinweis nur beim ersten Befund eines Codes - bei elf Widersprüchen
                # muss der Satz nicht elfmal stehen.
                print(f"  {f.format(with_hint=f.code not in seen_codes)}")
                seen_codes.add(f.code)
        if counts[ERROR]:
            worst = max(worst, 1)
        if args.strict and counts[WARN]:
            worst = max(worst, 1)
    return worst


def cmd_render(args: argparse.Namespace) -> int:
    journeys = [_load_valid(p) for p in args.files]
    html = render_html(journeys, title=args.title, lang=args.lang)
    out = args.output or (
        Path(args.files[0]).with_suffix(".html").name if len(args.files) == 1 else "journeys.html"
    )
    _write(html, out)
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    journey = _load_valid(args.file)
    if args.format == "storymap":
        text = story_map_markdown(journey)
    elif args.format == "actions":
        text = actions_csv(journey)
    elif args.format == "opportunities":
        text = opportunities_markdown(journey)
    elif args.format == "audit":
        text = audit_markdown(journey, lint_journey(journey))
    else:  # pragma: no cover - argparse schützt
        raise SystemExit(f"unbekanntes Format {args.format}")
    _write(text, args.output)
    return 0


def cmd_diff(args: argparse.Namespace) -> int:
    d = diff_journeys(_load_valid(args.old), _load_valid(args.new))
    _write(diff_markdown(d), args.output)
    return 0 if d.is_empty() else 1


def cmd_schema(args: argparse.Namespace) -> int:
    _write(json.dumps(load_schema(), ensure_ascii=False, indent=2), args.output)
    return 0


def scaffold(journey_id: str, title: str, persona: str, role: str, goal: str) -> dict:
    """Minimal valide Journey im Status «hypothesis» - Startpunkt für Workshop und Synthese."""
    today = date.today().isoformat()
    return {
        "schema_version": SCHEMA_VERSION,
        "meta": {
            "id": journey_id,
            "title": title,
            "version": "0.1",
            "status": "hypothesis",
            "map_type": "user_journey",
            "language": "de",
            "created": today,
            "updated": today,
            "diagnosis": {
                "rationale": "TODO: Warum ist das eine User Journey und kein Service Blueprint oder User Flow?"
            },
            "owner": {"role": "TODO: verantwortliche Rolle"},
            "review_cycle_days": 180,
        },
        "persona": {
            "id": "p-" + journey_id[:20],
            "name": persona,
            "role": role,
            "goals": [],
            "frustrations": [],
            "evidence_refs": [],
            "is_hypothesis": True,
        },
        "scenario": {"title": title, "goal": goal, "scope_exclusions": [], "evidence_refs": []},
        "phases": [
            {
                "id": "phase-1",
                "name": "TODO Phase 1",
                "steps": [
                    {
                        "id": "step-1-1",
                        "name": "TODO Schritt",
                        "action": "TODO: Was tut die Persona?",
                        "thinking": [],
                        "feeling": None,
                        "pain_points": [],
                        "edge_cases": [],
                        "recovery_paths": [],
                        "evidence_refs": [],
                    }
                ],
            }
        ],
        "opportunities": [],
        "sources": [],
        "evidence": [],
        "open_questions": [
            {
                "text": "TODO: Welche Erhebung validiert diese Hypothesen zuerst?",
                "proposed_method": "interview",
            }
        ],
        "changelog": [{"version": "0.1", "date": today, "summary": "Gerüst angelegt"}],
    }


def cmd_new(args: argparse.Namespace) -> int:
    journey = scaffold(args.id, args.title, args.persona, args.role, args.goal)
    _write(json.dumps(journey, ensure_ascii=False, indent=2), args.output)
    return 0


# -- Parser ------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="journeykit",
        description="Evidenzbasierte User Journeys: prüfen, rendern, exportieren.",
    )
    p.add_argument(
        "--version", action="version", version=f"journeykit {__version__} (schema {SCHEMA_VERSION})"
    )
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("validate", help="Schema-Validierung")
    s.add_argument("files", nargs="+")
    s.set_defaults(func=cmd_validate)

    s = sub.add_parser("lint", help="Methodische Prüfung (Fallstricke)")
    s.add_argument("files", nargs="+")
    s.add_argument("--strict", action="store_true", help="Warnungen gelten als Fehler (Exit 1)")
    s.add_argument("--quiet", action="store_true", help="Hinweise (INFO) unterdrücken")
    s.add_argument("--format", choices=["text", "json"], default="text")
    s.add_argument("--today", help="Stichtag für Review-Prüfungen (YYYY-MM-DD)")
    s.add_argument(
        "--lang",
        choices=LANGUAGES,
        help="Sprache der Meldungen (Standard: meta.language der Journey, sonst de)",
    )
    s.set_defaults(func=cmd_lint)

    s = sub.add_parser(
        "render", help="Interaktives HTML erzeugen (mehrere Dateien = Persona-Vergleich)"
    )
    s.add_argument("files", nargs="+")
    s.add_argument("-o", "--output")
    s.add_argument("--title")
    s.add_argument(
        "--lang",
        choices=UI_LANGUAGES,
        help="Sprache der Oberfläche (Standard: meta.language der ersten Journey, sonst de)",
    )
    s.set_defaults(func=cmd_render)

    s = sub.add_parser("export", help="Story Map, Massnahmenliste, Chancenmatrix, Audit-Report")
    s.add_argument("file")
    s.add_argument(
        "--format", choices=["storymap", "actions", "opportunities", "audit"], required=True
    )
    s.add_argument("-o", "--output")
    s.set_defaults(func=cmd_export)

    s = sub.add_parser("diff", help="Modelländerungen zwischen zwei Versionen")
    s.add_argument("old")
    s.add_argument("new")
    s.add_argument("-o", "--output")
    s.set_defaults(func=cmd_diff)

    s = sub.add_parser("schema", help="JSON Schema ausgeben")
    s.add_argument("-o", "--output")
    s.set_defaults(func=cmd_schema)

    s = sub.add_parser("new", help="Gerüst einer Journey anlegen (Status hypothesis)")
    s.add_argument("id")
    s.add_argument("--title", required=True)
    s.add_argument("--persona", required=True)
    s.add_argument("--role", required=True)
    s.add_argument("--goal", required=True)
    s.add_argument("-o", "--output")
    s.set_defaults(func=cmd_new)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
