# Beispiel: Kindergarteneintritt aus Elternsicht

Durchgerechnetes Beispiel für JourneyKit: aus einem Mix von Rohmaterial (Interviews, Anfragen, Befragung, Webanalytics, interne Dokumente) entstehen Evidenz-Atome und daraus eine schema-valide User Journey mit Lint-Befunden, Story Map und Versionsvergleich.

> **Synthetisch.** Alle Inputs, Zahlen, Zitate und Personen (E1, E2, E3) sind erfunden. Der Ablauf des Kindergarteneintritts ist **stark vereinfacht** und **keine Dokumentation des realen Verfahrens** der Stadt Zürich oder einer anderen Gemeinde. Rollen und Zuständigkeiten sind fiktiv; die Organisation heisst deshalb «Schulamt der Stadt Zürich (fiktives Beispiel)», und `meta.synthetic` ist in allen Dateien `true`.

## Szenario

Eltern aus Sicht der Volksschule: Kinder, die bis zum Stichtag vier werden, sind automatisch erfasst. Im Dezember kommt ein Informationsbrief der Kreisschulbehörde, im April der Zuteilungsentscheid (welcher Kindergarten), dazwischen melden Eltern bei Bedarf Betreuung an. Im Mai Informationsanlass, im Juni Schnupperbesuch, im August Eintritt mit zwei Eingewöhnungswochen, im Herbst Elterngespräch.

Diagnose: **User Journey**, nicht Service Blueprint. Gefragt ist das Erleben der Eltern über zehn Monate und mehrere Stellen hinweg; der interne Ablauf steht im (fiktiven) Prozessbeschrieb und würde separat als Blueprint dokumentiert.

## Dateien

| Datei | Inhalt |
|---|---|
| `journey.json` | **Hauptdatei.** Persona «Neu zugezogene Eltern», Version 1.0, Status `validated`. 5 Phasen, 13 Schritte, 13 Pain Points (4 Breakdowns), 8 Chancen, 60 Evidenz-Atome, 8 Quellen. |
| `journey-berufstaetig.json` | Zweite Persona «Berufstätige Eltern mit Betreuungsbedarf», Version 0.3, Status `draft`. Gleiche Phasen-IDs, eigene Gefühlskurve (Tief bei der Hortbestätigung), 25 Atome. Für den Persona-Vergleich im Viewer. |
| `workshop-hypothese.json` | Stand nach dem internen Hypothesen-Workshop, Version 0.1, Status `hypothesis`: gleiche Schritt-IDs wie `journey.json`, aber nur Annahmen (`assumed`) und eine deutlich optimistischere Gefühlskurve. Ausgangspunkt für `journeykit diff`. |
| `input/` | Das synthetische Rohmaterial, siehe unten. |

## Input → Quelle → Evidenzklasse

| Input | `sources[].id` | `kind` | `default_class` | `pii_status` | n | Atom-IDs |
|---|---|---|---|---|---|---|
| `input/interview-e1.md` – zugezogenes Elternteil, Brief kommt wegen Umzug spät | `int-e1` | interview | reported | anonymised | 1 | `e1-*` |
| `input/interview-e2.md` – berufstätiges Elternpaar, Betreuung ab Tag 1 | `int-e2` | interview | reported | anonymised | 1 | `e2-*` |
| `input/interview-e3.md` – fremdsprachiges Elternteil, Nachbarin übersetzt | `int-e3` | interview | reported | anonymised | 1 | `e3-*` |
| `input/anfragen-export.csv` – 30 Anfragen an die Kreisschulbehörde über ein Jahr | `anfragen` | inquiry_log | observed | anonymised | 30 | `anf-*` |
| `input/elternbefragung.csv` – aggregierte Befragung, 11 Fragen | `befragung` | survey | reported | anonymised | 412 | `bef-*` |
| `input/webanalytics.csv` – 8 Seiten, Aufrufe, Ausstiegsrate, Dauer | `analytics` | analytics | observed | none | – | `web-*` |
| `input/prozess-einschulung-intern.md` – Soll-Prozess, Innensicht | `prozessdok` | internal_document | **assumed** | none | – | `doc-*` |
| `input/workshop-notizen.md` – Hypothesen-Workshop ohne Eltern | `workshop` | workshop | **assumed** | none | 6 | `ws-*` |

Jedes Zitat-Atom steht **wörtlich** im Input, mit `locator` (Zeile, `anfrage_id`, Abschnitt). Zahlen aus den CSV-Dateien sind Atome vom Typ `metric` mit `value` und `unit`. Das Prozessdokument und der Workshop liefern nur `assumed`-Evidenz – sie zählen für die Lints nicht als Nutzerevidenz, bleiben aber sichtbar, vor allem dort, wo Interviews ihnen **widersprechen** (`contradicts`, Lint L101).

## Was das Beispiel zeigt

- **Breakdowns statt Happy Path**: Brief nicht erhalten → Anruf (`pp-brief-nicht-erhalten`), Brief nicht verstanden → Nichthandeln (`pp-brief-nicht-verstanden`), Betreuungsfrist unklar → Frist verpasst oder Plan B (`pp-betreuungsfrist-unklar`), Eingewöhnungslücke → zwei Wochen improvisieren (`pp-eingewoehnung-betreuungsluecke`). Jeder Breakdown-Schritt hat Recovery-Pfade, mindestens einer davon als Soll-Pfad (`exists: false`).
- **Ehrliche Lücken**: Drei Schritte haben `feeling: null` – etwa die Betreuungsanmeldung, zu der die zugezogene Persona keine Gefühlsevidenz liefert, obwohl die Pain Points dort belegt sind.
- **Widersprüche ausgewiesen, nicht geglättet**: «Alle Eltern erhalten den Informationsbrief bis Mitte Dezember» (`doc-01`) gegen E1 (Januar, alte Adresse) und Anfrage A-007; «Begründung nachvollziehbar» (`doc-03`) gegen 62 % Zustimmung und 112 Kommentare (`bef-04`).
- **Kennzahlen übersetzt**: «Anteil Eltern, die nach dem Brief wussten, was zu tun ist» (← Conversion), «Anteil Anfragen per Telefon trotz Online-Information» (← Churn / Workaround), «Anteil Anfragen zur Zuteilung» (← Support-Ticket-Rate); je mit `current_value` aus den synthetischen Daten und `source_ref`.
- **Chancen in allen vier Quadranten**: Quick Win (mehrsprachiger Kernsatz im Brief), Big Bet (Betreuung und Zuteilung zusammenführen), Nebenbei (Fragen schon im Dezember beantworten), Zurückstellen (Schnuppertermine ausserhalb der Arbeitszeit, `wontfix`).
- **Absichtliche INFO-Befunde** in `journey.json`: L043 (zwei Emotionspunkte abgeleitet statt ausdrücklich geäussert), L100 (zwei Atome bewusst nicht synthetisiert: `e2-26`, `anf-12`), L101 (Widersprüche). Ziel: 0 ERROR, 0 WARN.

## Reproduzieren

```bash
cd examples/kindergarteneintritt

# Schema
journeykit validate *.json

# Methodische Lints
journeykit lint journey.json                 # 0 Fehler · 0 Warnungen · 13 Hinweise
journeykit lint journey-berufstaetig.json    # 0 Fehler · 1 Warnung (Phase «Ankommen» noch ohne Reibung – Entwurf)
journeykit lint workshop-hypothese.json      # 0 Fehler · 3 Warnungen · L010 als INFO, weil status = hypothesis
journeykit lint workshop-hypothese.json --today 2025-11-18   # ohne die L032-Warnung (Review-Termin überschritten)

# Viewer: eine Journey oder Persona-Vergleich
journeykit render journey.json -o journey.html
journeykit render journey.json journey-berufstaetig.json -o vergleich.html --title "Kindergarteneintritt: zwei Personas"

# Exporte
journeykit export journey.json --format storymap
journeykit export journey.json --format opportunities
journeykit export journey.json --format actions -o massnahmen.csv
journeykit export journey.json --format audit

# Was die Nutzerevidenz an der Workshop-Hypothese geändert hat
journeykit diff workshop-hypothese.json journey.json        # Exit 1 = es gibt Änderungen
```

Der Diff zeigt den Inside-Out-Effekt direkt: Der Workshop setzte den Brief auf +1 («Eltern freuen sich»), die Interviews auf −2 («Angst bekommen», «nervös»); der Zuteilungsentscheid fiel von +2 auf −1; zehn Pain Points und sechs Chancen kamen erst mit der Nutzerevidenz dazu.

## Erweitern

- Neue Evidenz: Atom in `evidence` anlegen (ID-Schema `e4-01`, `anf-18`, …), `locator` setzen, dann in `evidence_refs` der betroffenen Aussage referenzieren. `journeykit lint` meldet nicht referenzierte Atome (L100) und fehlende Fundstellen (L102).
- Dritte Persona: `journey.json` kopieren, Phasen-IDs behalten, Schritt-IDs mit eigenem Suffix, dann `journeykit render` mit allen Dateien.
- Nächste Version: `meta.version` erhöhen, `changelog` ergänzen, `journeykit diff alt.json neu.json` ins Protokoll.
