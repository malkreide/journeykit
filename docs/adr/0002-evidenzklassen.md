# ADR-0002: Drei Evidenzklassen an der Quelle

Datum: 2026-10-05 · Status: angenommen

## Kontext

Inside-Out Bias ist der häufigste Fallstrick: Maps entstehen aus Innensicht
und validieren interne Vorurteile. Teams unterscheiden selten, ob eine Aussage
von Nutzenden stammt oder aus dem Prozessdokument.

## Entscheid

Jedes Evidenz-Atom trägt genau eine Klasse: `observed` (gemessen,
beobachtet), `reported` (von Nutzenden berichtet), `assumed` (interne
Annahme). Die Klasse hängt an der Quelle, nicht an der Plausibilität.
`observed` und `reported` gelten als Primärevidenz. Aussagen ohne
Primärevidenz sind Annahmen und werden im Viewer als solche gezeichnet.

## Verworfen

- Vier oder mehr Klassen (z. B. quantitativ/qualitativ getrennt): mehr Präzision, aber die Entscheidung «primär oder nicht» ist die, die zählt.
- Konfidenzwerte 0–1 pro Aussage: suggerieren Messung, wo Urteil ist.

## Folgen

- Lints können Inside-Out messen (L010–L012).
- Workshop-Ergebnisse sind legitim, aber sichtbar vorläufig.
