from __future__ import annotations

import copy
import json

from journeykit.cli import main
from journeykit.diff import diff_journeys, diff_markdown
from journeykit.export import (
    actions_csv,
    audit_markdown,
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
