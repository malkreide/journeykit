"""Texte der Kommandozeile (Meldungen, Hilfe, Gerüst von ``journeykit new``), je Sprache.

Gleiches Muster wie ``lint_messages.py`` und ``export_texts.py``; geprüft von
``tests/test_cli_texts.py``. Nicht übersetzt werden die Texte, die argparse
selbst erzeugt («usage:», «options:», Fehlermeldungen zu Argumenten), und die
Schemafehler aus ``jsonschema`` – beide sind heute auch in der deutschen
Ausgabe englisch.
"""

from __future__ import annotations

import os
from typing import Any

from .lint_messages import LANGUAGES, typo_fr

ENV_LANG = "JOURNEYKIT_LANG"

_DE: dict[str, str] = {
    # Meldungen
    "written": "geschrieben: {path}",
    "schema_errors": "{path}: {n} Schema-Fehler",
    "valid": "✓ {path}: schema-valide",
    "invalid": "✗ {path}: {n} Schema-Fehler",
    # Hilfe
    "help.description": "Evidenzbasierte User Journeys: prüfen, rendern, exportieren.",
    "help.epilog": "Sprache der Ausgaben: --lang je Befehl, sonst meta.language der Journey; ohne Journey (Hilfe, schema, new) die Umgebungsvariable JOURNEYKIT_LANG (de oder fr), sonst de.",
    "help.validate": "Schema-Validierung",
    "help.lint": "Methodische Prüfung (Fallstricke)",
    "help.strict": "Warnungen gelten als Fehler (Exit 1)",
    "help.quiet": "Hinweise (INFO) unterdrücken",
    "help.today": "Stichtag für Review-Prüfungen (YYYY-MM-DD)",
    "help.lint_lang": "Sprache der Meldungen (Standard: meta.language der Journey, sonst de)",
    "help.render": "Interaktives HTML erzeugen (mehrere Dateien = Persona-Vergleich)",
    "help.render_lang": "Sprache der Oberfläche (Standard: meta.language der ersten Journey, sonst de)",
    "help.export": "Story Map, Massnahmenliste, Chancenmatrix, Audit-Report",
    "help.export_lang": "Sprache der Texte (Standard: meta.language der Journey, sonst de; CSV ist sprachneutral)",
    "help.diff": "Modelländerungen zwischen zwei Versionen",
    "help.diff_lang": "Sprache des Reports (Standard: meta.language der neuen Version, sonst de)",
    "help.schema": "JSON Schema ausgeben",
    "help.new": "Gerüst einer Journey anlegen (Status hypothesis)",
    "help.new_lang": "Sprache der Journey (meta.language) und der Platzhalter",
    # Gerüst (journeykit new)
    "scaffold.diagnosis": "TODO: Warum ist das eine User Journey und kein Service Blueprint oder User Flow?",
    "scaffold.owner": "TODO: verantwortliche Rolle",
    "scaffold.phase": "TODO Phase 1",
    "scaffold.step": "TODO Schritt",
    "scaffold.action": "TODO: Was tut die Persona?",
    "scaffold.question": "TODO: Welche Erhebung validiert diese Hypothesen zuerst?",
    "scaffold.changelog": "Gerüst angelegt",
}

_FR: dict[str, str] = {
    # Messages
    "written": "écrit : {path}",
    "schema_errors": "{path} : {n} erreur(s) de schéma",
    "valid": "✓ {path} : conforme au schéma",
    "invalid": "✗ {path} : {n} erreur(s) de schéma",
    # Aide
    "help.description": "Parcours usagers fondés sur des preuves : vérifier, afficher, exporter.",
    "help.epilog": "Langue des sorties : --lang par commande, sinon meta.language du parcours ; sans parcours (aide, schema, new), la variable d'environnement JOURNEYKIT_LANG (de ou fr), sinon de.",
    "help.validate": "Validation du schéma",
    "help.lint": "Contrôle méthodologique (pièges)",
    "help.strict": "Les avertissements comptent comme des erreurs (code de sortie 1)",
    "help.quiet": "Masquer les remarques (INFO)",
    "help.today": "Date de référence pour les contrôles de révision (AAAA-MM-JJ)",
    "help.lint_lang": "Langue des messages (par défaut : meta.language du parcours, sinon de)",
    "help.render": "Générer le HTML interactif (plusieurs fichiers = comparaison de personas)",
    "help.render_lang": "Langue de l'interface (par défaut : meta.language du premier parcours, sinon de)",
    "help.export": "Story map, liste des mesures, matrice des opportunités, rapport d'audit",
    "help.export_lang": "Langue des textes (par défaut : meta.language du parcours, sinon de ; le CSV est neutre)",
    "help.diff": "Modifications du modèle entre deux versions",
    "help.diff_lang": "Langue du rapport (par défaut : meta.language de la nouvelle version, sinon de)",
    "help.schema": "Afficher le schéma JSON",
    "help.new": "Créer l'ossature d'un parcours (statut hypothesis)",
    "help.new_lang": "Langue du parcours (meta.language) et des textes provisoires",
    # Ossature (journeykit new)
    "scaffold.diagnosis": "TODO : pourquoi s'agit-il d'un parcours usager et non d'un service blueprint ou d'un user flow ?",
    "scaffold.owner": "TODO : rôle responsable",
    "scaffold.phase": "TODO Phase 1",
    "scaffold.step": "TODO Étape",
    "scaffold.action": "TODO : que fait la persona ?",
    "scaffold.question": "TODO : quelle enquête valide ces hypothèses en premier ?",
    "scaffold.changelog": "Ossature créée",
}

TEXTS: dict[str, dict[str, str]] = {
    "de": _DE,
    "fr": {k: typo_fr(v) for k, v in _FR.items()},
}


def text(lang: str, key: str, **params: Any) -> str:
    return TEXTS[lang][key].format(**params)


def env_language() -> str:
    """Sprache aus JOURNEYKIT_LANG, sonst Deutsch – für Ausgaben ohne Journey."""
    value = os.environ.get(ENV_LANG, "").strip().lower()
    return value if value in LANGUAGES else "de"
