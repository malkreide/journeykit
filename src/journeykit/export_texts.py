"""Texte der Exporte (Story Map, Chancenmatrix, Audit-Report) und des Diff-Reports, je Sprache.

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
    "audit.diagnosis": "## Diagnose",
    "audit.diagnosis_missing": "Keine Eingangsdiagnose (meta.diagnosis): Warum das ein Artefakt vom Typ `{map_type}` ist und kein anderes, steht nirgends.",
    "audit.diagnosis_alternative": "- Erwogen: {alternative}",
    "audit.diagnosis_backstage": "- Back-Stage dokumentiert in: {ref}",
    "audit.diagnosis_to_be": "**Soll-Konzept** (`scenario.perspective: to_be`): Die Journey beschreibt, wie der Weg künftig gehen soll, nicht wie Nutzende ihn heute erleben. Sie ist nie belastbar; ihre Begründung liegt in einer Ist-Journey.",
    "audit.verdict": "## Urteil (Vorschlag)",
    "audit.verdict_poster": "**Poster**: So, wie sie ist, wird die Journey nichts bewirken. Es fehlt: {missing}.",
    "audit.verdict_robust": "**Belastbar**: Primärevidenz an {pct}% der Erlebnis-Aussagen, jeder Breakdown mit Recovery-Pfad, Owner und Review gesetzt.",
    "audit.verdict_hypothesis": "**Hypothese**: strukturiert und gepflegt, aber noch nicht belegt – {reasons}.",
    "audit.verdict_to_be": "**Hypothese**: ein Soll-Konzept – es beschreibt, was sein soll, und lässt sich deshalb nicht durch Nutzende belegen, nur durch eine Ist-Journey begründen.",
    "audit.verdict_also": "Ausserdem: {reasons}.",
    "audit.missing_owner": "verantwortliche Rolle (meta.owner)",
    "audit.missing_review": "Review-Rhythmus (meta.review_cycle_days)",
    "audit.missing_anchored_opportunity": "eine Chance mit Bezug zu Pain Point, Schritt oder Phase",
    "audit.reason_no_experience": "keine einzige Erlebnis-Aussage",
    "audit.reason_low_primary": "Primärevidenz an {pct}% der Erlebnis-Aussagen (Schwelle 50%)",
    "audit.reason_status_hypothesis": "Status `hypothesis`",
    "audit.reason_breakdown_without_recovery": "{n} Schritt(e) mit Breakdown ohne Recovery-Pfad",
    "audit.verdict_note": "_Vorschlag aus dem Modell nach den Kriterien in `references/review-fragen.md` («Übergabe-Satz»). Sie prüfen das Modell, nicht die Texte; das Review bestätigt das Urteil oder begründet die Abweichung._",
    "audit.next_steps": "## Nächste Schritte",
    "audit.step": "{n}. **{code}**: {message}",
    "audit.step_source_request": "{n}. **Quellen anfordern**: {q} Zitat(e) schreibt die Quelle Nutzenden zu, sie liegen aber nur aus zweiter Hand vor. Mit dem Rohmaterial lassen sie sich als Primärevidenz übernehmen. Offene Frage: {text}",
    "audit.step_source_request_new": "{n}. **Quellen anfordern**: {q} Zitat(e) schreibt die Quelle Nutzenden zu, sie liegen aber nur aus zweiter Hand vor. Rückfrage festhalten (open_questions mit proposed_method: source_request): Wo liegt das Rohmaterial, wer hat es erhoben?",
    "audit.step_plan": "{n}. Erhebungsplan festhalten (open_questions mit proposed_method): welche Fragen zuerst, mit welcher Methode, mit wem.",
    "audit.no_steps": "Keine offenen Befunde.",
    "audit.evidence": "## Evidenzlage",
    "audit.sources": "- Quellen: {n} ({kinds})",
    "audit.atoms": "- Evidenz-Atome: {total} · beobachtet {observed} · berichtet {reported} · angenommen {assumed}",
    "audit.relayed_quotes": "  - davon {n} Zitat(e), die die Quelle Nutzenden zuschreibt, die aber nur aus zweiter Hand vorliegen (`quote` mit Klasse `assumed`)",
    "audit.experience": "- Erlebnis-Aussagen mit Primärevidenz: {backed}/{n} ({pct}%)",
    "audit.experience_none": "- Erlebnis-Aussagen: keine",
    "audit.counts": "- Breakdowns: {breakdowns} · Pain Points gesamt: {pain_points} · Chancen: {opps}",
    "audit.findings": "## Befunde: {errors} Fehler · {warnings} Warnungen · {infos} Hinweise",
    "audit.finding": "- **{level}** {code}{where}: {message}",
    "audit.no_findings": "Keine Befunde.",
    "audit.open_questions": "## Offene Fragen",
    "audit.method": " _(Methode: {method})_",
    "audit.oq_at": "«{name}»: ",
    # Diff-Report
    "diff.title": "# Änderungen {old} → {new}",
    "diff.none": "Keine Modelländerungen.",
    "diff.evidence": "Evidenz",
    "diff.evidence_delta": "- gesamt {total} · beobachtet {observed} · berichtet {reported} · angenommen {assumed}",
    "diff.added_sources": "Neue Quellen",
    "diff.added_steps": "Neue Schritte",
    "diff.removed_steps": "Entfernte Schritte",
    "diff.added_pain_points": "Neue Pain Points",
    "diff.removed_pain_points": "Entfernte Pain Points",
    "diff.pain_point_status": "Pain-Point-Status",
    "diff.added_opps": "Neue Chancen",
    "diff.removed_opps": "Entfernte Chancen",
    "diff.opp_status": "Chancen-Status",
    "diff.feeling": "Emotionale Kurve",
    "diff.change": "{id}: {old} → {new}",
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
    "audit.diagnosis": "## Diagnostic",
    "audit.diagnosis_missing": "Aucun diagnostic initial (meta.diagnosis) : rien n'explique pourquoi cet artefact est de type `{map_type}` et pas un autre.",
    "audit.diagnosis_alternative": "- Envisagé : {alternative}",
    "audit.diagnosis_backstage": "- Coulisses documentées dans : {ref}",
    "audit.diagnosis_to_be": "**Concept cible** (`scenario.perspective: to_be`) : le parcours décrit comment le chemin doit se dérouler à l'avenir, non comme les usagers le vivent aujourd'hui. Il n'est jamais fiable ; sa justification se trouve dans un parcours actuel.",
    "audit.verdict": "## Appréciation (proposition)",
    "audit.verdict_poster": "**Affiche** : en l'état, le parcours ne produira aucun effet. Il manque : {missing}.",
    "audit.verdict_robust": "**Fiable** : preuve primaire pour {pct} % des énoncés d'expérience, chaque rupture avec un chemin de rattrapage, responsable et révision définis.",
    "audit.verdict_hypothesis": "**Hypothèse** : structuré et tenu à jour, mais pas encore étayé – {reasons}.",
    "audit.verdict_to_be": "**Hypothèse** : un concept cible – il décrit ce qui doit être et ne peut donc pas être étayé par les usagers, seulement justifié par un parcours actuel.",
    "audit.verdict_also": "En outre : {reasons}.",
    "audit.missing_owner": "rôle responsable (meta.owner)",
    "audit.missing_review": "rythme de révision (meta.review_cycle_days)",
    "audit.missing_anchored_opportunity": "une opportunité liée à un irritant, une étape ou une phase",
    "audit.reason_no_experience": "aucun énoncé d'expérience",
    "audit.reason_low_primary": "preuve primaire pour {pct} % des énoncés d'expérience (seuil 50 %)",
    "audit.reason_status_hypothesis": "statut `hypothesis`",
    "audit.reason_breakdown_without_recovery": "{n} étape(s) avec rupture sans chemin de rattrapage",
    "audit.verdict_note": "_Proposition tirée du modèle selon les critères de `references/review-fragen.md` (« Übergabe-Satz »). Ils contrôlent le modèle, pas les textes ; la revue confirme l'appréciation ou justifie l'écart._",
    "audit.next_steps": "## Prochaines étapes",
    "audit.step": "{n}. **{code}** : {message}",
    "audit.step_source_request": "{n}. **Demander les sources** : la source attribue {q} citation(s) aux usagers, mais elles ne sont disponibles que de seconde main. Avec le matériel brut, elles peuvent être reprises comme preuves primaires. Question ouverte : {text}",
    "audit.step_source_request_new": "{n}. **Demander les sources** : la source attribue {q} citation(s) aux usagers, mais elles ne sont disponibles que de seconde main. Noter la demande (open_questions avec proposed_method: source_request) : où se trouve le matériel brut, qui l'a recueilli ?",
    "audit.step_plan": "{n}. Établir un plan d'enquête (open_questions avec proposed_method) : quelles questions d'abord, avec quelle méthode, auprès de qui.",
    "audit.no_steps": "Aucun constat ouvert.",
    "audit.evidence": "## État des preuves",
    "audit.sources": "- Sources : {n} ({kinds})",
    "audit.atoms": "- Atomes de preuve : {total} · observés {observed} · rapportés {reported} · supposés {assumed}",
    "audit.relayed_quotes": "  - dont {n} citation(s) que la source attribue aux usagers, mais disponibles seulement de seconde main (`quote` de classe `assumed`)",
    "audit.experience": "- Énoncés d'expérience avec preuve primaire : {backed}/{n} ({pct} %)",
    "audit.experience_none": "- Énoncés d'expérience : aucun",
    "audit.counts": "- Ruptures : {breakdowns} · irritants au total : {pain_points} · opportunités : {opps}",
    "audit.findings": "## Constats : {errors} erreur(s) · {warnings} avertissement(s) · {infos} remarque(s)",
    "audit.finding": "- **{level}** {code}{where} : {message}",
    "audit.no_findings": "Aucun constat.",
    "audit.open_questions": "## Questions ouvertes",
    "audit.method": " _(méthode : {method})_",
    "audit.oq_at": "« {name} » : ",
    # Rapport de différences
    "diff.title": "# Modifications {old} → {new}",
    "diff.none": "Aucune modification du modèle.",
    "diff.evidence": "Preuves",
    "diff.evidence_delta": "- total {total} · observées {observed} · rapportées {reported} · supposées {assumed}",
    "diff.added_sources": "Nouvelles sources",
    "diff.added_steps": "Nouvelles étapes",
    "diff.removed_steps": "Étapes supprimées",
    "diff.added_pain_points": "Nouveaux irritants",
    "diff.removed_pain_points": "Irritants supprimés",
    "diff.pain_point_status": "Statut des irritants",
    "diff.added_opps": "Nouvelles opportunités",
    "diff.removed_opps": "Opportunités supprimées",
    "diff.opp_status": "Statut des opportunités",
    "diff.feeling": "Courbe émotionnelle",
    "diff.change": "{id} : {old} → {new}",
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
