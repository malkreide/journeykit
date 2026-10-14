# Beispiel: Anmeldung an der Musikschule aus Elternsicht

Drittes durchgerechnetes Beispiel für JourneyKit, nach dem Kindergarteneintritt und der Baubewilligung. Es prüft die **Übertragbarkeit** auf eine Leistung zwischen Verwaltung und Verein: eine Musikschule mit Leistungsvereinbarung, Tarifen der Gemeinde, Ermässigung bei einer zweiten Stelle und Instrumenten aus dem Fachgeschäft. Gewählt wurde der Bereich, weil er viele Kanal- und Stellenwechsel hat. Alle vier Breakdowns liegen an einem solchen Wechsel. Der eigentliche Ertrag sind die [Übertragbarkeitsbefunde](#übertragbarkeitsbefunde), vor allem zu Kosten (#15) und vermeidbaren Schritten (#49). Für beide stand der Entscheid über ein Schemafeld aus, «bis ein drittes Beispiel es braucht».

> **Synthetisch.** Alle Inputs, Zahlen, Tarife, Zitate und Personen (M1, M2, M3) sind erfunden. Der Ablauf ist **vereinfacht** und **kein Abbild einer realen Musikschule oder Gemeinde**. Die Organisation heisst deshalb «Musikschule Musterau und Gemeinde Musterau, Abteilung Bildung (fiktives Beispiel)», und `meta.synthetic` ist `true`. Fachlich hat niemand aus einer Musikschule das Beispiel geprüft.

> **Kein Beleg für die Synthese-Qualität.** Rohmaterial und Journey stammen aus derselben Hand. Das Beispiel prüft, ob das **Modell** einen weiteren Bereich tragen kann – nicht, ob die Pipeline aus fremdem Material eine gute Journey macht. Dafür ist die Evaluation gegen eine reale Ground Truth da (Roadmap, `docs/konzept.md`).

## Szenario

Ein Kind kommt vom Instrumentenparcours an der Schule heim und will ein Instrument lernen. Die Eltern klären die Kosten, melden bis 31. März online an und erhalten im Mai eine Zusage oder einen Bescheid «Warteliste». Ein Platzangebot müssen sie innert zehn Tagen im Portal annehmen. Danach beantragen sie bei der Gemeinde die Tarifermässigung (Papier, Steuerveranlagung), machen mit der Lehrperson über einen Messenger die Unterrichtszeit ab und mieten ein Instrument im Musikgeschäft. Im September kommt die erste Rechnung. Gegen Ende des ersten Jahres entscheiden sie, ob das Kind weiterspielt. Abmelden müssen sie schriftlich beim Sekretariat bis 31. Mai – nicht bei der Lehrperson.

Diagnose: **User Journey**. Erwogen wurden ein Service Blueprint «Ermässigung und Fakturierung» (zeigt die Übergabe Gemeinde → Musikschule, nicht aber, warum Eltern zweimal anrufen) und eine Customer Journey: Die Musikschule ist ein Verein mit Vertrag und Kündigungsfrist, Tarife und Ermässigung regelt aber die Gemeinde. Die Persona sind die Eltern; das Kind ist die begünstigte Person (siehe H12).

## Dateien

| Datei | Inhalt |
|---|---|
| `journey.json` | Persona «Eltern bei der ersten Anmeldung», Version 1.0, Status `validated`. 6 Phasen, 15 Schritte, 15 Pain Points (4 Breakdowns), 6 Chancen, 140 Evidenz-Atome, 10 Quellen. |
| `journey.html` | Gerenderter Viewer. |
| `input/` | Das synthetische Rohmaterial, siehe unten. |

Eine zweite Persona gibt es bewusst nicht: Die Befunde betreffen das Modell, nicht den Vergleich von Personas, und den hat die Baubewilligung schon geprüft.

## Input → Quelle → Evidenzklasse

| Input | `sources[].id` | `kind` | `default_class` | `pii_status` | n | Atom-IDs |
|---|---|---|---|---|---|---|
| `input/interview-m1.md` – Mutter, Klavier, 13 Monate Warteliste, Platzangebot verpasst | `int-m1` | interview | reported | anonymised | 1 | `m1-*` |
| `input/interview-m2.md` – Vater, Cello, Tarifermässigung, volle Rechnung | `int-m2` | interview | reported | anonymised | 1 | `m2-*` |
| `input/interview-m3.md` – Mutter, Gitarre, Abmeldung über die Lehrperson | `int-m3` | interview | reported | anonymised | 1 | `m3-*` |
| `input/anfragen-export.csv` – 30 Anfragen an das Sekretariat, mit Kategorie | `anfragen` | inquiry_log | observed | anonymised | 30 | `anf-*` |
| `input/musikschul-statistik.csv` – Kennzahlen der Musikschulverwaltung | `statistik` | case_records | observed | none | 412 | `stat-*` |
| `input/elternbefragung.csv` – 9 Fragen, u. a. «Kosten vorab bekannt» | `befragung` | survey | reported | anonymised | 318 | `bef-*` |
| `input/webanalytics.csv` – 6 Seiten von Musikschule und Gemeinde | `analytics` | analytics | observed | none | – | `web-*` |
| `input/tarifordnung-auszug.md` – öffentlicher Erlass (Soll) | `tarife` | **internal_document** | **assumed** | none | – | `tar-*` |
| `input/prozess-anmeldung-intern.md` – Soll-Prozess, Innensicht | `prozessdok` | internal_document | **assumed** | none | – | `doc-*` |
| `input/workshop-notizen.md` – Hypothesen-Workshop ohne Eltern | `workshop` | workshop | **assumed** | none | 6 | `ws-*` |

Die Fundstellen (`Zeile N`, `anfrage_id MS-0xx`, `Spalte kategorie = …`) und die Zählwerte aus dem Anfragen-Export wurden aus den Dateien berechnet, nicht von Hand gesetzt. `tests/test_examples.py` prüft, dass jedes Zitat wörtlich in seiner Datei steht.

## Was das Beispiel zeigt

- **Breakdowns an Kanal- und Stellenwechseln**: Bescheid «Warteliste» ohne Stand (Web → E-Mail), Platzangebot in den Ferien verfallen (Telefon → E-Mail, Frist), volle Rechnung trotz Ermässigung (Übergabe Gemeinde → Musikschule, Brief), Abmeldung bei der Lehrperson ungültig (Messenger statt Brief, Formvorschrift). Jeder Breakdown hat einen Recovery-Pfad; drei haben zusätzlich einen Soll-Pfad (`exists: false`).
- **Kosten am Schritt** (`step.costs[]`, ADR-0007): Schulgeld pro Semester mit Spanne bei Ermässigung und Einschreibegebühr bei «Rechnung prüfen», Cello-Miete pro Monat beim Musikgeschäft oder ein gekauftes Digitalpiano bei «Instrument mieten oder kaufen», Folgekosten der verpassten Abmeldung bei «Nicht abgemeldetes Semester bezahlen». Keine Summe – Miete und Kauf sind Alternativen, die Folgekosten bedingt. Ob die Kosten vorher bekannt waren, zeigen Pain Points und die Kennzahlen der Phase «Ein Instrument finden».
- **Vermeidbare Kontakte und Folgen** (`pain_point.caused_by`, ADR-0008): Nachfrage zur Warteliste ← Bescheid ohne Stand (Schritt direkt davor); Nachfrage zur Rechnung ← volle Rechnung ← keine Bestätigung beim Ermässigungsantrag (eine Phase früher, andere Stelle, Ursache Back-Stage); bezahltes Semester ← ungültige Abmeldung (Folgekosten). Kennzahl «Anteil vermeidbarer Kontakte» 43 %.
- **Widersprüche ausgewiesen**: Soll «Bestätigung informiert über Tarife» (`doc-02`) gegen die Einschreibegebühr als Überraschung; Soll «halbjährlich über den Stand informiert» (`doc-03`) gegen M1 und `anf-14`; Soll «Gemeinde meldet bis 15. August» (`doc-07`) gegen 38 % nachträgliche Gutschriften; Soll «Schul-App» (`doc-06`) gegen den Messenger; Soll «Lehrpersonen weisen auf die Abmeldung hin» (`doc-09`) gegen M3 und 41 % (`stat-15`). Vier von fünf Workshop-Annahmen sind widerlegt. Eine ist bestätigt: Die Lehrpersonen stimmen die Unterrichtszeit gut ab (`ws-03`, 81 % Zustimmung).
- **Ehrliche Lücken**: Zwei Schritte haben `feeling: null`. Wie viele Familien wegen der Kosten gar nicht anmelden, zeigt das Material nicht; das steht als offene Frage in der Journey, ebenso das Erleben des Kindes.
- **Lint-Ergebnis** ohne angepasste Schwellen: 0 Fehler · 0 Warnungen · 19 Hinweise (L043, L100, L101). Vorgeschlagenes Urteil im Audit-Bericht: belastbar.

## Übertragbarkeitsbefunde

Die Hypothesen H8–H15 wurden **vor** dem Schreiben des Materials festgehalten; die Nummern setzen H1–H7 der Baubewilligung fort. Ergebnis je Hypothese: **passt**, **Workaround** (Modell trägt mit Abstrichen) oder **Lücke** (Vorschlag für ein Feld, mit ADR). Schema und Lints wurden für dieses Beispiel **nicht** verändert.

| # | Hypothese | Ergebnis | Was im Beispiel passiert ist | Vorschlag |
|---|---|---|---|---|
| H8 | Kosten, die wiederkehren, ermässigt werden, an Dritte gehen oder aus einem Breakdown folgen, trägt das Muster aus #15 nicht mehr | **Lücke → umgesetzt** | Jede einzelne Zahl trägt: 10 Atome in CHF, am Schritt verknüpft. Die Frage der Persona – «Was kostet uns das erste Jahr?» – beantwortet das Modell nicht. Die Einheiten sind Freitext (`CHF`, `CHF pro Semester`, `CHF pro Monat`), 820 Franken kommen viermal vor (Tarif als Soll, unverstandener Tarif, Rechnung, Folgekosten). Die Ermässigung ist ein Prozentsatz, kein Betrag. Wem bezahlt wird (Musikschule, Musikgeschäft), steht nur im Text. «Vorher bekannt» lässt sich belegen, aber als Befragungswert je Kostenart (Schulgeld 46 %, Ermässigung 31 %, Instrument 52 %), nicht als Ja/Nein je Betrag. | Optionales Feld `step.costs[]` mit Betrag, Spanne, Periode, Empfänger und Pflichtbeleg; im Viewer eine Zeile «Kosten», ohne Summe. `known_in_advance` **nicht** als Feld, sondern als Kennzahl je Kostenart (steht schon in `references/kpi-uebersetzung.md`). Umgesetzt mit [ADR-0007](../../docs/adr/0007-kosten-am-schritt.md) ([#15](https://github.com/malkreide/journeykit/issues/15), Stufe 2): fünf Einträge in drei Schritten, Lints L004 und L103. |
| H9 | Vermeidbare Schritte: Die Ursache liegt nicht immer direkt davor | **Workaround → umgesetzt** | Zwei vermeidbare Kontakte. Warteliste: Die Ursache steht direkt davor (`pp-warteliste-ohne-stand` → `pp-nachfrage-warteliste-vermeidbar`), das Muster passt. Rechnung: Die Nachfrage folgt auf die volle Rechnung (Breakdown dort, wo er sichtbar wird). Deren Ursache liegt vier Schritte und eine Phase früher bei einer anderen Stelle, Back-Stage. Die Kette steht nur im Text und in einer `backstage_notes`-Zeile. Weil diese keine `evidence_refs` kennt, stehen die Atom-IDs im Text. Indirekt verbindet die Chance Ursache (`step_ref`) und Folgen (`linked_pain_points`). Dieselbe Form hat die Kette ungültige Abmeldung → bezahltes Semester. Die Kennzahl «Anteil vermeidbarer Kontakte» (43 %) beruht auf einer Einordnung der Kategorien durch die Autorschaft. | Statt `step.avoidable` (#49, Option b) ein optionales `pain_point.caused_by` mit den IDs früherer Pain Points. Das deckt vermeidbare Kontakte und Folgekosten ab, auch über Phasen und Stellen hinweg; dieses Beispiel hat vier Verbindungen. Umgesetzt mit [ADR-0008](../../docs/adr/0008-ursachen-von-pain-points.md): vier Verbindungen im Beispiel; Lints L001 (unbekannte Ursache), L005 (Ursache nach der Folge) und L065 (Chance nur bei Folgen); im Viewer «Folge von ‹Schritt›». Offen bleibt, ob eine Chance an der Ursache L061 für deren Folgen erfüllt. |
| H10 | Fristen, die die Persona einhalten muss, kennt das Modell nur als Text | **Workaround** | Zwei der vier Breakdowns hängen an einer Frist der Persona: Annahme innert zehn Tagen und Abmeldung bis 31. Mai; dazu kommt die Antragsfrist der Ermässigung. Anders als die Behördenfrist in H2 ist das kein Soll, das einer Dauer widerspricht, sondern eine Bedingung mit Folgen (Platz weg, 820 Franken). Abgebildet als `document_excerpt` (`doc-04`, `tar-04`, `tar-06`), Tag `frist` und Pain Point. Kein Lint sieht eine Frist ohne Erinnerung, der Viewer kann sie nicht auf der Zeitachse zeigen. | Zuerst ein Muster im Skill, wie bei den Kosten in Stufe 1: Frist als `document_excerpt` am Schritt, Pain Point, wenn sie verpasst wird, Kennzahl «Anteil fristgerecht» (in `kpi-uebersetzung.md` als Pendant zur Activation Rate). Dazu die Review-Frage «Welche Frist muss die Persona einhalten – und wer erinnert sie?». Ein Feld erst mit einem weiteren Beispiel. |
| H11 | Warteliste: Wartephase mit unbekanntem Ende, Dauer je Instrument | **passt mit Abstrichen** | `duration_days` trägt: typisch 213 Tage, Spanne 30–486, `basis` nennt Grundgesamtheit und Umrechnung. Die Phase betrifft aber nur 47 % der Kinder. Das steht in `description` und `basis`, der Viewer zeichnet den Balken jedoch, als warteten alle. Die Spanne besteht aus Medianen je Instrument, nicht aus einer Verteilung. Nach `references/diagnose.md` («pro Variante eine Datei») wäre der Weg mit Warteliste eine eigene Datei – eine Kopie von 13 der 15 Schritte, die sich nur in einer Phase unterscheidet. | Regel in `diagnose.md` präzisieren: Eine Variante, die nur eine Phase einschiebt (Warteliste, Rückweisung mit Nachreichen), bleibt in der Datei, und der Anteil steht in `description`. Ein Feld für den Anteil erst, wenn der Viewer Pfadvarianten zeigen soll. |
| H12 | Die begünstigte Person (Kind) ist nicht die handelnde (Eltern) | **passt; Gefühlskurve braucht eine Regel** | Die Eltern als Persona sind richtig. Gegenprobe am Modell (nicht im Repo): Mit dem Kind als Persona führen in 12 von 15 Schritten Dritte aus, L073 meldet es und verweist auf die Diagnose. `performed_by` passt nicht auf das Kind: Es handelt nicht anstelle der Eltern. Seine Gefühle kommen nur aus zweiter Hand («Sie war so enttäuscht …», `m1-10`). `emotion_hint` kennt kein «wessen»: Ausdrücklich ist die Emotion des Kindes, für die Eltern bleibt sie abgeleitet (`explicit: false`), und das Label des Punkts mischt beides. | Kein Feld. Regel im Skill: `emotion_hint` nur für die Persona, Gefühle der begünstigten Person als Tag (hier `gefuehl-kind`) oder Edge Case. Review-Frage «Wessen Gefühl zeigt dieser Punkt?». Die offene Frage nach einem kindgerechten Gespräch steht in der Journey. |
| H13 | Ein inoffizieller Kanal (Messenger der Lehrperson) neben dem vorgeschriebenen | **Workaround** | `chat` trägt den Messenger. Der Breakdown entsteht aber nicht im Kanal, sondern in der Differenz zum vorgeschriebenen Kanal («schriftlich an das Sekretariat», `tar-06`). Ein Jahr lang war der Messenger der Kanal für alles; 41 % der verspäteten Abmeldungen gingen zuerst an die Lehrperson. Die Vorschrift steht nur in einem Atom. Dass statt der Schul-App (`doc-06`) ein privater Messenger läuft, ist auch eine Datenschutzfrage. Das Modell unterscheidet den Chat einer Behörde nicht von einem privaten Messenger. | Review-Frage «Wo nutzt die Persona einen Kanal, der für diesen Schritt nicht gilt (Formvorschrift)?» und ein Hinweis in der Synthese. Ein Feld für den vorgeschriebenen Kanal, mit Lint «genutzt ≠ vorgeschrieben», erst, wenn ein zweites Beispiel dieselbe Lücke zeigt. |
| H14 | Mehrere Träger: Verein, Gemeinde, Volksschule, Fachgeschäft | **passt; zwei Abstriche** | `counterpart` und `is_transition` tragen vier Stellen, L023 hat jeden Wechsel gefunden. Allerdings sind 12 von 15 Schritten Übergänge, die Markierung verliert an Trennschärfe. Aussagekräftig ist erst, dass alle vier Breakdowns an einem Übergang liegen, und das zeigt weder ein Lint noch der Audit-Bericht. Die Schemabeschreibung von `counterpart` («Wer auf Verwaltungsseite beteiligt ist») passt nicht auf ein Musikgeschäft. In der Baubewilligung steht dort schon die Installationsfirma. | Beschreibung von `counterpart` erweitern: Gegenüber der Persona, auch Dritte wie Fachgeschäfte (kein Breaking Change). Im Audit-Bericht eine Zeile «Breakdowns an Übergängen: n von m» prüfen. |
| H15 | Eine Dauerleistung mit Semestern und Wiederanmeldung passt in ein lineares Modell | **passt** | Eine Journey ist ein Durchgang. Die Folgen der verpassten Abmeldung fallen ins nächste Semester und stehen in der letzten Phase; Folgejahre sind `scope_exclusions`. Ein Abstrich betrifft die Übersetzung der Kennzahlen: Bei einer Dauerleistung heisst Retention wörtlich «bleibt dabei». `kpi-uebersetzung.md` übersetzt sie als Kanaltreue. | Zeile in `references/kpi-uebersetzung.md`: Retention bei Dauerleistungen (Unterricht, Betreuung) = «Anteil, der weiterführt». |

**Weitere Befunde, nicht vorab vermutet:**

- **Quellenart für Erlasse fehlt**: Die Tarifordnung ist öffentlich, steht aber als `internal_document`, und der Viewer beschriftet sie mit «Internes Dokument». Für die Lints folgenlos, weil beide `assumed` sind. Vorschlag mit niedriger Priorität: eigene Quellenart für Erlasse und Reglemente oder eine weitere Beschreibung von `internal_document`.
- **Back-Stage ohne Belege**: `backstage_notes` sind Freitext ohne `evidence_refs`. Liegt die Ursache eines Breakdowns Back-Stage (H9), lässt sie sich nicht belegen, ohne Atom-IDs in den Text zu schreiben.
- **Lints sind bereichsneutral und blind für H8–H13**, wie schon bei der Baubewilligung (für H8 und H9 inzwischen behoben: L004 und L103 nach ADR-0007, L005 und L065 nach ADR-0008). 0 Warnungen ohne angepasste Schwellen zeigen, dass die Struktur trägt. Die Lücken sind semantisch (Beträge, Ursachenketten, Fristen, Formvorschriften); ein Lint sieht sie erst, wenn das Schema sie ausdrückt.
- **Atomzahl**: 140 Atome bei 15 Schritten. 60 stammen aus den Interviews und liegen im Richtwert von 12–25 je Interview; der Rest kommt aus Export, Statistik, Befragung und zwei Dokumenten. Das bestätigt den Befund der Baubewilligung: Der Richtwert je Schritt im Skill passt nicht zu Material mit vielen strukturierten Quellen.

## Reproduzieren

```bash
cd examples/musikschule

journeykit validate journey.json
journeykit lint journey.json                   # 0 Fehler · 0 Warnungen · 19 Hinweise
journeykit lint journey.json --lang fr         # Meldungen französisch

journeykit render journey.json -o journey.html

journeykit export journey.json --format audit
journeykit export journey.json --format storymap
```

## Erweitern

- Ein kindgerechtes Gespräch (offene Frage in der Journey) zeigt, ob die Kurve der Eltern auch die des Kindes ist; dann `m4-*` und allenfalls eine eigene Datei mit dem Kind als Persona, gleiche Phasen-IDs.
- Wird ein weiterer Vorschlag aus den Befunden umgesetzt (Fristen der Persona, vorgeschriebener Kanal), dieses Beispiel nachführen und den Befund in der Tabelle als erledigt markieren.
