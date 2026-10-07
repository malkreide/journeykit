# Kennzahlen: Übersetzung von Markt in Verwaltung

Die Journey-Literatur ist kommerziell geprägt: Conversion, Churn, Customer
Lifetime Value, Cart Abandonment. In der Verwaltung können Nutzende nicht
abwandern – sie **weichen aus**: in andere Kanäle, in informelle Netzwerke,
in Beschwerden, ins Nichthandeln. Die Übersetzung ist keine Kosmetik, sondern
eine permanente Schicht: Was gemessen wird, bestimmt, was verbessert wird.

## Drei Kategorien (Schema: `kpi.category`)

| Kategorie | Frage | Beispiele |
|---|---|---|
| `perception` | Wie erleben Nutzende die Qualität? | Zufriedenheit mit Schritt X, Verständlichkeit (Zustimmung in %), **Aufwand pro Anliegen** (Verwaltungs-CES), Gefühl informiert zu sein |
| `outcome` | Was tun Nutzende tatsächlich, wie effizient läuft es? | Anteil vollständig erledigter Anliegen ohne Rückfrage, Rückfragequote pro Schritt, Durchlaufzeit bis Klarheit, Anteil Fristen eingehalten, Kanalverteilung (Telefon vs. Online) |
| `public_value` | Was bringt es dem Gemeinwesen und der Verwaltung? | Entlastung der Auskunftsstellen (Anfragen pro 100 Fälle), Chancengerechtigkeit (Erreichbarkeit fremdsprachiger Haushalte), Rechtssicherheit (Einsprachequote), Vertrauen (Weiterempfehlung des Verfahrens) |

`public_value` ersetzt «Business Impact». Es ist das, was eine Verwaltung
ihrer politischen Führung zeigen kann.

## Früh- und Spätindikatoren (`kpi.indicator_type`)

| | Frühindikator (`leading`) | Spätindikator (`lagging`) |
|---|---|---|
| Was | Signal, bevor es schiefgeht | Bestätigung, dass es schiefging |
| Beispiele | Aufwand pro Anliegen, Rückfragequote nach Brief, Ausstiegsrate Formularseite, Anteil Telefonanfragen trotz Online-Info | Einsprachen, formelle Beschwerden, verpasste Fristen, Zufriedenheit am Ende, Anteil ohne Betreuungsplatz |

Mindestens ein Frühindikator pro Journey, sonst meldet Lint L092.

## Übersetzungstabelle

| Kommerziell | Verwaltung | Messbar über |
|---|---|---|
| Conversion Rate | **Anteil vollständig erledigter Anliegen** (ohne Rückfrage, ohne zweiten Anlauf) | Fallstatistik, Anfragenexport, Befragung («Ich musste nachfragen») |
| Cart Abandonment / Drop-off | **Abbruchquote pro Schritt** (Formular angefangen, nicht eingereicht; Brief erhalten, nicht reagiert) | Formularstatistik, Analytics, Mahnquote |
| Churn | **Ausweichquote**: Anteil, der in Workarounds (Telefon, Schalter, Dritte) oder in formelle Beschwerden wechselt | Kanalstatistik, Beschwerdestatistik |
| Customer Effort Score | **Aufwand pro Anliegen** (Anzahl Kontakte, Zeit bis Klarheit, Zustimmung «war einfach») | Befragung, Fallverlauf |
| Time-to-first-value | **Zeit bis Klarheit** («Ich weiss, was gilt und was ich tun muss») | Befragung, Zeitstempel Brief → erste Rückfrage |
| Activation Rate | **Anteil, der den nächsten Pflichtschritt fristgerecht macht** | Fristenstatistik |
| Retention | **Anteil, der beim nächsten Anlass denselben Kanal wählt** | Kanalstatistik über Zeit |
| NPS | **Weiterempfehlung des Verfahrens** oder **Vertrauen in den Entscheid** (Zustimmung) | Befragung – nicht als Gesamtwert, sondern pro Phase |
| First Contact Resolution | **Erledigung im Erstkontakt** | Auskunftsstatistik |
| Price transparency, Checkout surprise | **Anteil, der die Kosten vorab kannte** (Gebühr, Auslagen) | Befragung («Ich wusste vorher, was es kostet»), Anfragen zur Gebühr pro 100 Fälle |
| Customer Acquisition Cost | **Aufwand der Verwaltung pro erledigtem Fall** (Minuten Auskunft pro 100 Fälle) | Zeiterfassung, Anfragenvolumen |
| Customer Lifetime Value | kein sinnvolles Pendant – weglassen | – |
| Branded Search, CPC | kein Pendant – weglassen | – |

Original in `commercial_equivalent` festhalten, damit nachvollziehbar bleibt,
woher die Kennzahl kommt.

## Regeln

- **Pro Phase, nicht pro Journey.** Eine Gesamtzufriedenheit sagt nichts; eine Zustimmung von 62 % beim Zuteilungsentscheid gegen 88 % beim Infoanlass sagt, wo das Problem liegt.
- **Eine Outcome-Kennzahl pro Phase mindestens.** Wahrnehmung ohne Verhalten ist Stimmung.
- **Istwert mit Quelle.** `current_value` nur mit `source_ref` auf eine Quelle im Register – sonst ist es eine Annahme.
- **Ziel setzen, wenn ein Owner da ist.** Ein `target` ohne verantwortliche Rolle ist ein Wunsch.
- **Keine Kennzahl, die niemand erhebt.** Lieber drei gemessene als zehn gewünschte; die gewünschten in `open_questions` mit `proposed_method: analytics` oder `survey`.

## Priorisierung von Chancen (`opportunity`)

Drei Scores von 1 bis 5:

- `user_impact`: Wie viele sind betroffen (Frequenz) und wie schwer (verhindert es das Ziel)?
- `public_value`: Entlastung, Chancengerechtigkeit, Rechtssicherheit, Vertrauen.
- `effort`: Aufwand für Umsetzung – inklusive Abstimmung mit anderen Stellen, nicht nur Technik.

Quadranten (Mittel aus Impact und Public Value ≥ 3 = hoher Nutzen; Aufwand ≤ 2
= gering):

| | Aufwand gering | Aufwand hoch |
|---|---|---|
| **Nutzen hoch** | Quick Win – sofort, für Momentum | Big Bet – in die Planung |
| **Nutzen gering** | Nebenbei – wenn Kapazität da ist | Zurückstellen – Kapazität schützen |
