# Review-Fragen: Was das Modell nicht prüfen kann

Die Lints prüfen Struktur und Evidenzlage. Ob ein Zitat gut gewählt ist, ob
eine Phase wirklich so heisst, wie Nutzende sie erleben, ob die Chance den
Kern trifft – das prüft ein Mensch. Diese Fragen stellt der Skill vor der
Übergabe und im Audit-Modus; die zutreffenden, nicht alle.

## Inside-Out

- Welche drei Aussagen in dieser Journey würden Nutzende selbst **nicht** so formulieren?
- Wo hat das Material zur gewählten Persona am wenigsten zu sagen – und warum haben wir die Persona trotzdem so geschnitten?
- Welche Aussage stützt sich nur auf das Prozessdokument? Haben wir sie als Annahme gekennzeichnet oder als Tatsache geschrieben?
- Wenn wir den Filter «nur Primärevidenz» einschalten: Erzählt die Journey noch eine Geschichte?

## Happy Path

- An welcher Stelle rufen Menschen an, obwohl sie es nicht müssten? Steht dort ein Breakdown?
- Was passiert, wenn der Brief nicht ankommt, die Frist verpasst ist, die Sprache nicht reicht, das System die Person nicht findet? Steht es drin?
- Für jeden Breakdown: Gibt es heute einen Rückweg? Wenn nein, ist das als `exists: false` festgehalten – oder haben wir einen Soll-Pfad als Ist-Pfad geschrieben?
- Welcher Übergang (Kanal- oder Zuständigkeitswechsel) ist am wenigsten belegt?
- Beschreibt die Journey, wie der Weg heute ist – oder wie er sein soll? Wenn Soll: Ist `scenario.perspective: to_be` gesetzt, und wo steht die Ist-Journey, die das Konzept begründet?
- Welche Aktivität beschreibt ein Scheitern (nicht verstanden, kein Anspruch, abgebrochen, zurück zum Start), das nicht als Pain Point geführt ist? Im Audit-Modus besonders: Bestehende Maps verstecken Breakdowns oft im Aktivitätstext oder in einem Zitat («ich kann keinen Brief schreiben» unter einem Schritt «Nachfrage»).
- Erreicht die Persona im letzten Schritt ihr Ziel (`scenario.end_state`)? Wenn nein: Ist das offene Ende ein Breakdown, der fehlt, oder eine Scope-Grenze, die in `scope_exclusions` gehört?
- Für jeden Breakdown: Ist das ein **Versagen der Leistung** – oder ein **Rechtsweg, der funktioniert** (Einsprache, Einwendung, Rekurs, begründete Rückweisung)? Wenn Rechtsweg: Wo liegt das eigentliche Versagen davor (Information, Verständlichkeit, Zeitpunkt)? Dort gehört der Breakdown hin; der Rechtsweg selbst ist Reibung, und die Chance zielt auf bessere Information, nicht auf weniger Einsprachen.

## Static Map

- Wer öffnet diese Datei in sechs Monaten – und was löst das aus?
- Welche Evidenz kommt als Nächstes (Befragung, neuer Export, Beschwerdestatistik), und wer arbeitet sie ein?
- Welche drei Pain Points haben einen Owner, der weiss, dass er Owner ist?
- Was unterscheidet diese Version von der letzten (`journeykit diff`)? Wenn nichts: Warum nicht?

## Empathie-Vakuum und Überkomplexität

- Welcher Schritt hat eine Gefühlslage, die wir nicht belegen können? Streichen oder stehen lassen – bewusst?
- Wo widerspricht der Gefühlswert dem, was im Schritt passiert (Scheitern, Ablehnung, Rücksprung) – und welche Quelle erklärt das? Ohne Erklärung ist der Wert eher gesetzt als erhoben.
- Steht ein Gefühlswert für mehrere Stimmen, die sich widersprechen («konnte nicht zum Schalter» neben «am Schalter sehr gut beraten»)? Dann ist er ein Mittelwert, der beide verdeckt – wer erlebt was, und braucht eine der Gruppen eine eigene Datei?
- Welche zwei Schritte könnten zu einem werden, ohne dass Erleben verloren geht?
- Welche Nutzergruppe würde an derselben Stelle anders fühlen? Braucht sie eine eigene Datei?
- Ist der Scope-Ausschluss noch richtig, oder hat das Material etwas gezeigt, das hineingehört?

## Micro-Level Disconnect

- Welche Chance landet nächste Woche in einem Ticket, einer Traktandenliste oder einem Auftrag?
- Welche Story ist der kleinste Schritt, der für Nutzende bereits etwas ändert (MVP)?
- Welcher Pain Point mit Severity 4 oder 5 hat keine Chance – und ist das Absicht?

## Blueprint-Grenze

- Welche Massnahmen betreffen Abläufe zwischen Stellen statt das Erleben? Gehören sie in einen Blueprint?
- Wo haben wir Back-Stage-Wissen in die Journey geschrieben, weil es uns wichtig war – nicht weil Nutzende es erleben?

## Datenschutz und Lesart

- Lässt sich aus einem Zitat eine Person erkennen (seltene Konstellation, Ort, Zeitpunkt)?
- Liest eine der genannten Stellen diese Journey als Vorwurf? Sind Befunde als Evidenz formuliert, nicht als Urteil?

## Übergabe-Satz

Vor der Übergabe in einem Satz sagen, was die Journey ist. Die drei Urteile
schliessen sich aus und werden in dieser Reihenfolge geprüft; das erste, das
zutrifft, gilt:

1. **Poster**, wenn eines davon fehlt: verantwortliche Rolle (`meta.owner`),
   Review-Rhythmus (`meta.review_cycle_days`), mindestens eine Chance mit Bezug
   zu einem Pain Point (`linked_pain_points`), einem Schritt (`step_ref`) oder einer
   Phase (`phase_ref`).
   So, wie sie ist, wird sie nichts bewirken – auch wenn sie viele Ideen enthält.
2. **Belastbar**, wenn Primärevidenz (`observed`, `reported`) an mindestens der
   Hälfte der Erlebnis-Aussagen (Denken, Fühlen, Pain Points) steht, `meta.status`
   nicht `hypothesis` ist, jeder Breakdown einen Recovery-Pfad hat (auch
   `exists: false`) und die Journey kein Soll-Konzept ist
   (`scenario.perspective: to_be`): Ein Soll-Konzept beschreibt, was sein soll,
   und lässt sich deshalb nicht durch Nutzende belegen.
3. **Hypothese** in allen übrigen Fällen: strukturiert und gepflegt, aber noch
   nicht belegt. Der Wert liegt im Erhebungsplan; fehlt er (`open_questions` mit
   `proposed_method`), ist er der erste nächste Schritt.

Die Kriterien prüfen nur das Modell, nicht die Qualität der Texte. Ein Urteil,
das ihnen widerspricht, ist möglich, braucht aber eine Begründung im Satz.
