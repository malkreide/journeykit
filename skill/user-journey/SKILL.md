---
name: user-journey
description: Erstellt, synthetisiert und prüft evidenzbasierte User Journeys für die öffentliche Verwaltung mit dem journeykit-Modell (JSON-Schema, Lints, interaktiver HTML-Viewer). Verwende diesen Skill, wenn der User (1) eine User Journey, Customer Journey oder Journey Map erstellen will, (2) Interviews, Befragungen, Anfragen-Exporte, Analytics oder Workshop-Notizen zu einer Journey verdichten will, (3) eine bestehende Journey prüfen, auditieren oder auf methodische Lücken abklopfen will, (4) fragt, ob etwas eine User Journey oder ein Service Blueprint ist, (5) Pain Points, emotionale Kurve, Touchpoints, Chancen oder eine Story Map aus Nutzerdaten ableiten will, oder (6) Begriffe wie «Journey Mapping», «Nutzerreise», «Persona-Workshop», «Happy Path», «Evidenz-Atome» nennt. Auch bei Aussagen wie «wir sollten das mal aus Sicht der Eltern anschauen» oder «ich habe 20 Interviews und weiss nicht, wie ich sie zusammenbringe».
---

# User Journey (journeykit)

Eine Journey ist hier **ein Datenbestand, keine Grafik**: eine JSON-Datei nach
`journeykit`-Schema, in der jede Aussage auf Evidenz-Atome verweist. HTML,
Story Map, Massnahmenliste und Audit-Report werden daraus erzeugt. Der Skill
beschleunigt die **Synthese** (Rohmaterial → Modell), nicht die Erhebung:
null Interviews ergeben null Wert, egal wie schön die Kurve ist.

Sprache der Inhalte: Deutsch in Schweizer Rechtschreibung (kein ß). Feldnamen
und Enum-Werte des Schemas bleiben englisch.

## Bundle

| Datei | Wann lesen |
|---|---|
| `references/diagnose.md` | Immer zu Beginn: Ist das eine User Journey? Welcher Modus? |
| `references/evidenz.md` | Vor dem Extrahieren: Evidenzklassen, Atom-Regeln, Prompt-Schablone |
| `references/methodik.md` | Bei Fragen zu Taxonomie, Fallstricken, Aufwand, Phasenmodellen |
| `references/kpi-uebersetzung.md` | Sobald Kennzahlen ins Modell kommen |
| `references/review-fragen.md` | Vor der Übergabe und im Audit-Modus |
| `../../src/journeykit/schema/journey.schema.json` | Das Schema – bei Unsicherheit über ein Feld dort nachsehen, nicht raten |

CLI (im Repo: `pip install -e .`):

```
journeykit new <id> --title … --persona … --role … --goal …   # Gerüst (Status hypothesis)
journeykit validate journey.json                               # Schema
journeykit lint journey.json [--strict] [--quiet] [--lang fr]  # Fallstricke
journeykit render journey.json [weitere.json] -o out.html      # Viewer, mehrere = Persona-Vergleich
journeykit export journey.json --format storymap|actions|opportunities|audit
journeykit diff alt.json neu.json                              # Was hat neue Evidenz verändert?
```

Steht keine Code-Ausführung zur Verfügung: die JSON-Datei trotzdem vollständig
nach Schema erzeugen und dem User die Befehle mitgeben. Keine HTML-Darstellung
von Hand bauen – der Viewer ist Teil des Pakets.

## Haltung

Der Skill verhält sich wie ein kritischer Research-Lead, nicht wie ein
Generator. Er fragt nach, diagnostiziert und benennt Lücken, bevor er liefert.
Konkret:

- **Keine Emotion ohne Beleg.** `feeling: null` ist eine ehrliche Lücke; ein
  erfundener Punkt auf der Kurve ist Pseudo-Präzision. Emotionen aus
  Workshop-Bauchgefühl bleiben `assumed` und werden im Viewer gestrichelt.
- **Kein Happy Path.** Pro Phase aktiv nach Breakdowns, Edge Cases und
  Recovery-Pfaden fragen. Wo Nutzende ausweichen (Anruf, Schalter, Beschwerde,
  Nichthandeln), ist der Breakdown – Anfragen- und Beschwerdedaten zeigen ihn.
- **Keine Persona aus vier Zitaten.** Unter drei unabhängigen Primärbelegen
  heisst die Persona `is_hypothesis: true`.
- **Innensicht ist Innensicht.** Prozessdokumente, Workshops ohne Nutzende und
  Erfahrungswissen sind Klasse `assumed`, auch wenn sie plausibel klingen.
  Ergibt das Material nur Annahmen, ist das Resultat eine Hypothesen-Map
  (`meta.status: hypothesis`) mit Erhebungsplan – und das wird so gesagt.
- **Verwaltung ist kein Shop.** Niemand «konvertiert» oder «churnt». Übersetzen:
  Conversion → Anteil vollständig erledigter Anliegen; Churn → Ausweichen in
  Workarounds oder formelle Beschwerden; CES → Aufwand pro Anliegen. Kanäle
  sind Brief, Telefon, Schalter, Veranstaltung – nicht nur Web.
- **Eine Persona, ein Szenario pro Datei.** Weitere Personas sind weitere
  Dateien; der Viewer legt sie übereinander.
- **Personendaten bleiben draussen.** Interviews mit Eltern, Kindern,
  Lehrpersonen sind Personendaten. Ins JSON kommen anonymisierte Zitate und die
  Ablage des Rohmaterials, nie das Material selbst. `pii_status` korrekt setzen.

## Ablauf

### 0. Intake – höchstens drei Fragen, dann Diagnose

Erfragen (oder aus dem Kontext übernehmen):

1. **Leistung und Szenario**: Welche Leistung, welches Ziel aus Nutzersicht, was löst die Journey aus, woran erkennen Nutzende das Ende?
2. **Persona**: Wessen Erleben? Eltern, Lehrperson, Schulleitung, Behördenmitglied, Mitarbeitende? Genau eine.
3. **Material**: Was liegt vor? Interviews, Befragungen, Anfragen-/Ticketexporte, Analytics, Beschwerden, Workshop-Notizen, Prozessdokumente, bestehende Journeys?

Dann `references/diagnose.md` anwenden:

- **Ist es eine User Journey?** Liegt das Interesse hinter der Sichtbarkeitslinie (Zuständigkeiten, Systeme, Durchlaufzeiten intern), ist es ein Service Blueprint. Geht es um Klickpfade in einer Oberfläche, ist es ein User Flow. Das offen sagen und `meta.map_type` sowie `meta.diagnosis.rationale` entsprechend setzen – oder das Vorhaben umbenennen.
- **Modus wählen**:

| Modus | Wann | Ergebnis |
|---|---|---|
| **Synthese** | Primärmaterial vorhanden (mindestens eine Nutzerquelle) | Journey mit Status `draft` → `validated` |
| **Workshop** | Kein Primärmaterial, Team will starten | Journey mit Status `hypothesis` plus Erhebungsplan in `open_questions` |
| **Audit** | Bestehende Journey (Bild, PDF, Miro, Excel, Text) soll geprüft werden | Audit-Report plus optional Übertrag ins Schema |

Den gewählten Modus und die Diagnose in einem Satz zurückmelden, dann weiter.

### 1. Scope festlegen

- `persona`: Name (archetypisch, keine reale Person), `role`, Ziele, Frustrationen, Kontext (Sprache, digitaler Zugang, Zeitbudget, Vorerfahrung).
- `scenario`: `goal` in Nutzerworten, `trigger`, `end_state`, `timeframe`, **`scope_exclusions`** (was bewusst draussen bleibt – schützt vor dem Stammbaum-Effekt).
- Phasenvorschlag: 4–7 Phasen, benannt aus Nutzersicht («Brief und Orientierung», nicht «Versand»). Phasen entstehen aus dem Material; im Synthese-Modus erst nach der Extraktion fixieren.
- `meta`: `owner` als Rolle mit Funktionsadresse, `review_cycle_days`, `next_review`, `context`.

### 2. Quellen registrieren

Pro Datei oder Datensatz ein `sources`-Eintrag: `kind`, `default_class`
(`observed` für Analytics, Ticket-/Anfragenexporte, Auswertungen der
Geschäftskontrolle (`case_records`), Beobachtung; `reported`
für Interviews, Befragungen, Tagebuchstudien, Beschwerden; `assumed` für
Prozessdokumente, Workshops ohne Nutzende), `n`, `date`, `participants` als
Rolle, `pii_status`, `location` als Pfad.

Enthält eine Quelle Personendaten: vor der Extraktion anonymisieren (Namen,
Adressen, Kontaktangaben, seltene Merkmale entfernen) und `pii_status:
anonymised` setzen. `contains_pii` darf nicht in eine geteilte Datei – Lint L080
blockiert.

### 3. Evidenz extrahieren

`references/evidenz.md` lesen. Pro Quelle einen Durchgang, Atome nach Schema:

- `kind: quote` für wörtliche Aussagen – **nicht paraphrasieren**, Fundstelle
  (`locator`) ist Pflicht.
- `kind: metric` für Zahlen aus Befragung, Analytics, Exporten – mit `value`,
  `unit` und der Zeile oder Spalte, aus der sie stammen. Grosse Exporte zuerst
  kategorisieren und als Metriken verdichten, nicht jede Zeile als Atom.
- `emotion_hint` nur, wenn die Emotion im Text steht (`explicit: true`).
  Abgeleitete Emotionen als `explicit: false` kennzeichnen.
- `signal`: friction, breakdown, positive, need, workaround, neutral.
- `phase_hint`, `persona_hint`, `channel_hint` als Sortierhilfe.
- Widersprüche zwischen Quellen in `contradicts` festhalten – sie werden
  ausgewiesen, nicht geglättet.

Richtwert: 40–80 Atome für eine Journey mit 12–18 Schritten. Material, das
nicht in die Journey passt, bleibt als Atom ohne Referenz stehen (Lint L100
zeigt es) oder wird bewusst als ausserhalb des Scopes markiert.

### 4. Synthetisieren

Atome zu Schritten clustern. Pro Schritt:

- `action` (was die Persona tut), `channel`, `touchpoint`, `counterpart`,
  `is_transition` bei Kanal- oder Zuständigkeitswechsel.
- `performed_by`, wenn typischerweise nicht die Persona allein handelt:
  `shared` (mit Hilfe) oder `intermediary` (Dritte anstelle der Persona), mit
  `role` und `mandate` (`formal` = Vollmacht, Vertretung, Auftrag; `informal`
  = Familie, Nachbarschaft). Behörden nie hier, sondern als `counterpart`.
  Betrifft es nur einen Teil der Persona, ist es ein Edge Case. Handeln
  mehrheitlich Dritte, meldet Lint L073: dann die Diagnose prüfen.
- `thinking`: Fragen und Zweifel mit `evidence_refs`.
- `feeling`: `valence` −2…+2 und `label` in Nutzerworten – oder `null`.
- `pain_points`: `type` friction oder breakdown, `severity`, `frequency`,
  `workaround` (wohin ausgewichen wird), `owner` als Rolle, `status`.
  Ein Rechtsmittel (Einsprache, Rekurs) ist kein Breakdown, sondern Reibung;
  das Versagen liegt meist davor (siehe `references/review-fragen.md`,
  Happy Path).
- `edge_cases` und `recovery_paths` (`exists: false` für Soll-Pfade, die heute
  fehlen). Jeder Breakdown braucht einen Recovery-Pfad oder die Feststellung,
  dass keiner existiert.
- `backstage_notes` sparsam. Werden es mehr als Schritte, ist ein Service
  Blueprint fällig (Lint L071).
- **Kosten** (Gebühren, Auslagen, Mehrkosten durch Verzögerung) haben kein
  eigenes Feld. Muster: Betrag als `metric`-Atom mit `unit` «CHF» und Quelle;
  im betroffenen Schritt verknüpfen (über `thinking`, einen Pain Point oder
  die `evidence_refs` des Schritts); kommen die Kosten
  überraschend oder hindern sie am Handeln, ein Pain Point mit `workaround`
  (z. B. Ratenzahlung, Verzicht, Nachfrage). Mehrkosten, die Dritte
  verrechnen, beim Schritt der Vermittlung festhalten (`performed_by`).
  Zeitkosten (Arbeitsausfall, Wartezeit) sind keine Kosten in diesem Sinn,
  sondern Dauer (`duration_days`, siehe unten).

Je Phase:

- `duration` in Worten, wie die Persona oder die Quellen sie nennen.
- `duration_days` nur mit Beleg: `typical` (z. B. Median), allenfalls `min`
  und `max` als belegte Spanne, alles in **Kalendertagen**, `evidence_refs`
  Pflicht. Misst die Quelle nicht genau die Phase (Statistik «vollständiges
  Gesuch bis Entscheid»), steht das in `basis`. Eine Frist ist keine Dauer:
  Sie ist ein Soll (`assumed`) und gehört als Widerspruch neben die
  gemessene Dauer, nicht an ihre Stelle. Ohne Beleg weglassen – der Viewer
  zeigt «keine belegte Dauer», und das ist ehrlicher als eine geschätzte
  Zahl. Nur an der Phase: Schritte sind Erlebnisse, keine Zeitabschnitte.
  Gerade Wartephasen ohne Kontaktpunkt brauchen die Zahl, weil sie im
  Raster sonst so kurz aussehen wie ein Termin.

Dann über die ganze Journey:

- `kpis` je Phase: eine Outcome-Kennzahl mindestens, Frühindikatoren bevorzugt,
  `commercial_equivalent` festhalten, wenn übersetzt wurde
  (`references/kpi-uebersetzung.md`).
- `opportunities`: pro Frustrationstal eine How-might-we-Frage, verknüpft mit
  Pain Points, mit `user_impact`, `public_value`, `effort` (1–5), `owner`,
  `status`, `stories` (erste = wichtigste, `mvp: true` für den MVP-Schnitt).
- `open_questions` mit `proposed_method`: Was muss die nächste Erhebung klären?
- `changelog`: Was diese Version gegenüber der letzten verändert hat.

### 5. Prüfen

```
journeykit validate journey.json
journeykit lint journey.json
```

Schema-Fehler beheben. Lint-Befunde einzeln beurteilen: ERROR immer beheben;
WARN beheben oder begründet stehen lassen (Begründung in `open_questions`);
INFO lesen. `--strict` vor dem Teilen. Die Befunde sind Review-Vorbereitung,
kein Ersatz für ein Review.

### 6. Ausgeben und übergeben

```
journeykit render journey.json -o journey.html            # --lang fr für die französische Oberfläche
journeykit export journey.json --format audit -o audit.md
journeykit export journey.json --format storymap -o storymap.md
journeykit export journey.json --format actions -o massnahmen.csv
```

Bei der Übergabe nennen: Evidenzlage in einem Satz (Quellen, Atome,
Primäranteil), die drei schwersten Pain Points, die Breakdowns, was
Hypothese geblieben ist, Owner und Review-Termin. Dann die Fragen aus
`references/review-fragen.md`, die das Modell nicht beantworten kann.

## Modus Workshop (Hypothesis-first)

`journeykit new` als Gerüst. Durch die Phasen führen, pro Phase fragen: Was
tut die Persona? Was fragt sie sich? Wo bricht es? Wohin weicht sie aus? Alle
Aussagen erhalten `assumed`-Atome aus einer Quelle `kind: workshop`.
Gefühlskurve nur, wenn das Team sie ausdrücklich als Hypothese setzen will.
Ergebnis ist `status: hypothesis`, `persona.is_hypothesis: true`, und ein
Erhebungsplan: welche drei Fragen zuerst, mit welcher Methode, mit wem. Hinweis
an das Team, dass Hypothesis-first laut NN/g **keine** Zeit spart
(`references/methodik.md`).

## Modus Audit

Bestehende Journey entgegennehmen (Bild, PDF, Export, Text). Vorgehen:

1. Diagnose: Journey, Blueprint, Flow, Experience Map? Eine Persona oder mehrere vermischt?
2. Soweit möglich ins Schema übertragen; fehlende Belege sind leere `evidence_refs`, Quellen ohne Angaben sind `assumed`.
3. `journeykit lint` plus die Fragen aus `references/review-fragen.md`.
4. Audit-Report (`export --format audit`) mit: Evidenzlage, Befunde je Fallstrick, drei wichtigste nächste Schritte. Urteil in einem Satz: belastbar, Hypothese oder Poster.

## Typische Fehler, die der Skill selbst vermeidet

- Phasen aus dem Prozessdokument übernehmen statt aus dem Material.
- Mehrere Personas in eine Datei pressen («Eltern» mit Zugezogenen, Berufstätigen und Fremdsprachigen in einer Kurve).
- Pain Points ohne `workaround` – der Workaround ist das Verwaltungs-Äquivalent zu Churn und die beste Quelle für Breakdowns.
- Chancen ohne verknüpfte Pain Points oder ohne Scores – dann gibt es keine Priorisierung.
- KPIs mit kommerziellen Namen stehen lassen.
- Den Viewer von Hand nachbauen statt `journeykit render` zu nutzen.
