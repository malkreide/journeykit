# ADR-0003: Viewer als eigenständige HTML-Datei ohne externe Abhängigkeiten

Datum: 2026-10-05 · Status: angenommen

## Kontext

Zielgruppe sind Verwaltungen mit geschlossenen Netzen, Proxys und
Datenschutzauflagen. Eine Journey enthält Zitate realer Personen (auch
anonymisiert). Externe Skripte, Fonts oder Tracking sind ausgeschlossen.

## Entscheid

`viewer/viewer.html` ist eine einzige Datei mit eingebettetem CSS und JS,
ohne CDN, ohne Netzwerkanfragen. Der Renderer injiziert die Daten als JSON an
genau einer Stelle. Kein Build-Schritt, kein Framework. Light/Dark über
Tokens; phone-tauglich.

## Verworfen

- React/Vue mit Bundler: besser wartbar bei Wachstum, aber Build-Toolchain und Abhängigkeiten, die in Verwaltungen schwer zu rechtfertigen sind.
- Jinja-Templates serverseitig: zweite Rendering-Logik neben dem Modell; Interaktivität bräuchte trotzdem JS.

## Folgen

- Der Viewer hat eine eigene kleine Index-Klasse, die `model.py` spiegelt – bewusst dupliziert, in Tests gegen dieselben Beispiele geprüft.
- Gerenderte Dateien sind per E-Mail oder Ablage teilbar und funktionieren offline.
