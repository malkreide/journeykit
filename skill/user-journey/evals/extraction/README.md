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
das an den Werkzeugaufrufen der 48 Subagenten geprüft: je ein Read (das eigene
Bundle) und ein Write (die eigene Antwort), sonst nichts.

## Was gemessen wird

- **Pflicht-Atome gefunden** – Anteil der Gold-Atome, für die die Extraktion ein passendes Atom hat. Ein umformuliertes Zitat zählt nicht als Treffer.
- **Feldtreue** – bei den gefundenen Atomen: `kind`, `class`, `signal`, Fundstelle, Emotion, `value`, `unit` (eine Schreibweise oder eine Liste gleichwertiger, z. B. «CHF» oder «Franken pro Betreuungstag»), `contradicts` und `text_has` (Angaben, die im `text` stehen müssen, etwa n einer Befragung), soweit das Gold sie vorgibt.
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

## Grenzen

- **Die aktuelle Schablone schöpft den Testsatz aus.** Auch die drei schwierigeren Fälle löst sie in drei von drei Läufen fehlerfrei. Der Testsatz erkennt damit Rückschritte, aber keine weitere Verbesserung. Über die Abdeckung trennt er gar nicht: Synthetische Fälle aus derselben Hand wie die Schablone machen die Pflicht-Atome offenbar zu gut sichtbar. Mehr trennen würde Material, das nicht für den Test geschrieben ist – anonymisierte Ausschnitte aus der Evaluation mit realer Ground Truth, lange Transkripte mit mehreren Sprechenden, Mundart in der Transkription, Aussagen, die sich erst über mehrere Redebeiträge ergeben.
- **Ein Modell.** Alle Läufe stammen vom selben Modell; ein anderes Modell kann anders streuen. Vor einem Urteil über eine Schablonenänderung mehrere Läufe vergleichen (`compare`).
- **Gold und Schablone stammen aus derselben Hand.** Das Gold prüft, was `evidenz.md` verlangt – nicht, ob das, was `evidenz.md` verlangt, die richtige Methode ist.
- **Ermessensfragen bleiben offen.** Wo das Gold mehrere Antworten zulässt (z. B. `signal` bei der Nachbarin, Emotion beim Wunsch nach einer Liste), steht das im Gold als Liste erlaubter Werte oder als `"emotion": "any"`.
