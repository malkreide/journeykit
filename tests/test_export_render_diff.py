from __future__ import annotations

import copy
import json
import xml.etree.ElementTree as ET
from datetime import date

from journeykit.cli import main
from journeykit.diff import diff_journeys, diff_markdown
from journeykit.export import (
    HEATMAP_KINDS,
    _wrap,
    actions_csv,
    audit_markdown,
    evidence_heatmap,
    heatmap_csv,
    heatmap_svg,
    opportunities_markdown,
    story_map_markdown,
)
from journeykit.lint import lint_journey
from journeykit.model import JourneyIndex, priority_quadrant, propose_verdict
from journeykit.render import PLACEHOLDER, render_html


def test_story_map_contains_backbone_and_mvp(example_journey):
    md = story_map_markdown(example_journey)
    for phase in example_journey["phases"]:
        assert phase["name"] in md
    assert "✅" in md
    assert "Quick Win" in md


def test_actions_csv_has_one_row_per_pain_point(example_journey):
    csv_text = actions_csv(example_journey)
    rows = [r for r in csv_text.splitlines() if r.strip()]
    n_pp = sum(len(s.get("pain_points", [])) for p in example_journey["phases"] for s in p["steps"])
    assert len(rows) == n_pp + 1
    assert rows[0].startswith("phase;step;pain_point_id")


def test_opportunities_markdown_lists_all(example_journey):
    md = opportunities_markdown(example_journey)
    for opp in example_journey["opportunities"]:
        assert opp["hmw"] in md


def test_audit_markdown(example_journey):
    md = audit_markdown(example_journey, lint_journey(example_journey))
    assert "## Evidenzlage" in md
    assert "Synthetisches Beispiel" in md
    assert "## Offene Fragen" in md


def test_audit_markdown_has_diagnosis_verdict_and_next_steps(example_journey):
    md = audit_markdown(example_journey, lint_journey(example_journey))
    head = md[: md.index("## Evidenzlage")]
    assert "## Diagnose" in head and example_journey["meta"]["diagnosis"]["rationale"] in head
    assert "## Urteil (Vorschlag)" in head and "**Belastbar**" in head
    assert "## Nächste Schritte" in head


def test_verdict_poster_names_what_is_missing(minimal):
    assert propose_verdict(JourneyIndex.build(minimal)).kind == "robust"
    del minimal["meta"]["owner"]
    minimal["opportunities"][0].pop("linked_pain_points")
    minimal["opportunities"][0].pop("phase_ref")
    v = propose_verdict(JourneyIndex.build(minimal))
    assert (v.kind, v.missing) == ("poster", ("owner", "anchored_opportunity"))
    md = audit_markdown(minimal, lint_journey(minimal))
    assert "**Poster**" in md and "meta.owner" in md


def test_step_ref_anchors_an_opportunity(minimal):
    minimal["phases"].append(
        {
            "id": "phase-2",
            "name": "Danach",
            "steps": [{"id": "step-2-1", "name": "Nachfragen", "action": "Ruft an."}],
        }
    )
    opp = minimal["opportunities"][0]
    for key in ("linked_pain_points", "phase_ref"):
        opp.pop(key)
    opp["step_ref"] = "step-2-1"
    idx = JourneyIndex.build(minimal)
    assert idx.opportunity_anchor(opp) == ("phase-2", "step-2-1")
    assert propose_verdict(idx).kind != "poster"
    md = story_map_markdown(minimal)
    assert f"### Danach\n**{opp['hmw']}**" in md


def test_verdict_hypothesis_names_failed_conditions(minimal):
    minimal["meta"]["status"] = "hypothesis"
    for atom in minimal["evidence"]:
        atom["class"] = "assumed"
    minimal["phases"][0]["steps"][0]["recovery_paths"] = []
    v = propose_verdict(JourneyIndex.build(minimal))
    assert v.kind == "hypothesis"
    assert v.reasons == ("low_primary", "status_hypothesis", "breakdown_without_recovery")
    assert v.primary_pct == 0 and v.breakdowns_without_recovery == 1


def test_relayed_quotes_are_counted_and_put_the_source_request_first(minimal):
    # Eine übernommene Map: Die Zitate schreibt sie Nutzenden zu, die Quelle bleibt die Map.
    for atom in minimal["evidence"]:
        atom.update(source_ref="doc-1", **{"class": "assumed"})
    minimal["sources"] = [s for s in minimal["sources"] if s["id"] == "doc-1"]
    md = audit_markdown(minimal, lint_journey(minimal))
    assert "  - davon 3 Zitat(e), die die Quelle Nutzenden zuschreibt" in md
    steps = md[md.index("## Nächste Schritte") : md.index("## Evidenzlage")]
    assert steps.splitlines()[2].startswith("1. **Quellen anfordern**: 3 Zitat(e)")
    assert "Rückfrage festhalten (open_questions mit proposed_method: source_request)" in steps
    minimal["open_questions"].insert(
        0, {"text": "Rohmaterial anfordern.", "proposed_method": "source_request"}
    )
    md = audit_markdown(minimal, lint_journey(minimal))
    assert "Offene Frage: Rohmaterial anfordern." in md
    fr = audit_markdown(minimal, lint_journey(minimal, lang="fr"), lang="fr")
    assert "**Demander les sources**" in fr and "dont 3 citation(s)" in fr


def test_audit_lists_costs_without_total(minimal):
    md = audit_markdown(minimal, lint_journey(minimal))
    assert "## Kosten" not in md, "ohne Kosten kein Abschnitt"
    minimal["phases"][0]["steps"][0]["costs"] = [
        {
            "label": "Schulgeld",
            "amount": 820,
            "min": 410,
            "period": "semester",
            "paid_to": "Musikschule",
            "evidence_refs": ["ev-1", "ev-4"],
        },
        {"label": "Miete", "amount": 35.5, "period": "month", "evidence_refs": ["ev-2"]},
    ]
    md = audit_markdown(minimal, lint_journey(minimal))
    costs = md[md.index("## Kosten") : md.index("## Befunde")]
    assert (
        "| Brief erhalten | Schulgeld | 820 CHF (410–820) | pro Semester | Musikschule | berichtet, angenommen |"
        in costs
    )
    assert "| Brief erhalten | Miete | 35.5 CHF | pro Monat | – | berichtet |" in costs
    assert "Keine Summe" in costs
    fr = audit_markdown(minimal, lint_journey(minimal, lang="fr"), lang="fr")
    assert "## Coûts" in fr and "par semestre" in fr and "rapporté, supposé" in fr
    assert "pro Semester" not in fr


def test_audit_counts_chains_of_causes(minimal):
    assert "Ursachenketten" not in audit_markdown(minimal, lint_journey(minimal))
    minimal["phases"].append(
        {
            "id": "phase-2",
            "name": "Nachfassen",
            "steps": [
                {
                    "id": "step-2",
                    "name": "Nachfragen",
                    "action": "Die Persona ruft an.",
                    "pain_points": [
                        {
                            "id": "pp-2",
                            "text": "Vermeidbarer Kontakt",
                            "type": "friction",
                            "caused_by": ["pp-1"],
                            "evidence_refs": ["ev-2"],
                        }
                    ],
                }
            ],
        }
    )
    md = audit_markdown(minimal, lint_journey(minimal))
    assert (
        "- Ursachenketten: 1 Pain Point(s) mit Ursache im Modell, davon 1 über Phasen hinweg" in md
    )
    fr = audit_markdown(minimal, lint_journey(minimal, lang="fr"), lang="fr")
    assert "Chaînes de causes" in fr and "d'une phase à l'autre" in fr


def test_audit_counts_breakdowns_at_transitions(minimal):
    step = minimal["phases"][0]["steps"][0]
    step["pain_points"][0]["type"] = "friction"
    assert "an Übergängen" not in audit_markdown(minimal, lint_journey(minimal)), (
        "ohne Breakdown keine Zeile"
    )
    step["pain_points"][0]["type"] = "breakdown"
    md = audit_markdown(minimal, lint_journey(minimal))
    assert "- Breakdowns an Übergängen: 0 von 1 · Übergänge: 0 von 1 Schritten" in md
    step["is_transition"] = True
    minimal["phases"][0]["steps"].append(
        {"id": "step-2", "name": "Anrufen", "action": "Die Persona ruft an."}
    )
    md = audit_markdown(minimal, lint_journey(minimal))
    assert "- Breakdowns an Übergängen: 1 von 1 · Übergänge: 1 von 2 Schritten" in md
    fr = audit_markdown(minimal, lint_journey(minimal, lang="fr"), lang="fr")
    assert "- Ruptures aux transitions\u00a0: 1 sur 1 · transitions\u00a0: 1 sur 2 étapes" in fr


def test_quotes_from_user_sources_are_not_relayed(minimal):
    for atom in minimal["evidence"]:
        atom["class"] = "assumed"  # Klasse gesetzt, die Quelle bleibt das Interview
    md = audit_markdown(minimal, lint_journey(minimal))
    assert "Zitat(e), die die Quelle Nutzenden zuschreibt" not in md
    assert "Quellen anfordern" not in md


def test_open_questions_show_where_they_belong(minimal):
    minimal["open_questions"] = [
        {"text": "Warum rufen sie an?", "step_ref": "step-1-1", "phase_ref": "phase-1"},
        {"text": "Wie lange dauert es?", "phase_ref": "phase-1", "proposed_method": "analytics"},
        {"text": "Ohne Bezug."},
        {"text": "Verweis ins Leere.", "step_ref": "gibt-es-nicht"},
    ]
    md = audit_markdown(minimal, lint_journey(minimal))
    oq = md[md.index("## Offene Fragen") :].splitlines()
    assert "- «Brief erhalten»: Warum rufen sie an?" in oq
    assert "- «TODO Phase 1»: Wie lange dauert es? _(Methode: analytics)_" in oq
    assert "- Ohne Bezug." in oq and "- Verweis ins Leere." in oq
    fr = audit_markdown(minimal, lint_journey(minimal, lang="fr"), lang="fr")
    assert "- «\u202fBrief erhalten\u202f»\u00a0: Warum rufen sie an?" in fr.splitlines()


def test_to_be_concept_is_never_robust(minimal):
    assert propose_verdict(JourneyIndex.build(minimal)).kind == "robust"
    minimal["scenario"]["perspective"] = "to_be"
    v = propose_verdict(JourneyIndex.build(minimal))
    assert (v.kind, v.reasons) == ("hypothesis", ("to_be",))
    md = audit_markdown(minimal, lint_journey(minimal))
    head = md[: md.index("## Urteil (Vorschlag)")]
    assert "**Soll-Konzept** (`scenario.perspective: to_be`)" in head
    assert "**Hypothese**: ein Soll-Konzept" in md and "noch nicht belegt" not in md
    minimal["meta"]["status"] = "hypothesis"
    md = audit_markdown(minimal, lint_journey(minimal))
    assert "Ist-Journey begründen. Ausserdem: Status `hypothesis`." in md
    fr = audit_markdown(minimal, lint_journey(minimal, lang="fr"), lang="fr")
    assert "**Concept cible**" in fr and "un concept cible" in fr


def test_verdict_and_report_without_experience_claims(minimal):
    step = minimal["phases"][0]["steps"][0]
    step.update(thinking=[], feeling=None, pain_points=[], recovery_paths=[])
    minimal["opportunities"][0].pop("linked_pain_points")
    v = propose_verdict(JourneyIndex.build(minimal))
    assert (v.kind, v.reasons) == ("hypothesis", ("no_experience",))
    md = audit_markdown(minimal, lint_journey(minimal))
    assert "- Erlebnis-Aussagen: keine" in md
    assert "keine einzige Erlebnis-Aussage" in md
    assert "0% der Erlebnis-Aussagen" not in md


def test_next_steps_put_research_plan_first_and_stop_at_three(minimal):
    minimal["meta"]["status"] = "hypothesis"
    for atom in minimal["evidence"]:
        atom["class"] = "assumed"
    minimal["open_questions"] = []
    del minimal["meta"]["diagnosis"]
    minimal["phases"][0]["steps"][0]["feeling"] = None
    findings = lint_journey(minimal)
    md = audit_markdown(minimal, findings)
    steps = md[md.index("## Nächste Schritte") : md.index("## Evidenzlage")]
    numbered = [line for line in steps.splitlines() if line[:2] in {"1.", "2.", "3.", "4."}]
    assert len(numbered) == 3
    assert numbered[0].startswith("1. Erhebungsplan festhalten")
    codes = [line.split("**")[1] for line in numbered[1:]]
    antipatterns = [next(f.antipattern for f in findings if f.code == c) for c in codes]
    assert len(set(antipatterns)) == len(antipatterns)


def test_next_steps_rank_errors_first(minimal):
    del minimal["meta"]["owner"]
    minimal["phases"][0]["steps"][0]["pain_points"][0]["type"] = "friction"
    md = audit_markdown(minimal, lint_journey(minimal))
    steps = md[md.index("## Nächste Schritte") : md.index("## Evidenzlage")]
    assert steps.index("**L020**") < steps.index("**L030**")


def test_priority_quadrant():
    assert priority_quadrant({"user_impact": 5, "public_value": 4, "effort": 1}) == "quick_win"
    assert priority_quadrant({"user_impact": 5, "public_value": 5, "effort": 5}) == "big_bet"
    assert priority_quadrant({"user_impact": 1, "effort": 1}) == "fill_in"
    assert priority_quadrant({"user_impact": 1, "public_value": 2, "effort": 4}) == "skip"
    assert priority_quadrant({"user_impact": 3}) is None


def test_render_injects_data_and_escapes_script(minimal):
    minimal["phases"][0]["steps"][0]["action"] = "Böse </script><script>alert(1)</script>"
    html = render_html([minimal])
    assert PLACEHOLDER not in html
    assert "</script><script>alert" not in html
    assert "<\\/script>" in html
    assert '"generator": "journeykit' in html or '"generator":"journeykit' in html


def test_render_multiple_journeys(example_journey, example_second_persona):
    html = render_html([example_journey, example_second_persona], title="Vergleich")
    assert "Vergleich" in html
    assert example_second_persona["persona"]["name"] in html


def test_diff_between_hypothesis_and_validated(example_hypothesis, example_journey):
    d = diff_journeys(example_hypothesis, example_journey)
    assert not d.is_empty()
    assert d.evidence_delta["reported"] > 0
    assert d.added_pain_points
    md = diff_markdown(d)
    assert "Neue Pain Points" in md


def test_diff_identical_is_empty(example_journey):
    d = diff_journeys(example_journey, copy.deepcopy(example_journey))
    assert d.is_empty()
    assert "Keine Modelländerungen" in diff_markdown(d)


def test_cli_roundtrip(tmp_path, minimal):
    src = tmp_path / "j.json"
    src.write_text(json.dumps(minimal), encoding="utf-8")
    assert main(["validate", str(src)]) == 0
    assert main(["lint", str(src), "--quiet"]) == 0
    out = tmp_path / "j.html"
    assert main(["render", str(src), "-o", str(out)]) == 0
    assert out.exists() and "Testjourney" in out.read_text(encoding="utf-8")
    md = tmp_path / "s.md"
    assert main(["export", str(src), "--format", "storymap", "-o", str(md)]) == 0
    assert "Story Map" in md.read_text(encoding="utf-8")
    assert main(["diff", str(src), str(src)]) == 0


def test_cli_lint_strict_fails_on_warning(tmp_path, minimal):
    del minimal["meta"]["owner"]
    src = tmp_path / "j.json"
    src.write_text(json.dumps(minimal), encoding="utf-8")
    assert main(["lint", str(src)]) == 0
    assert main(["lint", str(src), "--strict"]) == 1


def test_cli_new_produces_valid_file(tmp_path):
    out = tmp_path / "n.json"
    assert (
        main(
            [
                "new",
                "neue-journey",
                "--title",
                "Neu",
                "--persona",
                "P",
                "--role",
                "R",
                "--goal",
                "G",
                "-o",
                str(out),
            ]
        )
        == 0
    )
    assert main(["validate", str(out)]) == 0


def test_python_m_entrypoint():
    import subprocess
    import sys

    out = subprocess.run(
        [sys.executable, "-m", "journeykit", "--version"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert out.stdout.startswith("journeykit ")


def test_cli_lint_prints_each_hint_once(tmp_path, capsys, example_journey):
    src = tmp_path / "j.json"
    src.write_text(json.dumps(example_journey), encoding="utf-8")
    main(["lint", str(src), "--today", "2026-10-05"])
    out = capsys.readouterr().out
    assert out.count("[INFO] L101") > 1
    assert out.count("Widersprüche gehören in die Journey") == 1


def test_heatmap_counts_like_the_viewer(minimal):
    step = minimal["phases"][0]["steps"][0]
    step["edge_cases"] = [{"text": "Brief kommt nicht an", "evidence_refs": ["ev-4", "ev-x"]}]
    cells = {r["kind"]: r for r in evidence_heatmap(minimal)}
    assert list(cells) == list(HEATMAP_KINDS), "eine Zeile je Aussageart, auch ohne Aussage"
    # jede Referenz zählt, auch wenn eine andere Aussage dasselbe Atom nennt
    assert (cells["pain_point"]["statements"], cells["pain_point"]["primary"]) == (1, 2)
    assert (cells["thinking"]["primary"], cells["feeling"]["primary"]) == (1, 1)
    # angenommen zählt nicht als Primärbeleg, unbekannte IDs zählen gar nicht
    assert (cells["edge_case"]["primary"], cells["edge_case"]["assumed"]) == (0, 1)
    assert (cells["step"]["statements"], cells["step"]["primary"]) == (1, 0)


def test_heatmap_csv_has_full_grid(example_journey):
    rows = heatmap_csv(example_journey).splitlines()
    n_steps = sum(len(p["steps"]) for p in example_journey["phases"])
    assert len(rows) == n_steps * len(HEATMAP_KINDS) + 1
    assert rows[0] == (
        "phase_id;phase;step_id;step;kind;statements;"
        "evidence_primary;evidence_observed;evidence_reported;evidence_assumed"
    )


def test_heatmap_svg_is_standalone_and_escapes(minimal):
    minimal["phases"][0]["steps"][0]["name"] = "Brief <A> & B"
    svg = heatmap_svg(minimal, today=date(2026, 1, 2))
    root = ET.fromstring(svg.split("\n", 1)[1])  # ohne XML-Deklaration
    assert root.tag == "{http://www.w3.org/2000/svg}svg"
    assert "Brief &lt;A&gt; &amp; B" in svg
    # keine Schriften, Bilder oder Links von aussen
    assert "href" not in svg and svg.count("http") == 1
    assert "Entwurf" in svg and "2026-01-02" in svg
    fr = heatmap_svg(minimal, lang="fr")
    assert "Projet" in fr and "Irritants" in fr and "angen." not in fr


def test_heatmap_svg_marks_assumed_and_gaps(example_hypothesis):
    svg = heatmap_svg(example_hypothesis)
    assert "Hypothese" in svg and "Synthetisches Beispiel" in svg
    assert 'stroke-dasharray="4 3"' in svg and "angen." in svg


def test_wrap_hyphenates_instead_of_cutting():
    assert _wrap("Bei der Kreisschulbehörde nachfragen", 18, 3) == [
        "Bei der",
        "Kreisschulbehörde",
        "nachfragen",
    ]
    assert _wrap("Kindergartenstartwochenplanung", 18, 3) == ["Kindergartenstart-", "wochenplanung"]
    assert _wrap("eins zwei drei vier fünf sechs sieben", 9, 2)[-1].endswith("…")


def test_render_embeds_heatmap_exports(minimal, example_journey):
    html = render_html([minimal, example_journey])
    assert '"heatmap_svg"' in html and '"heatmap_csv"' in html
    assert '"slug": "test-journey-v0.1"' in html
    assert '"slug": "kindergarteneintritt-eltern-v1.0"' in html


def test_cli_exports_heatmap(tmp_path, minimal):
    src = tmp_path / "j.json"
    src.write_text(json.dumps(minimal), encoding="utf-8")
    svg, csv_out = tmp_path / "h.svg", tmp_path / "h.csv"
    assert main(["export", str(src), "--format", "heatmap-svg", "-o", str(svg)]) == 0
    assert svg.read_text(encoding="utf-8").startswith("<?xml")
    assert main(["export", str(src), "--format", "heatmap-csv", "-o", str(csv_out)]) == 0
    assert csv_out.read_text(encoding="utf-8").startswith("phase_id;")


def _payload(html: str) -> dict:
    start = html.index("const DATA = ") + len("const DATA = ")
    return json.JSONDecoder().raw_decode(html[start:].replace("<\\/", "</"))[0]


def test_render_embeds_previous_version_with_diff(example_hypothesis, example_journey):
    data = _payload(render_html([example_journey], previous=[example_hypothesis]))
    prev = data["previous"][0]
    assert prev["journey"]["meta"]["version"] == "0.1"
    assert prev["diff"]["added_steps"] == ["alltag-finden", "nachfragen", "zuteilung-nachfragen"]
    assert ["brief-erhalten", 1, -2] in prev["diff"]["feeling_changes"]
    assert set(prev["counts"]) == {"ERROR", "WARN", "INFO"} and prev["counts"]["WARN"] > 0
    # ohne Vorversion bleibt der Viewer wie bisher
    assert "previous" not in _payload(render_html([example_journey]))
    assert "previous" not in _payload(render_html([example_journey], previous=[None]))


def test_render_previous_needs_one_entry_per_journey(example_journey, example_hypothesis):
    import pytest

    with pytest.raises(ValueError):
        render_html([example_journey], previous=[example_hypothesis, None])


def test_cli_render_compare_pairs_by_id(
    tmp_path, capsys, example_journey, example_second_persona, example_hypothesis
):
    files = {}
    for name, j in [
        ("new", example_journey),
        ("other", example_second_persona),
        ("old", example_hypothesis),
    ]:
        files[name] = tmp_path / f"{name}.json"
        files[name].write_text(json.dumps(j), encoding="utf-8")
    out = tmp_path / "v.html"
    args = [
        "render",
        str(files["other"]),
        str(files["new"]),
        "--compare",
        str(files["old"]),
        "-o",
        str(out),
    ]
    assert main(args) == 0
    previous = _payload(out.read_text(encoding="utf-8"))["previous"]
    assert previous[0] is None and previous[1]["journey"]["meta"]["version"] == "0.1"
    # eine einzelne Journey mit anderer ID: verglichen, aber mit Hinweis
    other_id = copy.deepcopy(example_hypothesis)
    other_id["meta"]["id"] = "etwas-anderes"
    files["old"].write_text(json.dumps(other_id), encoding="utf-8")
    assert main(["render", str(files["new"]), "--compare", str(files["old"]), "-o", str(out)]) == 0
    assert "etwas-anderes" in capsys.readouterr().err
    # mehrere Journeys und keine passende ID: Abbruch statt Raten
    import pytest

    with pytest.raises(SystemExit) as exit_info:
        main(["render", str(files["new"]), str(files["other"]), "--compare", str(files["old"])])
    assert exit_info.value.code == 2
