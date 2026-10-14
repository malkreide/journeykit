Du extrahierst Evidenz-Atome aus der Quelle «Geschäftskontrolle Einwohnerdienste 2025» (source_ref «statistik», case_records, Klasse observed).
Regeln:
- Ein Atom pro belegbarer Aussage, nicht pro Satz: Sätze desselben Redebeitrags, die zusammen eine Aussage machen, bleiben ein Atom. Dieselbe Aussage nie doppelt erfassen (nicht als Zitat und zusätzlich als Messwert).
- Zitate wörtlich, mit Fundstelle (Zeile/Zeitstempel/ID). Kürzen mit «…» ist erlaubt; Namen und andere Personendaten im Zitat durch «[Name]», «[Ort]» ersetzen.
- Nennt ein Zitat eine Zahl oder Dauer, value und unit im selben Atom ergänzen.
- emotion_hint nur, wenn die Emotion im Text steht; explicit true nur bei ausdrücklicher Nennung.
- signal setzen (friction, breakdown, positive, need, workaround, neutral); breakdown nur, wenn die Person scheitert oder ausweicht (Anruf, Schalter, Aufgeben).
- channel_hint nur mit diesen Werten: web, app, email, phone, letter, paper_form, counter, in_person, event, chat, sms, publication, other.
- phase_hint aus dieser Liste: vorbereitung, anmeldung, nachweise, bestaetigung. persona_hint: zugezogen.
- Keine Personendaten im text (Namen, Orte, Kontaktangaben ersetzen).
- Widerspricht eine Aussage einer bekannten Soll-Aussage, contradicts setzen: keine.
Gib ausschliesslich ein JSON-Array von Atomen nach journeykit-Schema aus, IDs mit Präfix «stat-», source_ref «statistik».

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
