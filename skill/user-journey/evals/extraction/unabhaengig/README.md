# Unabhängige Fälle

Die ersten acht Fälle des Testsatzes stammen aus derselben Hand wie die
Prompt-Schablone. Die aktuelle Schablone löst sie fehlerfrei; über die
Abdeckung trennen sie nicht (siehe [`../README.md`](../README.md)). Die drei
Fälle `interview-eltern`, `fokusgruppe` und `interview-dolmetsch` sollen das
Problem der «gleichen Hand» teilweise brechen. Sie bleiben synthetisch, wie es
`CLAUDE.md` für den Testsatz verlangt.

## Verfahren (2026-10-14)

1. **Material**: Je Fall schrieb ein frischer Subagent ein langes, unordentliches
   Transkript – ohne `evidenz.md`, ohne zu wissen, was daraus extrahiert wird. Der
   Auftrag beschrieb nur die Situation und wie eine wortgetreue Abschrift klingt
   (Auftrag unten).
2. **Gold**: Ein zweiter frischer Subagent je Fall legte fest, was eine sorgfältige
   Auswertung finden muss. Er sah nur das Transkript und
   [`gold-anleitung.md`](gold-anleitung.md): das Atom-Modell aus `evidenz.md`
   (Evidenzklassen, Atom-Schema) und das Format des Golds – nicht die
   Prompt-Schablone und nicht die Extraktionsregeln je Quellentyp.
3. **Übernahme** mit [`build_case.py`](build_case.py), ohne inhaltliche Änderung am
   Gold:
   - `shared_atoms: true` – ein Atom darf mehrere Gold-Einträge abdecken. Das Gold
     zerlegt lange Redebeiträge feiner als jede Extraktion; sonst zählte die Körnung
     als Lücke.
   - Ausschnitte mit erfundenen Namen und Schulhausnamen um den Namen gekürzt, weil
     eine Extraktion sie ersetzen muss («[Name]», «[Ort]»). Gekürzte Ausschnitte
     behalten mindestens vier Wörter, sonst fällt die Alternative weg. Betroffen:
     13 Ausschnitte in `interview-eltern` (z. B. «seine Unterlagen an den Herrn
     Lüthi» → «seine Unterlagen an den»). Die Schulhausnamen kamen erst nach den
     Läufen dazu: Alle sechs Läufe hatten sie ersetzt, und eine Aussage galt in allen
     als übersehen, obwohl sie erfasst war.
   - Regeln des Falls: Arten `quote` und `metric`, Fundstelle Pflicht, die
     erfundenen Namen als Personendaten, die ersten sechs Wörter jedes längeren
     Redebeitrags der interviewenden Person als «keine Evidenz». Keine Regeln zur
     Anzahl und keine Regel «ein Atom je Fundstelle».
   - `reference.json` aus dem Gold abgeleitet (je Eintrag ein Atom aus dem ersten
     Ausschnitt). Sie belegt, dass das Gold mit voller Punktzahl erfüllbar ist; eine
     von Hand erstellte Extraktion ist sie nicht.
4. **Läufe** wie bei den übrigen Fällen: je Fall ein frischer Subagent, der nur sein
   Bundle las. An den Werkzeugaufrufen geprüft für alle 24 Subagenten dieser Runde
   (3 Autoren, 3 Gold, 18 Läufe). Ergebnisse im [README des Testsatzes](../README.md).

| Fall | Redebeiträge | Gold-Einträge | davon Pflicht |
|---|---|---|---|
| `interview-eltern` | 86 (Mutter, Vater, Interviewerin) | 99 | 63 |
| `fokusgruppe` | 78 (vier Eltern, Moderation) | 99 | 62 |
| `interview-dolmetsch` | 67 (Vater, Dolmetscherin, Interviewer) | 69 | 47 |

## Was das Verfahren nicht bricht

- **Ein Modell schreibt, eines legt fest, eines extrahiert.** Alle drei sind
  dasselbe Modell. Was ihm leichtfällt oder entgeht, fällt allen drei leicht oder
  entgeht allen dreien.
- **Das Gold ist das Urteil eines Subagenten**, nicht einer Fachperson. Es ist
  feinkörnig und eher grosszügig mit «Pflicht». Ein tiefer Wert der Abdeckung heisst
  deshalb zuerst: Gold und Schablone haben eine andere Vorstellung davon, was ein
  Atom ist – nicht zwingend, dass die Extraktion schlecht ist.
- **Synthetisch bleibt synthetisch.** Mundart, echte Unordnung und echte
  Widersprüche kommen erst mit realem Material aus der Evaluation.

## Aufträge

Autor `interview-eltern` (die beiden anderen analog, mit eigener Situation und eigenen
Sprecherkürzeln: Fokusgruppe zu den Klassenlagern mit vier Eltern; Vater mit
interkultureller Dolmetscherin zur Einschulung nach Zuzug):

> Schreibe ein realistisches, fiktives Interview-Transkript als Übungsmaterial für
> die Auswertung qualitativer Interviews in einer Schulverwaltung. […] Situation:
> Gemeinde Musterau (fiktiv), Volksschule. Eine Mitarbeiterin der Schulverwaltung
> interviewt ein Elternpaar (Mutter und Vater, beide sprechen) darüber, wie der
> Schulwechsel ihres Kindes (3. Klasse) mitten im Schuljahr nach einem Umzug
> innerhalb der Gemeinde abgelaufen ist […]. So soll es klingen – wie die
> wortgetreue Abschrift einer Tonaufnahme, nicht wie ein aufgeräumter Text: etwa
> 45 Minuten Gespräch, 70 bis 90 Redebeiträge, mit Zeitstempel […]; Füllwörter,
> abgebrochene Sätze, Unterbrechungen, Wiederholungen, Abschweifungen; die beiden
> Eltern erinnern sich teils unterschiedlich, korrigieren oder ergänzen einander;
> manches ergibt sich erst über mehrere Redebeiträge hinweg; vage Angaben, aber
> auch einzelne konkrete Angaben; Schweizer Hochdeutsch mit Helvetismen […].
> Alles ist erfunden: keine realen Personen, Schulen oder Adressen; keine
> E-Mail-Adressen, Telefonnummern oder AHV-Nummern.

Gold:

> Du legst das Gold für die Auswertung eines Interview-Transkripts fest. Lies genau
> zwei Dateien, sonst nichts: die Anleitung (`gold-anleitung.md`) und das
> Transkript. […] Halte im Feld «why» fest, wessen Aussage es ist. Wo sich die
> beiden widersprechen oder korrigieren, entscheide, was als Aussage gilt, und
> begründe es. […] Prüfe vor dem Schreiben jeden match-Ausschnitt Zeichen für
> Zeichen gegen das Transkript.
