"""Unabhängigen Fall in den Testsatz übernehmen: Gold → expected.json, case.json, reference.json.

Aufruf: python build_case.py <scratch-fall-dir> <repo-cases-dir> <fall-id> <json-config>
Das Gold bleibt inhaltlich unverändert; ergänzt werden nur shared_atoms und die Fallregeln.
Die Referenz wird aus dem Gold abgeleitet: je Eintrag ein Atom aus der ersten match-Alternative.
"""

import json
import re
import shutil
import sys
from pathlib import Path

src, dst_root, case_id, cfg = (
    Path(sys.argv[1]),
    Path(sys.argv[2]),
    sys.argv[3],
    json.loads(sys.argv[4]),
)
dst = dst_root / case_id
dst.mkdir(parents=True, exist_ok=True)
text = (src / "input.md").read_text(encoding="utf-8")
shutil.copy(src / "input.md", dst / "input.md")
gold = json.loads((src / "gold.json").read_text(encoding="utf-8"))

turns = [
    (m.group(1), m.group(2), m.group(3))
    for m in re.finditer(r"^\[(\d\d:\d\d)\] (\w+): (.*)$", text, re.M)
]


def norm(s):
    return re.sub(r"\s+", " ", s.replace("\u00a0", " ")).strip().casefold()


# Fragen und Zusammenfassungen der interviewenden Person sind keine Evidenz
forbidden = []
for ts, who, line in turns:
    if who in cfg["interviewer"]:
        words = line.split()
        if len(words) >= 8:
            forbidden.append(
                {
                    "text": " ".join(words[:6]),
                    "why": f"Redebeitrag der interviewenden Person ({ts})",
                }
            )

case = {
    "title": cfg["title"],
    "kind": cfg["kind"],
    "class": "reported",
    "source_id": cfg["source_id"],
    "prefix": cfg["prefix"],
    "input": "input.md",
    "phases": cfg["phases"],
    "persona": cfg["persona"],
    "known_atoms": [],
    "tests": cfg["tests"],
    "rules": {
        "kinds": ["quote", "metric"],
        "locator_required": True,
        "pii_terms": cfg["pii_terms"],
        "forbidden": forbidden,
    },
}
(dst / "case.json").write_text(
    json.dumps(case, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

# Ausschnitte mit erfundenen Namen um den Namen kürzen: Eine Extraktion muss Namen
# ersetzen («[Name]») und könnte sie sonst nie treffen. Teile mit weniger als zwei
# Wörtern fallen weg; bleibt nichts, bleibt der Ausschnitt unverändert.
name_rx = re.compile(
    r"\b(?:Herrn?|Frau)?\s*(?:" + "|".join(map(re.escape, cfg["pii_terms"])) + r")\b"
)
cut = []


def strip_names(fragment):
    if not name_rx.search(fragment):
        return fragment
    parts = [p.strip(" ,;.") for p in name_rx.split(fragment)]
    parts = [p for p in parts if len(p.split()) >= 2]
    if not parts:
        return fragment
    cut.append(fragment)
    return parts[0] if len(parts) == 1 else parts


for g in gold["atoms"]:
    new_match = []
    for alt in g["match"]:
        if isinstance(alt, str):
            new_match.append(strip_names(alt))
        else:
            flat = []
            for p in alt:
                r = strip_names(p)
                flat += [r] if isinstance(r, str) else r
            new_match.append(flat)
    g["match"] = new_match
expected = {"shared_atoms": True, **gold}
(dst / "expected.json").write_text(
    json.dumps(expected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)


def turn_of(fragment):
    for ts, who, line in turns:
        if norm(fragment) in norm(line):
            return ts
    return None


ref = []
for n, g in enumerate(gold["atoms"], 1):
    alt = g["match"][0]
    parts = [alt] if isinstance(alt, str) else alt
    parts = sorted(parts, key=lambda p: norm(text).find(norm(p)))
    ts = turn_of(parts[0])
    loc = ts if ts in g.get("locator", [ts]) else g["locator"][0]
    atom = {
        "id": f"{cfg['prefix']}-{n:02d}",
        "source_ref": cfg["source_id"],
        "class": "reported",
        "kind": (g.get("kind") or ["quote"])[0],
        "text": " … ".join(parts),
        "locator": f"[{loc}]",
        "signal": (g.get("signal") or ["neutral"])[0],
    }
    rule = g.get("emotion")
    if rule == "explicit_negative":
        atom["emotion_hint"] = {"valence": -1, "explicit": True}
    elif rule == "explicit_positive":
        atom["emotion_hint"] = {"valence": 1, "explicit": True}
    for f in ("value", "contradicts"):
        if f in g:
            atom[f] = g[f]
    if "unit" in g:
        atom["unit"] = g["unit"] if isinstance(g["unit"], str) else g["unit"][0]
    ref.append(atom)
(dst / "reference.json").write_text(
    json.dumps(ref, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print("gekürzt:", cut)
print(
    case_id,
    "Gold:",
    len(gold["atoms"]),
    "Pflicht:",
    sum(bool(g.get("required")) for g in gold["atoms"]),
    "verboten:",
    len(forbidden),
)
