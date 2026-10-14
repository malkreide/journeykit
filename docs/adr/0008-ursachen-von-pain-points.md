# ADR-0008: Ursachen von Pain Points (`pain_point.caused_by`)

Datum: 2026-10-13 · Status: angenommen (2026-10-13), Umsetzung offen · Issue: [#49](https://github.com/malkreide/journeykit/issues/49) (Muster umgesetzt, Feld offen)

## Kontext

Viele Reibungen in einer Verwaltungs-Journey wären nicht nötig, wenn ein
Schritt davor gelungen wäre. Typisch sind die Rückfrage, die Nachfrage und der
zweite Anlauf (failure demand). #49 hat dafür zwei Optionen gesammelt und
zunächst Option (a) umgesetzt, ein Muster im Skill: Der vermeidbare Schritt
erhält einen Pain Point `friction`, dessen Text die Vermeidbarkeit nennt. Die
Ursache steht «am Schritt davor», und die Chance setzt dort an (`step_ref`).
Option (b), ein Feld `step.avoidable`, sollte nach dem nächsten Beispiel
entschieden werden.

Das dritte Beispiel (`examples/musikschule/`, Befund H9) hat vier
Verbindungen von einer Folge zu ihrer Ursache:

| Folge (Pain Point) | Ursache (Pain Point) | Abstand |
|---|---|---|
| `pp-nachfrage-warteliste-vermeidbar` – Nachfrage beim Sekretariat | `pp-warteliste-ohne-stand` – Bescheid ohne Stand | Schritt direkt davor |
| `pp-nachfrage-rechnung-vermeidbar` – Nachfrage zur Rechnung | `pp-volle-rechnung` – volle Rechnung trotz Ermässigung | Schritt direkt davor |
| `pp-volle-rechnung` | `pp-ermaessigung-papier` – keine Bestätigung, dass die Musikschule die Ermässigung kennt | vier Schritte früher, andere Phase, andere Stelle |
| `pp-semester-ohne-nutzen` – 820 Franken für ein abgemeldetes Semester | `pp-abmeldung-ungueltig` – Abmeldung bei der Lehrperson gilt nicht | Schritt direkt davor, Monate später |

Mit dem Muster zeigen sich drei Schwächen:

1. **«Der Schritt davor» trifft nicht immer zu.** Bei der Rechnung ist die
   Kette zweistufig. Die eigentliche Ursache liegt eine Phase früher bei der
   Gemeinde, zum Teil Back-Stage. Im Modell steht die Kette nur im Text und
   in einer `backstage_notes`-Zeile ohne Evidenzreferenzen; deshalb schreibt
   das Beispiel dort Atom-IDs in den Text.
2. **Nicht jede Folge ist ein Kontakt.** Das bezahlte, aber abgemeldete
   Semester ist kein vermeidbarer Schritt, sondern Folgekosten (ADR-0007).
   Es hat dieselbe Form: Ohne die Ursache gäbe es den Pain Point nicht.
3. **Niemand kann die Verbindung prüfen.** Ob eine Chance bei der Ursache
   ansetzt, wie es das Muster verlangt, sieht nur, wer die Texte liest.
   Indirekt verbindet heute nur die Chance Ursache und Folge (`step_ref` auf
   die Ursache, `linked_pain_points` auf die Folgen).

Auch die Baubewilligung hat eine solche Kette: Der Standort wird nach der
Einsprache geändert, mit neuen Plänen und Mehrkosten
(`pp-standort-nachtraeglich`). Das ist die Folge davon, dass niemand ihn
vorher mit der Nachbarschaft besprochen hatte
(`pp-einsprache-unvorbereitet`).

## Optionen

| Option | Beschreibung | Für | Gegen |
|---|---|---|---|
| A – Muster beibehalten | Text, Chance mit `step_ref` auf die Ursache | keine Änderung | Schwächen 1–3 bleiben |
| B – `step.avoidable` | `true` mit `evidence_refs` am vermeidbaren Schritt; Lint: vermeidbar, aber kein Breakdown davor (#49, Option b) | markiert, was die Kennzahl zählt | nennt die Ursache nicht, ein Lint kann sie nur raten; deckt keine Folgekosten und keine Folgen in bestehenden Schritten (volle Rechnung) |
| **C – `pain_point.caused_by`** | IDs der Pain Points, aus denen dieser folgt | nennt die Ursache ausdrücklich, auch über Phasen und Stellen hinweg; deckt vermeidbare Kontakte und Folgekosten mit einem Begriff; klein und additiv | Belege für die Verbindung selbst stehen in den `evidence_refs` der Folge, nicht am Verweis |
| D – Verweise als Objekte | `caused_by: [{ "pain_point": …, "evidence_refs": […] }]` | eigener Beleg je Verbindung | doppelt sich mit den Belegen der Folge; in allen vier Fällen des Beispiels trägt die Folge den Beleg schon (`m1-23`: «Dann hätte ich nicht anrufen müssen.») |
| E – Ursachengraph auf Journey-Ebene | `causes[]` mit `from`, `to`, Evidenz | ausdrucksstark | grösster Umbau; die Journey wird zum Ursachenmodell oder Blueprint |

## Vorschlag

**Option C.** Beispiel aus der Musikschule:

```json
{
  "id": "pp-nachfrage-rechnung-vermeidbar",
  "text": "Vermeidbarer Kontakt: Die Nachfrage ist nur nötig, weil die Ermässigung nicht rechtzeitig übermittelt wurde. …",
  "type": "friction",
  "caused_by": ["pp-volle-rechnung"],
  "evidence_refs": ["m2-11", "m2-12", "anf-04", "anf-23", "bef-06"]
}
```

- `caused_by`: Array von Pain-Point-IDs, mindestens eine, keine doppelt. Es
  bedeutet: Diesen Pain Point gäbe es nicht, wenn der genannte nicht
  aufgetreten wäre.
- **Vermeidbar** ist damit ein Pain Point mit `caused_by`: Er verschwindet,
  wenn die Ursache behoben ist. Ein eigenes Feld `avoidable` braucht es nicht.
  Ob ein ganzer Schritt vermeidbar ist, sagt weiterhin der Text des Pain
  Points («Vermeidbarer Kontakt: …»).
- **Die Ursache ist immer ein Pain Point**, nie eine `backstage_notes`-Zeile.
  Liegt sie Back-Stage, verweist `caused_by` auf den Pain Point am Schritt,
  an dem sie die Persona trifft (in der Musikschule: keine Bestätigung, dass
  die Musikschule die Ermässigung kennt). Ist auch dieser nicht belegt, gilt
  das Muster aus #49 weiter: offene Frage mit `step_ref`.
- **Der Beleg für die Verbindung** gehört in die `evidence_refs` der Folge –
  eine Aussage der Persona («Dann hätte ich nicht anrufen müssen.») oder eine
  Zahl, die beides verknüpft (38 % der Ermässigungen erst nach der Rechnung).
- **Die Ursache liegt im selben oder einem früheren Schritt.** Eine Journey
  ist ein Durchgang; eine Ursache nach der Folge ist ein Modellfehler.
- **Ein Rückweg, der funktioniert, ist kein Pain Point** und braucht kein
  `caused_by`. Der Schritt «Nachfragen» im Kindergarteneintritt bleibt, wie
  er ist. Ob er als vermeidbarer Kontakt gilt, entscheidet das Review.

## Folgen

Nach den Konventionen in `CLAUDE.md` für Schemaänderungen:

- **Schema**: optionales Array `caused_by` an `pain_point`, Einträge als
  `$defs/id`, `uniqueItems`, `minItems: 1`. `schema_version` bleibt 1.0, weil
  die Änderung additiv ist.
- **`model.py`**: `JourneyIndex` erhält den Rückweg von der Ursache zu ihren
  Folgen (`consequences_of`) für Viewer, Audit und Lints. `all_refs()` bleibt
  unverändert, weil `caused_by` auf Pain Points zeigt, nicht auf Evidenz.
- **Lints**:
  - `L001`, neue Meldungsvariante `L001.caused_by` (ERROR): unbekannte
    Pain-Point-ID oder Verweis auf sich selbst.
  - `L005` (ERROR, am Ende des Blocks L001–L004): Die Ursache liegt in einem
    späteren Schritt, oder Verweise im selben Schritt bilden einen Kreis.
  - `L065` (INFO, am Ende des Blocks L060–L064): Eine Chance verknüpft nur
    Folgen, setzt aber weder per `linked_pain_points` noch per `step_ref` bei
    einer ihrer Ursachen an. Das prüft die Regel des Musters «die Chance setzt
    bei der Ursache an» am Modell.
  - Meldungen und Hinweise in `lint_messages.py` (de, fr), Tests in
    `tests/test_lint.py`, je eine Zeile in beiden READMEs.
- **Viewer**: Pain Points mit Ursache zeigen «Folge von ‹…›» als Link, der zum
  Schritt der Ursache springt, im Journey- und im Prozess-Layer; die Ursache
  zeigt «führt zu n Folgen». Gezeichnete Pfeile vorerst nicht: Sie über das
  Raster zu legen, ist ohne Framework aufwendig (ADR-0003). Neue Texte in
  `jk-i18n` (de, fr).
- **Audit-Bericht**: eine Zeile unter «Evidenzlage», etwa «Ursachenketten:
  4 Folgen, davon 1 über Phasen hinweg». Texte in `export_texts.py` (de, fr).
  Story Map und Diff bleiben unverändert.
- **Skill**:
  - `SKILL.md` (Synthese): Das Muster «Vermeidbare Schritte» wird zu den
    Regeln oben. Kennzahl «Anteil vermeidbarer Kontakte» unverändert.
  - Audit-Modus: `caused_by` nur, wenn die Vorlage die Ursache nennt; sonst
    bleibt es bei der offenen Frage.
  - `references/review-fragen.md`: Die Frage «An welcher Stelle rufen
    Menschen an, obwohl sie es nicht müssten?» verweist auf `caused_by`. Neu
    dazu: «Belegt die Folge auch die Verbindung zur Ursache – oder haben wir
    sie nur vermutet?»
- **Beispiele**:
  - Musikschule: die vier Verbindungen aus dem Kontext. Die `backstage_notes`
    bei «Ermässigung beantragen» verliert die Atom-IDs im Text.
  - Baubewilligung: `pp-standort-nachtraeglich` → `pp-einsprache-unvorbereitet`,
    wenn die Belege die Verbindung tragen (`b2-09`, `b2-10`); sonst nicht.
  - Kindergarteneintritt: keine Änderung.
  - Im README der Musikschule wird H9 als umgesetzt markiert, in
    `docs/konzept.md` («Evaluation») die Zeile «Vermeidbare Kontakte und
    Ursachenketten».
- **Tests**, **`docs/konzept.md`** (Schicht 3), **beide READMEs**,
  **`CHANGELOG.md`**.

## Entscheid

Angenommen am 2026-10-13 wie vorgeschlagen (Option C), zusammen mit ADR-0007.
Die Umsetzung folgt nach ADR-0007; die Codes stehen damit fest: L004 gehört
den Kosten, L005 dieser Regel. Die Frage zu L061 bleibt offen (siehe unten).

## Nicht entschieden

- **L061 und Folgen**: Heute braucht jeder Pain Point ab Severity 4 eine
  eigene Chance. Ob eine Chance an der Ursache auch ihre Folgen abdeckt,
  bleibt offen. Es würde L061 nachsichtiger machen, und das verlangt einen
  eigenen Entscheid (`CLAUDE.md`: «Was nicht tun»).
- **Belege an Back-Stage-Notizen**: `backstage_notes` bleiben Freitext. Erst
  wenn ein Beispiel Back-Stage-Ursachen belegen muss, die die Persona nicht
  trifft – und dann eher im Blueprint als in der Journey.
- **Verbindung über Dateien hinweg** (Ursache in der Journey einer anderen
  Persona, etwa der Installationsfirma): erst mit einem Beispiel, das es
  braucht.

## Voraussetzung

Keine. Die Änderung ist additiv und unabhängig von ADR-0007; nur die
Folgekosten nutzen beide Felder. Die Evaluation sollte prüfen, ob die
Pipeline Ursachen aus dem Material belegt oder nur vermutet.
