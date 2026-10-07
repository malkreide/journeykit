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

## Static Map

- Wer öffnet diese Datei in sechs Monaten – und was löst das aus?
- Welche Evidenz kommt als Nächstes (Befragung, neuer Export, Beschwerdestatistik), und wer arbeitet sie ein?
- Welche drei Pain Points haben einen Owner, der weiss, dass er Owner ist?
- Was unterscheidet diese Version von der letzten (`journeykit diff`)? Wenn nichts: Warum nicht?

## Empathie-Vakuum und Überkomplexität

- Welcher Schritt hat eine Gefühlslage, die wir nicht belegen können? Streichen oder stehen lassen – bewusst?
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

Vor der Übergabe in einem Satz sagen, was die Journey ist:

- **Belastbar**: Primärevidenz an den meisten Erlebnis-Aussagen, Breakdowns mit Recovery, Owner und Review gesetzt.
- **Hypothese**: strukturiert, aber aus Innensicht; der Wert liegt im Erhebungsplan.
- **Poster**: ohne Owner, ohne Chancen, ohne Review – wird nichts bewirken, so wie sie ist.
