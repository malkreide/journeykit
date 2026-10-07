"""Schema-Validierung einer Journey-Datei."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from . import load_schema


@dataclass(frozen=True)
class SchemaError:
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.path or '<root>'}: {self.message}"


def _pointer(parts: Any) -> str:
    out = ""
    for p in parts:
        out += f"[{p}]" if isinstance(p, int) else (f".{p}" if out else str(p))
    return out


def validate_journey(journey: dict[str, Any]) -> list[SchemaError]:
    """Alle Schema-Verstösse, sortiert nach Pfad. Leere Liste = valide."""
    validator = Draft202012Validator(load_schema(), format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(journey), key=lambda e: list(e.absolute_path))
    return [SchemaError(_pointer(e.absolute_path), e.message) for e in errors]


def is_valid(journey: dict[str, Any]) -> bool:
    return not validate_journey(journey)
