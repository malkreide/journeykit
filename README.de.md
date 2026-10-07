# JourneyKit

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10+-blue)

> Evidenzbasierte User Journeys für die öffentliche Verwaltung: ein JSON-Modell, in dem jede Aussage auf Evidenz verweist, Lints für die bekannten Fallstricke des Journey Mappings, ein interaktiver Single-File-Viewer und ein portabler Claude-Skill, der Journeys aus Rohmaterial synthetisiert.

🇬🇧 [English Version](README.md)

## Übersicht

Die meisten Journey Maps sind Poster: im Sitzungszimmer entstanden, auf den Happy Path verengt, nie aktualisiert, nie in Arbeit übersetzt. JourneyKit behandelt eine Journey als **Datenbestand, nicht als Bild**. Das Primärartefakt ist eine JSON-Datei (`journey.json`) mit Persona, Szenario, Phasen, Schritten, Pain Points, Recovery-Pfaden, Kennzahlen und Chancen – und jede Aussage darin verweist auf **Evidenz-Atome** (Zitate, Messwerte, Beobachtungen) mit Quelle und Evidenzklasse: *beobachtet*, *berichtet* oder *angenommen*. HTML, Story Map, Massnahmenliste, Audit-Report und Versionsvergleich werden aus diesem Modell erzeugt.

Das Vokabular ist für die Verwaltung übersetzt, wo niemand «konvertiert» oder «churnt» – Menschen weichen aus: ans Telefon, an den Schalter, in eine Beschwerde oder ins Nichthandeln. Inhalte sind deutsch in Schweizer Rechtschreibung; die Feldnamen des Schemas sind englisch.

## Funktionen

- **Journey-Modell** als JSON Schema (Draft 2020-12) mit Evidenz-Atomen, Quellenregister, Datenschutzstatus, Owner und Review-Rhythmus
- **Methodische Lints** für die fünf Fallstricke – Inside-Out Bias, Happy Path Bias, Static Map Trap, Empathie-Vakuum / Überkomplexität, Micro-Level Disconnect – plus Blueprint-Smell, Personendaten, KPI-Übersetzung und Evidenzqualität (L001–L102)
- **Interaktiver Viewer**: eine eigenständige HTML-Datei mit fünf Layern – Journey Map mit emotionaler Kurve, Prozess- und Fehlerpfade, Evidenz-Heatmap und Quellenregister, Impact/Effort-Matrix mit User Stories, Prüfung – Evidenz-Drilldown bis zum O-Ton auf jeder Zelle, Filter «nur Primärevidenz», Persona-Überlagerung, hell/dunkel, Druck
- **Exporte**: Story Map nach Patton (Markdown), Massnahmenliste (CSV), Chancenmatrix, Audit-Report
- **Diff** zwischen zwei Versionen – was hat neue Evidenz verändert?
- **Claude-Skill** `user-journey` mit drei Modi: *Synthese* (Rohmaterial → Journey), *Workshop* (Hypothesis-first mit Erhebungsplan), *Audit* (bestehende Journey prüfen)
- **Durchgerechnetes Beispiel**: Kindergarteneintritt aus Elternsicht, aus einem synthetischen Inputmix (3 Interviews, 30 Anfragen, Befragung, Webanalytics, internes Prozessdokument, Workshop-Notizen)

### Demo

![Journey-Layer des Viewers: Phasen, Handlungen, Gedanken, belegte Gefühlskurve, Pain Points](docs/demo.png)

`examples/kindergarteneintritt/journey.html` im Browser öffnen für die vollständige interaktive Fassung.

## Voraussetzungen

- Python 3.10+
- `jsonschema` (wird automatisch installiert)
- Keine JavaScript-Toolchain: der Viewer ist HTML, CSS und JS in einer Datei

## Installation

```bash
git clone https://github.com/malkreide/journeykit.git
cd journeykit
pip install -e ".[dev]"
```

Wird `journeykit` danach nicht gefunden (typisch bei Windows-Nutzerinstallationen, wo pip die Skripte nach `%APPDATA%\Python\Python3xx\Scripts` legt), stattdessen `python -m journeykit …` verwenden – jeder Befehl unten funktioniert auch so.

## Verwendung / Schnellstart

```bash
# Gegen das Schema prüfen
journeykit validate examples/kindergarteneintritt/journey.json

# Methodische Lints (ERROR / WARN / INFO)
journeykit lint examples/kindergarteneintritt/journey.json

# Interaktiven Viewer erzeugen (mehrere Dateien = Persona-Vergleich)
journeykit render examples/kindergarteneintritt/journey.json \
                  examples/kindergarteneintritt/journey-berufstaetig.json -o journey.html

# Exporte
journeykit export examples/kindergarteneintritt/journey.json --format storymap
journeykit export examples/kindergarteneintritt/journey.json --format actions -o massnahmen.csv
journeykit export examples/kindergarteneintritt/journey.json --format audit

# Was hat Nutzerevidenz gegenüber der Workshop-Hypothese verändert?
journeykit diff examples/kindergarteneintritt/workshop-hypothese.json \
                examples/kindergarteneintritt/journey.json

# Neue Journey anlegen (Status hypothesis)
journeykit new kita-anmeldung --title "Kita-Anmeldung" --persona "Eltern" --role "Elternteil" --goal "Platz sicher haben" -o kita.json
```

## Verfügbare Befehle

| Befehl | Beschreibung |
|---|---|
| `journeykit validate DATEI...` | JSON-Schema-Validierung (Exit 2 bei Fehlern) |
| `journeykit lint DATEI... [--strict] [--quiet] [--format json] [--today DATUM]` | Fallstrick-Lints; `--strict` lässt Warnungen scheitern |
| `journeykit render DATEI... [-o OUT] [--title T]` | Eigenständiges interaktives HTML; mehrere Dateien überlagern Personas |
| `journeykit export DATEI --format storymap\|actions\|opportunities\|audit [-o OUT]` | Markdown- / CSV-Exporte |
| `journeykit diff ALT NEU` | Modelländerungen zwischen Versionen (Exit 1, wenn es Änderungen gibt) |
| `journeykit new ID --title --persona --role --goal` | Gerüst einer validen Journey im Status `hypothesis` |
| `journeykit schema` | JSON Schema ausgeben |

### Lint-Regeln

| Bereich | Fallstrick | Beispiele |
|---|---|---|
| L001–L002 | Integrität | hängende Evidenz-Referenzen, doppelte IDs |
| L010–L012 | Inside-Out Bias | Erlebnis-Aussagen ohne Primärevidenz; Persona auf weniger als 3 Primärbelegen |
| L020–L023 | Happy Path Bias | keine Breakdowns; Phase ohne Reibung oder Edge Case; Breakdown ohne Recovery-Pfad |
| L030–L034 | Static Map Trap | kein Owner, kein Review-Rhythmus, schwerer Pain Point ohne Owner |
| L040–L043 | Empathie-Vakuum | Schritte ohne Gefühle oder Gedanken; Emotionen ohne Beleg |
| L050–L052 | Überkomplexität | zu viele Phasen/Schritte; kein Scope-Ausschluss |
| L060–L063 | Micro-Level Disconnect | keine Chancen; schwerer Pain Point ohne Chance; keine Stories |
| L070–L072 | Blueprint-Smell | keine Diagnose; mehr Back-Stage-Notizen als Schritte |
| L080–L081 | Personendaten | Quelle enthält Personendaten; E-Mail-/Telefonmuster im Evidenztext |
| L090–L092 | Kennzahlen | keine; kommerzielle Benennung; kein Frühindikator |
| L100–L102 | Evidenzqualität | unbenutzte Atome; Widersprüche; Primärevidenz ohne Fundstelle |

## Den Claude-Skill verwenden

Der Skill liegt in `skill/user-journey/`. Claude darauf zeigen (Claude Code: der Ordner wird über `CLAUDE.md` erschlossen; claude.ai: den Ordner als Skill hochladen) und das Material beschreiben. Der Skill diagnostiziert zuerst – *ist das eine User Journey oder ein Service Blueprint?* –, wählt einen Modus, registriert Quellen mit Datenschutzstatus, extrahiert Evidenz-Atome mit Fundstellen, synthetisiert das Modell und lässt die Lints laufen. Er erfindet keine Emotionen, besteht auf Breakdowns und Recovery-Pfaden und sagt offen, wenn das Material nur eine Hypothesen-Map trägt.

## Konfiguration

Keine. Der Viewer hat keine externen Abhängigkeiten und macht keine Netzwerkanfragen; gerenderte HTML-Dateien lassen sich in geschlossenen Netzen teilen.

## Projektstruktur

```
journeykit/
├── src/journeykit/
│   ├── schema/journey.schema.json   # das Journey-Modell (einzige Quelle der Wahrheit)
│   ├── model.py                     # Index und Aussagen-Iterator über eine Journey
│   ├── validate.py                  # JSON-Schema-Validierung
│   ├── lint.py                      # Fallstrick-Regeln L001–L102
│   ├── render.py                    # injiziert Daten in den Viewer
│   ├── export.py                    # Story Map, Massnahmen-CSV, Chancen, Audit
│   ├── diff.py                      # Versionsvergleich
│   ├── cli.py                       # Befehl journeykit
│   └── viewer/viewer.html           # eigenständiger interaktiver Viewer
├── skill/user-journey/              # Claude-Skill: SKILL.md + references/
├── examples/kindergarteneintritt/   # durchgerechnetes, synthetisches Beispiel inkl. Rohmaterial
├── docs/                            # Konzept, Architekturentscheide, Demo-Bild
├── tests/                           # pytest
└── CLAUDE.md                        # Einstieg für die Arbeit an diesem Repo mit Claude Code
```

## Changelog

Siehe [CHANGELOG.md](CHANGELOG.md)

## Mitwirken

Beiträge sind willkommen — siehe [CONTRIBUTING.md](CONTRIBUTING.md).

## Sicherheit

Schwachstellen bitte wie in [SECURITY.md](SECURITY.md) beschrieben melden. Journey-Dateien können Zitate realer Personen enthalten: vor dem Teilen anonymisieren (`pii_status`).

## Lizenz

MIT-Lizenz — siehe [LICENSE](LICENSE)

## Autor

Hayal Özkan · [malkreide](https://github.com/malkreide)
