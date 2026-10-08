# CLAUDE.md – Arbeiten an JourneyKit

Einstieg für Claude Code. Kurz halten; Details stehen in den verlinkten Dateien.

## Was das Projekt ist

Evidenzbasierte User Journeys für die öffentliche Verwaltung. **Modell vor
Darstellung**: `journey.json` (Schema in `src/journeykit/schema/journey.schema.json`)
ist das Primärartefakt; Viewer, Exporte, Audit und Diff werden daraus erzeugt.
Jede Aussage verweist auf Evidenz-Atome mit Klasse `observed` / `reported` /
`assumed`. Konzept und Begründungen: `docs/konzept.md`, Entscheide: `docs/adr/`.

## Konventionen

- **Sprache**: Inhalte, Kommentare und Docstrings auf Deutsch in **Schweizer Rechtschreibung (kein ß → ss)**. Code-Bezeichner, Schema-Feldnamen und Enum-Werte englisch. README bilingual (EN Hauptdatei, DE Zweitdatei, gleiche Struktur).
- **Ausgaben zweisprachig (de, fr)**: Kein Text, den Nutzende sehen, steht im Code (Ausnahme: Meldungen zu Programmierfehlern wie einem unbekannten `lang`); alle stehen in einem von vier Katalogen mit gleichen Schlüsseln und Platzhaltern je Sprache – neue Texte immer in beiden Sprachen.

  | Katalog | Zugriff | Test |
  |---|---|---|
  | `viewer.html`, JSON-Block `jk-i18n` | `t()`, `tn()` (Plural), `lbl()` (mit Doppelpunkt) | `test_viewer_i18n.py` (auch: jeder Enum-Wert des Schemas hat eine Beschriftung) |
  | `lint_messages.py` | `c.add(code, stufe, anti_pattern, pfad, msg=…, **werte)` | `test_lint_messages.py` (prüft jeden `c.add`-Aufruf per AST) |
  | `export_texts.py` (Exporte, Diff) | `t("schlüssel", …)` | `test_export_texts.py` |
  | `cli_texts.py` (Meldungen, Hilfe, Gerüst von `new`) | `_text(lang, "schlüssel", …)`, `h()`, `t()` | `test_cli_texts.py` |

  Sprache: `--lang` > `meta.language` der Journey > `JOURNEYKIT_LANG` > `de`. Französisch nach Schweizer Usanz (geschütztes Leerzeichen vor «:», «;», «?», «!», schmales in Guillemets); in den Python-Katalogen mit normalen Leerzeichen schreiben, `typo_fr()` setzt sie. Deutsche Ausgabe beim Umbau zeichengenau gegen `main` vergleichen. Bewusst englisch: Texte von argparse selbst und Details der Schemafehler aus `jsonschema`.
- **Python** 3.10+, einzige Laufzeitabhängigkeit `jsonschema`. Keine weiteren Dependencies ohne ADR.
- **Viewer** ist eine einzige HTML-Datei ohne externe Ressourcen (keine CDNs, keine Fonts von aussen, keine Netzwerkanfragen) – er muss in geschlossenen Verwaltungsnetzen laufen und darf keine Daten senden. Farben als Tokens in `:root`, Dark Mode über `prefers-color-scheme` und `data-theme`.
- **Schema-Änderungen**: `additionalProperties: false` bleibt überall. Neue Felder → Schema, `model.py` (falls Aussage/Referenz), Viewer, Beispiel-Journeys, Tests, `docs/konzept.md`. `schema_version` nur bei Breaking Changes erhöhen, dann Migrationshinweis in `CHANGELOG.md`.
- **Lints**: jede Regel hat Code (`Lxxx`), Stufe, Anti-Pattern, Meldung und Hinweis (`hint`) in `lint_messages.py` (de und fr), einen Test in `tests/test_lint.py` und eine Zeile in beiden READMEs. Regeln urteilen über das Modell, nicht über Textqualität. Neue Codes am Ende des jeweiligen Zehnerblocks.
- **Prompt-Schablone** in `skill/user-journey/references/evidenz.md`: Wer sie ändert, misst vorher und nachher mit dem Testsatz `skill/user-journey/evals/extraction/` (Ablauf im README dort) – blind, je Fall ein frischer Lauf ohne Zugriff auf `expected.json` und `reference.json` – und legt den Lauf unter `runs/` ab. Fälle sind synthetisch wie die Beispiele; jeder Fall braucht eine `reference.json`, die die volle Punktzahl erreicht.
- **Beispiel-Journeys** (`examples/*/`, je ein Verzeichnis mit `journey.json` und `input/`) sind synthetisch und müssen es bleiben: keine realen Personen, Adressen, Kontaktangaben, keine Zitate aus echten Interviews. `meta.synthetic: true`. Zitat-Atome müssen wörtlich in der Datei unter `sources[].location` stehen. Zielzustand `journey.json`: 0 ERROR, 0 WARN. `tests/test_examples.py` prüft das für jedes Beispiel automatisch; ein neues Beispiel braucht keinen Zusatzcode.
- **Secrets und Personendaten**: nichts davon ins Repo – auch nicht in Fixtures, Commits oder Issues. Vor jedem Push `git grep -nEI '(api[_-]?key|secret|passwo?rd|token)'` und PII-Muster prüfen.
- **Commits**: Conventional Commits (`feat`, `fix`, `docs`, `refactor`, `test`, `chore`). `CHANGELOG.md` unter `[Unreleased]` nachführen.

## Befehle

```bash
pip install -e ".[dev]"                       # einmalig
python -m pytest -q                           # Tests (CI nutzt denselben Runner)
ruff check . && ruff format --check .         # beide Gates; Pin in requirements-lint.txt
python scripts/validate_repo.py .             # Repo-Struktur, README-Regeln
journeykit validate examples/kindergarteneintritt/*.json
journeykit lint examples/kindergarteneintritt/journey.json
journeykit render examples/kindergarteneintritt/journey.json examples/kindergarteneintritt/journey-berufstaetig.json -o /tmp/j.html
journeykit lint examples/baubewilligung/journey.json --lang fr   # jede Ausgabe auch französisch
```

`journeykit` nicht im PATH (Windows-Nutzerinstallation)? `python -m journeykit …` ist
gleichwertig.

`ruff --version` muss dem Pin entsprechen – ein älteres ruff weiter vorne im
PATH ist schon vorgekommen (`which -a ruff`); `python -m ruff` nimmt das
ruff der aktiven Python-Umgebung (dort nach `requirements-lint.txt` installieren).

Viewer visuell prüfen: Playwright ist in vielen Umgebungen vorhanden
(`python -c "from playwright.sync_api import sync_playwright"`); Screenshot
aller fünf Tabs plus Drawer plus 390-px-Viewport, `pageerror` leer.

## Architektur in einem Absatz

`cli.py` → lädt JSON → `validate.py` (Schema) → `lint.py` (Regeln über
`model.JourneyIndex`) → `render.py` (ersetzt `/*__JOURNEYKIT_DATA__*/null` in
`viewer/viewer.html` durch `{journeys, findings, …}`) oder `export.py` /
`diff.py`. Der Viewer rendert client-seitig aus dem eingebetteten JSON; er hat
eine eigene kleine Index-Klasse (`Idx`) mit denselben Begriffen wie
`model.py`. Alle Ausgabetexte kommen aus den vier Katalogen (siehe
Konventionen). Der Skill (`skill/user-journey/`) steuert den Menschen und das
Modell durch Intake → Diagnose → Quellen → Evidenz → Synthese → Lint → Render.

## Offene Punkte (Stand 0.1.0 + Unreleased)

Siehe `docs/konzept.md`, Abschnitt «Roadmap». Kurz:

1. **Evaluation**: eine manuell erstellte, reale Journey als Ground Truth gegen die Pipeline laufen lassen (lokal, Material unter `/eval/`, nur der Vergleichsbericht kommt ins Repo). Dabei auch prüfen, ob die Pipeline handelnde Dritte (`performed_by`) und belegte Dauern erkennt – und Fristen nicht als Dauer übernimmt.
2. **Französisch gegenlesen**: Begriffe und Formulierungen aus #20, #21, #22 durch eine französischsprachige Person aus der Verwaltung prüfen lassen; Korrekturen sind einzelne Zeilen in den vier Katalogen.
3. **Kosten** (H5, #15): Muster im Skill umgesetzt; ein Schemafeld erst, wenn ein drittes Beispiel es braucht.
4. **Testsatz Extraktion ausbauen**: Der Testsatz unter `skill/user-journey/evals/extraction/` steht (fünf synthetische Fälle, Scorer `scripts/eval_extraction.py`). Er trennt Schablonen bisher nur über Regelverstösse, nicht über Abdeckung – schwierigere Fälle ergänzen, am besten anonymisierte Ausschnitte aus der Evaluation (Punkt 1), und mehrere Läufe je Schablone vergleichen.
5. **Viewer**: Vergleichsansicht zweier Versionen (Diff visuell), Kommentarfunktion, Export der Heatmap.
6. **Variante B**: MCP-Server, der Journeys als Datenbestand hält (SQLite oder Notion), Versionen und Evidenz verwaltet – siehe ADR-0004.

Erledigt seit 0.1.0 (Details in `CHANGELOG.md`): GitHub-Setup mit CI, Secret Scanning und Dependabot; zweites Beispiel `examples/baubewilligung/` mit den Befunden H1–H4, H7 (u. a. `step.performed_by` nach ADR-0005, Kanal `publication`, Quellenart `case_records`, `phase.duration_days`); alle Ausgaben auf Französisch.

## Was nicht tun

- Den Viewer in ein Framework portieren oder auf Build-Tools umstellen.
- Lints «freundlicher» machen, indem Schwellen gesenkt werden – lieber eine Regel mit klarem Hinweis als eine stille.
- Emotionen, Edge Cases oder Personas in den Beispielen ergänzen, ohne dafür Input-Material und Atome zu ergänzen.
- Reale Daten des Schulamts oder anderer Stellen ins Repo nehmen.
