# Lauf 2026-10-14 unabhängig koernung-2 – Schablone mit Körnungsregel (f2dd14d), Prompts wie koernung-1

| Fall | Atome | Pflicht-Atome gefunden | Feldtreue | Regelverstösse |
|---|---|---|---|---|
| fokusgruppe | 116 | 62/62 (100%) | 396/398 (99%) | 0 |
| interview-dolmetsch | 57 | 47/47 (100%) | 322/334 (96%) | 0 |
| interview-eltern | 102 | 63/63 (100%) | 395/401 (99%) | 0 |
| **gesamt** | 275 | 172/172 (100%) | 1113/1133 (98%) | 0 |

## fokusgruppe

- **b4-nicht-auf-notfallliste** – signal: erwartet ['breakdown'], erhalten friction
- **b3-tipp-vom-elternrat** – signal: erwartet ['positive', 'workaround', 'neutral'], erhalten friction

## interview-dolmetsch

- **erstgespraech-teilnehmende** – signal: erwartet ['neutral'], erhalten friction
- **sozialarbeiterin-erst-nach-zwei-wochen** – signal: erwartet ['friction'], erhalten workaround
- **sozialarbeiterin-sortiert-papiere** – signal: erwartet ['neutral', 'positive'], erhalten workaround
- **abendkurs-als-ersatz** – signal: erwartet ['workaround'], erhalten breakdown
- **loesung-ausstehend** – signal: erwartet ['friction'], erhalten breakdown
- **lehrerin-troestet** – signal: erwartet ['positive'], erhalten friction
- **lehrerin-troestet** – emotion: erwartet not_explicit, erhalten {'valence': -1, 'label': 'Angst (Kind)', 'explicit': True}
- **app-uebersetzung-ohne-tigrinya** – signal: erwartet ['friction'], erhalten workaround
- **schule-mehr-text** – signal: erwartet ['friction'], erhalten positive
- **schule-mehr-text** – emotion: erwartet none, erhalten {'valence': 1, 'label': 'zufrieden', 'explicit': True}
- **spd-abklaerung-vorgeschlagen** – signal: erwartet ['neutral'], erhalten friction
- **spd-abklaerung-vorgeschlagen** – emotion: erwartet none, erhalten {'valence': -1, 'label': 'Angst', 'explicit': True}

## interview-eltern

- **gesuch-ende-februar** – signal: erwartet ['neutral'], erhalten need
- **mittagstisch-platz-ab-september** – signal: erwartet ['neutral', 'positive'], erhalten friction
- **schulweg-dauer** – signal: erwartet ['neutral'], erhalten friction
- **tablet-wie-ein-baby** – signal: erwartet ['friction'], erhalten workaround
- **aufholen-bis-juni** – signal: erwartet ['workaround', 'positive'], erhalten friction
- **nicht-wissen-was-machen-hauptproblem** – signal: erwartet ['friction'], erhalten need
