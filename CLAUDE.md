# CLAUDE.md – Arbeiten an JourneyKit

Einstieg für Claude Code. Kurz halten; Details stehen in den verlinkten Dateien.

## Was das Projekt ist

Evidenzbasierte User Journeys für die öffentliche Verwaltung. **Modell vor
Darstellung**: `journey.json` (Schema in `src/journeykit/schema/journey.schema.json`)
ist das Primärartefakt; Viewer, Exporte, Audit und Diff werden daraus erzeugt.
Jede Aussage verweist auf Evidenz-Atome mit Klasse `observed` / `reported` /
`assumed`. Konzept und Begründungen: `docs/konzept.md`, Entscheide: `docs/adr/`.

## Konventionen

- **Sprache**: Inhalte, Kommentare, Docstrings, Lint-Meldungen, UI-Texte des Viewers auf Deutsch in **Schweizer Rechtschreibung (kein ß → ss)**. Code-Bezeichner, Schema-Feldnamen und Enum-Werte englisch. README bilingual (EN Hauptdatei, DE Zweitdatei, gleiche Struktur).
- **Viewer-Texte** stehen im JSON-Block `jk-i18n` von `viewer.html`, je Sprache (`de`, `fr`) mit denselben Schlüsseln; im Code nur über `t()`, `tn()` (Plural) oder `lbl()` (mit Doppelpunkt). Neue Texte immer in beiden Sprachen, neue Enum-Werte des Schemas brauchen eine Beschriftung – `tests/test_viewer_i18n.py` prüft beides. Französisch nach Schweizer Usanz (geschütztes Leerzeichen vor «:» und «?», «\u202f» in Guillemets).
- **Python** 3.10+, einzige Laufzeitabhängigkeit `jsonschema`. Keine weiteren Dependencies ohne ADR.
- **Viewer** ist eine einzige HTML-Datei ohne externe Ressourcen (keine CDNs, keine Fonts von aussen, keine Netzwerkanfragen) – er muss in geschlossenen Verwaltungsnetzen laufen und darf keine Daten senden. Farben als Tokens in `:root`, Dark Mode über `prefers-color-scheme` und `data-theme`.
- **Schema-Änderungen**: `additionalProperties: false` bleibt überall. Neue Felder → Schema, `model.py` (falls Aussage/Referenz), Viewer, Beispiel-Journeys, Tests, `docs/konzept.md`. `schema_version` nur bei Breaking Changes erhöhen, dann Migrationshinweis in `CHANGELOG.md`.
- **Lints**: jede Regel hat Code (`Lxxx`), Stufe, Anti-Pattern, Hinweis (`hint`), einen Test in `tests/test_lint.py` und eine Zeile in beiden READMEs. Regeln urteilen über das Modell, nicht über Textqualität. Neue Codes am Ende des jeweiligen Zehnerblocks.
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
```

`journeykit` nicht im PATH (Windows-Nutzerinstallation)? `python -m journeykit …` ist
gleichwertig.

`ruff --version` muss dem Pin entsprechen – ein älteres ruff weiter vorne im
PATH ist schon vorgekommen (`which -a ruff`).

Viewer visuell prüfen: Playwright ist in vielen Umgebungen vorhanden
(`python -c "from playwright.sync_api import sync_playwright"`); Screenshot
aller fünf Tabs plus Drawer plus 390-px-Viewport, `pageerror` leer.

## Architektur in einem Absatz

`cli.py` → lädt JSON → `validate.py` (Schema) → `lint.py` (Regeln über
`model.JourneyIndex`) → `render.py` (ersetzt `/*__JOURNEYKIT_DATA__*/null` in
`viewer/viewer.html` durch `{journeys, findings, …}`) oder `export.py` /
`diff.py`. Der Viewer rendert client-seitig aus dem eingebetteten JSON; er hat
eine eigene kleine Index-Klasse (`Idx`) mit denselben Begriffen wie
`model.py`. Der Skill (`skill/user-journey/`) steuert den Menschen und das
Modell durch Intake → Diagnose → Quellen → Evidenz → Synthese → Lint → Render.

## Offene Punkte (Stand 0.1.0)

Siehe `docs/konzept.md`, Abschnitt «Roadmap». Kurz:

1. ~~GitHub-Setup~~ – erledigt am 2026-10-07: Repo public, Topics, Secret Scanning + Push Protection, CI grün. Erster Dependabot-PR (checkout v7.0.1, setup-python v7.0.0) gemergt, CI auf `main` grün.
2. Evaluation: eine manuell erstellte, reale Journey als Ground Truth gegen die Pipeline laufen lassen.
3. Variante B: MCP-Server, der Journeys als Datenbestand hält (SQLite oder Notion), Versionen und Evidenz verwaltet – siehe ADR-0004.
4. Viewer: Vergleichsansicht zweier Versionen (Diff visuell), Kommentarfunktion, Export der Heatmap.
5. Extraktions-Qualität: Testsatz «Input → erwartete Atome» für die Prompt-Schablone in `skill/user-journey/references/evidenz.md`.
6. ~~Zweites Beispiel~~ – `examples/baubewilligung/` (Bauherrschaft + Nachbarschaft). Offene Befunde als Issues: ~~`step.performed_by` (H1, #6)~~ umgesetzt mit ADR-0005, ~~Kanal `publication` (H7, #7)~~ und ~~Quellenart `case_records` (#8)~~ umgesetzt; ~~Viewer-Hinweis bei Phasen ohne Overlay (H3, #9)~~ umgesetzt. ~~Review-Frage Rechtsweg statt Breakdown (H4, #14)~~ umgesetzt. ~~Dauer von Phasen (H2, #13)~~ umgesetzt (`phase.duration_days`, L003). Offen: Kosten (H5, #15: Muster im Skill umgesetzt, Schemafeld erst mit drittem Beispiel).
7. ~~Französische UI-Texte im Viewer~~ – umgesetzt (`render --lang fr`, Block `jk-i18n`). Offen: Lint-Meldungen und Hinweise auf Französisch (kommen aus `lint.py`).

## Was nicht tun

- Den Viewer in ein Framework portieren oder auf Build-Tools umstellen.
- Lints «freundlicher» machen, indem Schwellen gesenkt werden – lieber eine Regel mit klarem Hinweis als eine stille.
- Emotionen, Edge Cases oder Personas in den Beispielen ergänzen, ohne dafür Input-Material und Atome zu ergänzen.
- Reale Daten des Schulamts oder anderer Stellen ins Repo nehmen.
