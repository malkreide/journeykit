Du extrahierst Evidenz-Atome aus der Quelle «Geschäftskontrolle Einwohnerdienste 2025» (case_records, Klasse observed).
Regeln:
- Ein Atom pro belegbarer Aussage. Zitate wörtlich, mit Fundstelle (Zeile/Zeitstempel/ID).
- emotion_hint nur, wenn die Emotion im Text steht; explicit true nur bei ausdrücklicher Nennung.
- signal setzen; breakdown nur, wenn die Person scheitert oder ausweicht (Anruf, Schalter, Aufgeben).
- phase_hint aus dieser Liste: vorbereitung, anmeldung, nachweise, bestaetigung. persona_hint: zugezogen.
- Keine Personendaten im text (Namen, Orte, Kontaktangaben ersetzen).
- Widerspricht eine Aussage einer bekannten Soll-Aussage, contradicts setzen: keine.
Gib ausschliesslich ein JSON-Array von Atomen nach journeykit-Schema aus, IDs mit Präfix «stat-».

Quelle «input.csv»:

```
kennzahl;wert;einheit;zeitraum;bemerkung
anmeldungen_total;412;Anzahl;2025;Zuzüge mit Wohnsitzanmeldung
anteil_online;38;%;2025;Anmeldung vollständig über das Online-Formular
anteil_online_abgebrochen;21;%;2025;online begonnen und nicht abgeschlossen, Anteil an allen online begonnenen
anteil_verspaetet;17;%;2025;Anmeldung später als 14 Tage nach dem Umzug
bearbeitungsdauer_median;6;Arbeitstage;2025;Eingang bis Versand der Bestätigung
bearbeitungsdauer_p90;14;Arbeitstage;2025;90 % der Fälle sind schneller
anteil_rueckfragen;29;%;2025;mindestens eine Rückfrage wegen fehlender Unterlagen
```
