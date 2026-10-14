# Lauf 2026-10-14 unabhängig bestaetigung-3 – engere Körnungsregel, Bestätigung, Prompts wie bestaetigung-1

| Fall | Atome | Pflicht-Atome gefunden | Feldtreue | Regelverstösse |
|---|---|---|---|---|
| fokusgruppe | 97 | 62/62 (100%) | 399/406 (98%) | 0 |
| interview-dolmetsch | 57 | 47/47 (100%) | 326/339 (96%) | 0 |
| interview-eltern | 102 | 63/63 (100%) | 396/401 (99%) | 0 |
| **gesamt** | 256 | 172/172 (100%) | 1121/1146 (98%) | 0 |

## fokusgruppe

- **b2-save-the-date-app** – signal: erwartet ['neutral'], erhalten friction
- **b4-nicht-auf-notfallliste** – signal: erwartet ['breakdown'], erhalten friction
- **b1-kosten-80-qr-rechnung** – signal: erwartet ['neutral'], erhalten friction
- **b3-tipp-vom-elternrat** – signal: erwartet ['positive', 'workaround', 'neutral'], erhalten friction
- **b3-couvert-mit-zettel** – signal: erwartet ['workaround'], erhalten friction
- **b2-alte-nummer-aus-system** – signal: erwartet ['breakdown'], erhalten friction
- **b2-wunsch-nummern-stimmen** – signal: erwartet ['need'], erhalten friction

## interview-dolmetsch

- **erstgespraech-teilnehmende** – signal: erwartet ['neutral'], erhalten friction
- **sozialarbeiterin-erst-nach-zwei-wochen** – signal: erwartet ['friction'], erhalten workaround
- **sozialarbeiterin-sortiert-papiere** – signal: erwartet ['neutral', 'positive'], erhalten workaround
- **abendkurs-als-ersatz** – signal: erwartet ['workaround'], erhalten breakdown
- **loesung-ausstehend** – signal: erwartet ['friction'], erhalten breakdown
- **lehrerin-troestet** – signal: erwartet ['positive'], erhalten friction
- **lehrerin-troestet** – emotion: erwartet not_explicit, erhalten {'valence': -1, 'label': 'Angst', 'explicit': True}
- **app-uebersetzung-ohne-tigrinya** – signal: erwartet ['friction'], erhalten workaround
- **schule-mehr-text** – signal: erwartet ['friction'], erhalten positive
- **schule-mehr-text** – emotion: erwartet none, erhalten {'valence': 1, 'label': 'gefällt ihm', 'explicit': True}
- **kindergarten-tuer-zu** – signal: erwartet ['breakdown'], erhalten friction
- **spd-abklaerung-vorgeschlagen** – signal: erwartet ['neutral'], erhalten friction
- **spd-abklaerung-vorgeschlagen** – emotion: erwartet none, erhalten {'valence': -1, 'label': 'Angst', 'explicit': True}

## interview-eltern

- **kind-nichts-sagen-koennen** – emotion: erwartet not_explicit, erhalten {'valence': -1, 'label': 'bereut', 'explicit': True}
- **mittagstisch-platz-ab-september** – signal: erwartet ['neutral', 'positive'], erhalten friction
- **schulweg-dauer** – signal: erwartet ['neutral'], erhalten friction
- **papier-ausdrucke-luethi** – signal: erwartet ['workaround', 'positive'], erhalten friction
- **nicht-wissen-was-machen-hauptproblem** – signal: erwartet ['friction'], erhalten need
