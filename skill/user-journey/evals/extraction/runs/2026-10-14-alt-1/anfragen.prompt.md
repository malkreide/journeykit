Du extrahierst Evidenz-Atome aus der Quelle «Anfragen Einwohnerdienste August 2026» (inquiry_log, Klasse observed).
Regeln:
- Ein Atom pro belegbarer Aussage. Zitate wörtlich, mit Fundstelle (Zeile/Zeitstempel/ID).
- emotion_hint nur, wenn die Emotion im Text steht; explicit true nur bei ausdrücklicher Nennung.
- signal setzen; breakdown nur, wenn die Person scheitert oder ausweicht (Anruf, Schalter, Aufgeben).
- phase_hint aus dieser Liste: vorbereitung, anmeldung, nachweise, bestaetigung. persona_hint: zugezogen.
- Keine Personendaten im text (Namen, Orte, Kontaktangaben ersetzen).
- Widerspricht eine Aussage einer bekannten Soll-Aussage, contradicts setzen: keine.
Gib ausschliesslich ein JSON-Array von Atomen nach journeykit-Schema aus, IDs mit Präfix «anf-».

Quelle «input.csv»:

```
id;datum;kanal;kategorie;anliegen
A-01;2026-08-03;Telefon;Unterlagen;Welche Unterlagen braucht es für die Anmeldung?
A-02;2026-08-03;Telefon;Online-Formular;Upload bricht ab, Formular verloren.
A-03;2026-08-04;E-Mail;Unterlagen;Was ist ein Heimatschein und wo bekomme ich ihn?
A-04;2026-08-05;Telefon;Frist;Gilt die Frist von 14 Tagen ab Umzug oder ab Mietbeginn?
A-05;2026-08-06;Schalter;Online-Formular;Hat online angefangen, Upload ging nicht, kommt persönlich.
A-06;2026-08-07;Telefon;Unterlagen;Braucht es den Mietvertrag im Original?
A-07;2026-08-10;Telefon;Online-Formular;Formular akzeptiert keine Fotos vom Handy.
A-08;2026-08-11;E-Mail;Frist;Busse wegen verspäteter Anmeldung befürchtet.
A-09;2026-08-12;Telefon;Unterlagen;Heimatschein noch nicht da, reicht eine Bestellbestätigung?
A-10;2026-08-13;Telefon;Anderes;Herr Gerber fragt nach einer Parkkarte für Anwohnende.
A-11;2026-08-14;Telefon;Online-Formular;Upload bricht ab, zweiter Versuch ebenfalls.
A-12;2026-08-17;E-Mail;Unterlagen;Liste der Unterlagen auf der Website nicht gefunden.
A-13;2026-08-18;Telefon;Frist;Wie lange dauert die Bestätigung?
A-14;2026-08-19;Schalter;Unterlagen;Unterlagen unvollständig, Mietvertrag fehlte.
A-15;2026-08-20;Telefon;Online-Formular;Formular verlangt Heimatschein als PDF, hat nur Papier.
A-16;2026-08-21;E-Mail;Unterlagen;Welche Unterlagen braucht es für Kinder?
A-17;2026-08-24;Telefon;Frist;Bestätigung nach drei Wochen noch nicht erhalten.
A-18;2026-08-25;Schalter;Online-Formular;Online gescheitert, Anmeldung am Schalter erledigt.
A-19;2026-08-26;E-Mail;Unterlagen;Reicht eine Kopie des Mietvertrags?
A-20;2026-08-27;Telefon;Anderes;Frage zu Abfallmarken.
```
