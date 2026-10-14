Du extrahierst Evidenz-Atome aus der Quelle «Interview E7 – Schulwechsel nach Umzug innerhalb der Gemeinde» (interview, Klasse reported).
Regeln:
- Ein Atom pro belegbarer Aussage. Zitate wörtlich, mit Fundstelle (Zeile/Zeitstempel/ID).
- emotion_hint nur, wenn die Emotion im Text steht; explicit true nur bei ausdrücklicher Nennung.
- signal setzen; breakdown nur, wenn die Person scheitert oder ausweicht (Anruf, Schalter, Aufgeben).
- phase_hint aus dieser Liste: entscheid, anmeldung, uebergang, ankommen. persona_hint: eltern-umzug.
- Keine Personendaten im text (Namen, Orte, Kontaktangaben ersetzen).
- Widerspricht eine Aussage einer bekannten Soll-Aussage, contradicts setzen: keine.
Gib ausschliesslich ein JSON-Array von Atomen nach journeykit-Schema aus, IDs mit Präfix «e7-».

Quelle «input.md»:

```
# Interview E7 – Schulwechsel nach Umzug innerhalb der Gemeinde (synthetisch)
Gemeinde Musterau, Schulverwaltung. Interview vom 2026-09-30, etwa 45 Minuten. Befragte Personen: Mutter und Vater eines Kindes in der 3. Klasse. Namen sind erfunden.

[00:00] I: So, jetzt läuft es, glaube ich. Ja, das rote Lämpchen brennt. Gut. Also, nochmals grüezi miteinander und merci vielmals, dass ich zu Ihnen nach Hause kommen durfte. Wie ich am Telefon schon gesagt habe, ich bin von der Schulverwaltung, und wir möchten besser verstehen, wie das für Familien ist, wenn ein Kind mitten im Schuljahr das Schulhaus wechseln muss. Es gibt dabei keine richtigen oder falschen Antworten, und es geht auch nicht darum, jemanden zu beurteilen, weder Sie noch die Schule. Das Gespräch wird anonymisiert, und Sie können jederzeit sagen, wenn Sie zu etwas lieber nichts sagen möchten. Ist das so in Ordnung für Sie?

[00:49] M: Ja, sicher. Klar. Möchten Sie noch einen Kafi, bevor wir anfangen? Ich sag es lieber gleich, mein Mann macht ihn immer ein bisschen zu stark. (lacht)

[01:03] I: (lacht) Nein danke, ich habe noch, und er ist genau richtig. Also, vielleicht ganz am Anfang: Erzählen Sie mir doch einfach einmal, wie das angefangen hat. Wann war das bei Ihnen zum ersten Mal ein Thema, dass Sie zügeln?

[01:22] M: Ähm, ja, also eigentlich schon lange. Wir haben ja vorher unten im Dorf gewohnt, in der Nähe vom Lindenhof, gleich hinter der Post, in einer Dreieinhalbzimmerwohnung. Und mit zwei Kindern – das geht schon irgendwie, aber die Fina hat bei uns im Schlafzimmer geschlafen, im Gitterbettli, und irgendwann ist sie halt zu gross geworden dafür, und – ja. Wir haben eigentlich schon seit dem Sommer letztes Jahr geschaut, so nebenbei, im Internet. Und dann hat eine Arbeitskollegin von mir gesagt, im Oberried wird etwas frei, in diesen Blöcken oben beim Waldrand, die sind nicht mehr ganz neu, so zehn, fünfzehn Jahre vielleicht. Und dann sind wir das anschauen gegangen, das war kurz vor Weihnachten, und ich hab mich eigentlich sofort verliebt. Wegen dem Balkon. (lacht) Und dann haben wir den Vertrag – im Dezember, nein, im Januar unterschrieben, und gezügelt haben wir dann am 28. März. Das war ein Samstag, das weiss ich genau, weil es geschneit hat. Ende März! Die Matratzen waren alle nass.

[02:51] V: Es war Schneeregen. (lacht) Aber ja, den Vertrag haben wir im Januar unterschrieben, nach Neujahr, weil die Verwaltung über die Feiertage zu hatte. Bezug wäre eigentlich erst per 1. April gewesen, aber wir durften schon am Samstag vorher rein. Das war ein Entgegenkommen vom Vermieter, das muss man sagen.

[03:15] I: Mhm. Und wann haben Sie zum ersten Mal an die Schule gedacht? Also an den Elio?

[03:23] V: Ehrlich gesagt – also ich zumindest – ziemlich spät. Ich bin einfach davon ausgegangen, das ist ja die gleiche Gemeinde, dann bleibt er halt im Lindenhof, mindestens bis zum Sommer, und dann schaut man weiter. Ich hab gar nicht gewusst, dass das mit der Adresse so fix ist. Mit den Schulhäusern, meine ich. Wo ich aufgewachsen bin, da gab es nur ein Schulhaus im ganzen Dorf, da hat sich die Frage gar nie gestellt.

[04:01] M: Ich hab schon früher daran gedacht. Eigentlich schon bei der Besichtigung, weil die Frau, die vorher dort gewohnt hat, die hat erzählt, dass ihre Kinder in die Bachmatt gehen. Und ich so: Ah, stimmt, das ist dann ja die Bachmatt. Aber ich hab mir gedacht, vielleicht kann man irgendwie ein Gesuch machen oder so, ich hab es nicht genau gewusst. Und der Elio hatte ja dort seine Kollegen, vor allem den Mats, die waren seit dem Kindergarten zusammen, fast wie Brüder. Und das war für mich schon so ein – ja, so ein Stein im Bauch, sagen wir es so.

[04:54] I: Mhm. Und was haben Sie dann gemacht, als klar war, dass das ein Thema wird?

[05:02] M: Dann hab ich angerufen. Beim Schulsekretariat. Das war nach den Sportferien, also so Mitte Februar irgendwann, und die –

[05:11] V: Ich hab ja vorher schon geschrieben, über dieses Kontaktformular auf der Website. Ende Januar, Anfang Februar, ich weiss es nicht mehr genau, auf jeden Fall ein, zwei Wochen nach dem Vertrag. Da kam so eine automatische Antwort, «Wir haben Ihre Anfrage erhalten und melden uns so rasch wie möglich», und dann –

[05:37] M: Und dann nichts. (lacht) Also nichts gegen Sie, gell. Drum hab ich dann angerufen, ich wollte nicht mehr warten. Und die Frau am Telefon war sehr nett, das muss ich sagen, die hat sich Zeit genommen. Sie hat gesagt, die Zuteilung zum Schulhaus geht nach der Wohnadresse, und wenn wir ins Oberried ziehen, dann ist das die Bachmatt, und zwar ab dann, wenn wir dort angemeldet sind. Und wenn wir möchten, dass er im Lindenhof bleibt, dann müssen wir ein Gesuch machen, schriftlich, mit Begründung, das Formular sei auf der Website. Und dann hat sie noch gesagt – ich weiss nicht mehr genau wie, aber so ungefähr: «Machen Sie sich aber nicht zu grosse Hoffnungen.» Oder: «Das wird eher selten bewilligt.» Irgendwie so.

[06:40] V: Das hat sie so gesagt? Das hab ich gar nicht im Kopf gehabt. Sonst hätten wir das mit dem Gesuch vielleicht gar nicht erst –

[06:52] I: Und dann haben Sie das Gesuch gemacht. Wie ist das gegangen?

[06:58] V: Ja, das hab dann ich gemacht. Das Formular ist ein PDF, das muss man herunterladen, ausdrucken, von Hand ausfüllen, unterschreiben und per Post schicken. Im Couvert. Also im Jahr 2026, oder. (lacht) Ich hab extra noch Briefmarken kaufen müssen, wir hatten keine mehr im Haus. Und für die Begründung hatte es so ein Feld, vielleicht vier Zeilen, und ich hab dann noch ein separates Blatt dazugelegt. Ich hab geschrieben, dass er dort seine Freunde hat, dass es nur noch ein paar Monate sind bis zum Sommer, dass er im Lindenhof in die Logopädie geht und dass das gut läuft und wir das nicht unterbrechen möchten. Und dass wir den Schulweg selber organisieren, dass das die Gemeinde also nichts kostet. Ich hab gedacht, das ist vielleicht wichtig für die. Ende Februar war das, ungefähr.

[08:05] M: Und dann hast du meine Unterschrift vergessen. (lacht) Es braucht ja die Unterschrift von beiden Eltern, und er hat nur selber unterschrieben. Dann hat jemand vom Sekretariat angerufen, und wir mussten es nochmals schicken. Das hat sicher nochmals eine Woche gekostet.

[08:26] I: Mhm. Und waren Sie sich denn einig, dass er im Lindenhof bleiben soll?

[08:33] M: (lacht) Nein. Nicht ganz. Ich war – ich war hin und her. Einerseits der Mats und die Klasse und die Frau Ammann, die Lehrerin, die hatte er wirklich gern. Aber andererseits hab ich gedacht, wenn er sowieso wechseln muss, dann lieber nach den Frühlingsferien als nach dem Sommer. Dann kennt er schon ein paar Kinder, wenn es im August weitergeht. Und dann der Weg. Ich hätte ihn ja jeden Tag fahren müssen oder mit dem Bus schicken, zweieinhalb Kilometer, mit Umsteigen, für einen Neunjährigen –

[09:17] V: Man muss nicht umsteigen. Der Siebner fährt doch direkt bis –

[09:22] M: Am Morgen schon, weil der Siebner erst ab – Moment. (Kind ruft aus dem Nebenzimmer: «Mamiii! Ich ha Durscht!») Ja, gleich, Fina, ich chume! – Entschuldigung, ich bin grad zurück.

[09:35] V: Das ist die Kleine, die Fina. Die ist vier, die ist ein bisschen erkältet, drum ist sie heute nicht in der Spielgruppe. (Pause) Wegen dem Bus – ich hab halt gedacht, das schafft er schon, er ist ja nicht mehr so klein. Und ich hab einfach gefunden, man reisst ein Kind nicht mitten im Jahr aus der Klasse. Das war so mein Gefühl. Aber im Nachhinein war es ja eh egal, weil es dann anders gekommen ist.

[10:14] I: Alles gut? – Gut. Wir waren beim Gesuch. Sie haben es also ein zweites Mal geschickt, mit beiden Unterschriften. Wie ging es dann weiter?

[10:27] V: Dann haben wir gewartet. Und gewartet. (lacht) Ich hab gedacht, so etwas geht vielleicht zwei Wochen. Und dann, das war schon Mitte März oder so, also wirklich nicht mehr lange vor dem Zügeln, da hat die Schulleiterin von der Bachmatt angerufen. Die Frau Odermatt.

[10:51] M: Zuerst hat die Sekretärin angerufen. Bei mir, auf dem Natel. Und die hat gesagt, die Schulleiterin meldet sich dann noch bei uns.

[11:02] V: Ah so. Ja, kann sein. Auf jeden Fall hab ich dann mit der Frau Odermatt geredet, und die hat gesagt, sie freuen sich auf den Elio, und er ist ab dem 20. April bei ihnen, in der Klasse vom Herrn Lüthi. Die letzte Woche vor den Ferien darf er noch im Lindenhof fertig machen, das hätten sie so abgesprochen. Und ob wir vorher einmal zum Schnuppern kommen möchten. Und ich hab gesagt, ja, aber wir haben doch ein Gesuch gemacht. Und sie hat gesagt, das wisse sie nicht genau, das laufe über die Schulverwaltung, aber sie gehe davon aus, dass er zu ihnen komme. Ich hab dann nachher eine Weile nicht gewusst, was ich davon halten soll.

[11:59] M: Und dann eben das mit dem Brief, Sie wissen schon.

[12:04] I: Erzählen Sie ruhig, ich kenne die Details nicht. Zu dem Zeitpunkt hatten Sie also noch keinen Entscheid zum Gesuch?

[12:14] M: Nein, gar nichts. Der Entscheid, also der richtige, der schriftliche, der ist irgendwann per Post gekommen. An die neue Adresse. Aber da hatten wir unseren Namen noch nicht am Briefkasten, die Verwaltung hat die Namensschilder erst nach ein paar Wochen gemacht, wir hatten nur so einen Zettel mit Klebband dran, und der ist dann wahrscheinlich abgefallen, keine Ahnung. Auf jeden Fall ist der Brief bei der Nachbarin gelandet, im falschen Briefkasten. Und die war über Ostern in den Ferien und hat ihn uns erst gebracht, als der Elio schon in der Bachmatt war. Ein paar Tage sicher. Und da stand dann drin, dass das Gesuch abgelehnt ist, mit einer Begründung und mit so einer Rechtsmittelbelehrung unten dran, dass man innert dreissig Tagen Beschwerde machen kann, oder Rekurs, oder wie das heisst. Und datiert war er – ich hab nachher extra geschaut – auf Ende März. Also ungefähr die Woche, wo wir gezügelt haben.

[13:33] V: Das hat mich am meisten genervt, ehrlich gesagt. Nicht dass es abgelehnt wurde, das hab ich ja dann irgendwann auch begriffen. Aber dieser Brief. Das tönt so amtlich, als hätten wir etwas verbrochen. Und er war ja schon längst dort. Was willst du da noch einen Rekurs machen. Und wenn man rechnet: Das Gesuch ist Ende Februar weg, der Entscheid ist Ende März datiert, und bei uns war er dann Ende April. Also fast zwei Monate, bis wir es schwarz auf weiss hatten.

[14:14] I: Wenn ich das kurz zusammenfassen darf: Sie haben Ende Februar das Gesuch geschickt, Mitte März hat dann die Bachmatt angerufen und gesagt, Elio kommt nach den Frühlingsferien zu ihnen, und den schriftlichen Entscheid haben Sie erst nach den Ferien bekommen, als er schon dort war.

[14:36] V: Genau. Und dazwischen hat man nicht gewusst, was jetzt gilt. Wir haben dem Elio auch nichts Richtiges sagen können. Ich hab ihm am Anfang sogar noch gesagt, vielleicht kannst du bleiben. Das hätte ich nicht machen sollen.

[14:55] I: Wie haben Sie es Elio dann gesagt, dass er wechselt?

[15:01] M: Hm. Am Abend nach dem Anruf, beim Znacht. Und er hat zuerst gar nichts gesagt, und dann ist er in sein Zimmer und hat geweint. Und dann ist er wieder rausgekommen und wollte wissen, ob der Mats auch mitkommen kann. (Pause) Ja. Das war schon hart. Er ist ein sensibles Kind, er braucht immer ein bisschen Zeit für Neues. Aber die Frau Ammann, die muss ich wirklich loben. Die hat am letzten Tag vor den Ferien ein kleines Abschiedsfest gemacht in der Klasse. Die Kinder haben ihm ein Büchlein gemacht, jedes Kind eine Seite, mit Zeichnungen und so. Und es gab Muffins – die hab ich gebacken, aber das war ihre Idee. Und sie hat ihm gesagt, er darf jederzeit vorbeikommen und Hallo sagen. Das Büchlein hat er heute noch neben dem Bett.

[16:11] V: Und sie hat gesagt, sie schickt seine Unterlagen an den Herrn Lüthi. Also wo er steht und was sie gerade durchnehmen. Ob sie das dann gemacht hat, weiss ich nicht. Der Herr Lüthi hat nachher jedenfalls gewusst, dass er beim Einmaleins ein bisschen Mühe hat.

[16:34] M: Das hab ich ihm aber beim Schnuppern selber gesagt. Das mit dem Einmaleins.

[16:41] I: Sie haben das Schnuppern jetzt ein paarmal erwähnt. Wie war das?

[16:47] M: Das war am ersten April, am Mittwochmorgen. Ich hab zuerst gedacht, das ist ein Aprilscherz, als die Sekretärin das Datum gesagt hat. (lacht) Nein, aber es war wirklich schön. Ich hab mir den Morgen freigenommen – ich arbeite ja Teilzeit im Spital, in der Administration – und ich konnte zum Glück mit einer Kollegin abtauschen. Wir waren um Viertel nach acht dort, und der Herr Lüthi hat uns unten beim Eingang abgeholt. Und im Schulzimmer hatten die Kinder ein Plakat gemacht, «Willkommen Elio», mit allen Namen drauf. Und er hat ihm gleich einen Götti zugeteilt, den Nando. Also Götti – ich weiss nicht, wie man dem offiziell sagt, so ein Gspänli halt, das neben ihm sitzt, ihm alles zeigt und schaut, dass er in der Pause nicht allein herumsteht. Und der Nando wohnt bei uns im Quartier, zwei Häuser weiter. Das hat sich dann auch als super herausgestellt, wegen dem Schulweg.

[18:04] V: Ich war nicht dabei, ich musste arbeiten. Aber er ist am Mittag heimgekommen und hat gesagt: «Es isch mega cool gsi.» Und das bei ihm – das will etwas heissen. (lacht)

[18:20] I: (lacht) Gab es beim Schnuppern auch etwas, das weniger gut war?

[18:26] M: Hm. Nicht das Schnuppern selber. Aber der Herr Lüthi hat so nebenbei gefragt, ob der Elio am Mittagstisch ist. Und ich hab gesagt, ja, im Lindenhof ist er am Montag und am Donnerstag am Mittagstisch. Ich bin einfach davon ausgegangen, dass das mitgeht. Dass das automatisch – das ist ja auch die Gemeinde. Und er hat ein bisschen komisch geschaut und gesagt, da müsse ich mich bei den Tagesstrukturen melden, das sei separat. Und ich so: Ah. Okay. (seufzt) Das war dann eigentlich fast das Mühsamste von allem. Die Tagesstrukturen sind ja nicht im Schulsekretariat, das ist eine andere Stelle mit einer anderen Telefonnummer, und die haben nur am Vormittag Telefonzeit, bis halb zwölf. Und ich arbeite am Vormittag. Ich hab dann in der Pause angerufen, im Spital im Gang draussen, und dann hiess es, ich müsse das Anmeldeformular für die Bachmatt neu ausfüllen, das vom Lindenhof gelte dort nicht. Und die Anmeldung müsse bis zum Fünfzehnten vom Vormonat drin sein. Der Fünfzehnte März war natürlich schon vorbei. Dann hat sie geschaut und gesagt, den Donnerstag mache sie ausnahmsweise trotzdem schon ab April, aber der Montag sei in der Bachmatt voll, da gebe es eine Warteliste.

[20:09] I: Und wie haben Sie das mit dem Montag gelöst?

[20:14] V: Am Anfang ist das Grosi gekommen, also meine Mutter. Die wohnt im Nachbardorf, eine halbe Stunde mit dem Auto, und sie hat am Montag gekocht. Sie hat das gern gemacht, aber auf die Dauer – sie ist auch nicht mehr die Jüngste. Und dann hab ich mit meinem Chef geredet, und ab Mitte Mai hab ich am Montag Homeoffice gemacht, damit ich über Mittag zuhause bin. Das geht bei uns zum Glück, ich bin in der Planung bei einer Haustechnikfirma, das kann ich am Computer machen. Aber das musste man zuerst einmal organisieren. Und das kann ja nicht jeder.

[21:03] M: Und seit den Sommerferien hat er jetzt beide Tage. Er hat dann doch noch einen Platz bekommen.

[21:12] V: Nicht seit den Sommerferien. Seit dem September. Im August war er noch auf der Warteliste, da hab ich noch Homeoffice gemacht.

[21:23] M: Ah, stimmt, der Brief kam ja erst Ende August. Also seit dem September, ja. Seit vier Wochen. – Und was ich auch nicht gewusst hab: Im Lindenhof haben sie uns den Mittagstisch für den ganzen April noch verrechnet, obwohl er nach den Ferien gar nicht mehr dort war. Weil man das hätte abmelden müssen, mit Frist. Das hab ich dann reklamiert, per Mail, und sie haben es auch korrigiert. Aber eben. Nochmals ein Mail.

[22:00] I: Mhm. Also eigentlich ein knappes halbes Jahr mit einer Übergangslösung am Montag. – Darf ich nochmals zurück zum Zügeln selber? Wie war das mit dem Ummelden?

[22:13] V: Das hab ich gemacht, online, über dieses eUmzug. So um Ostern herum – nein, schon vorher, in der Woche vor dem Zügeln, man kann das ja vorher machen. Das ging eigentlich gut, das waren vielleicht zehn Minuten. Und ich hab ehrlich gesagt gedacht, damit weiss es dann die ganze Gemeinde. Also auch die Schule und die Tagesstrukturen und alle. Das ist ja eine Gemeinde. Die Schule hat es dann ja auch gewusst – gut, die wussten es vom Gesuch. Aber die Tagesstrukturen offenbar nicht, und die Logopädie auch nicht. – Und in der letzten Woche vor den Ferien, als wir schon oben gewohnt haben, da hab ich ihn am Morgen mit dem Auto in den Lindenhof gefahren, auf dem Weg zur Arbeit. Beim Schulhaus kann man ja nicht halten, da ist Halteverbot, also hab ich ihn beim Dorfladen rausgelassen, das sind zwei Minuten zu Fuss. Und am Mittag hat ihn das Grosi geholt. Allein gefahren ist er nie.

[23:26] M: Doch, einmal. Am Donnerstag, mit dem Bus, weil das Grosi zum Arzt musste. Nach der Schule, am Nachmittag. Mit dem Leandro aus der Klasse bis zum Bahnhof, und dann umsteigen und allein weiter bis zu uns hinauf. Ich hab dir das doch erzählt. Ich bin an der Haltestelle gestanden und fast gestorben vor Angst. (lacht) Er fand es super.

[23:57] V: Das hab ich echt nicht gewusst. (lacht) Wegen dem Bus hab ich übrigens noch gefragt, ob die Gemeinde da etwas zahlt, weil ich irgendwo gelesen hab, dass es bei einem langen Schulweg eine Entschädigung gibt. Da hiess es, das gelte nur für den Weg zum zugeteilten Schulhaus, und zugeteilt war er ja eigentlich schon der Bachmatt. Für eine Woche – das war eh nicht viel, eine Mehrfahrtenkarte für Kinder. Aber es ging mir mehr ums Prinzip.

[24:34] I: Mhm. Dann der erste Schultag in der Bachmatt, nach den Ferien. Wie war der?

[24:42] M: (lacht) Also das Erste war: Wir haben nicht gewusst, wann die Schule anfängt. Im Lindenhof fängt es am Montag um zehn nach acht an, und wir haben gedacht, das ist überall gleich. Und dann waren wir um acht parat vor dem Schulhaus, der Elio und ich, und alles war noch zu. Dann hat uns eine andere Mutter gesagt, am Montag haben die Dritten in der Bachmatt erst um zwanzig vor neun, wegen der Turnhalle oder so. Den Stundenplan hatten wir nicht. Der Herr Lüthi hat gesagt, er gibt ihn uns beim Schnuppern mit, und dann hat er es vergessen, oder ich hab ihn liegen lassen, ich weiss es nicht mehr. Und es hat geregnet wie verrückt, richtiges Aprilwetter, und wir sind eine halbe Stunde unter dem Vordach gestanden.

[25:45] V: Davon hast du mir gar nichts erzählt. Du hast gesagt, der erste Tag war gut. (lacht) – Ab dem Dienstag hab ich ihn dann begleitet, die ganze erste Woche. Zu Fuss sind es zehn, zwölf Minuten, das ist eigentlich nah. Aber er muss über die Hauptstrasse, bei der Garage, und dort hat es zwar einen Fussgängerstreifen, aber am Morgen ist viel Verkehr, die Pendler, und es hat keinen Lotsen. Im Lindenhof gab es ja die Schülerlotsen mit den Westen. Hier nicht. Und dann hab ich gemerkt, dass der Nando um die gleiche Zeit geht, und die Mutter vom Nando und ich, wir haben uns abgesprochen. Seither gehen die zwei zusammen. Oder er geht allein, wenn der Nando krank ist – aber das macht er nicht so gern. Zum Schulweg hat uns im April übrigens niemand etwas gesagt. Erst beim Elternabend im August hiess es, bei der Hauptstrasse sei ein Lotsendienst geplant.

[27:02] I: Mhm. Und im Unterricht, in den ersten Wochen – wie ist es Elio da gegangen?

[27:10] M: Gemischt. Mit den Kindern ging es recht gut, vor allem wegen dem Nando. Aber dann war die Sache mit dem Tablet. Im Lindenhof hatte er ein Tablet von der Schule, und das musste er am letzten Tag abgeben. In der Bachmatt hat er zwar gleich am ersten Tag wieder eins bekommen, aber kein Login. Er konnte sich nicht anmelden auf dieser Lernplattform, wo sie die Aufgaben und den Wochenplan drauf haben. Und das hat sicher zwei Wochen gedauert. In der Zeit musste er alles auf Papier machen, der Herr Lüthi hat ihm die Sachen ausgedruckt, das war lieb, aber alle anderen haben am Tablet gearbeitet, und er hat gesagt, er komme sich vor wie ein Baby. Das hat ihn, glaube ich, mehr beschäftigt als alles andere.

[28:15] V: Der Herr Lüthi hat gesagt, das Login macht der Informatik-Support von der Gemeinde, und die brauchen eine Meldung vom Sekretariat. Und das Sekretariat hat gesagt, sie hätten es gemeldet. Irgendwo dazwischen ist es halt hängen geblieben. Das Komische ist ja: Im Lindenhof hatte er ein Login, auf der gleichen Plattform. Ich versteh nicht, warum man das nicht einfach umhängen kann. Und die Infos für die Eltern laufen auch über diese Plattform. Den Waldtag zum Beispiel, mit Regenhosen und Gummistiefeln, das haben wir nicht gewusst, und er ist in den Turnschuhen gegangen. Und es hat natürlich geregnet. (lacht)

[29:06] I: Mhm. Und vom Schulstoff her, war das ähnlich wie im Lindenhof?

[29:12] M: Nicht ganz. In der Bachmatt arbeiten sie mit dem Wochenplan, das kannte er nicht, da muss er selber einteilen, was er wann macht. Das war am Anfang schwierig für ihn. Und in Mathe waren sie weiter, die hatten das Einmaleins schon fertig, und im Lindenhof waren sie erst beim Siebner.

[29:39] V: Beim Achter. (lacht) Egal. Er war auf jeden Fall hinten nach. Der Herr Lüthi hat ihm Zusatzblätter mitgegeben, zum Üben zuhause, und ich hab am Abend mit ihm geübt, mit so Kärtchen. Im Juni war er dann wieder ungefähr dort, wo die anderen sind. Dass er hinten nach ist, hat uns der Herr Lüthi beim Gespräch gesagt – er hat nach zwei, drei Wochen von sich aus angerufen und gefragt, ob wir einmal vorbeikommen möchten. Kein Problemgespräch, hat er gesagt, einfach um zu schauen, wie es läuft.

[30:23] M: Das war Mitte Mai. Und das hab ich sehr geschätzt, dass er das von sich aus gemacht hat. Da hat er uns auch gesagt, dass der Elio in der Pause ein paarmal Streit hatte. Wegen dem Fussball.

[30:42] V: Wegen dem Fussballplatz. In der Bachmatt dürfen die Dritten nur am Dienstag und am Donnerstag auf den Platz, an den anderen Tagen sind die Grossen dran. Das hat ihm niemand gesagt. Und dann ist er halt am Montag aufs Feld, und die Sechstklässler – ja. Der Nando hätte es ihm sagen können, aber gut, der ist auch erst neun. (lacht)

[31:13] I: (lacht) Haben Sie zu solchen Regeln – Hausordnung, Pausenplatz und so – etwas Schriftliches bekommen?

[31:20] M: Ja, so eine Willkommensmappe. Mit Stundenplan, Ferienplan, Hausordnung, was er mitnehmen muss, Finken, Turnsack, Znüni und so. Die war eigentlich gut gemacht, das muss ich sagen. Aber die hat er erst am ersten Schultag heimgebracht, im Schulsack. Hätten wir die vorher gehabt, dann hätten wir auch gewusst, wann die Schule anfängt. (lacht) Und in den Klassenchat von den Eltern sind wir auch erst im Mai gekommen, weil die Mutter vom Nando gefragt hat, ob wir da eigentlich drin sind.

[31:59] V: Und dass man kein Gipfeli zum Znüni mitgeben darf. (lacht) Das war für ihn eine Katastrophe. Im Lindenhof hatte er am Freitag immer ein Gipfeli, das war so ein Ritual. Und in der Bachmatt gibt es diese Regel, nur Früchte, Gemüse, Brot. Und die Lehrerin von der Pausenaufsicht hat ihm gesagt, das sei kein gesundes Znüni. Er war tagelang beleidigt.

[32:30] I: (lacht) Sie haben vorhin beim Gesuch die Logopädie erwähnt. Wie ist es damit weitergegangen?

[32:38] M: (seufzt) Ja. Die Logopädie. Also der Elio geht seit der zweiten Klasse in die Logopädie, er hat Mühe mit gewissen Lauten, mit dem «sch» und dem «s», und ein bisschen auch mit dem Lesen. Im Lindenhof war das die Frau Kunz, die kommt am Dienstag ins Schulhaus, und das lief super, er ist gern gegangen. Und ich hab gedacht, die Logopädie ist ja für die ganze Gemeinde der gleiche Dienst, dann geht das in der Bachmatt einfach weiter. Aber in der Bachmatt ist eine andere Logopädin, und die musste zuerst schauen, ob sie Platz hat. Und sie hatte die Unterlagen nicht, weil die Frau Kunz die nicht einfach weitergeben darf, wegen dem Datenschutz. Dafür braucht es eine Einverständniserklärung von den Eltern. Und das hab ich erst gemerkt, als nach den Ferien der Dienstag kam und niemand etwas von Logopädie gesagt hat. Dann hab ich die Frau Kunz angerufen, und sie hat gesagt, ah ja, da müssen Sie noch ein Formular unterschreiben, das schick ich Ihnen per Mail.

[34:05] V: Und das haben wir dann ausgedruckt, unterschrieben und mit dem Natel fotografiert, weil wir keinen Scanner mehr haben. (lacht) Aber ich glaube, das war nur eine kurze Pause mit der Logopädie. Zwei, drei Wochen oder so.

[34:24] M: Nein! Das war viel länger. Die letzte Stunde bei der Frau Kunz war vor den Ferien, Ende März, und angefangen hat es wieder nach Pfingsten, am vierten Juni. Das weiss ich, weil es in meiner Agenda steht. Mit den Ferien sind das über zwei Monate. Und ich hab nach dem Formular noch zweimal anrufen müssen, bis sich die Neue gemeldet hat, die Frau Bucher. Also insgesamt dreimal, bei zwei verschiedenen Stellen. Und die Frau Bucher hat dann beim ersten Mal gesagt, man merke, dass er ein bisschen zurückgefallen ist. Nicht viel, aber –

[35:11] V: Echt? So lange? Ich weiss noch, dass du dich aufgeregt hast. (lacht) Aber dass es zwei Monate waren, hab ich nicht gewusst.

[35:23] I: Hätte Ihnen jemand vorher sagen können, dass es diese Einverständniserklärung braucht?

[35:30] M: Ja, sicher. Die Frau Kunz hätte es mir sagen können, als ich ihr im Februar gesagt hab, dass wir zügeln. Oder die Schule, oder irgendwer. Ich mach ihr keinen Vorwurf, sie ist eine super Logopädin, aber ich glaube, sie hat einfach nicht daran gedacht. Oder sie hat gedacht, das macht die Schule.

[35:57] V: Das war irgendwie überall so. Jeder hat gedacht, das macht der andere. – (Kind ruft von draussen: «Papiii! De Ball isch wider bim Nachber!») Ja, ich chume! – Entschuldigung, das ist der Elio. Der Ball ist wieder im Garten vom Nachbarn. Ich bin gleich zurück.

[36:19] M: (lacht) Er ist draussen mit dem Nando, die spielen jeden Mittwochnachmittag Fussball hinten bei den Garagen. Das hat sich so ergeben. Am Anfang hab ich gedacht, er findet hier nie jemanden, er war die ersten Tage so still. Und jetzt sind die zwei unzertrennlich. Den Mats sieht er auch noch, so alle zwei, drei Wochen am Wochenende, die Mutter vom Mats und ich schauen, dass das klappt. Aber es wird weniger. Das ist halt so. (Pause) Und ehrlich gesagt, ich war froh, als es vorbei war. Die Wochen vor und nach dem Zügeln waren einfach viel. Ich weiss nicht, wie viele Telefonate ich in dieser Zeit gemacht hab. Zwanzig? Dreissig? Und immer in der Pause, weil man ja nur zu den Bürozeiten anrufen kann, und während den Bürozeiten bin ich selber im Büro. (lacht)

[37:29] I: (lacht) Ah, Sie sind wieder da. Wir waren gerade bei den vielen Telefonaten. Wenn ich kurz zusammenfassen darf, und Sie korrigieren mich: Sie hatten mit mehreren Stellen zu tun. Das Schulsekretariat für das Gesuch, die Schulleitung der Bachmatt, die Tagesstrukturen für den Mittagstisch, die Logopädie, für das Tablet noch der Informatik-Support und dann die Einwohnerkontrolle fürs Ummelden. Und Sie hatten den Eindruck, dass diese Stellen nicht voneinander wissen.

[38:01] V: Genau. Die Telefonate hat sie gemacht, das muss man sagen. Ich hab das Online-Zeug gemacht, das Ummelden und das Gesuch – ja, zweimal, ich weiss. (lacht) Aber eben: Man muss alles mehrmals sagen. Wir sind umgezogen, wir sind umgezogen, wir sind umgezogen. Und jedes Mal ein anderes Formular. Und man weiss als Eltern auch nicht, was man alles machen muss. Das ist eigentlich das Hauptproblem. Hätten wir am Anfang eine Liste gehabt – das müssen Sie machen, dort müssen Sie anrufen, bis dann und dann –, dann hätten wir das alles gemacht. Wir sind ja nicht unorganisiert. Aber wenn man es nicht weiss, dann weiss man es nicht.

[38:57] M: Wobei, die Leute waren alle nett. Das möchte ich schon sagen. Es war nie jemand unfreundlich. Es weiss einfach keiner, was der andere macht. Am ehesten den Überblick gehabt hat eigentlich der Herr Lüthi, aber der ist ja Lehrer, der ist dafür gar nicht zuständig. Und die Frau am Telefon, ganz am Anfang, die hat es ja eigentlich gesagt, dass es selten bewilligt wird. Das muss man fairerweise auch sagen.

[39:34] V: Ja, aber am Telefon. Das ist ja nicht verbindlich. Da denkt man, vielleicht haben wir Glück. Für mich war das Schwierigste dieses Nicht-Wissen. Wir haben wochenlang nicht gewusst, was jetzt gilt, und dann kommt der Brief, wenn alles schon passiert ist. Man kommt sich ein bisschen nicht ernst genommen vor. Wenn es sowieso fast nie bewilligt wird, dann soll man das auf der Website so hinschreiben, klar und deutlich. Dann hätte ich das Gesuch gar nicht gemacht, und wir hätten dem Elio nicht wochenlang Hoffnung gemacht. Und wenn man es macht, dann soll der Entscheid kommen, bevor man planen muss. Nicht nachher.

[40:27] I: Mhm. Und für Sie – was war am schwierigsten, und was hätten Sie gebraucht?

[40:34] M: Für mich der Mittagstisch. Weil uns das als Familie am meisten Organisation gekostet hat, mit dem Grosi und dem Homeoffice. Und gebraucht hätte ich – ja, eigentlich das, was er sagt. Ein Blatt. Wenn Sie innerhalb der Gemeinde zügeln und ein Kind in der Schule haben: erstens, zweitens, drittens. Ab wann das Schulhaus wechselt. Mittagstisch neu anmelden, bis wann. Logopädie, Formular. Tablet und Login. Und eine Ansprechperson, eine einzige, die man auch am Nachmittag erreicht. Und dass man das automatisch bekommt, wenn man sich ummeldet. Oder noch besser, dass man es gar nicht machen muss, dass die Stellen das unter sich regeln. Die Schule sagt den Tagesstrukturen, der Elio wechselt, fertig. Das wäre der Traum. (lacht)

[41:35] I: Ich möchte noch auf etwas vom Anfang zurückkommen. Sie waren sich ja nicht ganz einig, ob er bleiben oder wechseln soll. Wie sehen Sie das heute?

[41:48] V: (Pause) Heute würde ich sagen, es war richtig so. Also dass er nach den Frühlingsferien gewechselt hat. Er hatte so noch ein paar Monate, um anzukommen, bevor das neue Schuljahr angefangen hat. Wenn er erst im August gewechselt hätte, dann wäre alles gleichzeitig gekommen, neues Schulhaus, neue Kinder, neuer Stoff. Also – sie hatte recht. (lacht) Das muss jetzt aufs Band. Aber ich finde trotzdem, man hätte uns früher und klarer sagen müssen, woran wir sind.

[42:29] M: (lacht) Das ist jetzt aufgenommen. – Nein, aber heute ist er angekommen, wirklich. Er ist gern in der Schule, er hat seine Kollegen, er geht beide Tage an den Mittagstisch. Er ist auch nach den Sommerferien beim Herrn Lüthi geblieben, das war uns wichtig. Wobei wir das auch erst kurz vor den Sommerferien erfahren haben, vorher war das wieder so ein Fragezeichen. Und die Logopädie läuft, bei der Frau Bucher, jetzt am Donnerstag. Er hat sie gern. Nicht so gern wie die Frau Kunz, sagt er, aber gern. (lacht)

[43:15] I: Gibt es noch etwas zu den ersten Wochen, das wir nicht angesprochen haben? Vielleicht etwas, das Ihnen erst jetzt in den Sinn kommt?

[43:27] M: Hm. (Pause) Die Finken. (lacht) Das ist ein Detail, aber die Finken sind im Lindenhof geblieben, im Garderobenkasten, zusammen mit dem Turnsack. Das haben wir erst gemerkt, als er in der Bachmatt am ersten Tag keine hatte. Dann bin ich in der zweiten Woche in den Lindenhof, und der Hauswart hat mir den Sack gegeben, aber die Turnschuhe waren nicht mehr drin. Die sind bis heute verschwunden. Gut, die waren eh zu klein. Aber das sind so Sachen. Niemand denkt daran, dass das Kind ja noch Sachen im alten Schulhaus hat.

[44:13] V: Was ich noch sagen möchte, damit das nicht falsch ankommt: Wir sind eigentlich zufrieden mit der Schule. Mit der Bachmatt und vorher mit dem Lindenhof. Die Leute vor Ort, die Lehrer, die waren super. Das Problem war mehr das, was drumherum ist. Die Verwaltung, sagen wir es so – sorry. (lacht) Man hat einfach das Gefühl, wir sind die Ersten, die je gezügelt haben. Und das passiert doch sicher jedes Jahr ein paarmal. – Und schauen Sie, jetzt regnet es schon wieder. Immer, wenn wir über die Schule reden.

[44:59] I: (lacht) Vielleicht ist das ein Muster. Nein, genau solche Rückmeldungen brauchen wir, merci. Dann bedanke ich mich ganz herzlich bei Ihnen beiden. Sie bekommen von uns in ein paar Wochen eine kurze Rückmeldung, was wir aus den Gesprächen gelernt haben. Ich schalte das Gerät jetzt aus.

[45:24] M: Merci vielmals. Und jetzt geh ich schauen, was die Fina macht, es ist verdächtig ruhig da drin. (lacht)
```
