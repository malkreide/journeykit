# Evidenz: Klassen, Atome, Extraktion

Das Evidenz-Atom ist die kleinste belegbare Einheit. Alles, was die Journey
behauptet – ein Gedanke, ein Gefühl, ein Pain Point, eine Chance – zeigt per
`evidence_refs` auf Atome. Ein Feld ohne Referenz ist erlaubt, aber eine
Annahme, und der Viewer zeichnet es so.

## Evidenzklassen

| Klasse | Bedeutung | Typische Quellen |
|---|---|---|
| `observed` | Direkt beobachtet oder gemessen. Was Menschen **tun**. | Analytics, Anfragen- und Ticketexporte, Beobachtung vor Ort, Formularstatistiken |
| `reported` | Von Nutzenden **berichtet**. Was Menschen sagen, dass sie tun oder fühlen. | Interviews, Befragungen, Tagebuchstudien, Beschwerden, Rückmeldungen |
| `assumed` | Interne **Annahme**. Was die Organisation glaubt. | Prozessdokumente, Soll-Beschreibungen, Workshops ohne Nutzende, Erfahrungswissen |

`observed` und `reported` sind **Primärevidenz**. Eine Aussage ohne
Primärevidenz gilt als Annahme, auch wenn drei Prozessdokumente sie stützen.

Grenzfälle:

- Ein Mitarbeitender am Schalter berichtet, was Eltern fragen → `reported`,
  Quelle `kind: observation` oder `interview` mit `participants: Schaltermitarbeitende`. Kennzeichnen, dass es die Wahrnehmung der Verwaltung ist.
- Workshop **mit** Nutzenden → Aussagen der Nutzenden sind `reported`, Aussagen des Teams `assumed`. Zwei Quellen anlegen.
- Befragung mit Freitext → Aggregate als `metric`, einzelne Freitextantworten als `quote`, beides `reported`.

## Atom-Schema (Kurzform)

```json
{
  "id": "e1-07",
  "source_ref": "int-e1",
  "class": "reported",
  "kind": "quote",
  "text": "Ich hatte das Gefühl, alle anderen wissen Bescheid und ich nicht.",
  "locator": "Zeile 13",
  "signal": "friction",
  "phase_hint": "information",
  "persona_hint": "zugezogen",
  "channel_hint": "web",
  "emotion_hint": { "valence": -1, "label": "ausgeschlossen", "explicit": true },
  "tags": ["orientierung"],
  "contradicts": ["doc-01"]
}
```

| Feld | Regel |
|---|---|
| `id` | sprechend und stabil: Quellkürzel plus Laufnummer (`e1-07`, `anf-12`, `bef-03`, `web-02`, `doc-01`, `ws-04`) |
| `kind` | `quote` wörtlich · `observation` beschreibend (Export-Zeile, Beobachtung) · `metric` Zahl · `document_excerpt` Dokumentstelle · `workshop_statement` Team-Aussage |
| `text` | Bei `quote` **wörtlich**, auch mit Füllwörtern. Kürzen mit «…» ist erlaubt, Umformulieren nicht. |
| `locator` | Pflicht bei Primärevidenz: Zeile, Zeitstempel, Seite, Ticket-ID, Zeile oder Spalte im Export |
| `value`, `unit` | Bei `metric` |
| `signal` | `friction` (behindert) · `breakdown` (scheitert oder weicht aus) · `positive` · `need` · `workaround` · `neutral` |
| `emotion_hint` | Nur wenn die Emotion im Text steht. `explicit: true` = ausdrücklich geäussert («ich hatte Angst»), `explicit: false` = aus Ton oder Handlung abgeleitet. Kein `emotion_hint`, wenn beides nicht zutrifft. |
| `contradicts` | IDs von Atomen, denen dieses widerspricht. Typisch: Prozessdokument sagt A, Interview zeigt B. |

## Extraktionsregeln je Quellentyp

**Interview-Transkripte.** Durchgang pro Transkript. Ein Atom pro belegbarer
Aussage, nicht pro Satz. Zitate wörtlich. Emotionen nur mit Beleg im Text.
Typisch 12–25 Atome pro 45-Minuten-Interview. Fragen der interviewenden Person
sind keine Evidenz.

**Anfragen-, Ticket-, Beschwerdeexporte.** Erst kategorisieren (Kategorie ×
Kanal × Zeitraum), dann **Metriken** als Atome («17 von 30 Anfragen per
Telefon»), dazu 3–6 typische Einzelfälle als `observation` mit Ticket-ID.
Nicht jede Zeile ein Atom. Häufungen sind Breakdown-Kandidaten: Wo Menschen
anrufen, hat ein anderer Kanal versagt.

**Befragungen.** Aggregate als `metric` mit n und Fragewortlaut im `text`.
Freitextantworten als `quote`, wenn sie etwas zeigen, das die Zahlen nicht
zeigen. Zustimmungswerte unter 60 % sind Reibungskandidaten.

**Analytics.** Ausstiegsraten, Verweildauern, Suchbegriffe als `metric`,
Seite als `locator`. Analytics zeigt **wo**, nie **warum** – immer mit
berichteter Evidenz paaren.

**Prozessdokumente, Soll-Beschreibungen.** Klasse `assumed`. Wertvoll als
Vergleichsfolie: Jede Soll-Aussage, der ein Interview widerspricht, ist ein
Befund. `contradicts` setzen.

**Workshop-Notizen (ohne Nutzende).** Klasse `assumed`, `kind:
workshop_statement`. Hypothesen, die später bestätigt oder widerlegt werden.

**Fotos von Workshop-Wänden, Miro-Boards.** Haftnotizen transkribieren,
Autorenschaft klären (Team oder Nutzende?), dann wie oben.

## Prompt-Schablone für die Extraktion

Für einen Durchgang pro Quelle, mit der Datei im Kontext:

```
Du extrahierst Evidenz-Atome aus der Quelle «{title}» ({kind}, Klasse {class}).
Regeln:
- Ein Atom pro belegbarer Aussage. Zitate wörtlich, mit Fundstelle (Zeile/Zeitstempel/ID).
- emotion_hint nur, wenn die Emotion im Text steht; explicit true nur bei ausdrücklicher Nennung.
- signal setzen; breakdown nur, wenn die Person scheitert oder ausweicht (Anruf, Schalter, Aufgeben).
- phase_hint aus dieser Liste: {phasen}. persona_hint: {persona}.
- Keine Personendaten im text (Namen, Orte, Kontaktangaben ersetzen).
- Widerspricht eine Aussage einer bekannten Soll-Aussage, contradicts setzen: {bekannte_atome}.
Gib ausschliesslich ein JSON-Array von Atomen nach journeykit-Schema aus, IDs mit Präfix «{prefix}-».
```

Nach jedem Durchgang: Atome zählen, Signale zählen, Phasenverteilung
anschauen. Phasen ohne Atome sind Lücken, keine ruhigen Phasen.

## Synthese-Regeln

- **Clustern nach Handlung, nicht nach Quelle.** Ein Schritt bündelt Atome aus Interview, Export und Analytics, die dieselbe Handlung betreffen.
- **Gefühlskurve nur aus Atomen mit `emotion_hint`.** Mehrere Atome pro Schritt: den geäusserten Wert nehmen, nicht den Mittelwert über Personen – bei Streuung den Konflikt als Edge Case oder zweite Persona festhalten.
- **Breakdown vs. Reibung.** Reibung: behindert, die Person kommt weiter. Breakdown: die Person scheitert, bricht ab oder weicht aus. Der `workaround` beschreibt das Ausweichen.
- **Widersprüche ausweisen.** Als Edge Case («Soll-Prozess geht davon aus, dass …, Interviews zeigen …») oder als offene Frage – nie durch Weglassen einer Seite auflösen.
- **Lücken benennen.** Schritte ohne Primärevidenz bleiben in der Journey, aber mit leeren `evidence_refs` und einer `open_question`.
- **Nicht eingeordnete Atome** bleiben stehen. Lint L100 listet sie; sie sind der Rohstoff für die nächste Version oder eine andere Persona.

## Qualitätsmasse, die der Viewer zeigt

- Anteil Erlebnis-Aussagen (Denken, Fühlen, Pain Points) mit Primärevidenz – unter 50 % ist Inside-Out.
- Evidenz-Heatmap: Primärbelege je Dimension und Schritt.
- Gestrichelte Kurvenpunkte: Emotionen ohne Primärbeleg.
- Filter «nur Primärevidenz»: Was danach übrig bleibt, ist die belegte Journey.
