Du extrahierst Evidenz-Atome aus der Quelle «Workshop «Umzug digital», Notizen» (workshop, Klasse assumed).
Regeln:
- Ein Atom pro belegbarer Aussage. Zitate wörtlich, mit Fundstelle (Zeile/Zeitstempel/ID).
- emotion_hint nur, wenn die Emotion im Text steht; explicit true nur bei ausdrücklicher Nennung.
- signal setzen; breakdown nur, wenn die Person scheitert oder ausweicht (Anruf, Schalter, Aufgeben).
- phase_hint aus dieser Liste: vorbereitung, anmeldung, nachweise, bestaetigung. persona_hint: zugezogen.
- Keine Personendaten im text (Namen, Orte, Kontaktangaben ersetzen).
- Widerspricht eine Aussage einer bekannten Soll-Aussage, contradicts setzen: stat-02: «38 % der Anmeldungen 2025 vollständig über das Online-Formular.»; anf-07: «Formular akzeptiert keine Fotos vom Handy.».
Gib ausschliesslich ein JSON-Array von Atomen nach journeykit-Schema aus, IDs mit Präfix «ws-».

Quelle «input.md»:

```
# Workshop «Umzug digital» – Notizen (nur Team, keine Nutzenden)

Gemeinde Musterau (synthetisch), 2026-06-02. Teilnehmende: Einwohnerdienste (3), Informatik (1), Kommunikation (1).

- Die meisten Zuziehenden melden sich inzwischen online an, der Schalter wird kaum noch gebraucht.
- Die Leute sind sicher genervt, weil sie den Heimatschein selbst besorgen müssen.
- Das Upload-Problem betrifft nur alte Browser.
- Idee: Checkliste der Unterlagen als PDF zum Herunterladen.
- Idee: Erinnerungsmail nach 10 Tagen, wenn die Anmeldung noch fehlt.
- Wir vermuten, dass viele die Frist von 14 Tagen gar nicht kennen.
```
