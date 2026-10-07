# Diagnose: Ist das eine User Journey – und welcher Modus?

Nicht jede Anfrage nach einer «Journey» ist eine. In der Verwaltung betreffen
viele Journey-Anfragen in Wahrheit Back-Stage-Prozesse. Die Diagnose zu Beginn
spart die Enttäuschung am Ende.

## 1. Welches Artefakt?

| Frage | Ja → |
|---|---|
| Geht es darum, was **eine Nutzerrolle erlebt, denkt und fühlt**, über mehrere Kanäle und einen längeren Zeitraum? | **User Journey** (oder Customer Journey, wenn die ganze Beziehung zur Organisation gemeint ist) |
| Geht es darum, **welche internen Stellen, Systeme und Schritte** ein Erlebnis ermöglichen – Zuständigkeiten, Schnittstellen, Durchlaufzeiten? | **Service Blueprint** (Sichtbarkeitslinie, Front- und Back-Stage) |
| Geht es um **Klickpfade und Bildschirmwechsel** in einer Anwendung oder einem Formular? | **User Flow** |
| Geht es um **generelles Verhalten** von Menschen bei einem Vorhaben, unabhängig von der eigenen Organisation? | **Experience Map** |
| Geht es um **einen Projektlebenszyklus** oder eine Projektsteuerung? | Weder noch – das ist Projektmanagement. Allenfalls Service Blueprint für die Lieferprozesse. |

Warnsignale für «eigentlich Blueprint»:

- Die Auftraggebenden sprechen von Zuständigkeiten, Schnittstellen, Systemen, Fristen intern.
- Die gewünschten Massnahmen betreffen Abläufe zwischen Stellen, nicht das Erleben.
- Es gibt keinen Zugang zu Nutzenden und auch keinen Plan, ihn zu bekommen.
- Die Journey soll «den Prozess dokumentieren».

Was tun: Diagnose offen aussprechen. Entweder das Vorhaben umbenennen
(Blueprint) oder beides anlegen – Journey für das Erleben, Blueprint für die
Back-Stage – und in `meta.diagnosis.backstage_documented_in` verweisen.

## 2. Eine Persona oder mehrere?

Mischt die Anfrage Nutzergruppen mit grundverschiedener Ausgangslage (Eltern
mit und ohne Deutschkenntnisse, Lehrperson und Schulleitung, Erstnutzende und
Routinierte), dann **pro Gruppe eine Datei**. Faustregel: Wenn zwei Gruppen an
derselben Stelle gegensätzlich fühlen würden, sind es zwei Personas.

Der Viewer legt mehrere Dateien übereinander (`journeykit render a.json b.json`).

## 3. Welcher Modus?

```
Primärmaterial vorhanden? (Interviews, Befragung, Anfragen, Analytics, Beschwerden, Beobachtung)
├── ja  → Synthese
│         └── Ist eine bestehende Journey da, die eingearbeitet werden soll? → Audit zuerst, dann Synthese
├── nein, aber es gibt eine bestehende Journey → Audit
└── nein → Workshop (Hypothesis-first) mit Erhebungsplan
```

Hypothesis-first ist legitim als Start (62 % der Teams tun es laut NN/g),
spart aber keine Zeit und produziert ohne Validierung die Journey, die sich
die Organisation **wünscht**. Das Team darauf hinweisen; Status `hypothesis`
setzen; `open_questions` mit `proposed_method` füllen.

## 4. Was fehlt, bevor es losgeht?

Minimalkonfiguration für den Synthese-Modus:

- Mindestens **eine** Quelle, in der Nutzende selbst zu Wort kommen oder gemessen werden.
- Ein benennbares **Ziel in Nutzerworten** («Ich will wissen, ob mein Kind einen Platz hat»).
- Eine **Rolle**, die die Journey danach pflegt (`meta.owner`).

Fehlt eines davon, das zuerst klären. Zwei Fragen genügen meist; nicht mehr
als drei stellen, bevor Material gesichtet wird – oft ergeben sich bessere
Fragen aus den ersten Atomen.

## 5. Datenschutz-Vorprüfung

| Material | Typischer Status | Massnahme |
|---|---|---|
| Interview-Transkripte mit Namen, Wohnort, Schulname | `contains_pii` | Anonymisieren → `anonymised`; Transkript bleibt in der Ablage, ins JSON kommen nur anonymisierte Zitate |
| Anfragen-/Ticketexport mit Absenderangaben | `contains_pii` | Spalten entfernen, Kategorie und Kurztext behalten → `anonymised` |
| Befragung aggregiert | `none` oder `anonymised` | Nur Aggregate übernehmen |
| Analytics | `none` | – |
| Prozessdokument, Workshop-Notizen | `none` | Klarnamen von Mitarbeitenden durch Rollen ersetzen |

Lint L080 blockiert `contains_pii`; L081 warnt bei Mustern wie E-Mail-Adressen
oder Telefonnummern im Evidenztext.
