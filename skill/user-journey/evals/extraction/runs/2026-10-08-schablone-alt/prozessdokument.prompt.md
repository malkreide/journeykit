Du extrahierst Evidenz-Atome aus der Quelle «Prozessbeschreibung Wohnsitzanmeldung, Version 2.1» (internal_document, Klasse assumed).
Regeln:
- Ein Atom pro belegbarer Aussage. Zitate wörtlich, mit Fundstelle (Zeile/Zeitstempel/ID).
- emotion_hint nur, wenn die Emotion im Text steht; explicit true nur bei ausdrücklicher Nennung.
- signal setzen; breakdown nur, wenn die Person scheitert oder ausweicht (Anruf, Schalter, Aufgeben).
- phase_hint aus dieser Liste: vorbereitung, anmeldung, nachweise, bestaetigung. persona_hint: zugezogen.
- Keine Personendaten im text (Namen, Orte, Kontaktangaben ersetzen).
- Widerspricht eine Aussage einer bekannten Soll-Aussage, contradicts setzen: anf-17: «Bestätigung nach drei Wochen noch nicht erhalten.»; anf-07: «Formular akzeptiert keine Fotos vom Handy.»; anf-12: «Liste der Unterlagen auf der Website nicht gefunden.».
Gib ausschliesslich ein JSON-Array von Atomen nach journeykit-Schema aus, IDs mit Präfix «doc-».

Quelle «input.md»:

```
# Prozessbeschreibung Wohnsitzanmeldung (intern, Version 2.1)

Einwohnerdienste Gemeinde Musterau (synthetisch). Stand: März 2026.

## 1 Ablauf

1. Zuziehende melden sich innert 14 Tagen nach dem Umzug an, online oder am Schalter.
2. Für die Anmeldung sind Heimatschein, Mietvertrag und ein amtlicher Ausweis nötig.
3. Das Online-Formular nimmt PDF-Dateien und Fotos bis 10 MB entgegen.
4. Die Einwohnerdienste prüfen die Anmeldung innert 5 Arbeitstagen.
5. Die Anmeldebestätigung wird innert 10 Arbeitstagen nach Eingang per Post verschickt.

## 2 Information

6. Die Liste der Unterlagen ist auf der Website unter «Umzug» aufgeführt.
7. Bei verspäteter Anmeldung kann eine Ordnungsbusse erhoben werden; in der Praxis wird bei der ersten Anmeldung darauf verzichtet.

## 3 Verantwortung

8. Fachverantwortung: Leitung Einwohnerdienste.
```
