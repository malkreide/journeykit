# ADR-0005: Handelnde Dritte im Schritt (`step.performed_by`)

Datum: 2026-10-07 · Status: angenommen (2026-10-07) · Issue: [#6](https://github.com/malkreide/journeykit/issues/6)

## Kontext

Ein Schritt beschreibt, was die Persona tut. Das Modell nimmt still an, dass
die Persona ihn auch selbst ausführt. Das zweite Beispiel
(`examples/baubewilligung/`, Befund H1) zeigt, dass diese Annahme in der
Verwaltung oft nicht hält:

- 58 % der Baugesuche für Wärmepumpen reicht eine Installationsfirma als
  Vertreterin ein (`stat-03`). Den Lärmschutznachweis erstellt die Firma; die
  Eigentümerin ist «nur die Postbotin zwischen ihm und der Gemeinde» (`b1-26`).
- Ist die Firma als Vertreterin eingetragen, erhält die Eigentümerschaft keine
  Post und zunächst keine Auskunft (`b2-03`, `b2-13`) – ein Breakdown, der
  direkt aus der Vertretung entsteht.
- Die Vermittlung hat eigene Interessen: Die Firma wählte den heiklen
  Standort, weil er am günstigsten war (`b2-12`).

Auch das erste Beispiel kennt den Fall, nur informell: Im Kindergarteneintritt
liest und übersetzt eine Nachbarin den Brief für ein fremdsprachiges
Elternteil (`input/interview-e3.md`, Zeilen 12–19). Im Modell steht das heute
nur im Fliesstext.

Abgebildet wird das heute über `counterpart`, den Aktionstext, Edge Cases und
Tags. Das ist lesbar, aber nicht auswertbar: Weder Viewer noch Lints können
sehen, welche Schritte die Persona gar nicht selbst erlebt, und die Diagnose
«Ist das die Journey der Persona oder die der Vermittlung?» bleibt dem
Bauchgefühl überlassen.

## Optionen

| Option | Beschreibung | Für | Gegen |
|---|---|---|---|
| A – Status quo | `counterpart`, Text, Tags | keine Änderung | nicht auswertbar; jede Journey löst es anders |
| **B – optionales Feld am Schritt** | `step.performed_by` mit Art, Rolle und Mandat | klein, rückwärtskompatibel, deckt formelle und informelle Vermittlung | Interessen der Vermittlung bleiben Text |
| C – Vermittlung als eigene Persona | eigene Datei, z. B. «Installationsfirma» | nutzt bestehendes Modell, eigene Kurve | beantwortet nicht, *wer* im Schritt der Persona handelt; doppelte Pflege |
| D – Akteursliste auf Journey-Ebene | `actors[]` mit IDs, Schritte verweisen darauf; Interessen als Feld | ausdrucksstark, auch für Blueprints | grösster Umbau; Gefahr, die Journey zum Blueprint zu machen |

## Vorschlag

**Option B**, mit C als Ergänzung, wo die Vermittlung selbst untersucht wird.

```json
"performed_by": {
  "kind": "intermediary",
  "role": "Installationsfirma",
  "mandate": "formal"
}
```

- `kind`: `persona` (Standard, wenn das Feld fehlt) · `shared` (Persona mit
  Hilfe, z. B. Nachbarin übersetzt) · `intermediary` (Dritte handeln anstelle
  der Persona).
- `role`: Rolle in Nutzerworten, keine Namen.
- `mandate`: `formal` (Vollmacht, Vertretung) · `informal` (Familie,
  Nachbarschaft, Bekannte). Nur bei `shared` und `intermediary`.
- Behörden erscheinen nicht als `performed_by`: Was die Verwaltung tut, ist
  ein Kontaktpunkt (`counterpart`) oder Back-Stage – nicht ein Schritt der
  Persona.

## Folgen

Nach den Konventionen in `CLAUDE.md` für Schemaänderungen:

- **Schema**: neues optionales Objekt, `additionalProperties: false`.
  `schema_version` bleibt 1.0 (nicht brechend).
- **`model.py`**: keine Änderung, das Feld ist weder Aussage noch Referenz.
- **Viewer**: Chip «durch Installationsfirma» bzw. «mit Nachbarin» in der Zeile
  «Macht»; im Prozess-Layer Kennzeichnung der Knoten.
- **Lint** (Stufe INFO, Code am Ende des Blocks L070–L072, also `L073`): Mehr als die Hälfte der Schritte `intermediary` → Hinweis, die
  Diagnose zu prüfen (Journey der Persona oder der Vermittlung?). Kein WARN,
  weil delegierte Journeys legitim sind.
- **Beispiele**: Baubewilligung – `unterlagen-zusammenstellen` als
  `shared`/`formal` (Eigentümerschaft und Installationsfirma), `einbau` als
  `intermediary`/`formal`. Im Kindergarteneintritt bewusst **nicht** gesetzt:
  Die übersetzende Nachbarin kommt nur in einem von drei Interviews vor, ein
  Feld am Schritt würde für die ganze Persona gelten und überverallgemeinern.
  Sie bleibt Edge Case und Fliesstext.
- **Skill**: In `references/evidenz.md` und `SKILL.md` (Synthese) nach
  Vermittlung fragen: «Wer hat das gemacht – Sie selbst oder jemand für Sie?»
- **Tests**, **`docs/konzept.md`**, beide READMEs.

## Entscheid

Angenommen am 2026-10-07 wie vorgeschlagen (Option B). Die offenen Fragen
des Entwurfs sind so entschieden:

- **`mandate` bleibt.** Das Mandat entscheidet in der Verwaltung über
  Auskunftsrechte (vgl. `b2-13`). Das Schema verlangt `role` und `mandate`,
  sobald `kind` nicht `persona` ist, und verbietet beide bei `persona`.
- **Interessen der Vermittlung werden nicht strukturiert erfasst** (`b2-12`
  bleibt Edge Case), bis ein drittes Beispiel es verlangt; Option D bleibt
  offen.
- **`performed_by` nur am Schritt**, nicht an Pain Points.

Eine Bedeutung des Feldes, die beim Umsetzen klar wurde: `performed_by`
beschreibt den **typischen** Fall der Persona, nicht jeden Einzelfall. Wo nur
ein Teil der Persona so handelt, gehört das in einen Edge Case.

## Voraussetzung

Keine. Die Änderung ist additiv und kann vor der Evaluation umgesetzt werden;
die Evaluation sollte aber prüfen, ob die Pipeline Vermittlung im Rohmaterial
überhaupt erkennt.
