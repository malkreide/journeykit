Du extrahierst Evidenz-Atome aus der Quelle «Interview H1 – Anmeldung im Hort und Elternbeitrag» (interview, Klasse reported).
Regeln:
- Ein Atom pro belegbarer Aussage. Zitate wörtlich, mit Fundstelle (Zeile/Zeitstempel/ID).
- emotion_hint nur, wenn die Emotion im Text steht; explicit true nur bei ausdrücklicher Nennung.
- signal setzen; breakdown nur, wenn die Person scheitert oder ausweicht (Anruf, Schalter, Aufgeben).
- phase_hint aus dieser Liste: orientierung, anmeldung, warten, eintritt, kosten. persona_hint: berufstaetig.
- Keine Personendaten im text (Namen, Orte, Kontaktangaben ersetzen).
- Widerspricht eine Aussage einer bekannten Soll-Aussage, contradicts setzen: doc-02: «Die Eltern erhalten innert zwei Wochen nach dem Anmeldeschluss einen Bescheid.»; doc-03: «Anmeldungen sind online oder am Schalter im Schulhaus möglich.»; doc-05: «Alle Tarife der Tagesbetreuung sind auf der Website vollständig publiziert.».
Gib ausschliesslich ein JSON-Array von Atomen nach journeykit-Schema aus, IDs mit Präfix «h1-».

Quelle «input.md»:

```
# Interview H1 – Anmeldung im Hort und Elternbeitrag (synthetisch)

Gemeinde Musterau, Abteilung Bildung, Tagesbetreuung. Interview vom 2026-09-28, 45 Minuten. Befragte Person: Mutter, Sohn seit August in der ersten Klasse, arbeitet 60 Prozent. Namen sind erfunden.

[00:10] I: Danke, dass Sie sich Zeit nehmen. Wir nehmen das Gespräch auf, ist das in Ordnung?
[00:18] H1: Ja, kein Problem.
[00:35] I: Erzählen Sie zuerst, warum Sie einen Hortplatz gesucht haben.
[00:44] H1: Unser Sohn kam im August in die erste Klasse, und ich wollte nach der Elternzeit wieder sechzig Prozent arbeiten. Ohne Hort geht das bei uns nicht.
[01:20] I: Wie haben Sie erfahren, wie die Anmeldung läuft?
[01:31] H1: Von einer anderen Mutter beim Abholen in der Kita. Die hat mich gefragt, ob wir schon angemeldet sind, und da habe ich zum ersten Mal vom Anmeldeschluss gehört.
[02:05] H1: Der Anmeldeschluss war Ende März. Wir haben uns Mitte April angemeldet, und da hiess es, wir kommen auf die Warteliste.
[02:50] I: Wie lief die Anmeldung selbst?
[02:58] H1: Das Formular auf der Website habe ich gar nicht selbst ausgefüllt. Ich lag damals mit einer Lungenentzündung im Spital, das hat meine Schwiegermutter für mich gemacht, mit meinem Login.
[03:40] H1: Den Arbeitsvertrag konnte sie nicht hochladen, die Datei war zu gross. Sie hat ihn dann ausgedruckt und im Sekretariat im Schulhaus abgegeben.
[04:25] I: Und dann?
[04:30] H1: Dann haben wir gewartet. Auf der Website steht, man bekommt innert zwei Wochen nach dem Anmeldeschluss Bescheid. Bei uns waren es fünf Wochen – nein, warten Sie, sieben. Ich habe es extra nachgeschaut: sieben Wochen.
[05:15] H1: In der Zeit habe ich dreimal im Sekretariat angerufen und nie jemanden erreicht.
[05:40] H1: Am Schluss habe ich eine E-Mail geschrieben. Die Antwort kam nach vier Tagen, aber da stand nur, ich solle Geduld haben.
[06:20] H1: Ich war richtig verzweifelt, weil ich meinem Arbeitgeber zusagen musste, ab wann ich wieder komme.
[06:58] H1: Weil der Bescheid so spät kam, konnte ich erst Ende Juni zusagen. Mein Chef war nicht begeistert.
[07:30] I: Wie war der Start im Hort?
[07:38] H1: Die Leiterin vom Hort, Frau Brunner, hat sich am ersten Tag eine halbe Stunde Zeit genommen und uns alles gezeigt. Das war wirklich gut.
[08:15] H1: Unser Sohn hat in der ersten Woche jeden Abend geweint und wollte nicht mehr hin.
[08:52] I: War das für Sie belastend?
[09:00] H1: Ja, schon.
[09:20] I: Sprechen wir über die Kosten.
[09:26] H1: Der Elternbeitrag ist bei uns 23 Franken pro Betreuungstag, das wussten wir vom Tarifrechner auf der Website.
[10:02] H1: Dass das Mittagessen noch einmal 9 Franken pro Tag kostet, hat uns niemand gesagt. Das haben wir erst auf der ersten Rechnung gesehen.
[10:45] H1: Die Rechnung kommt jeden Monat, im September waren es 412 Franken. Das ist für uns viel Geld, aber es geht.
[11:20] H1: Wir haben eine Ermässigung beantragt, aber das Formular verlangt die Steuerveranlagung vom letzten Jahr, und die hatten wir noch nicht.
[12:05] I: Was würden Sie sich wünschen?
[12:12] H1: Dass man online sieht, auf welchem Platz der Warteliste man steht. Dann hätte ich wenigstens planen können.
[12:50] H1: Und dass die Kosten fürs Essen gleich beim Tarif stehen.
[13:20] I: Gibt es noch etwas, das Sie sagen möchten?
[13:25] H1: Nein, eigentlich nicht. Danke, dass Sie fragen.
```
