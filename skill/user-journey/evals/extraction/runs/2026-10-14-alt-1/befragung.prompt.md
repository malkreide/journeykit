Du extrahierst Evidenz-Atome aus der Quelle «Elternbefragung Tagesbetreuung 2026» (survey, Klasse reported).
Regeln:
- Ein Atom pro belegbarer Aussage. Zitate wörtlich, mit Fundstelle (Zeile/Zeitstempel/ID).
- emotion_hint nur, wenn die Emotion im Text steht; explicit true nur bei ausdrücklicher Nennung.
- signal setzen; breakdown nur, wenn die Person scheitert oder ausweicht (Anruf, Schalter, Aufgeben).
- phase_hint aus dieser Liste: orientierung, anmeldung, warten, eintritt, kosten. persona_hint: berufstaetig.
- Keine Personendaten im text (Namen, Orte, Kontaktangaben ersetzen).
- Widerspricht eine Aussage einer bekannten Soll-Aussage, contradicts setzen: keine.
Gib ausschliesslich ein JSON-Array von Atomen nach journeykit-Schema aus, IDs mit Präfix «bef-».

Quelle «input.md»:

```
# Elternbefragung Tagesbetreuung 2026 – Auswertung (synthetisch)

Gemeinde Musterau, Abteilung Bildung. Online-Befragung im Juni 2026 bei allen Eltern mit einem Kind im Hort. Rücklauf: 286 von 512 Fragebogen (56 %). Namen in den Freitexten sind erfunden.

## Geschlossene Fragen

Zustimmung = Anteil «trifft eher zu» und «trifft voll zu» an allen, die die Frage beantwortet haben. n = Anzahl Antworten auf die Frage.

| Frage | Wortlaut | n | Zustimmung | weiss nicht |
|---|---|---|---|---|
| F1 | Ich wusste rechtzeitig, bis wann ich mein Kind anmelden muss. | 286 | 47 % | 6 % |
| F2 | Die Anmeldung über die Website war einfach. (nur Eltern, die online angemeldet haben) | 201 | 71 % | 2 % |
| F3 | Ich wusste vor der ersten Rechnung, was die Betreuung insgesamt kostet. | 286 | 38 % | 9 % |
| F4 | Die Wartezeit bis zum Bescheid war zu lang. | 286 | 64 % | 11 % |
| F5 | Ich bin mit der Betreuung im Hort zufrieden. | 286 | 88 % | 3 % |
| F6 | Ich konnte die Ermässigung ohne Hilfe beantragen. (nur Eltern, die eine Ermässigung beantragt haben) | 52 | 31 % | 4 % |
| F7 | Die Informationen gab es in einer Sprache, die ich gut verstehe. | 286 | 79 % | 1 % |
| F8 | wie F7, nur Eltern mit einer anderen Erstsprache als Deutsch | 14 | 36 % | 0 % |

## Freitext F9: «Was sollten wir verbessern?»

Alle Antworten, ungekürzt, in der Reihenfolge des Eingangs.

1. Mehr Plätze.
2. Wir haben erst durch Zufall erfahren, dass es einen Anmeldeschluss gibt.
3. Das Mittagessen kostet extra, das stand nirgends.
4. Mein Mann hat die Anmeldung gemacht, weil ich mit dem Formular auf Deutsch nicht zurechtkam.
5. Die Betreuerinnen sind toll, mein Kind geht gern hin.
6. Frau Meier im Sekretariat hat mir am Telefon alles erklärt, ohne sie hätte ich aufgegeben.
7. Die Warteliste ist eine Blackbox. Niemand sagt einem, wo man steht.
8. Keine Angabe.
9. Für Schichtarbeit passen die Öffnungszeiten nicht. Wir können frühestens um halb sieben abholen, der Hort schliesst um sechs.
```
