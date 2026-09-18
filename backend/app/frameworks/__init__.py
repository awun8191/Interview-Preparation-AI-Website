"""Framework catalogs and rubric definitions for The-Plan-Software.

Exports registry lookup functions and catalog definitions for all 11 communication methodologies.
"""

from typing import Any

from app.frameworks.base import (
    CriteriaOption,
    FrameworkCatalog,
    JevQuestionDefinition,
    QuestionType,
)
from app.frameworks.catalogs import ALL_CATALOGS, CATALOG_MAP


def get_framework_catalog(framework: str | Any) -> FrameworkCatalog:
    """Retrieve the authoritative catalog for a given framework.

    Supports canonical names (e.g. 'STAR', 'CARL'), lowercase/mixed case,
    wire aliases ('VOSS_NEGOTIATION', 'DUARTE_SPARKLINE', 'MONROE_SEQUENCE'),
    and enum instances.
    """
    key = str(framework.value) if hasattr(framework, "value") else str(framework)

    normalized_key = key.strip().upper().replace(" ", "_").replace("-", "_")

    if normalized_key in CATALOG_MAP:
        return CATALOG_MAP[normalized_key]

    valid = sorted(list({c.framework for c in ALL_CATALOGS}))
    raise ValueError(
        f"Unsupported framework '{framework}'. Valid framework keys: {', '.join(valid)}"
    )


def list_framework_catalogs() -> list[FrameworkCatalog]:
    """Return all 11 framework catalogs."""
    return list(ALL_CATALOGS)


def list_supported_frameworks() -> list[str]:
    """Return canonical keys for all 11 supported frameworks."""
    return sorted(list({c.framework for c in ALL_CATALOGS}))


__all__ = [
    "ALL_CATALOGS",
    "CATALOG_MAP",
    "CriteriaOption",
    "FrameworkCatalog",
    "JevQuestionDefinition",
    "QuestionType",
    "get_framework_catalog",
    "list_framework_catalogs",
    "list_supported_frameworks",
]
