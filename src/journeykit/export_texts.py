"""Texte der Exporte (Story Map, Chancenmatrix, Audit-Report), je Sprache.

Wie ``lint_messages.py``: je Schlüssel ein Text mit Platzhaltern in ``{}``,
in allen Sprachen dieselben Schlüssel und Platzhalter – ``tests/test_export_texts.py``
prüft das. Inhalte der Journey (Namen, Zitate, Stories) und Enum-Werte
(Status, Quellenart, Kartentyp) bleiben, wie sie sind; die Massnahmenliste
(CSV) hat technische Spaltennamen und braucht keine Übersetzung.
"""

from __future__ import annotations

from typing import Any

from .lint_messages import typo_fr

_DE: dict[str, str] = {
    # Story Map
    "storymap.title": "# Story Map: {title}",
    "storymap.persona": "Persona: **{name}** ({role}) · Ziel: {goal}",
    "storymap.backbone": "## Backbone (Nutzeraktivitäten)",
    "storymap.stories": "## Stories je Phase (oben = wichtigste; ✅ = MVP-Schnitt)",
    "storymap.no_opps": "_Keine Chancen abgeleitet._",
    "storymap.no_stories": "- _(noch keine Stories)_",
    "storymap.no_phase": "### Ohne Phasenbezug",
    # Chancenmatrix
    "opps.title": "# Chancen und Priorisierung: {title}",
    "opps.header": "| Quadrant | Chance | Impact | Public Value | Aufwand | Pain Points | Owner | Status |",
    "opps.legend": "Quadranten: Quick Win = hoher Wert, Aufwand ≤ 2 · Big Bet = hoher Wert, Aufwand ≥ 3 · Nebenbei = geringer Wert, geringer Aufwand · Zurückstellen = geringer Wert, hoher Aufwand.",
    # Audit-Report
    "audit.title": "# Audit: {title}",
    "audit.meta": "Version {version} · Status `{status}` · Typ `{map_type}`",
    "audit.synthetic": "> Synthetisches Beispiel: Quellen und Evidenz sind erfunden.",
    "audit.evidence": "## Evidenzlage",
    "audit.sources": "- Quellen: {n} ({kinds})",
    "audit.atoms": "- Evidenz-Atome: {total} · beobachtet {observed} · berichtet {reported} · angenommen {assumed}",
    "audit.experience": "- Erlebnis-Aussagen mit Primärevidenz: {backed}/{n} ({pct}%)",
    "audit.counts": "- Breakdowns: {breakdowns} · Pain Points gesamt: {pain_points} · Chancen: {opps}",
    "audit.findings": "## Befunde: {errors} Fehler · {warnings} Warnungen · {infos} Hinweise",
    "audit.finding": "- **{level}** {code}{where}: {message}",
    "audit.no_findings": "Keine Befunde.",
    "audit.open_questions": "## Offene Fragen",
    "audit.method": " _(Methode: {method})_",
}

_FR: dict[str, str] = {
    # Story map
    "storymap.title": "# Story map : {title}",
    "storymap.persona": "Persona : **{name}** ({role}) · objectif : {goal}",
    "storymap.backbone": "## Colonne vertébrale (activités des usagers)",
    "storymap.stories": "## Stories par phase (en haut = la plus importante ; ✅ = périmètre MVP)",
    "storymap.no_opps": "_Aucune opportunité dégagée._",
    "storymap.no_stories": "- _(pas encore de stories)_",
    "storymap.no_phase": "### Sans lien avec une phase",
    # Matrice des opportunités
    "opps.title": "# Opportunités et priorisation : {title}",
    "opps.header": "| Quadrant | Opportunité | Impact | Valeur publique | Effort | Irritants | Responsable | Statut |",
    "opps.legend": "Quadrants : gain rapide = valeur élevée, effort ≤ 2 · grand chantier = valeur élevée, effort ≥ 3 · en passant = faible valeur, faible effort · à différer = faible valeur, effort élevé.",
    # Rapport d'audit
    "audit.title": "# Audit : {title}",
    "audit.meta": "Version {version} · statut `{status}` · type `{map_type}`",
    "audit.synthetic": "> Exemple synthétique : les sources et les preuves sont fictives.",
    "audit.evidence": "## État des preuves",
    "audit.sources": "- Sources : {n} ({kinds})",
    "audit.atoms": "- Atomes de preuve : {total} · observés {observed} · rapportés {reported} · supposés {assumed}",
    "audit.experience": "- Énoncés d'expérience avec preuve primaire : {backed}/{n} ({pct} %)",
    "audit.counts": "- Ruptures : {breakdowns} · irritants au total : {pain_points} · opportunités : {opps}",
    "audit.findings": "## Constats : {errors} erreur(s) · {warnings} avertissement(s) · {infos} remarque(s)",
    "audit.finding": "- **{level}** {code}{where} : {message}",
    "audit.no_findings": "Aucun constat.",
    "audit.open_questions": "## Questions ouvertes",
    "audit.method": " _(méthode : {method})_",
}

TEXTS: dict[str, dict[str, str]] = {
    "de": _DE,
    "fr": {k: typo_fr(v) for k, v in _FR.items()},
}

QUADRANT_LABELS: dict[str, dict[str, str]] = {
    "de": {
        "quick_win": "Quick Win",
        "big_bet": "Big Bet",
        "fill_in": "Nebenbei",
        "skip": "Zurückstellen",
    },
    "fr": {
        "quick_win": "Gain rapide",
        "big_bet": "Grand chantier",
        "fill_in": "En passant",
        "skip": "À différer",
    },
}


def text(lang: str, key: str, **params: Any) -> str:
    return TEXTS[lang][key].format(**params)
