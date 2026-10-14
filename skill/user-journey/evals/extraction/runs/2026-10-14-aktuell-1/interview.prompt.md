Du extrahierst Evidenz-Atome aus der Quelle «Interview U1 – Wohnsitzanmeldung nach Umzug» (source_ref «int-u1», interview, Klasse reported).
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
Gib ausschliesslich ein JSON-Array von Atomen nach journeykit-Schema aus, IDs mit Präfix «u1-», source_ref «int-u1».

Quelle «input.md»:

```
# Interview U1 – Wohnsitzanmeldung nach Umzug (synthetisch)

Gemeinde Musterau, Einwohnerdienste. Interview vom 2026-09-14, 40 Minuten. Befragte Person: aus einem anderen Kanton zugezogen, berufstätig. Namen sind erfunden.

[00:40] I: Erzählen Sie, wie Sie nach dem Umzug erfahren haben, dass Sie sich anmelden müssen.
[00:52] U1: Das hat mir die Vermieterin bei der Schlüsselübergabe gesagt. Vorher wusste ich nicht, dass man nur vierzehn Tage Zeit hat.
[01:30] I: Wie sind Sie dann vorgegangen?
[01:41] U1: Ich wollte es online machen, auf der Website der Gemeinde. Dort stand, ich brauche den Heimatschein. Ich hatte keine Ahnung, was das ist.
[02:20] U1: Ehrlich gesagt hatte ich richtig Angst, dass ich eine Busse bekomme, weil die vierzehn Tage schon fast vorbei waren.
[03:05] U1: Den Heimatschein musste ich bei meiner alten Gemeinde bestellen. Das ging per Post und hat neun Tage gedauert.
[03:48] U1: Das Online-Formular hat dann beim Hochladen immer abgebrochen. Nach dem dritten Versuch habe ich aufgegeben und bin an den Schalter gegangen.
[04:30] U1: Am Schalter war die Frau sehr freundlich, in zehn Minuten war alles erledigt.
[05:02] I: Gab es jemanden, der Ihnen geholfen hat?
[05:10] U1: Meine Nachbarin, Frau Roth, hat mir gezeigt, welche Unterlagen ich kopieren muss. Ohne sie hätte ich nicht gewusst, dass es auch den Mietvertrag braucht.
[05:55] U1: Die Bestätigung kam dann zwei Wochen später per Post. Ich weiss bis heute nicht, ob das normal ist.
[06:30] U1: Was ich mir wünschen würde: eine Liste am Anfang, was man alles braucht. Dann wäre ich viel ruhiger gewesen.
```
