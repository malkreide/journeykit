# ADR-0007: Kosten am Schritt (`step.costs[]`)

Datum: 2026-10-13 · Status: angenommen (2026-10-13) · Issue: [#15](https://github.com/malkreide/journeykit/issues/15)

## Kontext

Kosten, die die Persona trägt, haben im Modell keinen eigenen Ort. Seit der
Baubewilligung (Befund H5) gilt ein Muster im Skill, Stufe 1 von #15: Der
Betrag wird ein `metric`-Atom mit `unit` «CHF». Er wird am Schritt
verknüpft, und kommt er überraschend, entsteht ein Pain Point. Für eine
einmalige Gebühr trägt das (`stat-11`, Median 720 Franken; `b1-21`: «Die
Gebühr war 740 Franken. Das stand nirgends vorher.»). Ein Feld sollte erst
folgen, «wenn ein drittes Beispiel es braucht».

Das dritte Beispiel (`examples/musikschule/`, Befund H8) braucht es. Dort
fallen an:

| Kosten | Beleg | Art |
|---|---|---|
| Schulgeld 820 Franken pro Semester | `tar-01`, `m2-02` | wiederkehrend |
| Ermässigung 25 oder 50 % nach Einkommen | `tar-03`, `m2-08` | Spanne, keine eigene Zahlung |
| Einschreibegebühr 40 Franken | `tar-02`, `anf-21` | einmalig, überraschend |
| Cello-Miete 35 Franken im Monat | `m2-15`, `m2-16` | an Dritte (Musikgeschäft) |
| Digitalpiano gebraucht 600 Franken | `m1-20` | einmalig, Alternative zur Miete |
| Herbstsemester nach verpasster Abmeldung, 820 Franken | `m3-08`, `tar-07` | Folge eines Breakdowns |

Mit dem Muster stehen diese Beträge in zehn Atomen über vier Schritte
verteilt. Daran zeigen sich vier Schwächen:

1. **Die Periode ist Freitext.** `unit` lautet «CHF», «CHF pro Semester» oder
   «CHF pro Monat». Kein Werkzeug kann damit rechnen oder vergleichen.
2. **Ein Betrag sagt nicht, was er ist.** 820 Franken kommen viermal vor: als
   Tarif (Soll), als unverstandener Tarif, als Rechnung und als Folgekosten.
3. **Wem bezahlt wird, steht nur im Text.** Gerade Kosten bei Dritten
   (Musikgeschäft, Installationsfirma) sieht die Verwaltung sonst nicht.
4. **Viewer, Audit-Bericht und Lints sehen keine Kosten.** Die Frage der
   Persona – «Was kommt auf uns zu?» – beantwortet nur, wer alle Atome liest.

Eine Annahme aus #15 hat das Beispiel widerlegt: «Vorher bekannt» ist keine
Eigenschaft eines Betrags. Belegen lässt es sich als Befragungswert je
Kostenart: Schulgeld 46 %, Ermässigung 31 %, Instrument 52 % (`bef-01` bis
`bef-03`). Für dieselbe Gebühr ist es bei der einen Familie wahr und bei der
anderen falsch.

Der Kindergarteneintritt hat keine Kosten. Das Feld muss also optional sein.

## Optionen

| Option | Beschreibung | Für | Gegen |
|---|---|---|---|
| A – Muster beibehalten | `metric`-Atom in CHF, Pain Point bei Überraschung | keine Änderung; trägt einmalige Gebühren | Schwächen 1–4 bleiben; jede Journey löst es anders |
| **B – Liste am Schritt** | `step.costs[]` mit Betrag, Spanne, Periode, Empfänger und Pflichtbeleg | Kosten werden bei einem Ereignis fällig (Rechnung, Kauf, Entscheid); trägt alle Fälle beider Beispiele; gleiche Logik wie `duration_days` | wiederkehrende Kosten stehen an einem Schritt, obwohl sie weiterlaufen |
| C – Feld an der Phase | wie `phase.duration_days` | ein Ort je Phase | mischt Kosten verschiedener Schritte (Miete und Ermässigung in «Den Start vorbereiten»); der Schritt, an dem die Überraschung passiert, geht verloren |
| D – Kostenregister auf Journey-Ebene | `costs[]` mit IDs, auf die Schritte und Pain Points verweisen | Wiederverwendung, Verweise aus Pain Points | grösster Umbau; lädt dazu ein, Alternativen und bedingte Kosten zu einer Summe zu addieren |

Bei B und D erwogen und verworfen: `known_in_advance` als Ja/Nein je Betrag
(siehe Kontext).

## Vorschlag

**Option B.** Beispiel aus der Musikschule, Schritt «Rechnung prüfen»:

```json
"costs": [
  {
    "label": "Schulgeld Einzelunterricht 30 Minuten",
    "amount": 820,
    "min": 410,
    "currency": "CHF",
    "period": "semester",
    "paid_to": "Musikschule",
    "basis": "Tarif laut Tarifordnung; mit Ermässigung der Gemeinde 615 oder 410 Franken",
    "evidence_refs": ["tar-01", "tar-03", "m2-02"]
  },
  {
    "label": "Einschreibegebühr",
    "amount": 40,
    "period": "once",
    "paid_to": "Musikschule",
    "evidence_refs": ["tar-02", "anf-21"]
  }
]
```

| Feld | Pflicht | Bedeutung |
|---|---|---|
| `label` | ja | Was bezahlt wird, in Nutzerworten oder nach dem Erlass |
| `amount` | ja | Regelbetrag oder typischer Betrag (Tarif, Median), ≥ 0 |
| `min`, `max` | nein | belegte Spanne, etwa einkommensabhängig oder je Instrument; keine Extremwerte |
| `currency` | nein | ISO-Code, Standard `CHF` |
| `period` | ja | `once`, `month`, `semester`, `year` – Pflicht, weil ein Betrag ohne Periode nichts bedeutet (Schwäche 1) |
| `paid_to` | nein | Rolle der Empfängerin, keine Namen («Musikschule», «Musikgeschäft») |
| `basis` | nein | Was der Betrag misst oder wann er anfällt («Median 2025», «nur bei Miete», «nur nach verpasster Abmeldung») |
| `evidence_refs` | ja, mindestens 1 | Ohne Beleg kein Eintrag, wie bei `duration_days` |

Regeln für die Synthese:

- **Am Schritt, an dem der Betrag fällig wird** – Rechnung, Kauf, Vertrag,
  Entscheid. Wo die Persona vorher von den Kosten erfährt (oder eben nicht),
  zeigen Pain Points und die Kennzahl «vorher bekannt».
- **Wiederkehrende Kosten einmal** erfassen, am Schritt der ersten Fälligkeit,
  mit `period`.
- **Ohne belegten Betrag kein Eintrag.** Die Mehrkosten durch die Einsprache
  in der Baubewilligung (`b2-10`: «… das hat die Firma gemacht und mir
  verrechnet») haben keinen Betrag. Sie bleiben Pain Point und Text.
- **Keine Summe.** Kosten einer Journey sind oft Alternativen (mieten oder
  kaufen) oder bedingt (Ermässigung, Folgekosten). Eine Summe wäre
  Pseudo-Präzision; Viewer und Exporte zeigen keine.
- **Nicht erfasst werden** Zeitkosten (die zeigt `duration_days`), Kosten der
  Verwaltung (sie gehören in einen Blueprint) und Subventionen, die die
  Persona nicht trägt.
- **«Vorher bekannt» bleibt eine Kennzahl** je Kostenart, «Anteil, der die
  Kosten vorab kannte» (`references/kpi-uebersetzung.md`), kein Feld.
- **Folgekosten** eines Breakdowns stehen am Schritt, an dem sie fällig
  werden. Die Verbindung zur Ursache läuft über den Pain Point
  (`pain_point.caused_by`, ADR-0008).

## Folgen

Nach den Konventionen in `CLAUDE.md` für Schemaänderungen:

- **Schema**: optionales Array an `step`, Einträge mit
  `additionalProperties: false`; Pflicht sind `label`, `amount`, `period` und
  `evidence_refs`. `schema_version` bleibt 1.0, weil die Änderung additiv ist.
- **`model.py`**: Die `evidence_refs` der Kosten kommen in `all_refs()`, wie
  bei `duration_days`; so sehen L001 und L100 sie. Kosten sind keine
  Erlebnis-Aussage, `claims()` und L010 bleiben unverändert.
- **Lints**:
  - `L004` (ERROR, am Ende des Blocks L001–L003): widersprüchliche Spanne,
    also `min` > `amount` oder `amount` > `max`; analog L003.
  - `L103` (INFO, am Ende des Blocks L100–L102): Kosten, die nur mit
    `assumed`-Evidenz belegt sind, etwa allein mit der Gebührenordnung. Sie
    sagt, was gelten soll, nicht was bezahlt wurde (`references/evidenz.md`).
  - Meldungen und Hinweise in `lint_messages.py` (de, fr), Tests in
    `tests/test_lint.py`, je eine Zeile in beiden READMEs.
- **Viewer**: Zeile «Kosten» im Journey-Layer, nur wenn mindestens ein
  Schritt Kosten hat. Je Schritt ein Chip «820 CHF / Semester · an
  Musikschule», die Spanne «410–820» und ein Drill-down zur Evidenz. Keine
  Summe. Neue Texte in `jk-i18n` (de, fr); auch die vier Werte von `period`
  brauchen Beschriftungen, das prüft `test_viewer_i18n.py`.
- **Audit-Bericht**: Abschnitt «Kosten» mit einer Tabelle (Schritt,
  Bezeichnung, Betrag oder Spanne, Periode, Empfänger, Evidenzklassen). Texte
  in `export_texts.py` (de, fr). Story Map, Massnahmen-CSV und Diff bleiben
  unverändert; der Diff vergleicht auch `duration_days` heute nicht.
- **Skill**: `SKILL.md` (Synthese) ersetzt das Muster «Kosten ohne eigenes
  Feld» durch die Regeln oben. `references/evidenz.md` bleibt, wie es ist:
  Erst entstehen Atome, das Feld kommt bei der Synthese.
- **Beispiele**:
  - Musikschule: fünf Einträge. Schulgeld und Einschreibegebühr bei «Rechnung
    prüfen», Miete und Kauf bei «Instrument mieten oder kaufen», Folgekosten
    bei «Nicht abgemeldetes Semester bezahlen».
  - Baubewilligung: Gebühr bei «Entscheid erhalten» (`amount` 720 aus
    `stat-11`, Beleg auch `b1-21`, `basis` «Median 2025, inklusive
    Publikation, ohne Fachgutachten»).
  - Kindergarteneintritt: keine Änderung.
  - Im README der Musikschule wird H8 als umgesetzt markiert, in
    `docs/konzept.md` («Evaluation») die Zeile «Kosten und Gebühren».
- **Tests**, **`docs/konzept.md`** (Schicht 3), **beide READMEs**,
  **`CHANGELOG.md`**.

## Entscheid

Angenommen am 2026-10-13 wie vorgeschlagen (Option B), zusammen mit ADR-0008,
und gleich umgesetzt. Beim Umsetzen festgelegt:

- **Ort im Viewer**: Die Zeile «Kosten» steht direkt unter «Macht», bei den
  anderen Fakten zum Schritt, vor Denken und Fühlen. Unter dem Filter «nur
  Primärevidenz» verschwinden Einträge, die nur Annahmen belegen.
- **Darstellung**: Betrag, Währung und Periode als ein Beleg-Knopf
  («820 CHF pro Semester · Spanne 410–820 · an Musikschule»), darüber die
  Bezeichnung, darunter `basis`. Zahlen ohne Tausendertrennzeichen, wie im
  Audit-Bericht.
- **L103** fasst alle betroffenen Einträge in einem Befund zusammen, wie
  L100, statt einen je Eintrag.
- **Beispiele**: Die Musikschule hat fünf Einträge, die Baubewilligung einen;
  keiner löst L103 aus. Alle drei Viewer-Dateien sind mit der neuen Vorlage
  neu gerendert.

## Nicht entschieden

- **Weitere Perioden** (Tag, Woche, Quartal): additiv ergänzen, sobald ein
  Beispiel sie braucht, etwa Betreuungstarife pro Tag.
- **Summen je Periode im Viewer**: vorerst nicht, wegen Alternativen und
  bedingter Kosten. Erst wenn ein Feld beides unterscheidet.
- **Wer die Kosten trägt** (`paid_by`, etwa Versicherung oder Sozialhilfe
  statt der Persona): erst mit einem Beispiel, in dem das vorkommt.
- **Kosten im Diff**: zusammen mit `duration_days` entscheiden.

## Voraussetzung

Keine. Die Änderung ist additiv und kann vor der Evaluation umgesetzt werden.
Die Evaluation sollte aber prüfen, ob die Pipeline Beträge mit ihrer Periode
erkennt. Und ob sie einen Tarif aus der Gebührenordnung nicht als bezahlten
Betrag übernimmt.
