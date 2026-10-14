# Anleitung: Gold für eine Extraktion festlegen

Du legst fest, was eine sorgfältige Auswertung aus einem Transkript als
**Evidenz-Atome** herausholen muss. Eine andere Person (oder ein Modell) wird
das Transkript später auswerten; dein Gold dient dazu, deren Ergebnis zu
prüfen. Du kennst deren Anleitung nicht und sollst sie nicht erraten. Urteile
als erfahrene Person aus der Nutzerforschung: Welche Aussagen braucht eine
evidenzbasierte User Journey der Verwaltung – was ist passiert, wer hat was
getan, was hat behindert oder geholfen, was haben die Befragten gefühlt,
gebraucht, gewünscht, wie lange hat etwas gedauert, was hat es gekostet?

## Das Modell der Evidenz-Atome (Auszug)

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
| `text` | Bei `quote` **wörtlich**, auch mit Füllwörtern. Kürzen mit «…» ist erlaubt, Umformulieren nicht. Namen und andere Personendaten im Zitat durch eine Angabe in eckigen Klammern ersetzen («[Name]», «[Ort]») – so bleibt das Zitat nachprüfbar. |
| `locator` | Pflicht bei Primärevidenz: Zeile, Zeitstempel, Seite, Ticket-ID, Zeile oder Spalte im Export |
| `value`, `unit` | Bei `metric` |
| `signal` | `friction` (behindert) · `breakdown` (scheitert oder weicht aus) · `positive` · `need` · `workaround` · `neutral` |
| `emotion_hint` | Nur wenn die Emotion im Text steht. `explicit: true` = ausdrücklich geäussert («ich hatte Angst»), `explicit: false` = aus Ton oder Handlung abgeleitet. Kein `emotion_hint`, wenn beides nicht zutrifft. |
| `contradicts` | IDs von Atomen, denen dieses widerspricht. Typisch: Prozessdokument sagt A, Interview zeigt B. |

## Was du abgibst

Ein JSON-Objekt `{"atoms": [...]}`, ein Eintrag je Aussage, die eine gute
Auswertung finden muss oder finden darf:

```json
{
  "key": "kurzer-sprechender-schluessel",
  "required": true,
  "match": ["wörtlicher Ausschnitt", ["zwei Ausschnitte", "die beide vorkommen müssen"]],
  "kind": ["quote"],
  "class": ["reported"],
  "signal": ["friction"],
  "locator": ["12:34"],
  "emotion": "none",
  "why": "ein Satz, warum die Aussage zählt und warum die Felder so sind"
}
```

- `required`: `true` für Aussagen, die eine sorgfältige Auswertung nicht übersehen darf; `false` für solche, die zählen dürfen, aber nicht müssen. Entscheide nach Inhalt, nicht nach einer Zielzahl.
- `match`: kurze, **wörtliche** Ausschnitte aus dem Transkript (3–7 Wörter, genau so geschrieben wie dort, Gross-/Kleinschreibung egal), die in jedem Atom stehen, das diese Aussage erfasst. Ein Zitat darf später gekürzt sein – nimm deshalb den Kern der Aussage, nicht den Satzanfang. Jeder Eintrag der Liste ist eine Alternative; eine Unterliste heisst «alle diese Ausschnitte». Ergibt sich eine Aussage über mehrere Redebeiträge, gib aus jedem eine Alternative. Wähle Ausschnitte, die nicht auch in anderen Aussagen vorkommen.
- `locator`: Zeitstempel ohne Klammern (`"12:34"`); mehrere, wenn die Aussage mehrere Redebeiträge umfasst – einer davon muss in der Fundstelle stehen.
- `kind`, `class`, `signal`: nur angeben, wenn eindeutig; bei Ermessen eine Liste der vertretbaren Werte; sonst weglassen.
- `emotion`: `none` (kein emotion_hint), `not_explicit` (höchstens ein abgeleiteter, nicht ausdrücklich geäusserter), `explicit_negative` / `explicit_positive` (ausdrücklich geäussert, Vorzeichen), `any` (offen). Weglassen, wenn es keine Rolle spielt.
- Fragen und Zusammenfassungen der interviewenden oder moderierenden Person sind keine Evidenz und kommen nicht ins Gold.

Gib die Datei als gültiges JSON aus, ohne Kommentare.
