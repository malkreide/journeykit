Du extrahierst Evidenz-Atome aus der Quelle «Fokusgruppe F2 – Klassenlager aus Elternsicht» (source_ref «fg-f2», interview, Klasse reported).
Regeln:
- Ein Atom pro belegbarer Aussage, nicht pro Satz: Sätze desselben Redebeitrags, die zusammen eine Aussage machen, bleiben ein Atom. Nur bei Interviews (auch Fokusgruppen): Ein kurzer Redebeitrag (bis drei Sätze) bleibt ein Atom, auch wenn er Ursache und Folge oder Problem und Ausweg nennt; wechselt ein langer Redebeitrag das Thema oder den Schritt, wird jede Aussage ein eigenes Atom mit derselben Fundstelle. Dieselbe Aussage nie doppelt erfassen (nicht als Zitat und zusätzlich als Messwert).
- Zitate wörtlich, mit Fundstelle (Zeile/Zeitstempel/ID). Kürzen mit «…» ist erlaubt; Namen und andere Personendaten im Zitat durch «[Name]», «[Ort]» ersetzen.
- Nennt ein Zitat eine Zahl oder Dauer, value und unit im selben Atom ergänzen.
- emotion_hint nur, wenn die Emotion im Text steht; explicit true nur bei ausdrücklicher Nennung.
- signal setzen (friction, breakdown, positive, need, workaround, neutral); breakdown nur, wenn die Person scheitert oder ausweicht (Anruf, Schalter, Aufgeben).
- channel_hint nur mit diesen Werten: web, app, email, phone, letter, paper_form, counter, in_person, event, chat, sms, publication, other.
- phase_hint aus dieser Liste: information, anmeldung, vorbereitung, lager, nachher. persona_hint: eltern-mittelstufe.
- Keine Personendaten im text (Namen, Orte, Kontaktangaben ersetzen).
- Widerspricht eine Aussage einer bekannten Soll-Aussage, contradicts setzen: keine.
Gib ausschliesslich ein JSON-Array von Atomen nach journeykit-Schema aus, IDs mit Präfix «f2-», source_ref «fg-f2».

Quelle «input.md»:

```
# Fokusgruppe F2 – Klassenlager aus Elternsicht (synthetisch)
Gemeinde Musterau, Schulverwaltung. Fokusgruppe vom 2026-10-01, Ausschnitt von etwa 40 Minuten. Teilnehmende: vier Eltern (B1–B4), Moderation durch die Schulverwaltung. Namen sind erfunden.

[03:52] Mod: Gut. Dann steigen wir ein. Wie gesagt, es gibt kein Richtig oder Falsch, mich interessiert wirklich, wie Sie das erlebt haben – auch die kleinen Sachen, die man vielleicht gar nicht so wichtig findet. Wir fangen ganz vorne an: Wie haben Sie überhaupt erfahren, dass Ihr Kind ins Lager geht? Wer mag anfangen?

[04:22] B1: Ja, ich kann. Also bei uns, ähm, das war schon am Elternabend im September. Da hat die Frau Odermatt – das ist die Klassenlehrerin von der Selina – gesagt, im Juni ist das Lager, und das Datum stand dann auch auf dem Jahresplan, den wir an dem Abend bekommen haben. Also ich wusste das eigentlich ein Dreivierteljahr vorher. Was ich gut fand, weil ich musste ja auch schauen mit der Arbeit. Ich hab mir die Woche dann so eingerichtet, dass ich … also nicht frei, aber dass ich immer erreichbar bin. Sagen wir's so. [lacht] Die Selina hat eine Nussallergie, und da will ich nicht in einer Sitzung sitzen, wenn etwas ist. Aber dazu kommen wir wahrscheinlich noch.

[05:27] B2: Bei uns kam das über die App. Im Januar, glaub ich, so ein «Save the date», Abschlusslager im Mai, und später dann nochmals ein PDF mit allem drin. Ehrlich gesagt hab ich das erste fast übersehen, weil in dieser App, da kommt … also da kommt jeden Tag irgendwas. Läuse in der dritten Klasse, Turnsack liegen gelassen, Fundsachen, Adventssingen [B3 lacht], und irgendwann liest man das halt nicht mehr so genau. Meine Frau liest das alles. Ich, ehrlich gesagt, nicht. [lacht]

[06:15] Mod: Mhm. Und bei Ihnen, Jasmin?

[06:19] B3: Bei uns war's ein Zettel. Im Thek. [lacht] Ganz unten im Thek, zusammen mit, ich weiss nicht, einem alten Apfelbütschgi oder so. Die Lorena hat ihn mir nicht gegeben, die hat das einfach vergessen, und ich hab ihn am Sonntagabend gefunden, als ich den Thek ausgeräumt hab. Und da stand, man muss den Talon bis am Freitag zurückgeben. Also die Frist war schon vorbei, um zwei Tage, oder um einen, je nachdem, wie man zählt. Ich hab dann am Montag einfach ein Zettelchen dazugelegt, «Entschuldigung, zu spät gefunden», und es war kein Problem, die Frau Hänni hat nichts gesagt. Aber ich bin schon erschrocken. Ich hab gedacht, jetzt darf sie nicht mit.

[07:25] B1: Also ich glaube nicht, dass die da jemanden … die sind ja froh, wenn alle –

[07:33] B3: Ja, ja, das weiss ich jetzt auch. Aber vorher weiss man das halt nicht. Die Lorena war ja das erste Mal in einem Lager, und ich hab in der Klasse noch fast niemanden gekannt, den ich hätte fragen können.

[07:56] Mod: Mhm. Daniel, wie war das bei Ihnen?

[08:01] B4: Ich hab's vom Elias erfahren. [Pause] Also vom Sohn. Der kam nach den Sommerferien zu mir und hat gesagt, in drei Wochen gehen wir ins Lager. Und ich so: aha. [lacht leise] Bei uns war das Lager im September, also ganz am Anfang vom Schuljahr. Die Infos sind schon vorher gekommen, vor den Sommerferien, aber nicht zu mir. Das ist bei uns ein bisschen speziell. Wir sind getrennt, der Elias ist eine Woche bei mir, eine Woche bei der Mutter, und die Briefe gehen alle an ihre Adresse. Und die App hat auch nur sie.

[09:00] B2: Ah, das kenn ich von meinem Bruder. Genau dasselbe. Der erfährt auch alles über drei Ecken.

[09:11] Mod: Mhm. Darauf würde ich nachher gern nochmals zurückkommen, Daniel, wenn das für Sie okay ist. Ich würde gern noch kurz bei diesem Talon bleiben, den die Jasmin erwähnt hat, oder allgemein bei der Anmeldung. Was mussten Sie da alles ausfüllen, und wie ist das gegangen?

[09:37] B1: Bei uns war das ein PDF, das man ausdrucken musste [lacht], ausfüllen, unterschreiben und dem Kind wieder mitgeben. Drauf war: Notfallnummern, Krankenkasse, Hausarzt, Allergien, Medikamente, ob sie schwimmen darf, ob man Fotos von ihr machen darf, und ob die Leitung eine Zecke selber rausnehmen darf. [lacht] Das fand ich noch speziell. Und bei Allergien hab ich hingeschrieben: Nussallergie, Notfallset im Rucksack, vorderes Fach. Da war so eine Zeile, vielleicht drei Zentimeter. Da passt ja gar nicht rein, was man dazu eigentlich sagen müsste.

[10:26] Mod: Was hätten Sie denn dazu sagen wollen?

[10:31] B1: Ja eben: Wer kocht? Weiss die Person, dass auch Spuren gefährlich sind? Wer hat das Notfallset dabei, und wer kann damit umgehen, wenn's drauf ankommt? Ich hab dann der Frau Odermatt eine Mail geschrieben, und sie hat zurückgeschrieben, sie gebe das an die Küche weiter. Dann hab ich zwei Wochen nichts gehört und nochmals nachgefragt, und dann hat mich irgendwann die Köchin angerufen – das war eine Mutter aus der Parallelklasse, die macht das jedes Jahr. Und die war super, wirklich. Die hat gesagt, sie kocht die ganze Woche für alle ohne Nüsse, dann gibt's gar kein Durcheinander. Aber bis ich das wusste – das waren so drei Wochen, wo ich nicht wusste: Ist das jetzt angekommen oder nicht?

[11:42] Mod: Mhm. Marco, wie war das bei Ihnen mit dem Formular?

[11:48] B2: Ähnlich, glaub ich. Ich weiss es nicht mehr genau, das hat meine Frau gemacht. Was ich weiss, ist … wir haben da extra ihre neue Handynummer draufgeschrieben, und das hat dann trotzdem irgendwie nicht – nein, das erzähl ich nachher, sonst bring ich alles durcheinander. [lacht] Das gehört zum Lager selber.

[12:18] Mod: [lacht] Gut, wir kommen dahin. Jasmin, Sie haben vorhin gesagt, Sie dachten, die Lorena darf nicht mit. War für Sie klar, wie verbindlich das Lager ist?

[12:35] B3: Nein, eben nicht. Ich hab das zuerst so verstanden, dass man das Kind anmelden kann, wie bei einem Ferienlager. Also dass das freiwillig ist. Und ehrlich gesagt hab ich kurz überlegt, ob ich sie überhaupt anmelden soll, wegen dem Geld, aber das ist dann ein anderes Thema –

[13:03] B2: Aber das Lager ist doch obligatorisch. Das ist ganz normale Schulzeit.

[13:10] B3: Ja, das weiss ich jetzt auch. [lacht] Aber auf dem Zettel stand oben gross «Anmeldung Klassenlager». Da denk ich doch: Wenn man sich anmelden muss, dann kann man sich auch nicht anmelden. Oder?

[13:29] B1: Bei uns stand irgendwo, wer nicht mitkommt, geht die Woche in eine andere Klasse in den Unterricht. Also es ginge schon. Aber ich weiss nicht, ob das jemand macht.

[13:47] B4: Bei uns war, glaub ich, einer nicht dabei. Wegen … ich weiss es nicht genau. [unverständlich] irgendwas Medizinisches, hat der Elias gesagt.

[14:01] Mod: Mhm. Also da gab es unterschiedliche Vorstellungen, ob man muss oder ob man kann. Das nehme ich mal so auf. Daniel, das Formular bei Ihnen – das hat dann die Mutter ausgefüllt?

[14:20] B4: Ja. Und das ist eben auch so ein Punkt. Ich hab das Formular nie gesehen. Ich hab erst nach dem Lager gemerkt, dass ich auf der Notfallliste gar nicht drauf war. Nur sie, und als Zweite ihre Mutter, also das Grosi vom Elias. Und sie war in der Lagerwoche drei Tage geschäftlich weg, im Ausland. Wir haben das irgendwann im Oktober am Telefon besprochen, wegen etwas anderem, und dann sagt sie: Ah, ich hab nur mich draufgeschrieben, ich hab gedacht, die haben dich sowieso im System. Und die haben mich halt nicht im System. [Pause] Es ist nichts passiert. Aber wenn.

[15:23] Mod: Mhm. [Pause] Gehen wir zu den Informationen von der Schule vor dem Lager. Was haben Sie bekommen, was war hilfreich, was hat gefehlt? Marco, Sie haben das PDF erwähnt.

[15:44] B2: Ja, das PDF. «Merkblatt Abschlusslager», das waren, ich glaub, sechs Seiten. Mit Programm, Hausordnung, Packliste, Handyregel, Adresse vom Lagerhaus. Das war eigentlich gut gemacht, muss ich sagen, da war alles drin. Das Problem ist, man liest das einmal, am Handy, im Zug, und dann ist es weg. Und auf Seite zwei – das hab ich nachher gesehen – stand: Kranke Kinder werden von den Eltern abgeholt. Hab ich nicht gelesen. Oder gelesen, aber nicht gespeichert.

[16:29] B1: Bei uns kam das in drei Teilen. Zuerst im März der Brief mit Datum, Ort und Kosten, dann das Formular, und dann zwei Wochen vor dem Lager die Packliste und das Programm. Und die Packliste war mir eigentlich zu spät. Wegen den Wanderschuhen. Die Selina hatte keine passenden mehr, die vom letzten Sommer waren zu klein, und auf der Liste stand: «gute, eingelaufene Wanderschuhe». Eingelaufen! In zwei Wochen! [lacht] Wir sind dann jeden Abend eine Runde ums Quartier gelaufen, damit die eingelaufen sind. Sie hatte trotzdem Blasen.

[17:20] B3: [lacht] Bei uns waren's die Finken. Ich hab nicht gewusst, dass sie im Lagerhaus Finken braucht, und die vom Schulhaus darf man nicht mitnehmen, die bleiben dort. Das stand nicht auf der Liste, oder ich hab's nicht gesehen. Also ist sie am ersten Abend in den Socken rumgelaufen, und dann hat ihr eine Kollegin ein zweites Paar ausgeliehen. [lacht]

[17:54] Mod: Wie sind Sie überhaupt zur ganzen Ausrüstung gekommen, also zu allem, was auf der Liste stand?

[18:04] B3: Ja, also … die Liste war lang. Ich hab sie, glaub ich, sogar noch dabei, wart – [Papiergeraschel] nein, doch nicht. Also: Schlafsack, Leintuch, Kissenanzug, Taschenlampe, Regenjacke, Regenhose, Wanderschuhe, Badkleid, Sonnenhut, Trinkflasche, kleiner Rucksack für den Ausflug, und so weiter. Und wir hatten vieles nicht. Den Schlafsack hab ich von der Nachbarin ausgeliehen, die Wanderschuhe hab ich im Brocki gefunden, für zwölf Franken, die waren super. Die Regenhose hab ich neu gekauft, und dann hat's die ganze Woche nicht geregnet. [lacht] Und die Nachbarn einen Stock weiter unten, die haben einen Sohn in der Parallelklasse, und die sprechen nicht so gut Deutsch. Die haben mich gefragt, ob ich ihnen den Brief erklären kann. Und die dachten, man muss das alles neu kaufen. Die waren schon im Laden und haben einen Schlafsack für hundertzwanzig Franken angeschaut. Und ich hab gesagt, nein, das muss nicht neu sein, das kann man auch ausleihen. Aber das stand halt nirgends.

[19:41] Mod: Mhm. Gab es den Brief auch in anderen Sprachen?

[19:47] B3: Ich glaub nicht. Also ich hab keinen gesehen. Vielleicht auf Anfrage?

[19:55] B1: Bei uns stand unten so eine Zeile in verschiedenen Sprachen, «Brauchen Sie eine Übersetzung? Melden Sie sich bei …» – ich weiss nicht mehr, bei wem. Aber ob das bei allen Briefen so war, keine Ahnung. Und ob dann jemand anruft, der den Brief gar nicht lesen kann … [lacht] Das ist ja auch so eine Sache.

[20:26] Mod: Daniel, wie war das bei Ihnen mit der Ausrüstung?

[20:32] B4: [lacht] Das ist eigentlich das Lustigste an der ganzen Sache. Der Elias hat bei mir gesagt, er braucht einen Schlafsack, der alte ist zu klein. Also hab ich einen gekauft. Und bei der Mutter hat er's auch gesagt. Und dann hatte er zwei. [alle lachen] Ja. Jetzt hat er halt zwei, einer ist bei ihr, einer bei mir. Aber es zeigt halt, dass wir das nicht abgesprochen haben, und dass die Schule eben nur mit ihr kommuniziert. Das gibt dann so ein Puff. Ich hab dann im Sekretariat angerufen, ob ich auch auf die App kann. Und da hiess es, pro Kind gibt es ein Konto, für den Hauptkontakt. Inzwischen geht's, glaub ich, ich hab jetzt einen eigenen Zugang. Aber ich musste drei- oder viermal nachfragen, und das hat gedauert bis … ungefähr Weihnachten. Da war das Lager längst vorbei.

[21:59] Mod: Wenn ich kurz zusammenfasse, was ich bis jetzt höre: Die Infos kamen auf ganz verschiedenen Wegen – Elternabend, App, Papier im Thek. Teilweise früh, teilweise eher knapp, vor allem die Packliste. Wichtige Sachen, wie das mit dem Abholen, standen zwar drin, aber man hat sie nicht gesehen. Und die Infos erreichen nicht immer alle, die sie brauchen. Stimmt das so ungefähr?

[22:34] B2: Ja. Es ist zu viel auf einmal, und dann zu wenig, wenn man's braucht. [lacht] Ich weiss nicht, ob das Sinn macht.

[22:46] Mod: Doch, ich glaube, ich verstehe, was Sie meinen. Dann zum Geld – die Jasmin hat das schon zweimal angetönt. Wie war das mit den Kosten? Was mussten Sie bezahlen, und wie?

[23:03] B1: Bei uns waren das achtzig Franken, mit einer QR-Rechnung von der Gemeinde, die kam mit dem Brief im März. Und es hiess, wenn am Schluss etwas übrig bleibt, gibt's eine Rückzahlung. Hab ich aber nie mehr etwas gehört.

[23:26] B2: Achtzig? Bei uns war's mehr. Hundert oder hundertzehn, ich bin nicht mehr sicher. Aber da war noch ein Ausflug dabei, so ein Seilpark. Und das Taschengeld extra, «maximal dreissig Franken», und dann haben natürlich alle dreissig mitgenommen. [lacht] Der Nevio kam mit fünfzig Rappen zurück und einem Sackmesser, das er überhaupt nicht braucht.

[23:58] B3: Bei uns hundertzwanzig, für vier Tage. Plus zwanzig Franken Taschengeld. Und das alles bar, im Couvert, mit Namen drauf, am ersten Morgen der Lehrerin abgeben. Hundertvierzig Franken gibt man einer Zehnjährigen in den Thek.

[24:19] B1: Bar? Wirklich?

[24:22] B3: Ja. Also bei uns waren's dann am Schluss weniger, dazu komm ich noch, aber trotzdem. Ich hab's ihr ganz unten in den Thek getan, in das Fach mit dem Reissverschluss –

[24:41] B2: – da, wo die Zettel verschwinden. [lacht]

[24:45] B3: [lacht] Ja, genau, da, wo die Zettel verschwinden. Nein, es ist angekommen. Aber ich war den ganzen Morgen nervös.

[24:57] Mod: Und die Höhe von dem Betrag – wie war das für Sie?

[25:04] B3: [Pause] Ja … also. Ich bin alleinerziehend, ich arbeite sechzig Prozent. Der Brief kam im April, und im April hatten wir noch die Zahnarztrechnung von der Lorena. Hundertzwanzig Franken plus Taschengeld plus das, was man noch kaufen muss – das ist für uns nicht nichts. Und im Brief stand ganz unten so ein Satz, irgendwie: «In finanziellen Härtefällen wenden Sie sich bitte vertraulich an die Klassenlehrperson.» Und das wollte ich nicht. Ehrlich nicht. Die Frau Hänni ist super, aber die sieht die Lorena jeden Tag, und ich will nicht, dass sie denkt … ich weiss auch nicht. Dass sie sie anders anschaut. Also hab ich das einfach mal liegen lassen.

[26:14] B1: Das versteh ich total.

[26:17] B3: Und dann hat mir eine Mutter vom Elternrat, beim Abholen vom Turnen, so nebenbei gesagt, dass man das auch direkt bei der Schulverwaltung machen kann und dass die Gemeinde dann einen Teil übernimmt. Das wusste ich nicht. Also hab ich dort angerufen. Und – ja. Ich wurde zweimal weiterverbunden – nichts gegen Sie [lacht] –, die erste Person wusste nicht genau, wer zuständig ist. Und dann eine Frau, die war sehr nett, die hat gesagt, das geht, ich soll ein Formular ausfüllen und den Lohnausweis oder die letzte Steuerveranlagung mitschicken. Hab ich gemacht, und nach ungefähr zwei Wochen kam ein Brief: Ich zahle vierzig Franken statt hundertzwanzig. Aber das war knapp vor dem Lager. Ich hab bis zum Schluss nicht gewusst, ob ich jetzt hundertzwanzig ins Couvert tun soll oder vierzig. Ich hab dann vierzig plus die zwanzig Taschengeld reingetan und einen Zettel dazu, und das war okay. Aber ich hab schon schlecht geschlafen die Tage davor.

[27:48] B2: Also ich find ja, das darf eigentlich gar nicht so viel kosten. Mein Schwager ist Lehrer, und der sagt, die Schule darf den Eltern eigentlich nur das Essen verrechnen, so sechzehn Franken pro Tag oder so, weil die Volksschule gratis sein muss. Ich weiss nicht, ob das stimmt, ich bin kein Jurist. Aber hundertzwanzig Stutz für vier Tage, das wären ja dann –

[28:24] B3: Vierundsechzig. [lacht] Hab ich mir auch schon ausgerechnet.

[28:29] B2: Eben. Und dann frag ich mich halt, wieso zahlt der eine achtzig für fünf Tage und der andere hundertzwanzig für vier. In derselben Gemeinde, hier in Musterau.

[28:46] Mod: Mhm. Also die Beträge sind von Schulhaus zu Schulhaus verschieden, und es war nicht ganz klar, wofür genau man bezahlt. Das nehme ich so mit. Daniel, wie war das bei Ihnen?

[29:05] B4: Achtzig, glaub ich. Die Mutter hat's bezahlt, und ich hab ihr die Hälfte überwiesen. [lacht] Das hat funktioniert. Das ist so ziemlich das Einzige, was wir gut abgesprochen haben.

[29:23] B1: Und was man nicht vergessen darf, wie die Jasmin vorhin gesagt hat: die Ausrüstung. Wenn ich das zusammenrechne – Wanderschuhe, eine neue Regenjacke, ein neuer Rucksack, weil der alte kaputt war –, dann waren das schnell zweihundert Franken. Mehr als das Lager selber. Wir können uns das leisten, aber … ja.

[29:53] Mod: Kommen wir zur Lagerwoche selber. Wie lief die Kommunikation während der Woche – zwischen Ihnen und der Schule, oder auch mit den Kindern?

[30:07] B1: Bei uns gab's einen Lagerblog, mit Passwort, das stand auf der Packliste. Und die Frau Odermatt hat jeden Abend, also fast jeden Abend, drei, vier Fotos raufgeladen und zwei, drei Sätze geschrieben, was sie gemacht haben. Ich hab das geliebt, ehrlich. Ich bin jeden Abend um neun vor dem Laptop gesessen und hab gewartet, bis es neu lädt. [lacht] Und die Selina war, glaub ich, jeden Tag mal irgendwo drauf, im Hintergrund. Telefonieren durften sie nicht, die Handys wurden beim Car eingesammelt. Nur im Notfall.

[30:58] B2: Bei uns auch, das mit den Handys. Aber genau das mit dem Blog find ich … also nichts gegen Sie, aber –

[31:07] B1: [lacht] Nein, nein, sagen Sie's ruhig.

[31:11] B2: Ich find, das macht so einen Druck. In der Klasse von meinem Neffen gab's das auch, und dann haben die Eltern im Klassenchat geschrieben: «Meiner ist auf keinem Foto, ist etwas passiert?» Und die Lehrerin muss dann am Abend, nach einem ganzen Tag mit fünfundzwanzig Kindern, noch Fotos aussuchen, damit jedes Kind einmal drauf ist. Bei uns hat der Herr Wyss einmal am Tag in der App eine Nachricht geschrieben: «Alle gesund, heute gewandert, morgen Seilpark.» Fertig. Und das fand ich, ehrlich gesagt, genug. Also – bis am Donnerstag. [lacht]

[32:01] Mod: Bis am Donnerstag? Sie wollten vorhin schon von der Krankheit erzählen.

[32:09] B2: Ja. Also. Der Nevio hat am Mittwochabend Fieber bekommen, ziemlich hoch, neununddreissig irgendwas. Ausgerechnet vor dem Seilpark. Die haben ihm ein Fiebermittel gegeben, das hatten wir auf dem Formular erlaubt. Und am Donnerstagmorgen um sieben hat der Herr Wyss angerufen – aber zuerst meine Frau, auf ihre alte Nummer. Die hat sie seit über einem Jahr nicht mehr. Und eben, auf dem Formular stand die neue. Aber die Formulare waren in einem Ordner im Schulhaus, und mitgenommen hat er die Klassenliste aus dem System, also von der Schulverwaltung, und dort war noch die alte Nummer drin. Das hat er mir nachher so erklärt. Nach einer Viertelstunde oder so hat er's dann bei mir probiert, ich war als Zweiter drauf. Und dann hiess es: Er muss heim, Sie müssen ihn holen. Also hab ich im Geschäft angerufen, mich abgemeldet, ins Auto, zwei Stunden hin, zwei Stunden zurück. Der arme Kerl lag auf einer Matratze im Leiterzimmer, mit einem Kübel neben sich. [lacht] Nein, er wurde gut betreut, das muss ich sagen. Aber ich hab nicht gewusst, dass man selber holen muss. Ich hab gedacht, die gehen mit ihm dort zum Arzt oder so. Und das stand eben auf Seite zwei.

[34:01] B4: Und wenn man nicht kann? Also wenn man kein Auto hat, oder arbeitet und nicht weg kann?

[34:12] B3: Ich hab kein Auto. Bei uns wär das mit dem Zug gewesen, zweimal umsteigen und dann noch mit dem Bus, ich weiss nicht, wie lange. [Pause] Daran hab ich gar nie gedacht. – Bei uns war's eben das Heimweh. Da stand auch: keine Anrufe. Und die Lorena hatte am zweiten Abend Heimweh, also richtig, sie hat geweint und nicht mehr aufgehört, und die Frau Hänni hat ihr dann erlaubt, mich anzurufen, mit dem Handy von der Lehrerin. Das war so um halb zehn, ich war schon im Pyjama. [lacht] Wir haben zehn Minuten geredet, und dann ging's. Ich fand das extrem lieb von ihr. Aber ich hätte gern vorher gewusst, dass das überhaupt möglich ist. Ich hab nämlich die ganzen Tage vorher gedacht: Und wenn sie Heimweh hat, dann erfahr ich das gar nicht.

[35:37] Mod: Mhm. Daniel, und während der Lagerwoche – wie war das bei Ihnen?

[35:45] B4: Ruhig. [lacht] Ich hab nichts gehört, ich war ja nicht in der App. Es gab, glaub ich, schon Nachrichten von der Lehrerin, die hat mir die Mutter dann am Freitag als Screenshots weitergeleitet. Aber eben: Wenn etwas gewesen wäre – die Mutter war weg, ich nicht auf der Liste –, dann hätten die das Grosi angerufen. Die ist zweiundachtzig. [lacht] Die hätte sicher sofort mich angerufen, das schon. Aber es ist halt ein Umweg. Und ich wär eigentlich der Erste gewesen, der hätte hinfahren können.

[36:35] Mod: Gehen wir zum Ende vom Lager und zu dem, was danach kam. Die Rückkehr, und was von der Schule nachher noch gekommen ist.

[36:49] B1: Also die Rückkehr war am Freitag um vier beim Schulhaus, das hat gut geklappt, der Car war sogar zehn Minuten zu früh. [lacht] Und danach – ja, die Wäsche. [lacht] Es fehlten ein Pulli und ein Frottiertuch. Es hiess, die Fundsachen kommen in eine Kiste im Eingang vom Schulhaus. Den Pulli hab ich dann gefunden, aber erst drei Wochen später, weil der Hauswart die Kiste erst dann rausgestellt hat. Das Frottiertuch nie. Und was ich mich auch frage: die Abrechnung. Hat bei Ihnen jemand eine bekommen? Weil bei uns hiess es ja, Rückzahlung, wenn's weniger kostet.

[37:45] B2: Nein. Wir haben auch nichts zurückbekommen, obwohl der Nevio den Seilpark gar nicht gemacht hat und früher heim ist. Nicht, dass es mir um die zwanzig Franken geht. Aber man weiss halt nicht, was mit dem Geld passiert. Fotos gab's dann, einen Link zu so einem Ordner, der war dreissig Tage gültig.

[38:14] B4: Ja, genau, so einen Link gab's bei uns auch. Bei mir war der abgelaufen. Die Mutter hat ihn mir weitergeleitet, aber erst nach ein paar Wochen, sie hat's vergessen, was ja passieren kann. Und dann hab ich draufgeklickt, und es kam: «Dieser Link ist nicht mehr gültig.» Sie hat mir dann ein paar geschickt, die sie gespeichert hatte. Aber nicht alle. [Pause] Ich will aber nicht, dass das jetzt so tönt, als wär das Lager schlecht gewesen. Der Elias war begeistert. Der kam heim, hat drei Tage nur geschlafen und dann eine Woche lang nur vom Lager erzählt. [lacht]

[39:14] B3: Die Lorena auch. Trotz Heimweh. Die will nächstes Jahr unbedingt wieder. Und sie haben eine Lagerzeitung gemacht, die Kinder, mit Zeichnungen und kleinen Berichten, die kam dann vor den Sommerferien nach Hause. Die ist richtig herzig, die hängt jetzt am Kühlschrank. Eine Abrechnung hab ich aber auch nie gesehen.

[39:45] B1: Darf ich noch etwas zur Allergie sagen, weil das hier reinpasst? Die Selina hat mir am Sonntag nach dem Lager erzählt, dass am Mittwoch beim Ausflug ein anderes Kind ein Schoggistängeli mit Haselnüssen dabeihatte, und die Frau Odermatt hat das gesehen und ihr gesagt, sie soll sich woanders hinsetzen. Es ist nichts passiert. Aber das hab ich vom Kind erfahren, beim Znacht. Von der Schule kam da nichts. Und ich hätte das schon gern von der Lehrerin gehört. Nicht als Vorwurf, einfach … dass man weiss, was war.

[40:36] Mod: Mhm. Wenn ich das zusammenfasse für die Zeit nach dem Lager: Die Rückkehr hat gut geklappt, und die Kinder waren mehrheitlich begeistert. Offen blieb bei mehreren, was mit dem Geld passiert ist, also eine Abrechnung. Fotos und Fundsachen waren nicht für alle gleich gut erreichbar. Und eine Rückmeldung von der Schule, wie die Woche für das eigene Kind war, gab es eigentlich nicht. [Pause] Wir haben noch ein paar Minuten in diesem Block. Ich würde gern eine kurze Runde machen: Wenn Sie ans nächste Lager denken – was müsste anders sein, damit es für Sie einfacher wird? Daniel, möchten Sie anfangen?

[41:36] B4: [Pause] Ja, ganz einfach: Beide Eltern bekommen die Infos. Wenn das geteiltes Sorgerecht ist, dann beide, in der App und per Post. Und beide stehen auf der Notfallliste, ohne dass man das extra verlangen muss. Mehr eigentlich nicht. Der Rest war gut.

[42:04] B3: Bei mir ist's halt das Geld, gäll. Dass im Brief steht, an wen man sich wenden kann, und zwar nicht nur an die Lehrerin. Und vielleicht nicht bar. Und dass nicht «Anmeldung» drübersteht, wenn's obligatorisch ist. Und dass man Sachen ausleihen kann – ich hab nachher gehört, bei Ihnen im Schulhaus, Andrea, gibt's so eine Kiste mit Schlafsäcken? Und das mit dem Telefonieren: dass man vorher weiss, wenn das Kind Heimweh hat, darf's anrufen. Oder eben nicht. Aber dass man's weiss.

[42:51] B1: Ja, das hab ich auch gehört, aber nur vom Hörensagen, wir haben nie gefragt. [lacht] Bei mir: die Packliste früher, mindestens einen Monat vorher. Und bei medizinischen Sachen ein richtiges Gespräch vorher, nicht ein Feld auf dem Formular, sondern dass jemand anruft. Und nachher eine kurze Rückmeldung. Und – zum Blog nochmals, wegen vorhin: Ich versteh schon, was Sie meinen mit dem Druck. Vielleicht wär's schon genug, wenn man vorher weiss, wie kommuniziert wird. Weil das Schlimmste ist ja, wenn man nichts hört und nicht weiss, ob man etwas hören sollte.

[43:47] B2: Das unterschreib ich. Wenn ich weiss, es kommt einmal am Tag eine Nachricht, und sonst heisst nichts eine gute Nachricht, dann ist das für mich okay. Und sonst: weniger Nachrichten in der App, dafür die wichtigen markiert. Also das Lager nicht zwischen den Läusen. [lacht] Das mit dem Abholen gehört auf die erste Seite, fett. Und dass die Nummern stimmen. Ich hab nachher im Sekretariat angerufen und die Nummer korrigieren lassen, und da hiess es, das Lagerformular geht gar nicht ins System, das ist nur für die Lehrperson. Das versteh ich ehrlich gesagt nicht ganz. Man schreibt's ja nicht zum Spass auf.

[44:48] Mod: Gut. Vielen Dank, das war sehr viel und sehr konkret. Ich nehme mal mit: dass die Infos an beide Eltern gehen, dass die Kontaktdaten dort stimmen, wo man sie im Notfall braucht, dass früh und klar steht, was obligatorisch ist und was es kostet, dass es bei den Kosten einen Weg gibt, der nicht über die Lehrperson läuft, und dass man vorher weiss, wie während der Woche kommuniziert wird – auch beim Heimweh. Nach der Pause würde ich gern noch bei ein, zwei Punkten genauer nachfragen. Draussen hat's Kaffee und Gipfeli. [Stuhlrücken]
```
