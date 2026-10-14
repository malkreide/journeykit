# Testsatz «Input → erwartete Atome»

Prüft die Prompt-Schablone für die Extraktion in
[`references/evidenz.md`](../../references/evidenz.md): Findet eine Extraktion
die Atome, die eine gute Extraktion enthalten muss? Setzt sie die Felder
richtig? Hält sie die Regeln ein?

Alles hier ist **synthetisch** (Gemeinde Musterau, erfundene Namen). Der
Testsatz braucht kein Modell im Repo: Die CI prüft nur, dass Fälle, Gold und
Scorer zusammenpassen. Extraktionsläufe macht, wer die Schablone ändert.

## Fälle

| Fall | Quelle | Was er prüft |
|---|---|---|
| `interview` | Interview-Transkript, `reported` | wörtliche Zitate mit Zeitstempel; Fragen der interviewenden Person sind keine Evidenz; ausdrückliche vs. abgeleitete Emotion; Breakdown (aufgeben, an den Schalter ausweichen) vs. Reibung; Vermittlung durch die Nachbarin; Name im Zitat ersetzen; ein Atom pro Aussage, nicht pro Satz |
| `anfragen` | Anfragen-Export (CSV), `observed` | erst kategorisieren, dann Metriken; 3–6 Einzelfälle mit Ticket-ID; nicht jede Zeile ein Atom; Ausweichen an den Schalter; Name im Freitext ersetzen |
| `prozessdokument` | Prozessbeschreibung, `assumed` | `document_excerpt` statt `metric`; eine Frist ist keine gemessene Dauer; `contradicts` gegen bekannte Anfragen |
| `statistik` | Geschäftskontrolle (CSV), `observed` | `metric` mit `value` und `unit` genau wie in der Quelle – Arbeitstage nicht in Kalendertage umrechnen |
| `workshop` | Workshop ohne Nutzende, `assumed` | `workshop_statement`; Vermutungen des Teams über Gefühle sind keine ausdrücklich geäusserte Emotion; `contradicts` gegen Messwert und Anfrage |
| `interview-hort` | längeres Interview, `reported`, 16 Pflicht-Atome | Frist neben erlebter Dauer, mit Korrektur mitten im Satz («fünf – nein, sieben Wochen»: value 7); handelnde Dritte (Schwiegermutter füllt das Formular aus); Kosten mit Periode und ob sie vorher bekannt waren; Gefühle anderer (Kind weint, Chef nicht begeistert); Suggestivfrage; `contradicts` gegen zwei von drei bekannten Soll-Aussagen |
| `befragung` | Elternbefragung mit Freitext, `reported` | n und Fragewortlaut im `text`, auch bei Teilgruppen (n = 201, 52, 14); eine negativ formulierte Frage mit 64 % Zustimmung ist Reibung; Freitexte nur, wo sie zeigen, was die Zahlen nicht zeigen |
| `beschwerde` | Beschwerde per E-Mail, `reported` | Treuhänder mit Vollmacht; Soll-Frist neben erlebter Dauer; Ursache und Folge; «1'236» als Zahl; Mahngebühr vorher nicht bekannt; Ironie ist kein positives Signal; Kopf-, Gruss- und Signaturzeilen bleiben draussen |
| `interview-eltern` | langes Interview mit zwei Befragten, `reported` – **unabhängig** | 86 Redebeiträge, Mutter und Vater korrigieren einander, Abschweifungen, Aussagen über mehrere Redebeiträge; 63 Pflicht-Einträge |
| `fokusgruppe` | Fokusgruppe mit vier Eltern, `reported` – **unabhängig** | 78 Redebeiträge, Ins-Wort-Fallen, Zustimmung und Widerspruch, Bezüge auf früher Gesagtes; 62 Pflicht-Einträge |
| `interview-dolmetsch` | Interview über eine Dolmetscherin, `reported` – **unabhängig** | 67 Redebeiträge, Übersetzung in Ich- und Er-Form, eigene Erklärungen der Dolmetscherin; 47 Pflicht-Einträge |

**Unabhängig** heisst: Ein Subagent ohne `evidenz.md` schrieb das Material, ein zweiter, der nur das Atom-Modell kannte, legte das Gold fest. Verfahren und Grenzen in [`unabhaengig/`](unabhaengig/README.md).

Je Fall:

- `input.*` – die Quelle,
- `case.json` – Werte für die Schablone (Titel, Art, Klasse, `source_id`, Präfix, Phasen, Persona, bekannte Atome) und die Regeln des Falls (Anzahl, erlaubte Arten, Fundstelle, verbotene Textstellen, Personendaten),
- `expected.json` – das **Gold**: Pflicht-Atome als Textbausteine (bei Messwerten mit Wert) und die Felder, die sie haben müssen,
- `reference.json` – eine von Hand erstellte korrekte Extraktion. Sie muss die volle Punktzahl ohne Regelverstoss erreichen (`tests/test_extraction_eval.py`).

## Ablauf

```bash
python scripts/eval_extraction.py prompts -o /tmp/prompts --bundle
# Je Fall /tmp/prompts/<fall>.bundle.md (evidenz.md und gefüllter Prompt) an ein
# Modell geben, die Antwort (JSON-Array) als /tmp/antworten/<fall>.json speichern.
python scripts/eval_extraction.py score /tmp/antworten -o bericht.md
# Mehrere Läufe nebeneinander; Läufe «<name>-1», «<name>-2» … gelten als eine Schablone
python scripts/eval_extraction.py compare runs/a-1 runs/a-2 runs/b-1 -o vergleich.md
```

Eine ältere Schablone prüft man mit ihrer `evidenz.md`:
`git show <commit>:skill/user-journey/references/evidenz.md > /tmp/alt.md` und
`prompts --evidenz /tmp/alt.md`.

Das Modell darf weder `expected.json` noch `reference.json` sehen. Die Läufe
unten wurden so gemacht: je Fall ein frischer Subagent, der nur das Bundle lesen
und nur seine Antwortdatei schreiben durfte. Für die Läufe vom 2026-10-14 ist
das an den Werkzeugaufrufen aller 132 Subagenten geprüft (48 + 18 + 33 + 33): je ein
Read (das eigene Bundle) und ein Write (die eigene Antwort), sonst nichts.

## Was gemessen wird

- **Pflicht-Atome gefunden** – Anteil der Gold-Atome, für die die Extraktion ein passendes Atom hat. Ein umformuliertes Zitat zählt nicht als Treffer.
- **Feldtreue** – bei den gefundenen Atomen: `kind`, `class`, `signal`, Fundstelle, Emotion, `value`, `unit` (eine Schreibweise oder eine Liste gleichwertiger, z. B. «CHF» oder «Franken pro Betreuungstag»), `contradicts` und `text_has` (Angaben, die im `text` stehen müssen, etwa n einer Befragung), soweit das Gold sie vorgibt.
- Bei den unabhängigen Fällen darf ein Atom mehrere Gold-Einträge abdecken (`shared_atoms` in `expected.json`): Ihr Gold zerlegt lange Redebeiträge feiner als jede Extraktion. Wie grob eine Extraktion zusammenfasst, zeigt deshalb nicht die Abdeckung, sondern die Zahl der Atome und die **geteilten Pflicht-Einträge**: gefundene Pflicht-Einträge, deren Atom auch einen anderen gefundenen Pflicht-Eintrag abdeckt (Abschnitt «Körnung» in `compare`).
- **Regelverstösse** – über alle Atome: Schema, Präfix und `source_ref`, Klasse, erlaubte Arten, Zitat wörtlich (Auslassungen «…» und Ersetzungen «[Name]» erlaubt), Fundstelle, Personendaten, Fragen statt Aussagen, Emotionen, wo keine geäussert werden, eine Aussage auf mehrere Atome verteilt, Anzahl und Einzelfälle.

## Ergebnisse (2026-10-08)

| Lauf | Schablone | Atome | Pflicht-Atome | Feldtreue | Regelverstösse |
|---|---|---|---|---|---|
| [`runs/2026-10-08-schablone-alt`](runs/2026-10-08-schablone-alt/bericht.md) | vor der Überarbeitung | 52 | 32/32 | 93/93 | 48 |
| [`runs/2026-10-08-schablone-neu`](runs/2026-10-08-schablone-neu/bericht.md) | überarbeitet | 42 | 32/32 | 93/93 | 0 |

Was Lauf 1 an der Schablone gezeigt hat und wie sie geändert wurde:

| Befund | Verstösse | Änderung in `evidenz.md` |
|---|---|---|
| Die Schablone nannte die Quellen-ID nicht; das Modell erfand eine (`anf`, `doc` …) | 35 | Platzhalter `{source_id}` in Einleitung und Schlusssatz |
| Ein Redebeitrag auf mehrere Atome verteilt; Dauern doppelt als Zitat und als `metric` – Widerspruch zwischen «Zitate wörtlich» und «Dauern als `metric`» | 6 (+ Anzahl) | «Ein Atom pro Aussage, nicht pro Satz», «nie doppelt»; Dauer im Interview bleibt `quote` mit `value` und `unit` |
| `channel_hint: "mail"` – die erlaubten Werte standen nirgends im Skill | 3 | Liste der Werte in der Schablone |
| Name im Zitat: ersetzen oder wörtlich bleiben? | – (Scorer) | «[Name]», «[Ort]» als Ersetzung; der Scorer akzeptiert eckige Klammern |
| Anfragen-Export in zehn Metriken zerlegt | Anzahl | «Eine Metrik je Kategorie und je Kanal» |

## Ergebnisse (2026-10-14): drei schwierigere Fälle, je drei Läufe

Je drei blinde Läufe über alle acht Fälle mit der Schablone vor der
Überarbeitung (`alt`, Stand vor `a1485a7`) und mit der aktuellen (`aktuell`).
Vollständiger Vergleich in [`runs/2026-10-14-vergleich.md`](runs/2026-10-14-vergleich.md).

| Schablone | Läufe | Atome je Lauf | Pflicht-Atome | Feldtreue | Regelverstösse |
|---|---|---|---|---|---|
| alt | 3 | 103–106 | 71/71 in jedem Lauf | 96 % (263–265 von 275) | 82–83 |
| aktuell | 3 | 87 | 71/71 in jedem Lauf | 100 % (275/275) | 0 |

Was die Läufe zeigen:

- **Die neuen Fälle trennen die Schablonen jetzt auch über die Feldtreue**, nicht nur über die Regeln. Die alte Schablone verfehlt in allen drei Läufen dieselben Felder: Dauern als `metric` statt als Zitat mit Wert (`kind`), Zahlen im Zitat ohne `value` und `unit` (Anrufe, Antwortfrist, Mahngebühr, Mittagessen). Das sind genau die Regeln, die die Überarbeitung ergänzt hat («value und unit im selben Atom», «Dauer im Interview bleibt quote»).
- **Über die Abdeckung trennen sie nicht.** Kein Lauf übersieht ein Pflicht-Atom – auch nicht die Schwiegermutter, die erst im zweiten Satz eines Redebeitrags auftaucht, oder die Mahngebühr, die im selben Satz steht wie der Hinweis, dass sie nirgends angekündigt war.
- **Die inhaltlichen Fallen fängt das Modell mit beiden Schablonen ab**: Korrektur «fünf – nein, sieben Wochen» (value 7), negativ formulierte Frage (64 % Zustimmung als Reibung), Ironie («Vielen Dank auch …» nicht positiv), Weinen des Kindes nicht als ausdrückliche Emotion, n der Teilgruppen im `text`, Fragen der interviewenden Person und Signaturzeile ausgelassen. Inhaltliche Ausrutscher gab es nur mit der alten Schablone: zweimal die Öffnungszeiten im Freitext als `need` statt als Reibung, einmal die ausweichende E-Mail-Antwort als `breakdown`.
- **Die Streuung innerhalb einer Schablone ist klein – im Ergebnis, nicht im Wortlaut.** Zwei Läufe derselben Schablone stimmen nur in 3 bis 11 Atomen in allen Feldern überein (Kürzungen, Tags, Emotionslabels, Phasen unterscheiden sich). Was der Scorer prüft, bleibt aber gleich: Die drei aktuellen Läufe liefern je Fall dieselbe Anzahl Atome, die drei alten verfehlen fast dieselben Felder. Für diesen Abstand zwischen zwei Schablonen hätte ein Lauf gereicht; ob das für knappere Unterschiede gilt, zeigt erst ein Vergleich mit kleinerem Abstand.

Nach dem ersten Lauf korrigiert, für alle Läufe gleich: Der Scorer liest «1'236»
als 1236 (vorher 1 und 236), `mahnung-voll` wird am Betrag statt am Wortlaut
erkannt (ein `metric`-Atom darf umschreiben), und `beschwerde` hat keine Regel
«ein Atom je Fundstelle», weil eine Briefzeile zwei vertretbar getrennte
Aussagen tragen kann. Die Extraktionen selbst blieben unberührt.

## Ergebnisse (2026-10-14): unabhängige Fälle, je drei Läufe

Je drei blinde Läufe über die drei unabhängigen Fälle mit beiden Schablonen.
Vollständiger Vergleich in [`runs/2026-10-14-unabhaengig-vergleich.md`](runs/2026-10-14-unabhaengig-vergleich.md).

| Schablone | Läufe | Atome je Lauf | Pflicht-Einträge | Feldtreue | Regelverstösse |
|---|---|---|---|---|---|
| alt | 3 | 222–229 | 168–172 von 172 | 96–97 % | 0, 93, 0 |
| aktuell | 3 | 168–179 | 170 von 172 in jedem Lauf | 96 % | 0 |

- **Über die Abdeckung trennen auch unabhängige Fälle nicht.** Beide Schablonen finden 98–100 % dessen, was ein unabhängiges Gold als Pflicht festlegt. Die vier Fehlstellen eines alten Laufs sind umschriebene Messwerte («80 Franken» statt «achtzig Franken»): Der Inhalt ist da, der wörtliche Abgleich findet ihn nicht. Die aktuelle Schablone übersieht im Elterninterview in jedem Lauf zwei Aussagen wirklich – an der Stelle steht kein Atom.
- **Die Körnung trennt.** Die aktuelle Schablone fasst gröber zusammen: im Elterninterview 41–47 Atome gegenüber 70–83, und 37–42 der 61 gefundenen Pflicht-Einträge teilen sich dort ein Atom mit einem anderen (alt: 12–26 von 63). Das ist die Regel «Ein Atom pro Aussage, nicht pro Satz: Sätze desselben Redebeitrags … bleiben ein Atom» aus der Überarbeitung. In der Fokusgruppe mit kurzen Beiträgen ist der Unterschied klein (80–86 gegen 88–96 Atome).
- **Die Feldtreue misst hier die Uneinigkeit zweier Urteile**, nicht eine Schablone: 96–97 % für beide. Die Extraktion wertet schärfer als das Gold – Gold «neutral», Extraktion «friction» (17-mal in je drei Läufen beider Schablonen), Reibung als Breakdown (aktuell 15, alt 9), ausdrückliche Emotion, wo das Gold keine sieht (8–9).
- **Die Regeln trennen kaum.** Die Quellen-IDs (`int-e7`, `fg-f2`, `int-d3`) lassen sich aus den Beispielen in `evidenz.md` erraten; nur ein alter Lauf verfehlt sie in einem Fall (93 Verstösse).

Was daraus folgt: Die Überarbeitung vom 2026-10-08 hat Doppelungen beseitigt und
die Regeln durchgesetzt, aber die Atome gröber gemacht. In langen Redebeiträgen
gehen dadurch einzelne Aussagen unter, und ein Atom mit mehreren Aussagen trägt
nur ein `signal`. Das ist der nächste Kandidat für eine Schablonenänderung
(«in langen Redebeiträgen je Aussage ein Atom») – mit Messlauf vorher und nachher.
Gemessen im Abschnitt «Messlauf Körnung» unten: verworfen.

Nach den Läufen korrigiert, für alle Läufe gleich: Ausschnitte im Gold, die
Schulhausnamen enthielten, sind um den Namen gekürzt wie zuvor die Personennamen;
alle sechs Läufe hatten «Bachmatt» und «Lindenhof» ersetzt, wie es die Schablone
für Orte verlangt. Gekürzte Ausschnitte behalten mindestens vier Wörter.

## Messlauf Körnung (2026-10-14): verworfen

### Kriterium, vorab festgelegt

Festgelegt und gepusht vor dem ersten Lauf (Commit `f2dd14d`), hier unverändert.

Änderung in `evidenz.md`, ein Hebel an zwei Stellen (Schablone und Abschnitt
«Interview-Transkripte»): «Ein Atom pro belegbarer Aussage, nicht pro Satz **und
nicht pro Redebeitrag**: … wechselt ein Redebeitrag das Thema oder den Schritt,
wird jede Aussage ein eigenes Atom mit derselben Fundstelle.» Der Richtwert
«Typisch 12–25 Atome pro 45-Minuten-Interview» bleibt unverändert, damit nur die
neue Regel gemessen wird.

**Vorher** sind die Läufe `2026-10-14-aktuell-1..3` (acht Fälle) und
`2026-10-14-unabhaengig-aktuell-1..3` (drei Fälle) – gleiche Schablone, gleiche
Prompts. **Nachher** sind je drei blinde Läufe über alle elf Fälle mit der
geänderten Schablone.

Die Änderung wird **übernommen**, wenn über die drei Läufe nachher alle drei
Bedingungen gelten, sonst wird `evidenz.md` zurückgesetzt und die Läufe bleiben
als Beleg:

1. Unabhängige Fälle: Die gefundenen Pflicht-Einträge nehmen nicht ab (im Mittel
   mindestens 170 von 172, wie vorher).
2. Elterninterview: Im Mittel teilen sich weniger als 30 der gefundenen
   Pflicht-Einträge ein Atom mit einem anderen (vorher 37–42 von 61).
3. Die acht übrigen Fälle: in jedem Lauf 71/71 Pflicht-Atome und Feldtreue von
   mindestens 99 %; Regelverstösse im Mittel höchstens 2 (vorher 0) – die Regel
   darf nicht in Aufteilen umschlagen, wo die Fälle einen Redebeitrag als eine
   Aussage meinen.

### Ergebnis

Je drei blinde Läufe über alle elf Fälle mit der geänderten Schablone
(`runs/2026-10-14-koernung-1..3`, `runs/2026-10-14-unabhaengig-koernung-1..3`;
die Prompts liegen jeweils in Lauf 1). Vollständige Vergleiche in
[`runs/2026-10-14-koernung-vergleich.md`](runs/2026-10-14-koernung-vergleich.md) und
[`runs/2026-10-14-unabhaengig-koernung-vergleich.md`](runs/2026-10-14-unabhaengig-koernung-vergleich.md).

| Bedingung | vorher | nachher | erfüllt |
|---|---|---|---|
| 1. Unabhängige Fälle: gefundene Pflicht-Einträge | 170 von 172 in jedem Lauf | 172 von 172 in jedem Lauf | ja |
| 2. Elterninterview: Pflicht-Einträge, die sich ein Atom teilen | 42, 40, 37 von 61 | 12, 6, 10 von 63 (Mittel 9,3) | ja |
| 3. Acht übrige Fälle: Pflicht-Atome · Feldtreue · Regelverstösse | 71/71 · 100 % · 0 | 71/71 · 100 % · 6, 6, 4 (Mittel 5,3) | nein |

Die dritte Bedingung ist verfehlt, die Änderung damit **verworfen**: `evidenz.md`
steht wieder auf dem Stand vor `f2dd14d`. Die Läufe bleiben als Beleg.

Was die Läufe zeigen:

- **Auf langen Redebeiträgen wirkt die Regel wie gewollt.** Im Elterninterview finden alle drei Läufe alle 63 Pflicht-Einträge (vorher je 61), und nur noch 6–12 teilen sich ein Atom (vorher 37–42, alte Schablone 12–26). Die Feldtreue gegen das unabhängige Gold steigt von 96 auf 98 %, fast nur beim `signal`: 50 statt 111 Abweichungen über drei Läufe. Ein Atom mit einer Aussage trägt das Signal dieser Aussage statt eines für mehrere.
- **Sie greift auch dort, wo sie nicht soll.** Im Fall `interview` teilt sie Redebeiträge aus zwei Sätzen, die der Fall als eine Aussage meint (3, 5 und 3 Verstösse) – etwa «Das hat mir die Vermieterin bei der Schlüsselübergabe gesagt.» als eigenes Atom, das ohne den folgenden Satz nichts mehr belegt. «Wechselt das Thema oder den Schritt» liest das Modell schon innerhalb von zwei Sätzen. Weil die Zeile der Schablone für alle Quellenarten gilt, liegen zudem die Befragung in zwei Läufen und die Beschwerde in einem über der Spanne ihres Falls (16 statt höchstens 15 bzw. 14 Atome).
- **Die Zahl der Atome steigt stark:** Elterninterview 91–102 (vorher 41–47, alte Schablone 70–83), Fokusgruppe 115–116 (80–86), Dolmetsch-Interview 57–58 (47). Mehr Atome heissen mehr Prüfaufwand in der Synthese. Den Richtwert «12–25 Atome pro 45-Minuten-Interview» hält bei diesen Transkripten schon die aktuelle Schablone nicht ein.
- **Nicht jeder Verstoss ist ein Fehler.** In `interview-hort` [03:40] trennen zwei Läufe «Den Arbeitsvertrag konnte sie nicht hochladen …» (`breakdown`) von «Sie hat ihn dann ausgedruckt und … abgegeben» (`workaround`) – zwei Signale, die ein Atom nicht beide tragen kann. Die Fallregel «ein Atom je Fundstelle» zählt das als Verstoss. Ob sie dort passt, ist eine Frage an den Testsatz; sie wird nicht nach dem Ergebnis entschieden.

Nächster Kandidat, mit eigenem Kriterium vor dem Lauf: die Regel auf lange
Redebeiträge in Interviews beschränken – kurze Redebeiträge, die eine Sache
erzählen, ausdrücklich ausnehmen und die übrigen Quellenarten nicht berühren.
Dieselben elf Fälle und dieselben drei Bedingungen taugen als Messlatte.

## Messlauf engere Körnungsregel (2026-10-14): übernommen

### Kriterium, vorab festgelegt

Festgelegt und gepusht vor dem ersten Lauf (Commit `afd8ea5`, PR #68), hier
unverändert.

Änderung in `evidenz.md` gegenüber `main`, an denselben zwei Stellen wie im
Messlauf Körnung. Die Regel gilt nur noch für Interviews (Quellenart
`interview`, auch Fokusgruppen), und kurze Redebeiträge sind ausdrücklich
ausgenommen: «Ein kurzer Redebeitrag (bis drei Sätze) bleibt ein Atom, auch wenn
er Ursache und Folge oder Problem und Ausweg nennt; wechselt ein langer
Redebeitrag das Thema oder den Schritt, wird jede Aussage ein eigenes Atom mit
derselben Fundstelle.» Der Teil für lange Redebeiträge ist wörtlich der
verworfene, damit nur die Einschränkung gemessen wird. Der Richtwert «Typisch
12–25 Atome pro 45-Minuten-Interview» bleibt unverändert.

Die Schwelle «bis drei Sätze» ist so gewählt, dass alle Redebeiträge, die der
letzte Messlauf aufgeteilt hat, darunter fallen. Die eigenen Interviewfälle
haben fast nur solche (`interview` 12 von 12, `interview-hort` 30 von 31), die
unabhängigen viele längere (Elterninterview 51 von 86 Redebeiträgen mit vier und
mehr Sätzen, Fokusgruppe 42 von 78, Dolmetsch-Interview 24 von 67). Ob die
Wirkung auf die langen Redebeiträge damit erhalten bleibt, zeigt erst der Lauf.

**Vorher** sind dieselben Läufe wie im Messlauf Körnung
(`2026-10-14-aktuell-1..3`, `2026-10-14-unabhaengig-aktuell-1..3`). **Nachher**
sind je drei blinde Läufe über alle elf Fälle mit der geänderten Schablone.

Die Änderung wird **übernommen**, wenn über die drei Läufe nachher dieselben drei
Bedingungen gelten wie im Messlauf Körnung, sonst wird `evidenz.md`
zurückgesetzt und die Läufe bleiben als Beleg:

1. Unabhängige Fälle: Die gefundenen Pflicht-Einträge nehmen nicht ab (im Mittel
   mindestens 170 von 172).
2. Elterninterview: Im Mittel teilen sich weniger als 30 der gefundenen
   Pflicht-Einträge ein Atom mit einem anderen gefundenen Pflicht-Eintrag
   (Abschnitt «Körnung» in `compare`; vorher 37–42 von 61, verworfene Regel 6–12
   von 63).
3. Die acht übrigen Fälle: in jedem Lauf 71/71 Pflicht-Atome und Feldtreue von
   mindestens 99 %; Regelverstösse im Mittel höchstens 2 (vorher 0, verworfene
   Regel 5,3).

Die Fallregeln bleiben für diesen Messlauf unverändert, auch «ein Atom je
Fundstelle» in `interview-hort`.

### Ergebnis

Je drei blinde Läufe über alle elf Fälle mit der engeren Regel
(`runs/2026-10-14-eng-1..3`, `runs/2026-10-14-unabhaengig-eng-1..3`; die Prompts
liegen jeweils in Lauf 1). Vollständige Vergleiche in
[`runs/2026-10-14-eng-vergleich.md`](runs/2026-10-14-eng-vergleich.md) und
[`runs/2026-10-14-unabhaengig-eng-vergleich.md`](runs/2026-10-14-unabhaengig-eng-vergleich.md)
(dort auch die verworfene Regel zum Vergleich).

| Bedingung | vorher | verworfene Regel | engere Regel | erfüllt |
|---|---|---|---|---|
| 1. Unabhängige Fälle: gefundene Pflicht-Einträge | 170 von 172 | 172 von 172 | 172 von 172 in jedem Lauf | ja |
| 2. Elterninterview: Pflicht-Einträge, die sich ein Atom teilen | 42, 40, 37 von 61 | 12, 6, 10 von 63 | 14, 16, 14 von 63 (Mittel 14,7) | ja |
| 3. Acht übrige Fälle: Pflicht-Atome · Feldtreue · Regelverstösse | 71/71 · 100 % · 0 | 71/71 · 100 % · 5,3 | 71/71 · ≥ 99,6 % · 1, 1, 1 | ja |

Alle drei Bedingungen gelten, die Regel bleibt in `evidenz.md`.

**Abweichung vom festgelegten Stand, offengelegt.** Mit dem Scorer, wie er beim
Festlegen des Kriteriums war, zählt Lauf 1 in den acht Fällen 70/71, und
Bedingung 3 wäre verfehlt. Der fehlende Eintrag ist ein Fehler des Scorers, nicht
der Extraktion: Das Atom «8 von 20 Anfragen … in der Kategorie Unterlagen» nennt
auch «3 Telefon» und die Ticket-Nummer «A-12» und passte damit auch auf
`kanal-telefon` (12 Anrufe). Der Scorer ordnete gierig in Gold-Reihenfolge zu und
gab es diesem früheren Eintrag, obwohl die Extraktion ein eigenes Telefon-Atom
hatte. Korrigiert in PR #69 (`76589fa`): Zuerst ein freies Atom wie bisher, sonst
wird ein besetztes umgehängt, wenn dessen Eintrag ein anderes passendes Atom
bekommt. Die Korrektur entstand nach dem Blick auf dieses Ergebnis. Sie ändert
aber keinen der früher abgelegten Läufe – auch nicht die verworfene Regel – und
ist mit einem Test belegt, der mit dem alten Scorer fehlschlägt.

Was die Läufe zeigen:

- **Die kurzen Redebeiträge bleiben ganz.** `interview` hat in jedem Lauf 9 Atome
  wie vorher (verworfene Regel 12–14), `interview-hort` 18–19 (vorher 18), kein
  Redebeitrag ist aufgeteilt. Befragung und Beschwerde liegen wieder in ihrer
  Spanne. Die drei Verstösse haben mit der Körnung nichts zu tun: einmal eine
  ausdrückliche Emotion im Workshop, zweimal ein Zitat der Beschwerde über zwei
  Briefzeilen, bei dem die Zeilennummer «08» dazwischen den wörtlichen Abgleich
  bricht – eine Grenze des Scorers.
- **Auf langen Redebeiträgen bleibt der grösste Teil der Wirkung.** Alle 63
  Pflicht-Einträge des Elterninterviews in jedem Lauf (vorher je 61), 14–16
  geteilte statt 37–42.
- **Beim `signal` bleibt weniger.** Feldtreue gegen das unabhängige Gold 97 %
  (vorher 96 %, verworfene Regel 98 %): 93 Abweichungen beim `signal` über drei
  Läufe, vorher 111, verworfene Regel 50.
- **Die Zahl der Atome steigt weniger stark:** Elterninterview 87–92 (vorher
  41–47, verworfene Regel 91–102), Fokusgruppe 87–94 (80–86; 115–116),
  Dolmetsch-Interview 50–54 (47; 57–58). Die Ausnahme für kurze Redebeiträge
  wirkt vor allem in der Fokusgruppe, wo viele Beiträge kurz sind.

Offen: Der Richtwert «Typisch 12–25 Atome pro 45-Minuten-Interview» passt zu
keiner der Schablonen mehr – das Elterninterview (etwa 45 Minuten) ergibt 87–92
Atome. Ihn anzupassen ist eine Änderung an `evidenz.md` und braucht einen eigenen
Messlauf.

## Grenzen

- **Über die Abdeckung trennt der Testsatz nicht.** Die acht Fälle aus derselben Hand wie die Schablone löst die aktuelle Schablone fehlerfrei; auch die drei unabhängigen Fälle finden beide Schablonen zu 98–100 %. Autor, Gold und Extraktion sind bisher dasselbe Modell – was ihm entgeht, entgeht allen dreien. Erst reales Material aus der Evaluation (anonymisierte Ausschnitte, Mundart, echte Unordnung) kann zeigen, was eine Extraktion wirklich übersieht.
- **Ein Modell.** Alle Läufe stammen vom selben Modell; ein anderes Modell kann anders streuen. Vor einem Urteil über eine Schablonenänderung mehrere Läufe vergleichen (`compare`).
- **Gold und Schablone stammen aus derselben Hand.** Das Gold prüft, was `evidenz.md` verlangt – nicht, ob das, was `evidenz.md` verlangt, die richtige Methode ist.
- **Der Scorer ist selbst ein Messinstrument.** Zweimal hat erst ein Lauf einen Fehler gezeigt (das Tausendertrennzeichen in «1'236», die Zuordnung in Gold-Reihenfolge). Korrekturen gelten für alle Läufe gleich; die abgelegten Berichte und Vergleiche prüft `tests/test_extraction_eval.py` nach jeder Änderung. Bekannte Grenze: Ein Zitat über zwei Zeilen einer Quelle mit Zeilennummern gilt als nicht wörtlich.
- **Ermessensfragen bleiben offen.** Wo das Gold mehrere Antworten zulässt (z. B. `signal` bei der Nachbarin, Emotion beim Wunsch nach einer Liste), steht das im Gold als Liste erlaubter Werte oder als `"emotion": "any"`.
