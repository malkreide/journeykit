# Lauf 2026-10-14 unabhängig bestaetigung-2 – engere Körnungsregel, Bestätigung, Prompts wie bestaetigung-1

| Fall | Atome | Pflicht-Atome gefunden | Feldtreue | Regelverstösse |
|---|---|---|---|---|
| fokusgruppe | 102 | 62/62 (100%) | 403/410 (98%) | 0 |
| interview-dolmetsch | 57 | 47/47 (100%) | 328/339 (97%) | 0 |
| interview-eltern | 106 | 63/63 (100%) | 406/410 (99%) | 0 |
| **gesamt** | 265 | 172/172 (100%) | 1137/1159 (98%) | 0 |

## fokusgruppe

- **b4-nicht-auf-notfallliste** – signal: erwartet ['breakdown'], erhalten friction
- **b1-schuhe-einlaufen** – signal: erwartet ['workaround'], erhalten friction
- **b4-app-zugang-bis-weihnachten** – signal: erwartet ['friction'], erhalten breakdown
- **b1-kosten-80-qr-rechnung** – signal: erwartet ['neutral'], erhalten friction
- **b3-tipp-vom-elternrat** – signal: erwartet ['positive', 'workaround', 'neutral'], erhalten friction
- **b3-couvert-mit-zettel** – signal: erwartet ['workaround'], erhalten friction
- **b2-wunsch-nummern-stimmen** – signal: erwartet ['need'], erhalten friction

## interview-dolmetsch

- **erstgespraech-teilnehmende** – signal: erwartet ['neutral'], erhalten friction
- **sozialarbeiterin-erst-nach-zwei-wochen** – signal: erwartet ['friction'], erhalten workaround
- **sozialarbeiterin-sortiert-papiere** – signal: erwartet ['neutral', 'positive'], erhalten workaround
- **abendkurs-als-ersatz** – signal: erwartet ['workaround'], erhalten breakdown
- **lehrerin-troestet** – signal: erwartet ['positive'], erhalten friction
- **lehrerin-troestet** – emotion: erwartet not_explicit, erhalten {'valence': -1, 'label': 'Angst (Kind)', 'explicit': True}
- **app-uebersetzung-ohne-tigrinya** – signal: erwartet ['friction'], erhalten workaround
- **schule-mehr-text** – signal: erwartet ['friction'], erhalten positive
- **schule-mehr-text** – emotion: erwartet none, erhalten {'valence': 1, 'label': 'gefällt', 'explicit': True}
- **spd-abklaerung-vorgeschlagen** – signal: erwartet ['neutral'], erhalten friction
- **spd-abklaerung-vorgeschlagen** – emotion: erwartet none, erhalten {'valence': -1, 'label': 'Angst', 'explicit': True}

## interview-eltern

- **gesuch-ende-februar** – signal: erwartet ['neutral'], erhalten need
- **mittagstisch-platz-ab-september** – signal: erwartet ['neutral', 'positive'], erhalten friction
- **schulweg-dauer** – signal: erwartet ['neutral'], erhalten friction
- **tablet-wie-ein-baby** – signal: erwartet ['friction'], erhalten workaround
