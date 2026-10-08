"""Meldungen und Hinweise der Lints, je Sprache.

Die Regeln in ``lint.py`` urteilen; was sie sagen, steht hier. Jede Meldung hat
eine ID (der Regelcode, bei mehreren Meldungen einer Regel ``Lxxx.variante``),
einen Text und einen Hinweis (leer, wenn die Meldung für sich spricht).
Platzhalter in ``{}`` werden mit ``str.format`` gefüllt und müssen in allen
Sprachen dieselben sein – ``tests/test_lint_messages.py`` prüft das.

Französisch wird hier mit normalen Leerzeichen geschrieben; die Typografie
(geschütztes Leerzeichen vor «:», «;», «?», «!» und in Guillemets) setzt
``typo_fr`` beim Laden (auch für die Exporte, ``export_texts.py``).
"""

from __future__ import annotations

from typing import Any

LANGUAGES = ("de", "fr")

_DE: dict[str, tuple[str, str]] = {
    # Integrität
    "L001.ref": ("Referenz «{ref}» zeigt auf kein Evidenz-Atom.", ""),
    "L001.source": ("Evidenz «{atom}» verweist auf unbekannte Quelle «{source}».", ""),
    "L001.contradicts": ("Evidenz «{atom}» widerspricht unbekanntem Atom «{other}».", ""),
    "L001.opp_pain_point": ("Chance «{opp}» verweist auf unbekannten Pain Point «{pp}».", ""),
    "L001.opp_phase": ("Chance «{opp}» verweist auf unbekannte Phase «{phase}».", ""),
    "L001.question_phase": ("Offene Frage verweist auf unbekannte Phase «{phase}».", ""),
    "L001.question_step": ("Offene Frage verweist auf unbekannten Schritt «{step}».", ""),
    "L002": (
        "ID «{id}» wird {n}-mal vergeben.",
        "IDs eindeutig machen; sie sind Referenzziele.",
    ),
    "L003": (
        "Dauer der Phase «{phase}» ist widersprüchlich: min {min}, typisch {typical}, max {max}.",
        "Es muss min ≤ typical ≤ max gelten; Grenzen weglassen, die die Belege nicht tragen.",
    ),
    # Inside-Out Bias
    "L010.none": (
        "Keine der {n} Erlebnis-Aussagen (Denken, Fühlen, Pain Points) stützt sich auf Nutzerevidenz.",
        "meta.status auf «hypothesis» setzen und einen Erhebungsplan unter open_questions festhalten - oder Interviews, Befragungen, Anfragen auswerten.",
    ),
    "L010.most": (
        "{unsupported} von {n} Erlebnis-Aussagen ({pct}%) ohne Primärevidenz (beobachtet/berichtet).",
        "Im Viewer den Filter «nur Primärevidenz» einschalten: Was dann übrig bleibt, ist die belegte Journey.",
    ),
    "L011": (
        "Quellenregister enthält keine Nutzerquelle (Interview, Befragung, Anfragen, Analytics, Beobachtung).",
        "Mindestens eine Quelle, in der Nutzende selbst zu Wort kommen oder gemessen werden.",
    ),
    "L012": (
        "Persona «{name}» stützt sich auf {n} Primärevidenz(en).",
        "Weniger als drei unabhängige Belege: persona.is_hypothesis = true setzen oder Evidenz nachreichen.",
    ),
    # Happy Path Bias
    "L020": (
        "Kein einziger Pain Point vom Typ «breakdown»: Die Journey kennt keinen Punkt, an dem sie scheitert.",
        "Wo weichen Nutzende aus - Anruf, Beschwerde, Nichthandeln? Das ist der Breakdown. Anfragen- und Beschwerdedaten zeigen ihn.",
    ),
    "L021": (
        "Phase «{phase}»: keine Reibung, kein Edge Case.",
        "Entweder ist die Phase wirklich reibungslos (dann Evidenz dafür anfügen) oder sie wurde aus Innensicht beschrieben.",
    ),
    "L022": (
        "Schritt «{step}» hat einen Breakdown, aber keinen Recovery-Pfad.",
        "Wie kommt die Persona zurück in die Journey? Falls heute gar nicht: recovery_paths mit exists=false als Soll-Pfad festhalten.",
    ),
    "L023": (
        "Kanalwechsel {from_channel} → {to_channel} bei «{step}» ist nicht als Übergang markiert.",
        "Übergangspunkte sind die häufigsten Reibungsstellen; is_transition = true und gezielt nach Evidenz suchen.",
    ),
    # Static Map Trap
    "L030": (
        "Keine verantwortliche Rolle (meta.owner).",
        "Ohne Owner wird die Journey zum Poster. Rolle und Funktionsadresse eintragen.",
    ),
    "L031": (
        "Kein Review-Rhythmus (meta.review_cycle_days).",
        "Zum Beispiel 180 Tage, gekoppelt an die nächste Erhebung oder den Jahreszyklus.",
    ),
    "L032": ("Review-Termin {date} ist überschritten.", ""),
    "L033": ("Schwerer Pain Point «{pp}» (Severity {severity}) ohne Owner.", ""),
    "L034": ("{n} Chance(n) ohne Status: {ids}.", ""),
    # Empathie-Vakuum
    "L040": (
        "{missing} von {n} Schritten ohne Gefühlslage.",
        "Lücken sind ehrlich - aber wenn mehr als die Hälfte fehlt, fehlt die Nutzerperspektive. Interviews nach Emotionen pro Schritt auswerten.",
    ),
    "L041": ("{missing} von {n} Schritten ohne Gedanken/Fragen der Persona.", ""),
    "L042": (
        "{n} Emotionspunkt(e) ohne Beleg - werden im Viewer als Annahme gezeichnet.",
        "Emoji-Kurven aus Workshop-Bauchgefühl sind Pseudo-Präzision. Belegen oder als Hypothese stehen lassen.",
    ),
    "L043": (
        "{n} Emotionspunkt(e) sind aus Evidenz abgeleitet, nicht ausdrücklich geäussert (emotion_hint.explicit fehlt).",
        "",
    ),
    # Überkomplexität
    "L050": (
        "{n} Phasen - mehr als acht lassen sich kaum noch lesen.",
        "Szenario enger fassen oder in zwei Journeys teilen.",
    ),
    "L051": (
        "{n} Schritte - das ist ein User Flow, keine Journey.",
        "Schritte auf Erlebnis-Ebene zusammenfassen; UI-Pfade gehören in einen User Flow.",
    ),
    "L052": (
        "Kein expliziter Scope-Ausschluss (scenario.scope_exclusions).",
        "Was bewusst nicht abgedeckt ist, schützt die Journey vor dem Stammbaum-Effekt.",
    ),
    # Micro-Level Disconnect
    "L060": (
        "Keine Chancen (opportunities) abgeleitet.",
        "Eine Map ohne Handlungsableitung ist ein Poster. Pro Frustrationstal mindestens eine How-might-we-Frage.",
    ),
    "L061": ("Schwerer Pain Point «{pp}» ohne verknüpfte Chance.", ""),
    "L062": ("{n} Chance(n) ohne Impact/Effort-Score - keine Priorisierung möglich.", ""),
    "L063": (
        "Keine Chance hat User Stories - die Story Map bleibt leer.",
        "journeykit export --format storymap zeigt, was ankommt.",
    ),
    # Blueprint statt Journey
    "L070": (
        "Keine Eingangsdiagnose (meta.diagnosis): Warum ist das eine User Journey und kein Service Blueprint?",
        "",
    ),
    "L071": (
        "{notes} Back-Stage-Notizen bei {n} Schritten.",
        "Das Interesse liegt offenbar hinter der Sichtbarkeitslinie. Service Blueprint anlegen und in meta.diagnosis.backstage_documented_in verweisen.",
    ),
    "L072": ("map_type = {map_type}: Erlebnis-Lints gelten nur eingeschränkt.", ""),
    "L073": (
        "{delegated} von {n} Schritten führen Dritte anstelle der Persona aus (performed_by.kind = intermediary).",
        "Ist das noch die Journey der Persona – oder die der Vermittlung? Diagnose prüfen; die Vermittlung allenfalls als eigene Persona erheben.",
    ),
    # Personendaten
    "L080": (
        "Quelle «{source}» enthält Personendaten (pii_status = contains_pii).",
        "Vor dem Teilen anonymisieren oder pseudonymisieren; nur die Ablage referenzieren, nicht das Material.",
    ),
    "L081": ("Evidenz «{atom}» enthält möglicherweise {what}.", ""),
    # Kennzahlen
    "L090": (
        "Keine Kennzahlen hinterlegt.",
        "Pro Phase mindestens eine Outcome-Kennzahl (Erledigungsquote, Rückfragen, Durchlaufzeit) - sonst lässt sich Wirkung nicht zeigen.",
    ),
    "L091": (
        "Kennzahl «{name}» ist kommerziell geprägt.",
        "In Verwaltungsbegriffe übersetzen (Conversion → Anteil erledigter Anliegen, Churn → Ausweichen in Workarounds oder Beschwerden); Original in commercial_equivalent festhalten.",
    ),
    "L092": (
        "Nur Spätindikatoren (lagging) - kein Frühwarnsignal.",
        "Aufwand pro Anliegen oder Rückfragequote pro Schritt sind Frühindikatoren.",
    ),
    # Evidenzqualität
    "L100": (
        "{n} Evidenz-Atom(e) werden nirgends referenziert: {ids}.",
        "Nicht synthetisiertes Material - entweder einordnen oder bewusst als «ausserhalb Scope» markieren.",
    ),
    "L101": (
        "Evidenz «{atom}» widerspricht {others}.",
        "Widersprüche gehören in die Journey (z. B. als Edge Case oder offene Frage), nicht geglättet.",
    ),
    "L102": (
        "{n} Primärevidenz(en) ohne Fundstelle (locator).",
        "Ohne Fundstelle lässt sich ein Zitat nicht nachprüfen.",
    ),
}

_FR: dict[str, tuple[str, str]] = {
    # Intégrité
    "L001.ref": ("La référence « {ref} » ne renvoie à aucun atome de preuve.", ""),
    "L001.source": ("La preuve « {atom} » renvoie à une source inconnue « {source} ».", ""),
    "L001.contradicts": ("La preuve « {atom} » contredit un atome inconnu « {other} ».", ""),
    "L001.opp_pain_point": ("L'opportunité « {opp} » renvoie à un irritant inconnu « {pp} ».", ""),
    "L001.opp_phase": ("L'opportunité « {opp} » renvoie à une phase inconnue « {phase} ».", ""),
    "L001.question_phase": ("Une question ouverte renvoie à une phase inconnue « {phase} ».", ""),
    "L001.question_step": ("Une question ouverte renvoie à une étape inconnue « {step} ».", ""),
    "L002": (
        "L'ID « {id} » est attribué {n} fois.",
        "Rendre les ID uniques ; ce sont des cibles de référence.",
    ),
    "L003": (
        "La durée de la phase « {phase} » est contradictoire : min {min}, typique {typical}, max {max}.",
        "Il faut que min ≤ typical ≤ max ; omettre les bornes que les preuves ne soutiennent pas.",
    ),
    # Biais de la vue interne
    "L010.none": (
        "Aucun des {n} énoncés d'expérience (pensées, ressenti, irritants) ne s'appuie sur des preuves issues des usagers.",
        "Passer meta.status à « hypothesis » et consigner un plan d'enquête sous open_questions – ou exploiter des entretiens, des enquêtes, des demandes.",
    ),
    "L010.most": (
        "{unsupported} des {n} énoncés d'expérience ({pct} %) sans preuve primaire (observée/rapportée).",
        "Activer dans le viewer le filtre « Preuves primaires seulement » : ce qui reste est le parcours étayé.",
    ),
    "L011": (
        "Le registre des sources ne contient aucune source usager (entretien, enquête, demandes, analyse d'audience, observation).",
        "Au moins une source dans laquelle les usagers s'expriment eux-mêmes ou sont mesurés.",
    ),
    "L012": (
        "La persona « {name} » s'appuie sur {n} preuve(s) primaire(s).",
        "Moins de trois preuves indépendantes : mettre persona.is_hypothesis = true ou compléter les preuves.",
    ),
    # Biais du parcours idéal
    "L020": (
        "Aucun irritant de type « breakdown » : le parcours ne connaît aucun point où il échoue.",
        "Où les usagers contournent-ils – appel, réclamation, renoncement ? C'est là la rupture. Les données de demandes et de réclamations la montrent.",
    ),
    "L021": (
        "Phase « {phase} » : ni friction, ni cas limite.",
        "Soit la phase se déroule vraiment sans friction (ajouter alors des preuves), soit elle a été décrite depuis la vue interne.",
    ),
    "L022": (
        "L'étape « {step} » comporte une rupture, mais aucune voie de rattrapage.",
        "Comment la persona revient-elle dans le parcours ? Si ce n'est pas possible aujourd'hui : consigner recovery_paths avec exists=false comme parcours cible.",
    ),
    "L023": (
        "Le changement de canal {from_channel} → {to_channel} à « {step} » n'est pas marqué comme transition.",
        "Les transitions sont les points de friction les plus fréquents ; mettre is_transition = true et chercher des preuves de manière ciblée.",
    ),
    # Piège de la carte figée
    "L030": (
        "Aucun rôle responsable (meta.owner).",
        "Sans responsable, le parcours devient une affiche. Indiquer le rôle et une adresse de fonction.",
    ),
    "L031": (
        "Aucun rythme de révision (meta.review_cycle_days).",
        "Par exemple 180 jours, liés à la prochaine enquête ou au cycle annuel.",
    ),
    "L032": ("L'échéance de révision {date} est dépassée.", ""),
    "L033": ("Irritant grave « {pp} » (gravité {severity}) sans responsable.", ""),
    "L034": ("{n} opportunité(s) sans statut : {ids}.", ""),
    # Vide d'empathie
    "L040": (
        "{missing} des {n} étapes sans ressenti.",
        "Les lacunes sont honnêtes – mais s'il en manque plus de la moitié, c'est la perspective des usagers qui manque. Exploiter les entretiens pour les émotions par étape.",
    ),
    "L041": ("{missing} des {n} étapes sans pensées ni questions de la persona.", ""),
    "L042": (
        "{n} point(s) émotionnel(s) sans preuve – dessiné(s) comme supposition dans le viewer.",
        "Des courbes d'émoticônes tirées de l'intuition d'un atelier sont une pseudo-précision. Les étayer ou les laisser comme hypothèse.",
    ),
    "L043": (
        "{n} point(s) émotionnel(s) déduit(s) des preuves, non exprimé(s) explicitement (emotion_hint.explicit manque).",
        "",
    ),
    # Surcomplexité
    "L050": (
        "{n} phases – au-delà de huit, la lecture devient difficile.",
        "Resserrer le scénario ou le partager en deux parcours.",
    ),
    "L051": (
        "{n} étapes – c'est un user flow, pas un parcours.",
        "Regrouper les étapes au niveau de l'expérience ; les chemins d'interface relèvent d'un user flow.",
    ),
    "L052": (
        "Aucune exclusion de périmètre explicite (scenario.scope_exclusions).",
        "Ce qui n'est volontairement pas couvert protège le parcours de l'effet arbre généalogique.",
    ),
    # Déconnexion du niveau micro
    "L060": (
        "Aucune opportunité (opportunities) dégagée.",
        "Une carte qui ne débouche sur aucune action est une affiche. Au moins une question « Comment pourrions-nous … » par creux de frustration.",
    ),
    "L061": ("Irritant grave « {pp} » sans opportunité liée.", ""),
    "L062": ("{n} opportunité(s) sans score impact/effort – pas de priorisation possible.", ""),
    "L063": (
        "Aucune opportunité n'a de user stories – la story map reste vide.",
        "journeykit export --format storymap montre ce qui en ressort.",
    ),
    # Blueprint au lieu de parcours
    "L070": (
        "Aucun diagnostic initial (meta.diagnosis) : pourquoi s'agit-il d'un parcours usager et non d'un service blueprint ?",
        "",
    ),
    "L071": (
        "{notes} notes de coulisses pour {n} étapes.",
        "L'intérêt se situe manifestement derrière la ligne de visibilité. Établir un service blueprint et y renvoyer dans meta.diagnosis.backstage_documented_in.",
    ),
    "L072": (
        "map_type = {map_type} : les règles sur l'expérience ne s'appliquent que partiellement.",
        "",
    ),
    "L073": (
        "{delegated} des {n} étapes sont exécutées par des tiers à la place de la persona (performed_by.kind = intermediary).",
        "Est-ce encore le parcours de la persona – ou celui de l'intermédiaire ? Vérifier le diagnostic ; le cas échéant, étudier l'intermédiaire comme persona à part entière.",
    ),
    # Données personnelles
    "L080": (
        "La source « {source} » contient des données personnelles (pii_status = contains_pii).",
        "Anonymiser ou pseudonymiser avant de partager ; ne référencer que l'emplacement, pas le matériel.",
    ),
    "L081": ("La preuve « {atom} » contient peut-être {what}.", ""),
    # Indicateurs
    "L090": (
        "Aucun indicateur saisi.",
        "Au moins un indicateur de résultat par phase (taux de traitement, demandes de précision, délai de traitement) – sinon l'effet ne peut pas être démontré.",
    ),
    "L091": (
        "L'indicateur « {name} » a une connotation commerciale.",
        "Traduire en termes administratifs (conversion → part des demandes abouties, churn → recours à des contournements ou à des réclamations) ; consigner l'original dans commercial_equivalent.",
    ),
    "L092": (
        "Uniquement des indicateurs retardés (lagging) – aucun signal d'alerte précoce.",
        "La charge par demande ou le taux de demandes de précision par étape sont des indicateurs avancés.",
    ),
    # Qualité des preuves
    "L100": (
        "{n} atome(s) de preuve référencé(s) nulle part : {ids}.",
        "Matériel non synthétisé – soit l'intégrer, soit le marquer délibérément comme « hors périmètre ».",
    ),
    "L101": (
        "La preuve « {atom} » contredit {others}.",
        "Les contradictions ont leur place dans le parcours (p. ex. comme cas limite ou question ouverte), sans être lissées.",
    ),
    "L102": (
        "{n} preuve(s) primaire(s) sans emplacement (locator).",
        "Sans emplacement, une citation ne peut pas être vérifiée.",
    ),
}

# Was L081 gefunden hat, mit Artikel – die Grammatik unterscheidet sich je Sprache.
_PII_LABELS = {
    "de": {"email": "eine E-Mail-Adresse", "phone": "eine Telefonnummer", "ahv": "eine AHV-Nummer"},
    "fr": {
        "email": "une adresse e-mail",
        "phone": "un numéro de téléphone",
        "ahv": "un numéro AVS",
    },
}

_SUMMARY = {
    "de": "{path}: {errors} Fehler · {warnings} Warnungen · {infos} Hinweise",
    "fr": "{path} : {errors} erreur(s) · {warnings} avertissement(s) · {infos} remarque(s)",
}

_NBSP, _NNBSP = " ", " "


def typo_fr(text: str) -> str:
    """Französische Typografie: geschützte Leerzeichen vor Doppelpunkt & Co. und in Guillemets."""
    for mark in (":", ";", "?", "!"):
        text = text.replace(f" {mark}", f"{_NBSP}{mark}")
    return text.replace("« ", f"«{_NNBSP}").replace(" »", f"{_NNBSP}»")


MESSAGES: dict[str, dict[str, tuple[str, str]]] = {
    "de": _DE,
    "fr": {k: (typo_fr(m), typo_fr(h)) for k, (m, h) in _FR.items()},
}
PII_LABELS = _PII_LABELS
SUMMARY = {"de": _SUMMARY["de"], "fr": typo_fr(_SUMMARY["fr"])}


# Anti-Patterns, nach denen der Audit-Report gliedert (der Viewer hat eigene Kurzformen)
ANTIPATTERN_LABELS: dict[str, dict[str, str]] = {
    "de": {
        "integrity": "Referenzen und IDs",
        "inside_out": "Inside-Out Bias (Annahmen statt Nutzerevidenz)",
        "happy_path": "Happy Path Bias (keine Breakdowns, keine Recovery)",
        "static_map": "Static Map Trap (keine Verantwortung, kein Review)",
        "empathy_vacuum": "Empathie-Vakuum (Klicks ohne Gedanken und Gefühle)",
        "overcomplexity": "Überkomplexität (zu viele Phasen, kein Scope)",
        "micro_disconnect": "Micro-Level Disconnect (keine Übersetzung in Massnahmen)",
        "blueprint": "Service Blueprint statt User Journey",
        "privacy": "Personendaten",
        "kpi": "Kennzahlen",
        "evidence": "Evidenzqualität",
    },
    "fr": {
        "integrity": "Références et ID",
        "inside_out": "Biais de la vue interne (suppositions au lieu de preuves issues des usagers)",
        "happy_path": "Biais du parcours idéal (ni ruptures, ni rattrapage)",
        "static_map": "Piège de la carte figée (ni responsabilité, ni révision)",
        "empathy_vacuum": "Vide d'empathie (des clics sans pensées ni ressenti)",
        "overcomplexity": "Surcomplexité (trop de phases, pas de périmètre)",
        "micro_disconnect": "Déconnexion du niveau micro (pas de traduction en mesures)",
        "blueprint": "Service blueprint au lieu de parcours usager",
        "privacy": "Données personnelles",
        "kpi": "Indicateurs",
        "evidence": "Qualité des preuves",
    },
}


def check_language(lang: str) -> str:
    if lang not in LANGUAGES:
        raise ValueError(f"Keine Lint-Meldungen in «{lang}» – verfügbar: {', '.join(LANGUAGES)}.")
    return lang


def resolve_language(journey: dict[str, Any], lang: str | None = None) -> str:
    """Ausdrücklich gewählt, sonst meta.language der Journey, sonst Deutsch."""
    if lang is not None:
        return check_language(lang)
    meta_lang = journey.get("meta", {}).get("language")
    return meta_lang if meta_lang in LANGUAGES else "de"


def render_message(lang: str, msg_id: str, **params: Any) -> tuple[str, str]:
    """(Meldung, Hinweis) in der Sprache, Platzhalter gefüllt."""
    message, hint = MESSAGES[lang][msg_id]
    return message.format(**params), hint.format(**params)
