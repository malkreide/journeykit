Du extrahierst Evidenz-Atome aus der Quelle «Prozessbeschreibung Wohnsitzanmeldung, Version 2.1» (source_ref «prozess», internal_document, Klasse assumed).
Regeln:
- Ein Atom pro belegbarer Aussage, nicht pro Satz: Sätze desselben Redebeitrags, die zusammen eine Aussage machen, bleiben ein Atom. Dieselbe Aussage nie doppelt erfassen (nicht als Zitat und zusätzlich als Messwert).
- Zitate wörtlich, mit Fundstelle (Zeile/Zeitstempel/ID). Kürzen mit «…» ist erlaubt; Namen und andere Personendaten im Zitat durch «[Name]», «[Ort]» ersetzen.
- Nennt ein Zitat eine Zahl oder Dauer, value und unit im selben Atom ergänzen.
- emotion_hint nur, wenn die Emotion im Text steht; explicit true nur bei ausdrücklicher Nennung.
- signal setzen (friction, breakdown, positive, need, workaround, neutral); breakdown nur, wenn die Person scheitert oder ausweicht (Anruf, Schalter, Aufgeben).
- channel_hint nur mit diesen Werten: web, app, email, phone, letter, paper_form, counter, in_person, event, chat, sms, publication, other.
- phase_hint aus dieser Liste: vorbereitung, anmeldung, nachweise, bestaetigung. persona_hint: zugezogen.
- Keine Personendaten im text (Namen, Orte, Kontaktangaben ersetzen).
- Widerspricht eine Aussage einer bekannten Soll-Aussage, contradicts setzen: anf-17: «Bestätigung nach drei Wochen noch nicht erhalten.»; anf-07: «Formular akzeptiert keine Fotos vom Handy.»; anf-12: «Liste der Unterlagen auf der Website nicht gefunden.».
Gib ausschliesslich ein JSON-Array von Atomen nach journeykit-Schema aus, IDs mit Präfix «doc-», source_ref «prozess».

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
