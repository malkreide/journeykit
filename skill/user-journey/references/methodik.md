# Methodik: Taxonomie, Fallstricke, Prozess

Kondensat der methodischen Grundlage, auf der journeykit aufbaut. Belastbar
sind vor allem die Arbeiten der Nielsen Norman Group (Journey Mapping 101,
User Journeys vs. User Flows, UX Mapping Cheat Sheet, User Story Mapping) und
Jeff Pattons Story Mapping. Zwei viel zitierte Zahlen – «67 % der Maps bewirken
nichts» (Qualtrics) und «70 % entstehen ohne Nutzerinput» (Gartner 2023) –
laufen aus zweiter Hand über Anbieterblogs; als Anekdote brauchbar, in einer
Geschäftsleitungsvorlage nicht ohne Primärquelle verwenden.

## Taxonomie

| Artefakt | Fokus | Flughöhe | Kernelemente |
|---|---|---|---|
| **User Journey Map** | Erleben einer Nutzerrolle beim Erreichen eines Ziels | Makro, szenariobasiert, kanalübergreifend, Tage bis Monate | Handlungen, Gedanken, Gefühle (Kurve), Touchpoints, Pain Points, Chancen |
| **Customer Journey Map** | Gesamte Beziehung zur Organisation | Makro, Lebenszyklus | wie oben plus Beziehungs- und Wirkungskennzahlen |
| **User Flow** | Pfad durch eine Oberfläche | Mikro, Bildschirm für Bildschirm | Klickpfade, Systementscheide, Abzweigungen – keine Emotion |
| **Service Blueprint** | Was intern nötig ist, damit das Erleben funktioniert | Front- und Back-Stage, Sichtbarkeitslinie | Mitarbeitendenhandlungen, Systeme, Support-Prozesse |
| **Experience Map** | Allgemeines menschliches Verhalten bei einem Vorhaben | Makro, organisationsunabhängig | Bedürfnisse, generische Lösungswege |

Theater-Analogie: Journey = vor dem Vorhang, Blueprint = hinter dem Vorhang.
In der Verwaltung sind viele «Journey»-Anfragen Blueprint-Anfragen.

## Wofür Journeys gebraucht werden

1. **Silos aufbrechen** – die Journey ist ein Boundary Object: Kreisschulbehörde, Schulleitung, Betreuung und zentrale Kommunikation sehen dieselbe Reise statt je ihren Touchpoint.
2. **Empathie-Vakuum schliessen** – Analytics zeigt *wo* abgebrochen wird, nie *warum*.
3. **Reibung lokalisieren** – jeder unklare Brief, jedes doppelte Formular summiert sich zu Anrufen, Beschwerden, Nichthandeln.
4. **Priorisieren** – Ressourcen dorthin, wo Nutzende scheitern, nicht dorthin, wo intern am lautesten geklagt wird.

## Die fünf Fallstricke – und was journeykit dagegen tut

| Fallstrick | Symptom | Gegenmittel im Modell | Lint |
|---|---|---|---|
| **Static Map Trap** | Map wird erstellt, bewirkt nichts, veraltet | `meta.owner`, `review_cycle_days`, `next_review`, Status pro Pain Point und Chance, `journeykit diff` | L030–L034 |
| **Inside-Out Bias** | Map aus dem Sitzungszimmer, ohne Nutzende | Evidenzklassen, `evidence_refs` an jeder Aussage, Status `hypothesis`, Filter «nur Primärevidenz» | L010–L012 |
| **Happy Path Bias** | Nur der Idealpfad, keine Fehlschläge | Pflichtfelder `pain_points` (friction/breakdown), `edge_cases`, `recovery_paths`, `workaround` | L020–L023 |
| **Überkomplexität vs. Empathie-Vakuum** | Stammbaum-Chaos oder Klickliste ohne Gefühl | Eine Persona pro Datei, `scope_exclusions`, `thinking`/`feeling` pro Schritt, `null` als ehrliche Lücke | L040–L052 |
| **Micro-Level Disconnect** | Makro-Erkenntnis erreicht nie das Backlog | `opportunities` mit Scores und `stories`, Story-Map-Export, Massnahmen-CSV | L060–L063 |

Dazu: Blueprint-Smell (L070–L072), Personendaten (L080–L081), Kennzahlen
(L090–L092), Evidenzqualität (L100–L102).

## Erstellungsprozess und Aufwand

NN/g-Befragung von 343 UX-Fachleuten: eine Journey Map kostet im
geometrischen Mittel **73,8 Stunden**; In-House-Teams 79,8 h, Agenturen 71,7 h,
Organisationen über 500 Mitarbeitende 87 h. Davon rund **20,6 h Erhebung**.

Zwei Startpunkte:

- **Hypothesis-first** (62 %): Workshop auf Basis internen Wissens. Senkt die Hürde, erzeugt Buy-in, birgt den Inside-Out-Bias – und spart **keine** Zeit, weil die Validierung nachgeholt werden muss.
- **Research-first** (35 %): erst erheben, dann konsolidieren.

Sechs Phasen:

1. **Erhebung** – Tiefeninterviews und Beobachtung (86 % der Teams), Tagebuchstudien (12 %, wertvoll, weil Frustration schnell verblasst), quantitativ: Analytics, Exporte, Befragungen.
2. **Persona** – datenbasiert, trennscharf; ein Produkt mit grundverschiedenen Gruppen braucht mehrere Maps.
3. **Szenario und Phasen** – ein Ziel; Phasen entstehen aus Forschung (31 %) oder Workshop (31 %), selten vorab.
4. **Touchpoints, Handlungen, Kanäle** – Übergangspunkte besonders beleuchten.
5. **Denken und Fühlen** – die emotionale Kurve; das Herzstück und zugleich die grösste Quelle von Pseudo-Präzision.
6. **Synthese und Chancen** – How-might-we, Edge Cases, Priorisierung.

Was journeykit beschleunigt: Phasen 2–6 (Synthese und Darstellung), von
Wochen auf Tage. Was es nicht beschleunigt: Phase 1. Wer ohne Erhebung
startet, bekommt eine formvollendete Hypothesen-Map – und das Modell sagt es.

## Von der Journey ins Backlog: Story Mapping (Patton)

- **Horizontale Achse (Backbone)**: Nutzeraktivitäten in der Reihenfolge der Journey – Phasen und Schritte.
- **Vertikale Achse**: Stories je Aktivität, oben die wichtigsten.
- **MVP-Linie**: horizontaler Schnitt – was darüber liegt, ist der erste Release.

`journeykit export --format storymap` erzeugt genau diese Struktur aus
`phases` und `opportunities[].stories` (`mvp: true` über der Linie).

## Verwaltungskontext: was anders ist

- **Keine Abwanderung, sondern Ausweichen** – der `workaround` ist das wichtigste Feld für Breakdowns.
- **Nicht-digitale Kanäle dominieren** – Brief, Telefon, Schalter, Elternabend. Analytics deckt nur einen Teil ab.
- **Pflichtkontexte** – Nutzende haben keine Wahl, die Journey zu beginnen; Frustration hat kein Ventil ausser Beschwerde oder Resignation.
- **Mehrsprachigkeit und Vorerfahrung** streuen stark – fast immer Grund für mehrere Personas.
- **Personendaten** – Interviews mit Eltern, Kindern, Lehrpersonen; Anonymisierung vor der Synthese.
- **Politische Lesart** – eine Journey kann als Kritik an einer Stelle gelesen werden. Owner als Rolle, Befunde als Evidenz, nicht als Urteil formulieren.
