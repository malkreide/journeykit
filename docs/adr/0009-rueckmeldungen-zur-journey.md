# ADR-0009: Rückmeldungen zur Journey (Kommentarfunktion)

Datum: 2026-10-28 · Status: angenommen (2026-10-28), Umsetzung von Stufe 1 mit der Evaluation

## Kontext

Die Roadmap führt seit 0.1.0 eine «Kommentarfunktion» für den Viewer
(`docs/konzept.md`, Roadmap 5). Gemeint ist das Review: Eine Journey geht an
Fachstellen, Kreisschulbehörden, Schulleitungen oder die verantwortliche
Stelle, und diese melden zurück, was nicht stimmt, was fehlt und was bei
ihnen anders ist. Heute geschieht das ausserhalb des Werkzeugs, als
Randnotiz im Ausdruck, als E-Mail oder in einer Sitzung. Dabei geht der
Bezug verloren: Welche Aussage ist gemeint, in welcher Version? Die
Rückmeldung muss jemand von Hand in das Modell übertragen, oder sie bleibt
liegen.

Drei Randbedingungen engen die Lösung ein:

1. **Der Viewer sendet nichts** (ADR-0003). Er ist eine einzelne HTML-Datei
   ohne Server, läuft in geschlossenen Verwaltungsnetzen und wird per E-Mail
   oder Ablage weitergegeben. Eine Kommentarfunktion, die Daten an einen
   Dienst schickt, widerspricht dem Grundentscheid.
2. **Das Modell ist die Quelle der Wahrheit** (ADR-0001). Was im Viewer
   kommentiert wird, muss in `journey.json` ankommen können, sonst entsteht
   neben dem Modell eine zweite, unsichtbare Wahrheit.
3. **Rückmeldungen aus der Verwaltung sind Innensicht** (ADR-0002). Eine
   Fachstelle, die schreibt «das stimmt so nicht», spricht nicht als Nutzende. Würde
   ihr Kommentar eine Aussage überschreiben, die auf Beobachtung oder
   Interviews beruht, käme genau der Inside-Out-Bias zurück, gegen den
   JourneyKit gebaut ist. Die Kommentarfunktion ist deshalb kein reines
   Oberflächenthema, sondern berührt die Evidenzlogik.

Dazu kommt der Datenschutz: Rückmeldungen nennen leicht Personen oder
Einzelfälle («wie bei der Familie, die letzte Woche am Schalter war»). Sie gehören nicht in ein
öffentliches Repository und nicht ungeprüft in die Journey.

## Optionen

| Option | Beschreibung | Für | Gegen |
|---|---|---|---|
| A – Keine Funktion, nur Prozess | Review über Ausdruck, E-Mail oder Sitzung; der Skill beschreibt, wie man Rückmeldungen überträgt | kein Code; nichts verlässt den bisherigen Weg | Bezug zur Aussage und zur Version geht verloren; Übertragung von Hand; Rückmeldungen bleiben liegen |
| B – Kommentare nur im Browser | Kommentare im `localStorage` des Viewers | sofort nutzbar, offline | bleiben auf einem Gerät; gehen beim Leeren des Browsers verloren; auf geteilten Arbeitsplätzen für andere lesbar; erreichen das Modell nie |
| **C – Rückmeldedatei** | Der Viewer erfasst Rückmeldungen offline und speichert sie als eigene JSON-Datei (Download, kein Versand). Diese geht auf dem üblichen Weg zurück. `journeykit review` prüft sie und erstellt eine Triage-Liste gegen die aktuelle Journey | bleibt im Rahmen von ADR-0003; Bezug zu Aussage und Version bleibt erhalten; mehrere Rückmeldungen lassen sich zusammenführen; nichts ändert das Modell ohne Entscheid | ein zusätzliches Dateiformat; der Rückweg bleibt E-Mail oder Ablage; keine Echtzeit |
| D – Gemeinsamer Speicher | Kommentare auf einem Server, in Variante B (ADR-0004) oder in einem bestehenden Werkzeug (Notion, SharePoint, Teams) | mehrere Personen sehen sich gegenseitig; Echtzeit | Viewer müsste Daten senden (gegen ADR-0003); setzt ADR-0004 voraus, das erst nach der Evaluation kommt; bei Fremdwerkzeugen landet die Rückmeldung ausserhalb des Modells |
| E – Kommentare in `journey.json` | Feld `comments[]` im Schema, gepflegt von Hand oder per CLI | eine einzige Datei | vermischt Modell und Diskussion; Rückmeldungen mit Personenbezug wandern mit jeder Version mit; Fachleute ohne JSON-Kenntnis können nicht beitragen |

## Vorschlag

**Option C**, in zwei Stufen. Leitsatz: **Eine Rückmeldung ist ein Hinweis
an die Autorschaft, kein Beleg.** Sie ändert die Journey nur über einen
Entscheid, der im Changelog steht. Was sie inhaltlich beiträgt, kommt als
offene Frage oder – wenn dokumentiert – als Evidenz-Atom der Klasse
`assumed` ins Modell, nie als Korrektur einer belegten Aussage.

### Stufe 1: Erfassen und auswerten

**Viewer.** Im Drawer jeder Aussage steht «Rückmeldung geben». Es gibt fünf
Arten, weil jede im Modell zu einem anderen Schritt führt:

| Art (`kind`) | Beschriftung | Was daraus werden kann |
|---|---|---|
| `contradicts` | «Trifft nicht zu» | offene Frage mit Erhebungsmethode; bei belegter Aussage nie eine direkte Änderung |
| `evidence_question` | «Beleg fraglich» | Prüfung des Atoms und seiner Quelle (Transkript, Zuordnung, Klasse) |
| `local_difference` | «Bei uns anders» | Hinweis auf eine Variante, eine weitere Persona oder einen Scope-Ausschluss |
| `addition` | «Ergänzung» | Kandidat für ein Atom `assumed`, sobald eine Quelle dokumentiert ist |
| `question` | «Frage» | Antwort im Review oder offene Frage |

Rückmeldungen bleiben im Speicher der Seite. «Rückmeldungen speichern» lädt
sie als Datei herunter, wie die Heatmap-Exporte (Blob, kein Netzwerk). Wer
die Seite mit ungespeicherten Rückmeldungen schliessen will, wird gewarnt.
Eine Liste im Tab «Prüfung» zeigt die eigenen Rückmeldungen dieser Sitzung.

**Format** (`review.schema.json`, eigenes Schema, nicht Teil von
`journey.schema.json`):

```json
{
  "review_version": "1.0",
  "journey": { "id": "kindergarteneintritt-eltern", "version": "1.0" },
  "reviewer": { "role": "Kreisschulbehörde, Sachbearbeitung Aufnahme" },
  "created": "2026-11-03",
  "comments": [
    {
      "id": "r-1",
      "anchor": {
        "path": "phases[0].steps[0].pain_points[1]",
        "step_id": "brief-erhalten",
        "pain_point_id": "pp-brief-nicht-verstanden",
        "text": "Der Brief wird sprachlich nicht verstanden (Verwaltungsbegriffe, nur Deutsch)."
      },
      "kind": "local_difference",
      "text": "Seit dem Frühling verschicken wir den Brief zusätzlich in zwölf Sprachen."
    }
  ]
}
```

- **Anker**: Pfad der Aussage wie in `model.Claim.path`, dazu die stabilen IDs,
  die es gibt (Schritt, Pain Point, Chance, Atom), und eine Kopie des Texts.
  Gedanken, Gefühle, Edge Cases und Recovery-Pfade haben keine eigene ID; ihr
  Pfad verschiebt sich zwischen Versionen. Die Textkopie macht sichtbar,
  wenn die Aussage inzwischen geändert wurde.
- **Rolle statt Name**, wie bei `meta.owner`. Der Viewer weist beim
  Speichern darauf hin, keine Personen oder Einzelfälle zu nennen.
- **Eigene Datei**, weil Rückmeldungen Diskussion sind, nicht Modell, und weil
  sie Personenbezug haben können. Rückmeldedateien realer Journeys gehören
  nicht ins Repository; für Tests gibt es eine synthetische.

**CLI.** `journeykit review journey.json rueckmeldung-*.json` prüft jede
Datei gegen `review.schema.json` und die Journey und gibt eine Triage-Liste
aus (Markdown, de/fr):

- je Aussage alle Rückmeldungen, nach Art gruppiert, mit Rolle;
- markiert, wenn die Rückmeldung für eine andere Version geschrieben wurde,
  wenn der Anker nicht mehr gefunden wird oder wenn sich der Text der
  Aussage geändert hat;
- markiert `contradicts` an Aussagen mit Primärevidenz ausdrücklich: Hier
  steht Innensicht gegen Nutzerevidenz, der Weg ist eine Erhebung, keine
  Korrektur;
- je Rückmeldung ein Vorschlag für den Modellschritt (offene Frage mit
  `step_ref`, Atom-Kandidat, Scope-Ausschluss) als JSON-Ausschnitt zum
  Übernehmen.

`journeykit review` ändert die Journey nicht. Übernehmen bleibt ein
bewusster Schritt mit Changelog-Eintrag.

### Stufe 2: Rückmeldungen anderer im Viewer zeigen

Der Viewer liest Rückmeldedateien über einen Dateidialog ein (FileReader,
kein Netzwerk) und zeigt sie an den Aussagen. So sieht eine Arbeitsgruppe vor
der Sitzung, was andere angemerkt haben. Erst umsetzen, wenn Stufe 1 in
einer echten Review-Runde benutzt wurde.

## Folgen

Nach den Konventionen in `CLAUDE.md`:

- **Schema**: neue Datei `src/journeykit/schema/review.schema.json` mit
  `additionalProperties: false`. `journey.schema.json` und `schema_version`
  bleiben unverändert.
- **`model.py`**: Auflösung eines Ankers auf eine Aussage
  (`JourneyIndex.claim_at(anchor)`), über IDs vor Pfad, mit Textvergleich.
- **CLI**: Befehl `review`, Texte in `cli_texts.py` und – für die Triage-Liste –
  in `export_texts.py` (de, fr). Keine neue Abhängigkeit.
- **Viewer**: Knopf im Drawer, Formular, Liste im Tab «Prüfung», Download,
  Warnung beim Schliessen; alle Texte in `jk-i18n` (de, fr). Kein
  `localStorage` in Stufe 1 (siehe «Entscheid»). Weiterhin keine
  Netzwerkanfrage; der bestehende Test auf externe Verweise deckt das ab.
- **Lints**: keine neue Regel. Rückmeldungen sind kein Teil des Modells;
  Befunde über sie gehören in die Triage-Liste, nicht in `journeykit lint`.
- **Skill**: `references/review-fragen.md` erhält einen Abschnitt «Rückmeldungen
  übernehmen» mit dem Leitsatz und der Tabelle oben; `SKILL.md` verweist im
  Review-Schritt darauf.
- **Beispiele**: eine synthetische Rückmeldedatei zum Kindergarteneintritt
  für Tests und Dokumentation, mit mindestens einem `contradicts` an einer
  belegten Aussage.
- **Tests**, **`docs/konzept.md`** (Schicht 5 und Roadmap), **beide READMEs**,
  **`CHANGELOG.md`**.

## Entscheid

Angenommen am 2026-10-28 wie vorgeschlagen (Option C, Stufe 1 und 2 wie
beschrieben). Die vier Punkte, die der Vorschlag offen liess, sind nach den
Empfehlungen entschieden:

- **Keine Entwürfe im Browser** in Stufe 1. Rückmeldungen bleiben im
  Speicher der Seite; die Warnung beim Schliessen schützt vor Verlust. Nach
  der ersten Review-Runde wird neu beurteilt, ob Entwürfe verloren gingen.
- **Nur Rolle und Einheit**, kein Name. Rückfragen laufen über den Weg, auf
  dem die Datei kam.
- **Kein `journeykit review --apply`.** Übernommen wird von Hand mit den
  JSON-Ausschnitten der Triage-Liste und mit Changelog-Eintrag. Nach der
  ersten Review-Runde wird geprüft, ob das genügt.
- **Keine Diskussionsfäden** in Dateien. Sie gehören zu einem gemeinsamen
  Speicher (Option D) und damit zu ADR-0004.

**Zeitpunkt**: Stufe 1 wird zusammen mit der Evaluation umgesetzt
(`docs/konzept.md`, Roadmap 2), nicht vorher. Die reale Ground-Truth-Journey
geht ins Review und ist die erste Runde, in der die Rückmeldedatei benutzt
wird. Stufe 2 folgt erst, wenn diese Runde gezeigt hat, dass Stufe 1 trägt.

## Nach der ersten Review-Runde zu prüfen

- Reichen die fünf Arten, oder fehlt eine (etwa «veraltet»)?
- Wie viele Rückmeldungen stellen Innensicht gegen Nutzerevidenz, und führte
  die Markierung in der Triage-Liste zu Erhebungen statt Korrekturen?
- Gingen Rückmeldungen verloren, weil der Browser keine Entwürfe sichert?
- Genügen die JSON-Ausschnitte, oder kostet die Übernahme so viel, dass ein
  `--apply` mit Vorschau gerechtfertigt ist?

## Voraussetzung

Keine technische. Stufe 1 wird mit der Evaluation (`docs/konzept.md`,
Roadmap 2) umgesetzt und erprobt (siehe «Entscheid»): Die reale Ground-Truth-Journey
geht ohnehin ins Review, und erst diese Runde zeigt, ob die fünf Arten
reichen und wie viele Rückmeldungen Innensicht gegen Nutzerevidenz stellen.
ADR-0004 (Variante B) bleibt unabhängig; kommt es, kann es dasselbe Format
zentral speichern.
