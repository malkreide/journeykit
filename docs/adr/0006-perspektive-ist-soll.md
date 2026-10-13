# ADR-0006: Perspektive Ist-Zustand oder Soll-Konzept (`scenario.perspective`)

Datum: 2026-10-13 · Status: angenommen (2026-10-13) · Issue: [#41](https://github.com/malkreide/journeykit/issues/41)

## Kontext

Das zweite Audit galt einer öffentlich publizierten Präsentation einer
Kantonsverwaltung, die sich «Parcours» nennt. Inhaltlich ist sie ein
**Soll-Konzept**: Sie stellt Lösungen vor (Standards, Systeme, Kosten) und
beschreibt, wie der Weg damit gelingen soll. Die Inhalte der Vorlage stehen
nicht im Repo.

Das Modell kann diesen Unterschied nicht ausdrücken:

- Im Übertrag sieht ein Soll-Konzept aus wie eine Ist-Journey ohne Reibung,
  und so wird es auch gelesen.
- L020 meldet ERROR «kein Breakdown». Für eine Ist-Journey stimmt das. Hier
  geht es aber am Kern vorbei: Das Problem ist nicht der Happy Path, sondern
  dass das Artefakt nicht den heutigen Weg zeigt.
- Den Unterschied zwischen Ist und Soll kennt das Modell nur an einer Stelle,
  bei `recovery_paths.exists`.

## Optionen

| Option | Beschreibung | Für | Gegen |
|---|---|---|---|
| A – nur Diagnose | Warnsignale in `diagnose.md`, Befund im Übergabe-Satz | keine Schemaänderung | Viewer und Lints sehen es nicht; der Übertrag bleibt irreführend, sobald er ohne Audit-Bericht gelesen wird |
| **B – Feld am Szenario** | `scenario.perspective: as_is \| to_be`, Default `as_is` | klein, rückwärtskompatibel; Viewer, Lints und Urteil können darauf reagieren | ein Feld mehr, das gesetzt werden muss |
| C – eigener `map_type` | etwa `concept` neben `user_journey` | nutzt die bestehende Diagnose | vermischt zwei Fragen: welches Artefakt (Journey oder Blueprint) und welche Zeit (heute oder künftig); ein Blueprint kann ebenfalls Ist oder Soll sein |

## Entscheid

**Option B**, angenommen am 2026-10-13 mit dem Auftrag, #41 umzusetzen.

```json
"scenario": {
  "title": "Schalterbesuch mit Termin",
  "goal": "…",
  "perspective": "to_be"
}
```

- `as_is`: der Weg, wie Nutzende ihn heute erleben. Das gilt auch, wenn das
  Feld fehlt.
- `to_be`: Soll-Konzept, also wie der Weg künftig gehen soll.
- Das Feld gehört zum **Szenario**, nicht zu `meta`: Ist und Soll desselben
  Anliegens sind zwei Szenarien und damit zwei Dateien. Mit gleichen
  Phasen-IDs lassen sie sich im Viewer übereinanderlegen.

## Folgen

- **Schema**: Ein optionales Enum ergänzt `scenario`. `schema_version` bleibt
  1.0, denn die Änderung ist additiv.
- **`model.py`**: Ein Soll-Konzept ist nie «belastbar».
  `propose_verdict` nennt `to_be` als ersten Grund für «Hypothese». Was sein
  soll, lässt sich nicht durch Nutzende belegen, wie gut das Konzept auch
  begründet ist. Das Poster-Urteil hat weiterhin Vorrang.
- **Lint L020**: Bei `to_be` meldet L020 auf Stufe INFO, mit einer eigenen
  Meldung (`L020.to_be`): Welche Breakdowns von heute das Konzept beheben
  soll, steht nicht im Modell. Die Schwelle sinkt damit nicht. Die Frage ist
  eine andere, und der Hinweis zeigt auf die Ist-Journey. L021 bleibt
  unverändert: Eine Phase ohne Reibung ist auch in einem Soll-Konzept ein
  Zeichen für Innensicht.
- **Audit-Bericht**: Der Abschnitt «Diagnose» nennt das Soll-Konzept. Das
  Urteil hat einen eigenen Satz: Ein Soll-Konzept lässt sich nicht durch
  Nutzende belegen, nur durch eine Ist-Journey begründen. Die Formel «noch
  nicht belegt» würde nahelegen, dass mehr Evidenz es belastbar machen könnte.
- **Viewer**: Im Kopf erscheint das Badge «Soll-Konzept» bzw. «Concept cible»;
  ein Tooltip erklärt den Unterschied. Bei `as_is` bleibt die Anzeige wie
  bisher.
- **Skill**: `diagnose.md` erhält Warnsignale für ein Soll-Konzept. Im
  Audit-Modus setzt der Übertrag `to_be` als vom Audit erschlossene Aussage,
  mit Eintrag im `changelog`. In `review-fragen.md` kommen eine Review-Frage
  und die neue Bedingung für «belastbar» hinzu.
- **Beispiele**: keine Änderung, beide sind Ist-Journeys. Ein Beispiel für ein
  Soll-Konzept bräuchte eigenes synthetisches Input-Material. Es folgt erst,
  wenn ein Fall es verlangt.

## Nicht entschieden

- Ob ein Soll-Konzept auf seine Ist-Journey verweisen soll (etwa
  `scenario.based_on`), bleibt offen, bis ein Fall beide Dateien hat. Bis dahin
  hält eine offene Frage fest, wo die Begründung liegt.
