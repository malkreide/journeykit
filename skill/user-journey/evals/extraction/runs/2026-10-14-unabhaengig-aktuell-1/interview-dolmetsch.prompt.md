Du extrahierst Evidenz-Atome aus der Quelle «Interview D3 – Einschulung nach Zuzug, mit Dolmetscherin» (source_ref «int-d3», interview, Klasse reported).
Regeln:
- Ein Atom pro belegbarer Aussage, nicht pro Satz: Sätze desselben Redebeitrags, die zusammen eine Aussage machen, bleiben ein Atom. Dieselbe Aussage nie doppelt erfassen (nicht als Zitat und zusätzlich als Messwert).
- Zitate wörtlich, mit Fundstelle (Zeile/Zeitstempel/ID). Kürzen mit «…» ist erlaubt; Namen und andere Personendaten im Zitat durch «[Name]», «[Ort]» ersetzen.
- Nennt ein Zitat eine Zahl oder Dauer, value und unit im selben Atom ergänzen.
- emotion_hint nur, wenn die Emotion im Text steht; explicit true nur bei ausdrücklicher Nennung.
- signal setzen (friction, breakdown, positive, need, workaround, neutral); breakdown nur, wenn die Person scheitert oder ausweicht (Anruf, Schalter, Aufgeben).
- channel_hint nur mit diesen Werten: web, app, email, phone, letter, paper_form, counter, in_person, event, chat, sms, publication, other.
- phase_hint aus dieser Liste: ankunft, anmeldung, einschulung, alltag. persona_hint: zugezogen-fremdsprachig.
- Keine Personendaten im text (Namen, Orte, Kontaktangaben ersetzen).
- Widerspricht eine Aussage einer bekannten Soll-Aussage, contradicts setzen: keine.
Gib ausschliesslich ein JSON-Array von Atomen nach journeykit-Schema aus, IDs mit Präfix «d3-», source_ref «int-d3».

Quelle «input.md»:

```
# Interview D3 – Einschulung nach Zuzug, mit Dolmetscherin (synthetisch)
Gemeinde Musterau, Schulverwaltung. Interview vom 2026-10-02, etwa 35 Minuten. Befragte Person: Vater von zwei Kindern (Kindergarten, Primarschule), übersetzt von einer interkulturellen Dolmetscherin. Namen sind erfunden.

[00:00] I: So, ich glaube, es läuft. Ja, das rote Licht ist an. Also, nochmals grüezi, Herr Weldu, und merci vielmals, dass Sie gekommen sind. Ihnen auch, Frau Asfaha. Ich sage es fürs Protokoll nochmals kurz: Ich bin von der Schulverwaltung, und wir möchten besser verstehen, wie es für Familien ist, die neu nach Musterau kommen, mit Kindern, die in den Kindergarten oder in die Schule gehen. Was gut gegangen ist und was, äh, weniger gut. Es gibt keine richtigen oder falschen Antworten. Wir nehmen das Gespräch auf, nachher wird es abgeschrieben, und die Namen werden geändert. Und es hat keinen Einfluss auf Ruta und Abel in der Schule. Ist das für Sie in Ordnung?

[00:45] D: [spricht Tigrinya]

[01:20] V: [spricht Tigrinya] Ja. Okay, okay.

[01:28] D: Er sagt, ja, das ist in Ordnung. Er hat noch gefragt, ob die Lehrerin die Aufnahme hört. Ich habe gesagt, ich glaube nicht, das bleibt bei der Gemeinde. Stimmt das so?

[01:43] I: Ja, das stimmt, die Lehrpersonen bekommen das nicht. Gut. Dann vielleicht ganz am Anfang: Wann sind Sie nach Musterau gekommen, mit wem – und waren die Kinder vorher schon einmal in einer Schule?

[02:00] D: [spricht Tigrinya]

[02:15] V: [spricht Tigrinya]

[03:10] D: Also, wir sind letztes Jahr in die Schweiz gekommen, im September. Zuerst waren wir in einem Zentrum, ungefähr sechs Wochen, ich weiss nicht mehr, wie der Ort heisst. Dann nach Musterau, mit meiner Frau und den zwei Kindern. Ruta war acht, Abel vier. Wann genau, das weiss er nicht mehr, Ende Oktober oder schon November. Zur Schule: Ruta war vorher ein Jahr in der Schule, in der ersten Klasse, auf Tigrinya. Sie kann die Tigrinya-Buchstaben ein bisschen lesen, aber nicht die Buchstaben von hier. Im Zentrum ist sie ein paar Mal am Morgen in die Schule gegangen, aber da haben sie mehr gezeichnet und gesungen. Abel war nirgends. Bei uns kommt man mit sieben in die Schule, einen Kindergarten gibt es schon, aber den muss man bezahlen, und viele gehen nicht.

[04:06] I: Mhm. Und als Sie dann hier in Musterau angekommen sind, wer hat Ihnen am Anfang geholfen? Und wie haben Sie erfahren, wann und wo die Kinder in die Schule können?

[04:19] D: [spricht Tigrinya]

[04:30] V: [spricht Tigrinya] … Sandra … [spricht Tigrinya] … zwei Woche, drei Woche … [spricht Tigrinya]

[06:05] D: Das war jetzt lang, ich fasse ein bisschen zusammen. Geholfen hat die Sozialarbeiterin, er sagt Sandra – den Nachnamen weiss ich nicht, sie ist vom Sozialdienst. Sie hat ihnen die Wohnung gezeigt und ist mit ihnen auf die Gemeinde gegangen, an den Schalter, für die Anmeldung. Dort hat die Frau am Schalter gesagt, so hat er es verstanden: «Die Schule kommt.» Dann hat er gewartet, zwei oder drei Wochen. Dann ist ein Brief gekommen, auf Deutsch. Aber am Anfang kommen so viele Briefe, von der Krankenkasse, von der Gemeinde, von der Bank, alle im weissen Couvert mit Fenster. Er hat ihn auf den Tisch gelegt, zu den anderen. Am Sonntag nach der Kirche hat dann ein Mann aus der Kirche, der schon lange hier ist, die Briefe angeschaut und gesagt: Das ist von der Schule, ihr habt am Dienstag einen Termin. Und es war ein Formular dabei, das musste man zum Termin mitbringen. Das haben sie am Sonntagabend zusammen ausgefüllt, bis spät. Welche Sprache spricht das Kind, wie viele Jahre Schule, Impfungen, Allergien und so weiter. Bei den Impfungen haben sie nichts hingeschrieben, weil die Impfbüchlein bei der Sozialarbeiterin waren.

[07:25] I: Habe ich das richtig verstanden – bei «Die Schule kommt» hat er gedacht, jemand kommt zu Ihnen nach Hause?

[07:33] D: Ja, genau, so hat er es gesagt. Er hat gedacht, jemand von der Schule kommt vorbei und schaut die Kinder an, oder holt sie ab. Darum hat er auch nicht angerufen. Er wusste auch nicht, wo.

[07:48] I: Mhm. Dann erzählen Sie doch vom Termin am Dienstag. Wer war dabei, und was wurde entschieden?

[07:56] D: [spricht Tigrinya]

[08:03] V: [spricht Tigrinya]

[09:13] D: Dabei waren die Schulleiterin und die Lehrerin, und am Telefon eine –

[09:17] V: Nein. Nicht Lehrerin. Sekretärin.

[09:20] D: Ah, Entschuldigung. [spricht Tigrinya] Ja, die Sekretärin, nicht die Lehrerin. Also die Schulleiterin und die Sekretärin, und eine Dolmetscherin am Telefon. Das Telefon lag auf dem Tisch, mit Lautsprecher. Die Frau am Telefon hat gut Tigrinya gesprochen, aber man hat schlecht gehört, und manchmal haben zwei gleichzeitig geredet, dann hat sie gesagt «bitte nochmals». Er hat vielleicht die Hälfte verstanden. Die Kinder waren auch dabei und seine Frau – das hat er mir vorher im Gang erzählt, jetzt hat er es nicht gesagt. Er war die ganze Zeit nervös, weil Abel unter dem Tisch herumgekrochen ist. Entschieden haben sie: Ruta kommt in die zweite Klasse, im grossen Schulhaus, und bekommt dazu Deutschunterricht. Sie soll in der nächsten Woche anfangen. Abel kommt in den Kindergarten, aber nicht in den bei uns in der Nähe, sondern in den oben beim Wald, weil der in der Nähe voll ist. Und Abel soll erst nach den Weihnachtsferien anfangen, weil es bis Weihnachten nur noch zwei, drei Wochen sind, und im Januar kann er dann in Ruhe anfangen. Am Schluss hat er einen Stapel Papiere bekommen, er sagt, zehn Blätter, vielleicht mehr.

[10:42] I: Mhm. Und diese Papiere – wissen Sie noch, was das war? Und dann der Mittagstisch, hat das geklappt? Und, äh, wer hat am Mittag geschaut, und wissen Sie, was das kostet?

[10:57] D: Das sind jetzt viele Fragen auf einmal, ich stelle sie ihm nacheinander. [spricht Tigrinya]

[11:25] V: [spricht Tigrinya] Ferienplan … [spricht Tigrinya] Mittagstisch nein. (lacht) [spricht Tigrinya]

[12:25] D: Den Ferienplan hat er erkannt, wegen der Daten. Ein Blatt war für den Mittagstisch, eins vom Zahnarzt, und viele mit viel Text, er weiss nicht, was das war. Er hat alles der Sozialarbeiterin gezeigt, aber sie hatte erst nach zwei Wochen oder so Zeit, weil sie so viele Familien hat. Sie hat gesagt, das meiste ist nur Information, wichtig sind der Mittagstisch und der Zahnarzt. Beim Mittagstisch stand auf dem Blatt, man muss sich bis zu einem Datum im Monat vorher anmelden, er glaubt, bis zum Fünfzehnten. Und als die Sozialarbeiterin es gelesen hat, war das Datum schon vorbei. Darum konnte Ruta erst ab Februar in den Mittagstisch, nicht schon im Januar. Bis dahin hat er sie jeden Mittag geholt und wieder gebracht. Was es kostet, weiss er nicht genau, neun Franken oder elf, die Rechnung geht direkt an den Sozialdienst.

[13:27] I: Mhm. Und wie ist das mit den Wegen? Sie haben ja zwei Kinder an zwei verschiedenen Orten.

[13:34] D: [spricht Tigrinya]

[13:40] V: [spricht Tigrinya]

[14:25] D: Das ist für mich das grösste Problem, nicht nur am Anfang, eigentlich bis heute. Ruta ist im grossen Schulhaus, Abel im Kindergarten beim Wald, und das ist in die andere Richtung. Der Kindergarten geht am Morgen von Viertel nach acht bis zehn vor zwölf, die Schule hat andere Zeiten, und am Mittwoch ist es wieder anders. Meine Frau hat jeden Morgen Deutschkurs in der Stadt, mit dem Bus eine halbe Stunde. Also laufe ich den ganzen Morgen hin und her. Ich bin das Taxi, aber ohne Auto. (lacht) Die Sozialarbeiterin hat mir am Anfang ein Programm angeboten, am Morgen, mit Deutsch und auch mit Arbeit, aber ich musste absagen, weil wer bringt dann die Kinder? Jetzt habe ich einen Abendkurs, zweimal in der Woche. Die Sozialarbeiterin hat gesagt, man sucht eine Lösung. Bis jetzt gibt es keine.

[15:25] I: (lacht) Ja. Ich komme nachher nochmals auf den Kindergarten. Zuerst zu Ruta: Wie war der Anfang in der Schule? Der erste Tag, die ersten Wochen?

[15:37] D: [spricht Tigrinya]

[15:46] V: [spricht Tigrinya] (lacht) [spricht Tigrinya]

[16:36] D: Er lacht, weil am ersten Tag ist ein Mann gekommen mit einem roten Mantel und einem langen weissen Bart, mit einem Sack, und hat Nüssli und Mandarinen verteilt. Ruta hatte grosse Angst, sie hat geweint, und die Lehrerin hat sie auf den Schoss genommen. Zu Hause hat sie gesagt, sie geht nie mehr in die Schule. Aber am nächsten Tag ist sie trotzdem gegangen. Und in den ersten Wochen: Ruta geht jeden Tag eine Stunde aus der Klasse raus, zu einer anderen Lehrerin, in ein kleines Zimmer. Am Anfang hat er nicht verstanden, warum. Er hat gedacht, vielleicht ist sie nicht gut genug, oder sie darf nicht bei den anderen sein, weil sie neu ist. Oder weil sie schwarz ist. Er hat sich Sorgen gemacht, aber er hat niemanden gefragt.

[17:31] I: Mhm. Also, der Mann mit dem Bart, das war der Samichlaus, der kommt immer so um den sechsten Dezember. Das ist interessant, weil, äh, bei uns ist bei Ruta als Eintritt der erste Dezember eingetragen. Und das kleine Zimmer, das ist der DaZ-Unterricht, also Deutsch als Zweitsprache. Hat ihm das irgendwann jemand erklärt?

[17:53] D: [spricht Tigrinya]

[18:11] V: Nein. Nein. [spricht Tigrinya] Ruta. [spricht Tigrinya]

[18:41] D: Zuerst zum Datum: Er sagt nein, der erste Tag war der Tag mit dem Samichlaus, da ist er ganz sicher. Vorher war sie keinen Tag in der Schule. Und das Zimmer hat ihm Ruta selber erklärt, nach ein paar Wochen. Sie hat gesagt, das ist die Deutschschule, dort sind auch Kinder aus anderen Ländern, und man macht Spiele. Dann war er beruhigt. Von der Schule hat es ihm niemand erklärt. – Er hat vorher «jeden Tag» gesagt, ich frage nochmals nach. [spricht Tigrinya]

[19:13] V: [spricht Tigrinya] Mittwoch nicht.

[19:18] D: Nicht am Mittwoch. Also viermal in der Woche.

[19:22] I: Gut, danke. Wie bekommen Sie denn Informationen von der Schule? Von der Lehrerin zum Beispiel.

[19:29] D: [spricht Tigrinya]

[19:35] V: Handy. App. [spricht Tigrinya]

[20:10] D: Über eine App auf dem Handy, die Sozialarbeiterin hat ihm geholfen, sie zu installieren. Es kommen viele Nachrichten, fast jeden Tag. In der App gibt es einen Knopf zum Übersetzen, aber Tigrinya hat es dort nicht. Er nimmt Englisch, er kann ein bisschen Englisch, aber nicht gut. Oder er kopiert den Text in eine andere App, die kann Tigrinya, aber manchmal kommt etwas ganz Komisches raus. Einmal stand dort, Ruta muss einen Vogel mitbringen. Einen kleinen Vogel, fürs Schulzimmer. Er hat gedacht, vielleicht ist das für den Unterricht, für Biologie, und er wusste nicht, wo man so einen Vogel kauft.

[20:55] I: Einen Vogel? (lacht) Ah – das waren sicher die Finken! Die Hausschuhe, die heissen bei uns Finken, wie der Vogel. Hatte Ruta dann Finken?

[21:07] D: (lacht) Ja, natürlich, die Finken. Ich erkläre es ihm kurz. [spricht Tigrinya]

[21:27] V: Ah! Finken! (lacht) [spricht Tigrinya]

[21:57] D: Jetzt hat er es verstanden. Nein, die erste Zeit hatte sie keine, sie war in den Socken. Die Lehrerin hat dann nochmals geschrieben, und Ruta hat zu Hause geweint, weil alle anderen Finken haben und sie nicht. Dann sind sie mit der Nachbarin ins Brockenhaus. Er sagt, so etwas hätte er gern am Anfang gewusst: eine Liste, was das Kind braucht. Finken, Thek, Turnsack, was für ein Znüni, für den Kindergarten Regenhosen. Es kam alles einzeln, immer erst dann, wenn es schon fehlt.

[22:33] I: Mhm. Sie sagen Regenhosen – wie war denn der Anfang im Kindergarten für Abel?

[22:39] D: [spricht Tigrinya]

[22:45] V: [spricht Tigrinya] … Bilder gut … [spricht Tigrinya]

[23:50] D: Abel hat nach Neujahr angefangen. Die ersten Tage musste ich am Morgen dabeibleiben, drei Morgen, damit Abel sich gewöhnt. Das war gut. Aber am Donnerstag ist immer Waldtag, und das wusste er nicht. Abel kam mit normalen Hosen und Turnschuhen, es hat geregnet, und er ist ganz nass und dreckig nach Hause gekommen und hat gefroren. Am nächsten Tag hat ihm die Kindergärtnerin einen Zettel gegeben, mit Bildern drauf: Stiefel, Regenhose, Mütze, Handschuhe. Das hat er verstanden, wegen den Bildern. Sie macht das immer so, auch jetzt noch: Sie schickt Fotos in die App, was die Kinder gemacht haben, und Bilder, was man mitbringen muss. Das gefällt ihm sehr. Bei der Schule von Ruta ist es mehr Text. Und einmal, im Frühling, ist er am Morgen mit Abel zum Kindergarten gekommen, und die Tür war zu, niemand war da. Er hat eine Viertelstunde gewartet, dann hat eine Frau, die vorbeigekommen ist, gesagt: Heute ist keine Schule. Warum, weiss er bis heute nicht.

[25:08] I: Das war wahrscheinlich ein Weiterbildungstag, die stehen, äh, im Ferienplan oder in einem Elternbrief. Und wie kommt Abel in den Kindergarten beim Wald? Und hat man Ihnen erklärt, warum er nicht in den in der Nähe gehen kann?

[25:26] D: [spricht Tigrinya]

[25:40] V: [spricht Tigrinya]

[26:35] D: Er bringt ihn zu Fuss, zwanzig Minuten, mit Abel eher fünfundzwanzig, weil er langsam ist. Ein Velo hat er nicht. Dazwischen ist die grosse Strasse, mit viel Verkehr, auch Lastwagen. Es hat einen Fussgängerstreifen, aber kein Lichtsignal. Im Frühling hat die Kindergärtnerin gesagt, Abel soll jetzt allein gehen oder mit den anderen Kindern, das ist gut für die Selbstständigkeit. Er sagt, das macht er nicht. Ein Kind mit fünf allein über diese Strasse, nein. Bei uns gehen die Kinder auch allein, aber nicht so klein, und es hat nicht so viele Autos. Zum Kindergarten in der Nähe: Sie haben gesagt, er ist voll. Aber im Frühling ist ein Mädchen ins gleiche Haus gezügelt, auch neu, und sie geht in den Kindergarten in der Nähe. Er fragt sich, warum. Vielleicht, weil sie Deutsch kann und Abel nicht. Aber er weiss es nicht, und er möchte sich nicht beklagen. Er hat die Kindergärtnerin im Juni gefragt, ob Abel wechseln kann, und sie hat gesagt, das entscheidet die Schulleitung. Wie man die Schulleitung fragt, weiss er nicht. Mit einem Brief? Er hat es dann nicht gemacht.

[27:51] V: Abel allein? Nein. Zu gefährlich.

[27:55] I: (lacht) Das habe ich verstanden. Und danke, dass Sie das mit dem Kindergarten sagen. Ich mache die Einteilung nicht selber, ich kann das jetzt nicht beantworten, aber ich nehme es auf. – Gab es mit der Schule auch Elterngespräche, mit Dolmetscherin?

[28:12] D: Bei einem war ich dabei, im März. Ich frage ihn trotzdem. [spricht Tigrinya]

[28:21] V: [spricht Tigrinya]

[29:31] D: Im März war ein Gespräch mit der Lehrerin von Ruta, mit mir als Dolmetscherin. Das war gut, er hat alles verstanden. Aber die Lehrerin hat gesagt, Ruta ist sehr still und liest langsam, und sie möchte, dass Ruta beim Schulpsychologischen Dienst abgeklärt wird. Und er hat gedacht, Psychologe ist für Leute, die krank im Kopf sind. Er hatte grosse Angst, dass man Ruta in eine andere Schule tut, eine Schule für Kranke. Er hat in dieser Nacht nicht geschlafen. Ruta war dann zweimal dort, mit einer Dolmetscherin, nicht mit mir. Im Juli ist ein Brief gekommen, vier Seiten, auf Deutsch. Der Mann aus der Kirche war in den Ferien, die Sozialarbeiterin auch. Nach den Sommerferien hat die Lehrerin ihm gesagt, mündlich, dass alles gut ist, Ruta ist nicht krank, sie braucht Zeit und Deutsch. Das hat ihn sehr gefreut. Aber im Brief steht noch etwas von einer Förderung, und er weiss nicht, ob Ruta jetzt noch etwas dazu bekommt oder nicht. Er hat den Brief mitgebracht. Ah, und gewartet haben sie lange, das hat er am Anfang gesagt: Das Gespräch war im März, der Termin beim Schulpsychologen im Juni, also drei Monate.

[30:47] V: Juni – nein. Ende Juni. Fast Ferien.

[30:51] D: Ja, er korrigiert: Der Termin war Ende Juni, kurz vor den Sommerferien. Also fast vier Monate. – Darf ich da noch etwas von mir aus sagen? Ich habe es im Gespräch im März versucht zu erklären, aber das Wort, das man auf Tigrinya für Psychologe braucht, das braucht man eigentlich nur für psychisch Kranke. Darum haben viele Familien Angst, wenn sie das hören. Das ist jetzt meine Erfahrung, nicht von ihm.

[31:21] I: Danke, das ist sehr hilfreich. Den Brief schauen wir nachher gern zusammen an, wenn Sie noch Zeit haben, Frau Asfaha. – Wir kommen langsam zum Schluss. Eine letzte Frage: Wenn jetzt eine andere Familie neu nach Musterau kommt, mit Kindern, so wie Sie letztes Jahr – was müsste die Schule anders machen? Was hätte Ihnen am meisten geholfen?

[31:48] D: Ja, ich habe nachher noch Zeit. [spricht Tigrinya]

[32:08] V: [spricht Tigrinya] (Pause) [spricht Tigrinya]

[33:23] D: Er hat mehreres gesagt, ich fasse zusammen. Erstens: am Anfang ein Gespräch mit einer Dolmetscherin, die im Zimmer sitzt, nicht am Telefon. Und dort alles erklären: wie die Schule hier funktioniert, was DaZ ist, was ein Waldtag ist, wer wer ist, Lehrerin, Schulleiterin, Sekretärin. Zweitens: eine Liste mit Bildern, was man kaufen muss, Finken, Turnsack, Regenhosen und so weiter, so wie die von der Kindergärtnerin. Drittens: wenn möglich beide Kinder am gleichen Ort, oder nahe beieinander, dann könnte er am Morgen auch einen Kurs machen. Und wenn ein Brief wichtig ist, soll oben etwas sein, eine Farbe oder ein Zeichen, damit man sieht: Das ist von der Schule, und das ist wichtig. Sonst liegt er bei den anderen Briefen. Und er wollte unbedingt noch sagen: Die Lehrerin von Ruta ist sehr gut, sehr geduldig. Und der Mittagstisch auch. Sie geben Ruta kein Schweinefleisch, das haben sie aufs Formular geschrieben, und das klappt.

[34:23] I: Schön, das freut mich. Und danke für diese Punkte, die sind sehr konkret. Dann sind wir am Schluss. Herzlichen Dank, Herr Weldu, und Ihnen auch, Frau Asfaha. Ich stelle die Aufnahme jetzt ab.

[34:35] V: Danke. Danke vielmals.
```
