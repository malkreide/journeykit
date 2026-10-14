Du extrahierst Evidenz-Atome aus der Quelle «Beschwerde per E-Mail: Mahnung Elternbeitrag Hort» (source_ref «beschwerde-0922», complaint, Klasse reported).
Regeln:
- Ein Atom pro belegbarer Aussage, nicht pro Satz: Sätze desselben Redebeitrags, die zusammen eine Aussage machen, bleiben ein Atom. Nur bei Interviews (auch Fokusgruppen): Ein kurzer Redebeitrag (bis drei Sätze) bleibt ein Atom, auch wenn er Ursache und Folge oder Problem und Ausweg nennt; wechselt ein langer Redebeitrag das Thema oder den Schritt, wird jede Aussage ein eigenes Atom mit derselben Fundstelle. Dieselbe Aussage nie doppelt erfassen (nicht als Zitat und zusätzlich als Messwert).
- Zitate wörtlich, mit Fundstelle (Zeile/Zeitstempel/ID). Kürzen mit «…» ist erlaubt; Namen und andere Personendaten im Zitat durch «[Name]», «[Ort]» ersetzen.
- Nennt ein Zitat eine Zahl oder Dauer, value und unit im selben Atom ergänzen.
- emotion_hint nur, wenn die Emotion im Text steht; explicit true nur bei ausdrücklicher Nennung.
- signal setzen (friction, breakdown, positive, need, workaround, neutral); breakdown nur, wenn die Person scheitert oder ausweicht (Anruf, Schalter, Aufgeben).
- channel_hint nur mit diesen Werten: web, app, email, phone, letter, paper_form, counter, in_person, event, chat, sms, publication, other.
- phase_hint aus dieser Liste: orientierung, anmeldung, warten, eintritt, kosten. persona_hint: berufstaetig.
- Keine Personendaten im text (Namen, Orte, Kontaktangaben ersetzen).
- Widerspricht eine Aussage einer bekannten Soll-Aussage, contradicts setzen: doc-01: «Gesuche um Ermässigung können online oder auf Papier eingereicht werden.»; doc-04: «Gesuche um Ermässigung werden innert 20 Arbeitstagen entschieden.»; doc-07: «Die Mahnung weist auf die Mahngebühr von 40 Franken hin.».
Gib ausschliesslich ein JSON-Array von Atomen nach journeykit-Schema aus, IDs mit Präfix «bes-», source_ref «beschwerde-0922».

Quelle «input.md»:

```
# Beschwerde per E-Mail an die Abteilung Bildung (synthetisch)

Gemeinde Musterau, Abteilung Bildung, Tagesbetreuung. Eingang 2026-09-22. Für den Testsatz mit Zeilennummern versehen; Namen sind erfunden.

01 Betreff: Mahnung Elternbeitrag Hort – Beschwerde
02
03 Sehr geehrte Damen und Herren
04
05 Ich schreibe Ihnen, weil ich mit dem Vorgehen Ihrer Abteilung überhaupt nicht einverstanden bin.
06 Im Februar habe ich eine Ermässigung des Elternbeitrags beantragt. Das Gesuch hat mein Treuhänder für mich eingereicht, mit Vollmacht, weil er auch meine Steuern macht.
07 Gemäss Ihrer Website erhalten Gesuchstellende innert 20 Arbeitstagen einen Entscheid.
08 Ihr Entscheid kam nach elf Wochen, und zwar an meine alte Adresse, obwohl ich den Umzug im März gemeldet hatte.
09 Weil ich den Entscheid nie erhalten habe, wusste ich nicht, dass ich noch eine Lohnabrechnung nachreichen muss. Die Frist dafür ist abgelaufen, und die Ermässigung wurde abgelehnt.
10 Ende August kam dann eine Mahnung über den vollen Beitrag von 1'236 Franken für die Monate Mai bis Juli.
11 Dazu kam eine Mahngebühr von 40 Franken, und dass eine solche Gebühr anfällt, stand in keinem Ihrer Schreiben.
12 Ich habe zweimal die Nummer auf der Mahnung angerufen. Beide Male kam nur eine Ansage, das Büro sei geschlossen.
13 Am 9. September bin ich deshalb am Schalter im Gemeindehaus vorbeigegangen. Dort sagte man mir, man könne nichts machen, ich müsse schriftlich Beschwerde einreichen.
14 Vielen Dank auch für die schnelle und unkomplizierte Hilfe.
15 Ich bin wütend und fühle mich von Ihrer Verwaltung nicht ernst genommen.
16 Ich verlange, dass Sie mein Gesuch neu prüfen und die Mahngebühr streichen.
17 Ausserdem wünsche ich mir, dass Entscheide per E-Mail kommen, wenn man das im Gesuch so angibt.
18
19 Freundliche Grüsse
20 Sandra Imhof
```
