"""Kommandozeile: validate · lint · render · export · diff · new · schema.

Texte je Sprache in ``cli_texts.py``. Sprache: ``--lang``, sonst meta.language der
Journey, sonst die Umgebungsvariable JOURNEYKIT_LANG, sonst Deutsch.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from . import SCHEMA_VERSION, __version__, load_journey, load_schema
from .cli_texts import env_language
from .cli_texts import text as _text
from .diff import diff_journeys, diff_markdown
from .export import actions_csv, audit_markdown, opportunities_markdown, story_map_markdown
from .lint import ERROR, INFO, WARN, lint_journey, summarize
from .lint_messages import LANGUAGES, SUMMARY
from .render import render_html
from .validate import validate_journey


def _lang(journey: object, explicit: str | None = None) -> str:
    """--lang, sonst meta.language der Journey, sonst JOURNEYKIT_LANG, sonst de."""
    if explicit:
        return explicit
    meta = journey.get("meta") if isinstance(journey, dict) else None
    meta_lang = meta.get("language") if isinstance(meta, dict) else None
    return meta_lang if meta_lang in LANGUAGES else env_language()


def _early_lang(argv: list[str]) -> str:
    """Sprache der Hilfe, bevor argparse gelaufen ist: --lang im Aufruf, sonst Umgebung."""
    for i, arg in enumerate(argv):
        value = arg.split("=", 1)[1] if arg.startswith("--lang=") else None
        if arg == "--lang" and i + 1 < len(argv):
            value = argv[i + 1]
        if value in LANGUAGES:
            return value
    return env_language()


def _write(text: str, out: str | None, lang: str = "de") -> None:
    if out:
        Path(out).write_text(text, encoding="utf-8")
        print(_text(lang, "written", path=out), file=sys.stderr)
    else:
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")


def _load_valid(path: str, explicit_lang: str | None = None) -> dict:
    journey = load_journey(path)
    errors = validate_journey(journey)
    if errors:
        lang = _lang(journey, explicit_lang)
        print(_text(lang, "schema_errors", path=path, n=len(errors)), file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        sys.exit(2)
    return journey


# -- Befehle -----------------------------------------------------------------


def cmd_validate(args: argparse.Namespace) -> int:
    rc = 0
    for path in args.files:
        journey = load_journey(path)
        errors = validate_journey(journey)
        lang = _lang(journey, args.lang)
        if errors:
            rc = 2
            print(_text(lang, "invalid", path=path, n=len(errors)))
            for e in errors:
                print(f"  {e}")
        else:
            print(_text(lang, "valid", path=path))
    return rc


def cmd_lint(args: argparse.Namespace) -> int:
    today = date.fromisoformat(args.today) if args.today else None
    worst = 0
    for path in args.files:
        journey = _load_valid(path, args.lang)
        lang = _lang(journey, args.lang)
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
    journeys = [_load_valid(p, args.lang) for p in args.files]
    lang = _lang(journeys[0], args.lang)
    html = render_html(journeys, title=args.title, lang=lang)
    out = args.output or (
        Path(args.files[0]).with_suffix(".html").name if len(args.files) == 1 else "journeys.html"
    )
    _write(html, out, lang)
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    journey = _load_valid(args.file, args.lang)
    lang = _lang(journey, args.lang)
    if args.format == "storymap":
        text = story_map_markdown(journey, lang=lang)
    elif args.format == "actions":
        text = actions_csv(journey)
    elif args.format == "opportunities":
        text = opportunities_markdown(journey, lang=lang)
    elif args.format == "audit":
        text = audit_markdown(journey, lint_journey(journey, lang=lang), lang=lang)
    else:  # pragma: no cover - argparse schützt
        raise SystemExit(f"unbekanntes Format {args.format}")
    _write(text, args.output, lang)
    return 0


def cmd_diff(args: argparse.Namespace) -> int:
    old, new = _load_valid(args.old, args.lang), _load_valid(args.new, args.lang)
    d = diff_journeys(old, new)
    lang = _lang(new, args.lang)
    _write(diff_markdown(d, lang=lang), args.output, lang)
    return 0 if d.is_empty() else 1


def cmd_schema(args: argparse.Namespace) -> int:
    _write(json.dumps(load_schema(), ensure_ascii=False, indent=2), args.output, env_language())
    return 0


def scaffold(
    journey_id: str, title: str, persona: str, role: str, goal: str, lang: str = "de"
) -> dict:
    """Minimal valide Journey im Status «hypothesis» - Startpunkt für Workshop und Synthese.

    ``lang`` setzt meta.language und die Sprache der Platzhalter (TODO-Texte).
    """
    today = date.today().isoformat()

    def t(key: str) -> str:
        return _text(lang, f"scaffold.{key}")

    return {
        "schema_version": SCHEMA_VERSION,
        "meta": {
            "id": journey_id,
            "title": title,
            "version": "0.1",
            "status": "hypothesis",
            "map_type": "user_journey",
            "language": lang,
            "created": today,
            "updated": today,
            "diagnosis": {"rationale": t("diagnosis")},
            "owner": {"role": t("owner")},
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
                "name": t("phase"),
                "steps": [
                    {
                        "id": "step-1-1",
                        "name": t("step"),
                        "action": t("action"),
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
                "text": t("question"),
                "proposed_method": "interview",
            }
        ],
        "changelog": [{"version": "0.1", "date": today, "summary": t("changelog")}],
    }


def cmd_new(args: argparse.Namespace) -> int:
    lang = args.lang or env_language()
    journey = scaffold(args.id, args.title, args.persona, args.role, args.goal, lang)
    _write(json.dumps(journey, ensure_ascii=False, indent=2), args.output, lang)
    return 0


# -- Parser ------------------------------------------------------------------


def build_parser(lang: str = "de") -> argparse.ArgumentParser:
    def h(key: str) -> str:
        return _text(lang, f"help.{key}")

    p = argparse.ArgumentParser(prog="journeykit", description=h("description"), epilog=h("epilog"))
    p.add_argument(
        "--version", action="version", version=f"journeykit {__version__} (schema {SCHEMA_VERSION})"
    )
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("validate", help=h("validate"))
    s.add_argument("files", nargs="+")
    s.add_argument("--lang", choices=LANGUAGES, help=h("lint_lang"))
    s.set_defaults(func=cmd_validate)

    s = sub.add_parser("lint", help=h("lint"))
    s.add_argument("files", nargs="+")
    s.add_argument("--strict", action="store_true", help=h("strict"))
    s.add_argument("--quiet", action="store_true", help=h("quiet"))
    s.add_argument("--format", choices=["text", "json"], default="text")
    s.add_argument("--today", help=h("today"))
    s.add_argument("--lang", choices=LANGUAGES, help=h("lint_lang"))
    s.set_defaults(func=cmd_lint)

    s = sub.add_parser("render", help=h("render"))
    s.add_argument("files", nargs="+")
    s.add_argument("-o", "--output")
    s.add_argument("--title")
    s.add_argument("--lang", choices=LANGUAGES, help=h("render_lang"))
    s.set_defaults(func=cmd_render)

    s = sub.add_parser("export", help=h("export"))
    s.add_argument("file")
    s.add_argument(
        "--format", choices=["storymap", "actions", "opportunities", "audit"], required=True
    )
    s.add_argument("-o", "--output")
    s.add_argument("--lang", choices=LANGUAGES, help=h("export_lang"))
    s.set_defaults(func=cmd_export)

    s = sub.add_parser("diff", help=h("diff"))
    s.add_argument("old")
    s.add_argument("new")
    s.add_argument("-o", "--output")
    s.add_argument("--lang", choices=LANGUAGES, help=h("diff_lang"))
    s.set_defaults(func=cmd_diff)

    s = sub.add_parser("schema", help=h("schema"))
    s.add_argument("-o", "--output")
    s.set_defaults(func=cmd_schema)

    s = sub.add_parser("new", help=h("new"))
    s.add_argument("id")
    s.add_argument("--title", required=True)
    s.add_argument("--persona", required=True)
    s.add_argument("--role", required=True)
    s.add_argument("--goal", required=True)
    s.add_argument("-o", "--output")
    s.add_argument("--lang", choices=LANGUAGES, help=h("new_lang"))
    s.set_defaults(func=cmd_new)
    return p


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    args = build_parser(_early_lang(argv)).parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
