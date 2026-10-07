# Beispiel: Baubewilligung für eine Wärmepumpe

Zweites durchgerechnetes Beispiel für JourneyKit, bewusst aus einem anderen Verwaltungsbereich als der Kindergarteneintritt. Es prüft, ob Schema, Lints, Skill und Viewer **übertragbar** sind. Der eigentliche Ertrag ist deshalb nicht die Journey, sondern der Abschnitt [Übertragbarkeitsbefunde](#übertragbarkeitsbefunde).

> **Synthetisch.** Alle Inputs, Zahlen, Zitate und Personen (B1, B2, N1) sind erfunden. Das Verfahren ist **stark vereinfacht** und **kein Abbild eines realen kantonalen oder kommunalen Baubewilligungsverfahrens**. Die Organisation heisst deshalb «Gemeinde Musterau, Bauamt (fiktives Beispiel)», und `meta.synthetic` ist in allen Dateien `true`. Fachlich hat niemand aus dem Bauwesen das Beispiel geprüft.

> **Kein Beleg für die Synthese-Qualität.** Rohmaterial und Journey stammen aus derselben Hand. Das Beispiel prüft, ob das **Modell** einen anderen Bereich tragen kann – nicht, ob die Pipeline aus fremdem Material eine gute Journey macht. Dafür ist die Evaluation gegen eine reale Ground Truth da (Roadmap, `docs/konzept.md`).

## Szenario

Eine Eigentümerschaft ersetzt die Heizung durch eine Luft-Wasser-Wärmepumpe mit Aussengerät – oft nach einem Ausfall, unter Zeitdruck. Für das Aussengerät braucht es ein ordentliches Baubewilligungsverfahren: Gesuch im Portal, Vollständigkeitsprüfung, Publikation und Auflage, Prüfung, allenfalls Einsprache und Einigung, Entscheid mit Auflagen und Gebühr, Einbau.

Diagnose: **User Journey**, nicht Service Blueprint – obwohl das Verfahren stark in diese Richtung zieht. Gefragt ist das Erleben der Eigentümerschaft; Fachstellen, Fristen und Baukommission erscheinen nur dort, wo die Persona sie bemerkt (Brief, Statusmeldung, Wartezeit). Die Nachbarschaft ist eine **zweite Persona** mit eigenem Rechtsanspruch und eigenem Interesse.

## Dateien

| Datei | Inhalt |
|---|---|
| `journey.json` | **Hauptdatei.** Persona «Erstbauherrschaft beim Heizungsersatz», Version 1.0, Status `validated`. 5 Phasen, 12 Schritte, 13 Pain Points (2 Breakdowns), 7 Chancen, 84 Evidenz-Atome, 7 Quellen. |
| `journey-nachbarschaft.json` | Zweite Persona «Direkte Nachbarschaft», Version 0.2, Status `draft`, `is_hypothesis: true` (ein Interview). Drei Phasen mit denselben IDs wie die Hauptdatei (`warten`, `entscheid`, `umsetzung`), damit der Viewer die Kurven überlagert. 23 Atome. |
| `journey.html` | Gerenderter Viewer mit beiden Personas. |
| `input/` | Das synthetische Rohmaterial, siehe unten. |

## Input → Quelle → Evidenzklasse

| Input | `sources[].id` | `kind` | `default_class` | `pii_status` | n | Atom-IDs |
|---|---|---|---|---|---|---|
| `input/interview-b1.md` – Eigentümerin, erstes Gesuch nach Heizungsausfall, reicht selbst ein | `int-b1` | interview | reported | anonymised | 1 | `b1-*` |
| `input/interview-b2.md` – Eigentümer, Gesuch durch die Installationsfirma vertreten, Einsprache | `int-b2` | interview | reported | anonymised | 1 | `b2-*` |
| `input/interview-n1.md` – Nachbarin, Einsprache wegen Lärm (eigener Fall) | `int-n1` | interview | reported | anonymised | 1 | `n1-*` |
| `input/anfragen-export.csv` – 30 Anfragen an die Bauberatung, mit Rolle der anfragenden Person | `anfragen` | inquiry_log | observed | anonymised | 30 | `anf-*` |
| `input/gesuchsstatistik.csv` – Auswertung der Geschäftskontrolle, 84 Gesuche | `statistik` | **other** | observed | none | 84 | `stat-*` |
| `input/webanalytics.csv` – 5 Seiten, Aufrufe, Ausstiegsrate, Dauer | `analytics` | analytics | observed | none | – | `web-*` |
| `input/prozess-baubewilligung-intern.md` – Soll-Prozess, Innensicht | `prozessdok` | internal_document | **assumed** | none | – | `doc-*` |
| `input/workshop-notizen.md` – Hypothesen-Workshop ohne Gesuchstellende und Nachbarn | `workshop` | workshop | **assumed** | none | 5 | `ws-*` |

Jedes Zitat-Atom steht **wörtlich** im Input; die Fundstellen (`Zeile N`, `anfrage_id B-0xx`) wurden aus den Dateien berechnet, nicht von Hand gesetzt. `tests/test_examples.py` prüft beides.

## Was das Beispiel zeigt

- **Breakdowns**: Rückweisung wegen Unvollständigkeit nach rund drei Wochen (`pp-rueckweisung-nach-wochen`, Severity 5, 41 % der Gesuche); keine Auskunft an die Eigentümerschaft, wenn die Firma vertritt (`pp-vertretung-keine-auskunft`); in der Nachbarschafts-Datei: von der Auflage nur zufällig erfahren (`pp-n-zufall`). Jeder Breakdown hat einen Recovery-Pfad, die beiden letzten nur als Soll-Pfad (`exists: false`).
- **Wartephase als eigene Phase**: «Warten auf den Entscheid» hat fast keinen Kontaktpunkt; Schritte sind Publikation, Statusseite und Einsprache-Brief. Die Gefühlskurve hat hier ihr Tief («zermürbt»).
- **Widersprüche ausgewiesen**: Soll «Vollständigkeitsprüfung innert zehn Arbeitstagen» (`doc-01`) gegen 17 Arbeitstage im Median (`stat-06`) und B1; Soll «Gesuchstellende werden über die Publikation informiert» (`doc-03`) gegen B1; Workshop-Annahme «Wartezeit unproblematisch» (`ws-02`) gegen 37 % Ersatz nach Ausfall (`stat-02`) und B1; Annahme «Einsprachen von grundsätzlichen Gegnern» (`ws-03`) gegen N1.
- **Kennzahlen übersetzt**: «Anteil Gesuche ohne Rückweisung» (← Conversion Rate), «Anteil Status- bzw. Bewilligungsfragen an allen Anfragen» (← Support-Ticket-Rate), «Anteil Einsprachen, die durch Einigung erledigt werden» und «Lärmklagen je 100 Anlagen» als `public_value`.
- **Ehrliche Lücken**: Fünf Schritte der Hauptdatei haben `feeling: null`; die Nachbarschafts-Persona bleibt Hypothese.
- **Lint-Ergebnis** ohne angepasste Schwellen: `journey.json` 0 Fehler · 0 Warnungen · 11 Hinweise (L043, L100, L101), `journey-nachbarschaft.json` 0 · 0 · 4.

## Übertragbarkeitsbefunde

Die Hypothesen H1–H7 wurden **vor** dem Schreiben des Materials festgehalten (Plan vom 2026-10-07). Ergebnis je Hypothese: **passt**, **Workaround** (dokumentiert, Modell trägt mit Abstrichen) oder **Lücke** (Vorschlag für Issue oder ADR). Schema und Lints wurden für dieses Beispiel **nicht** verändert.

| # | Hypothese | Ergebnis | Was im Beispiel passiert ist | Vorschlag |
|---|---|---|---|---|
| H1 | Handlungen durch Dritte im Auftrag der Persona lassen sich abbilden | **Lücke** | Ein `step` kennt kein Feld dafür, *wer* handelt. «Unterlagen zusammenstellen» macht faktisch die Installationsfirma; die Persona «ist nur die Postbotin» (`b1-26`). Abgebildet über `counterpart`, Aktionstext, Edge Case und Tag `vermittlung`. Dass die Firma eigene Interessen hat (`b2-12`), bleibt ein Edge Case. 58 % der Gesuche sind vertreten (`stat-03`). | Optionales Feld `step.performed_by` – Entscheid über ADR-0005 (`docs/adr/0005-handelnde-dritte.md`), [#6](https://github.com/malkreide/journeykit/issues/6). Offene Frage: Installationsfirmen als eigene Persona. |
| H2 | Wartephasen ohne Kontaktpunkt | **Workaround** | Trägt als eigene Phase mit Schritten «Status verfolgen» usw. Aber der Viewer zeichnet zwei Tage und vier Monate gleich breit; `phase.duration` ist Freitext. | Optionale numerische Dauer (z. B. `duration_days`) für Phase oder Schritt, damit der Viewer Zeit proportional zeigen kann. Niedrige Priorität. |
| H3 | Gegenpersona im Persona-Vergleich | **passt, mit Einschränkung** | Überlagerung funktioniert, sobald die Phasen-IDs geteilt sind. Phasen ohne Gegenstück lässt der Viewer **stillschweigend** weg; Punkte der anderen Persona werden innerhalb der Phase nach Position verteilt, nicht nach Zeit. Die Kurven sind übrigens nicht gegenläufig: In der Auflage fühlen beide negativ, bei der Einigung beide positiv – getrennt sind die Personas wegen ihrer Ziele, nicht wegen der Kurve. | Viewer: Phasen ohne Daten der anderen Persona kennzeichnen. Diagnose-Faustregel in `references/diagnose.md` um «gegensätzliche Ziele» ergänzen. [#9](https://github.com/malkreide/journeykit/issues/9) |
| H4 | Einsprache als Recht, nicht als Fehler | **passt** | Kein Lint erzwingt `breakdown`; die Einsprache ist für die Bauherrschaft `friction`, der Breakdown liegt bei der fehlenden Vorabinformation. Die Unterscheidung steht aber nur im Text und hängt am Urteil der modellierenden Person. | Review-Frage in `references/review-fragen.md`: «Ist dieser Breakdown ein Versagen der Leistung oder ein Rechtsweg, der funktioniert?» |
| H5 | Gebühren und Kosten | **Lücke** | Kein Feld. Die Gebühr steht als Pain Point (`pp-gebuehr-unbekannt`) und als Atom (`stat-11`); Mehrkosten durch die Einsprache (`b2-10`) nur im Text. | Niedrige Priorität: als Muster in der Skill-Anweisung dokumentieren statt Schemafeld; erst bei einem dritten Beispiel mit Kosten entscheiden. |
| H6 | Durchlaufzeit als Kennzahl | **passt** | Als `outcome`/`lagging` hinterlegt; L071 (Blueprint-Smell) schlägt nicht an, weil es nur eine Back-Stage-Notiz gibt. Die Persona erlebt die Durchlaufzeit als Warten – sie gehört in die Journey. | – |
| H7 | Kanäle wie Baugespann und amtliche Publikation | **Lücke** | Die amtliche Publikation ist `channel: other`. Gerade ihr Fehlen als wahrnehmbarer Kanal ist der Breakdown der Nachbarschaft (`pp-n-zufall`). | Kanal `publication` (amtliche Publikation, Aushang, Baugespann) ergänzen – kleine, rückwärtskompatible Schemaerweiterung. [#7](https://github.com/malkreide/journeykit/issues/7) |

**Weitere Befunde, nicht vorab vermutet:**

- **Viewer-Fehler (behoben in diesem PR)**: Das Persona-Badge im Kopf brach nie um. Mit «Erstbauherrschaft beim Heizungsersatz · Eigentümerschaft (gesuchstellend)» lief die Seite bei 390 px auf 481 px Breite. Das Kindergarten-Beispiel hatte kurze Namen und zeigte den Fehler nicht.
- **Quellenart fehlt**: Für eine Auswertung aus der Geschäftskontrolle gibt es keinen `kind`-Wert; sie steht als `other`. Weil L011 Nutzerquellen über `kind` erkennt, würde eine Journey, die sich nur auf solche Statistiken stützt, fälschlich als «ohne Nutzerquelle» gewarnt – obwohl die Atome `observed` sind. Vorschlag: `kind: case_records` in `PRIMARY_SOURCE_KINDS` ([#8](https://github.com/malkreide/journeykit/issues/8)).
- **Lints sind bereichsneutral – und deshalb blind für H1, H4, H5.** 0 Warnungen ohne angepasste Schwellen zeigt, dass die Struktur trägt. Die gefundenen Lücken sind semantisch; ein Lint kann sie erst sehen, wenn das Schema sie ausdrückt.
- **Atomzahl**: 84 Atome bei 12 Schritten liegen über dem Richtwert 40–80 aus dem Skill, weil einzelne Anfragen als Atome erfasst sind. Der Richtwert ist eher eine Untergrenze für Material mit vielen Kurztexten.

## Reproduzieren

```bash
cd examples/baubewilligung

journeykit validate *.json
journeykit lint journey.json                   # 0 Fehler · 0 Warnungen · 11 Hinweise
journeykit lint journey-nachbarschaft.json     # 0 Fehler · 0 Warnungen · 4 Hinweise

# Viewer mit beiden Personas
journeykit render journey.json journey-nachbarschaft.json -o journey.html

# Exporte
journeykit export journey.json --format storymap
journeykit export journey.json --format audit
```

## Erweitern

- Weitere Nachbarschafts-Interviews: Atome `n2-*` anlegen; ab drei unabhängigen Primärbelegen `persona.is_hypothesis` auf `false`.
- Installationsfirmen als dritte Persona: eigene Datei, Phasen-IDs `gesuch`, `warten`, `umsetzung` übernehmen.
- Wird ein Vorschlag aus den Befunden umgesetzt, dieses Beispiel nachführen und den Befund in der Tabelle als erledigt markieren.
