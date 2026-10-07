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
from journeykit.model import priority_quadrant
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
