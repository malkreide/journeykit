# ADR-0001: Modell vor Darstellung

Datum: 2026-10-05 · Status: angenommen

## Kontext

Heutige Journey-Werkzeuge (Whiteboards, Spezialsoftware) machen die Map zum
Primärartefakt. Aussagen sind nicht nachprüfbar, Versionen sind Kopien,
Massnahmen bleiben in der Grafik hängen.

## Entscheid

Das Primärartefakt ist eine JSON-Datei nach `journey.schema.json`. Viewer,
Story Map, Massnahmenliste, Audit-Report und Diff werden daraus erzeugt und
sind jederzeit reproduzierbar. Darstellungen werden nicht von Hand editiert.

## Folgen

- Schema-Änderungen sind teuer (Viewer, Beispiele, Tests nachziehen) – dafür gibt es eine Quelle der Wahrheit.
- Die Journey kann in Git, Notion, einer Datenbank oder einem MCP-Server leben.
- Lints sind möglich, weil das Modell weiss, was eine Aussage und was ein Beleg ist.
