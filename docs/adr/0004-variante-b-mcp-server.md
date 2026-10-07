# ADR-0004: Variante B – MCP-Server für Journeys als Datenbestand

Datum: 2026-10-05 · Status: vorgeschlagen

## Kontext

Variante A (Skill + CLI + Datei in Git) reicht für einzelne Journeys. Sobald
mehrere Journeys, Personas und Versionen gepflegt werden, fehlen Suche über
Journeys hinweg, Evidenz-Wiederverwendung und eine Oberfläche für Reviews.

## Vorschlag

Ein MCP-Server (`journeys-mcp`, Python, Spec-Stand gemäss Portfolio-Regeln)
hält Journeys, Quellen und Evidenz-Atome in SQLite (oder spiegelt sie nach
Notion). Tools: `journey_get`, `journey_list`, `journey_save` (mit
Schema-Validierung und Lint), `evidence_search`, `journey_diff`,
`journey_render`. Der Skill `user-journey` nutzt die Tools statt lokaler
Dateien; die CLI bleibt für Offline-Arbeit.

## Offene Fragen

- Wo läuft der Server (lokal, Pi, Verwaltungsserver)? Datenschutz entscheidet.
- Evidenz-Atome quer über Journeys teilen oder pro Journey kopieren?
- Rechte: Wer darf eine Journey als `validated` setzen?

## Voraussetzung

Erst nach der Evaluation (docs/konzept.md) – Infrastruktur folgt der
nachgewiesenen Synthese-Qualität, nicht umgekehrt.
