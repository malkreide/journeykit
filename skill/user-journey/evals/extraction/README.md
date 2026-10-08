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

Je Fall:

- `input.*` – die Quelle,
- `case.json` – Werte für die Schablone (Titel, Art, Klasse, `source_id`, Präfix, Phasen, Persona, bekannte Atome) und die Regeln des Falls (Anzahl, erlaubte Arten, Fundstelle, verbotene Textstellen, Personendaten),
- `expected.json` – das **Gold**: Pflicht-Atome als Textbausteine (bei Messwerten mit Wert) und die Felder, die sie haben müssen,
- `reference.json` – eine von Hand erstellte korrekte Extraktion. Sie muss die volle Punktzahl ohne Regelverstoss erreichen (`tests/test_extraction_eval.py`).

## Ablauf

```bash
python scripts/eval_extraction.py prompts -o /tmp/prompts
# Je Fall den Prompt zusammen mit references/evidenz.md an ein Modell geben,
# die Antwort (JSON-Array) als /tmp/antworten/<fall>.json speichern.
python scripts/eval_extraction.py score /tmp/antworten -o bericht.md
```

Das Modell darf weder `expected.json` noch `reference.json` sehen. Die Läufe
unten wurden so gemacht: je Fall ein frischer Subagent, der nur eine Datei mit
`evidenz.md` und dem gefüllten Prompt lesen durfte.

## Was gemessen wird

- **Pflicht-Atome gefunden** – Anteil der Gold-Atome, für die die Extraktion ein passendes Atom hat. Ein umformuliertes Zitat zählt nicht als Treffer.
- **Feldtreue** – bei den gefundenen Atomen: `kind`, `class`, `signal`, Fundstelle, Emotion, `value`, `unit`, `contradicts`, soweit das Gold sie vorgibt.
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

## Grenzen

- **Zu leicht für Abdeckung und Feldtreue.** Beide Läufe finden alle Pflicht-Atome und setzen alle geprüften Felder richtig; unterschieden haben sich die Läufe nur bei den Regeln. Längeres, widersprüchlicheres Material – am besten anonymisierte Ausschnitte aus der Evaluation mit realer Ground Truth – würde mehr trennen.
- **Ein Lauf je Schablone, ein Modell.** Extraktionen streuen; vor einem Urteil über eine Schablonenänderung mehrere Läufe vergleichen.
- **Gold und Schablone stammen aus derselben Hand.** Das Gold prüft, was `evidenz.md` verlangt – nicht, ob das, was `evidenz.md` verlangt, die richtige Methode ist.
- **Ermessensfragen bleiben offen.** Wo das Gold mehrere Antworten zulässt (z. B. `signal` bei der Nachbarin, Emotion beim Wunsch nach einer Liste), steht das im Gold als Liste erlaubter Werte oder als `"emotion": "any"`.
