# Lauf 2026-10-14 unabhängig richtwert-2 – neuer Satz zur Atomzahl (Wortlaut im README), Prompts wie richtwert-1

| Fall | Atome | Pflicht-Atome gefunden | Feldtreue | Regelverstösse |
|---|---|---|---|---|
| fokusgruppe | 106 | 62/62 (100%) | 403/410 (98%) | 0 |
| interview-dolmetsch | 65 | 47/47 (100%) | 329/339 (97%) | 0 |
| interview-eltern | 99 | 63/63 (100%) | 395/401 (99%) | 0 |
| **gesamt** | 270 | 172/172 (100%) | 1127/1150 (98%) | 0 |

## fokusgruppe

- **b2-save-the-date-app** – signal: erwartet ['neutral'], erhalten friction
- **b4-nicht-auf-notfallliste** – signal: erwartet ['breakdown'], erhalten neutral
- **b1-kosten-80-qr-rechnung** – signal: erwartet ['neutral'], erhalten friction
- **b3-tipp-vom-elternrat** – signal: erwartet ['positive', 'workaround', 'neutral'], erhalten friction
- **b3-reduktion-nach-zwei-wochen** – signal: erwartet ['positive', 'neutral'], erhalten friction
- **b3-couvert-mit-zettel** – signal: erwartet ['workaround'], erhalten friction
- **b2-wunsch-nummern-stimmen** – signal: erwartet ['need'], erhalten friction

## interview-dolmetsch

- **sozialarbeiterin-erst-nach-zwei-wochen** – signal: erwartet ['friction'], erhalten workaround
- **sozialarbeiterin-sortiert-papiere** – signal: erwartet ['neutral', 'positive'], erhalten workaround
- **abendkurs-als-ersatz** – signal: erwartet ['workaround'], erhalten breakdown
- **lehrerin-troestet** – signal: erwartet ['positive'], erhalten friction
- **lehrerin-troestet** – emotion: erwartet not_explicit, erhalten {'valence': -1, 'label': 'Angst', 'explicit': True}
- **app-uebersetzung-ohne-tigrinya** – signal: erwartet ['friction'], erhalten workaround
- **schule-mehr-text** – signal: erwartet ['friction'], erhalten positive
- **schule-mehr-text** – emotion: erwartet none, erhalten {'valence': 1, 'label': 'zufrieden', 'explicit': True}
- **spd-abklaerung-vorgeschlagen** – signal: erwartet ['neutral'], erhalten friction
- **spd-abklaerung-vorgeschlagen** – emotion: erwartet none, erhalten {'valence': -1, 'label': 'Angst', 'explicit': True}

## interview-eltern

- **gesuch-ende-februar** – signal: erwartet ['neutral'], erhalten need
- **mittagstisch-platz-ab-september** – signal: erwartet ['neutral', 'positive'], erhalten friction
- **schulweg-dauer** – signal: erwartet ['neutral'], erhalten friction
- **papier-ausdrucke-luethi** – signal: erwartet ['workaround', 'positive'], erhalten friction
- **aufholen-bis-juni** – signal: erwartet ['workaround', 'positive'], erhalten friction
- **nicht-wissen-was-machen-hauptproblem** – signal: erwartet ['friction'], erhalten need
