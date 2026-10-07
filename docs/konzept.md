# Konzept: Evidenz-zu-Journey-Pipeline

Stand 0.1.0. Begründet, warum JourneyKit so gebaut ist, wie es gebaut ist.
Die methodische Grundlage steht in `skill/user-journey/references/methodik.md`;
Architekturentscheide einzeln in `docs/adr/`.

## Ausgangslage

Journey Mapping ist etabliert und scheitert trotzdem regelmässig – nicht am
Konzept, sondern an der Praxis: Maps entstehen aus Innensicht, verengen auf den
Happy Path, werden nicht gepflegt und erreichen das Backlog nie. Die
Tool-Landschaft (Whiteboards, Spezialsoftware, Analytics-Plattformen)
adressiert die **Darstellung**, nicht die **Synthese**: Wie kommt man von
20 Interviewtranskripten, 300 Anfragen und einem Analytics-Export zu einer
Map, deren Aussagen man nachprüfen kann? Dieser Schritt dauert heute Tage und
wird abgekürzt – und genau dort kann ein Sprachmodell helfen, wenn es
methodisch eingehegt ist.

Für die öffentliche Verwaltung kommt dazu: Das Vokabular ist kommerziell
(Conversion, Churn, Checkout), die Kanäle sind analog (Brief, Telefon,
Schalter, Veranstaltung), die Nutzenden haben keine Wahl, und das Material
enthält Personendaten.

## Kernidee: Modell vor Darstellung

Das Primärartefakt ist nicht die Map, sondern ein **strukturiertes
Journey-Modell** (`journey.json`). Die Map ist eine von mehreren Sichten
darauf. Daraus folgt:

- Jede Aussage trägt Evidenz-Referenzen. Eine Map ohne Primärevidenz ist als Hypothese erkennbar, nicht als Befund getarnt.
- Methodische Qualität wird prüfbar: Lints statt Checkliste.
- Neue Evidenz erzeugt ein **Diff**, keine neue Map.
- Dieselben Daten werden zu Viewer, Story Map, Massnahmenliste, Audit-Report.
- Das Modell ist werkzeugneutral: Es kann in Notion, einer Datenbank, einem MCP-Server oder einfach in Git leben.

## Sechs Schichten

| Schicht | Inhalt | Umsetzung 0.1.0 |
|---|---|---|
| 1 Input | Interviews, Befragungen, Anfragen-/Ticketexporte, Analytics, Fotos von Workshop-Wänden, Prozessdokumente, bestehende Journeys | Quellenregister (`sources`) mit Art, Standard-Evidenzklasse, Stichprobe, Datenschutzstatus, Ablage |
| 2 Evidenz-Atome | Kleinste belegbare Einheit: Zitat, Beobachtung, Messwert, Dokumentstelle, mit Fundstelle, Klasse, Signal, Emotion (nur explizit), Widerspruch | `evidence[]` im Schema; Extraktionsregeln und Prompt-Schablone im Skill |
| 3 Journey-Modell | Persona, Szenario, Phasen, Schritte, Denken/Fühlen, Pain Points (Reibung/Breakdown), Edge Cases, Recovery, KPIs, Chancen, offene Fragen, Owner, Review | JSON Schema 2020-12 |
| 4 Synthese-Engine | Clustern, Kurve nur aus Evidenz, Widersprüche und Lücken ausweisen, Chancen und Scores vorschlagen | Claude-Skill (Modi Synthese / Workshop / Audit) + Lints als Rückkopplung |
| 5 Darstellung | Journey mit Kurve, Prozess/Fehlerpfade, Evidenz-Heatmap, Chancenmatrix, Prüfung; Drilldown bis zum O-Ton; Filter «nur Primärevidenz»; Persona-Überlagerung | Single-File-Viewer |
| 6 Betrieb | Owner, Review-Rhythmus, Status pro Pain Point und Chance, Versionen, Diff | Schema-Felder, Lints L030–L034, `journeykit diff` |

## Evidenzklassen als tragendes Prinzip

| Klasse | Was | Gewicht |
|---|---|---|
| `observed` | gemessen oder beobachtet (Analytics, Exporte, Beobachtung) | primär |
| `reported` | von Nutzenden berichtet (Interview, Befragung, Tagebuch, Beschwerde) | primär |
| `assumed` | interne Annahme (Prozessdokument, Workshop ohne Nutzende) | sekundär |

Die Klasse hängt an der **Quelle**, nicht an der Plausibilität der Aussage.
Drei Prozessdokumente machen keine Nutzerevidenz. Der Viewer macht das
sichtbar: gestrichelte Kurvenpunkte, Heatmap, Filter. Die Lints machen es
hörbar: Eine validierte Journey ohne Primärevidenz an den Erlebnis-Aussagen
ist ein Fehler, keine Warnung.

## Fallstricke → Anforderungen → Umsetzung

| Fallstrick | Anforderung | Umsetzung |
|---|---|---|
| Inside-Out Bias | Evidenzklasse und Quelle an jeder Aussage; Hypothesen als solche kennzeichnen | `evidence_refs`, `meta.status: hypothesis`, `persona.is_hypothesis`, L010–L012, Filter im Viewer |
| Happy Path Bias | Pflichtfelder für Edge Cases, Breakdowns, Recovery; aktives Nachfragen | `pain_points.type`, `workaround`, `edge_cases`, `recovery_paths.exists`, L020–L023, Prozess-Layer |
| Static Map Trap | Datenbestand mit Versionen, Owner, Status; neuer Input erzeugt Diff | `meta.owner`, `review_cycle_days`, `next_review`, `status` an Pain Points und Chancen, `changelog`, `journeykit diff`, L030–L034 |
| Empathie-Vakuum / Überkomplexität | Drilldown bis zum O-Ton; eine Persona, ein Szenario; Scope-Ausschlüsse | Drawer im Viewer, Schema erzwingt eine Persona, `scope_exclusions`, L040–L052 |
| Micro-Level Disconnect | Export als Story Map und Backlog; Diagnose Journey vs. Blueprint | `opportunities.stories`, `export --format storymap/actions`, `meta.diagnosis`, L060–L063, L070–L072 |

Zusätzlich für die Verwaltung: KPI-Übersetzungsschicht (`kpi.category:
public_value`, `commercial_equivalent`, L090–L092), Kanäle jenseits des Webs
(`channel`-Enum), Personendaten (`pii_status`, L080–L081).

## Was das Tool verspricht – und was nicht

- Es beschleunigt die **Synthese und Darstellung** (Phasen 2–6 nach NN/g) von etwa zwei Wochen auf etwa zwei Tage.
- Es beschleunigt die **Erhebung nicht**. Rund 20 der 74 Stunden bleiben. Null Interviews ergeben null Wert, und das Modell sagt es (L010, L011).
- Es verhindert nicht, dass billige Maps zu mehr Maps statt zu mehr Veränderung führen. Dagegen hilft nur die Betriebsschicht – Owner, Review, Status – und die wird am ehesten weggelassen. Deshalb sind diese Felder Lint-Gegenstand.
- Es ersetzt kein Review. Die Lints prüfen Struktur und Evidenzlage; ob ein Zitat gut gewählt oder eine Phase richtig geschnitten ist, prüft ein Mensch (`references/review-fragen.md`).

## Architekturvarianten

| Variante | Beschreibung | Status |
|---|---|---|
| **A: Skill + CLI + HTML** | Alles in der Claude-Sitzung und lokal; Journey lebt als Datei in Git | **0.1.0** |
| **B: Skill + MCP-Server** | Journey-Modell in einem Server (SQLite oder Notion); Versionen, Evidenz, Suche über Journeys hinweg; Skill steuert die Pipeline | geplant (ADR-0004) |
| **C: Web-App** | Backend mit Pipeline, Frontend als Editor für nicht-KI-affine Teams | nicht vor Evaluation |

A zuerst, weil es beweisen muss, dass die Synthese methodisch trägt, bevor
Infrastruktur entsteht. B passt zum bestehenden MCP-Portfolio und macht die
Journey zum lebenden Datenbestand. C erst, wenn die Zielgruppe wechselt.

## Datenschutz

Interviews mit Eltern, Kindern, Lehrpersonen sind Personendaten. Das Modell
zieht die Grenze an der Quelle: Ins JSON kommen anonymisierte Zitate und die
Ablage des Rohmaterials, nie das Material selbst. `pii_status: contains_pii`
blockiert das Teilen (L080). Wo das Modell läuft – Cloud oder lokal –
entscheidet die Organisation; die Pipeline funktioniert mit beidem, und eine
lokale Variante (vgl. KOMKI) ändert am Modell nichts.

## Evaluation (offen)

Wie weiss man, ob die Synthese gut ist? Vorschlag: eine bestehende, manuell
erstellte und reviewte Journey als Ground Truth nehmen, das zugehörige
Rohmaterial durch die Pipeline schicken, vergleichen – Schritte, Pain Points,
Breakdowns, Emotionen, Chancen. Abweichungen in drei Klassen: Pipeline hat
etwas übersehen, Pipeline hat etwas erfunden, Pipeline hat etwas gefunden,
das die manuelle Journey übersehen hat. Erst dieser Vergleich sagt, was
«methodisch rigoros» konkret heisst.

## Roadmap

1. GitHub-Repo, CI grün, Secret Scanning (0.1.x)
2. Evaluation gegen eine reale Ground-Truth-Journey (0.2)
3. Testsatz für die Extraktion: Input → erwartete Atome (0.2)
4. ~~Zweites Beispiel aus einem anderen Verwaltungsbereich (0.2)~~ – `examples/baubewilligung/`; Befunde zur Übertragbarkeit (Handelnde Dritte, Kanal «Publikation», Quellenart für Geschäftskontrolle u. a.) im Beispiel-README, Umsetzung offen
5. Viewer: visueller Versionsvergleich, Export der Heatmap, französische UI (0.3)
6. Variante B: MCP-Server für Journeys als Datenbestand (0.4)
