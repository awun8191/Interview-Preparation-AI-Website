"""Registry of all 11 Communication Framework Catalogs.

Provides pre-instantiated catalogs for Jev System One question submission,
rubric grading, and deterministic scoring.
"""

from app.frameworks.base import FrameworkCatalog
from app.frameworks.catalogs.carl import CATALOG as CARL_CATALOG
from app.frameworks.catalogs.gottman import CATALOG as GOTTMAN_CATALOG
from app.frameworks.catalogs.monroe import CATALOG as MONROE_CATALOG
from app.frameworks.catalogs.par import CATALOG as PAR_CATALOG
from app.frameworks.catalogs.radical_candor import CATALOG as RADICAL_CANDOR_CATALOG
from app.frameworks.catalogs.sbi import CATALOG as SBI_CATALOG
from app.frameworks.catalogs.scqa import CATALOG as SCQA_CATALOG
from app.frameworks.catalogs.sparkline import CATALOG as SPARKLINE_CATALOG
from app.frameworks.catalogs.star import CATALOG as STAR_CATALOG
from app.frameworks.catalogs.state import CATALOG as STATE_CATALOG
from app.frameworks.catalogs.voss import CATALOG as VOSS_CATALOG

ALL_CATALOGS: list[FrameworkCatalog] = [
    STAR_CATALOG,
    CARL_CATALOG,
    PAR_CATALOG,
    SCQA_CATALOG,
    SBI_CATALOG,
    RADICAL_CANDOR_CATALOG,
    STATE_CATALOG,
    GOTTMAN_CATALOG,
    VOSS_CATALOG,
    SPARKLINE_CATALOG,
    MONROE_CATALOG,
]

CATALOG_MAP: dict[str, FrameworkCatalog] = {
    "STAR": STAR_CATALOG,
    "CARL": CARL_CATALOG,
    "PAR": PAR_CATALOG,
    "SCQA": SCQA_CATALOG,
    "SBI": SBI_CATALOG,
    "RADICAL_CANDOR": RADICAL_CANDOR_CATALOG,
    "STATE": STATE_CATALOG,
    "GOTTMAN": GOTTMAN_CATALOG,
    "VOSS": VOSS_CATALOG,
    "VOSS_NEGOTIATION": VOSS_CATALOG,
    "SPARKLINE": SPARKLINE_CATALOG,
    "DUARTE_SPARKLINE": SPARKLINE_CATALOG,
    "MONROE": MONROE_CATALOG,
    "MONROE_SEQUENCE": MONROE_CATALOG,
}

__all__ = [
    "ALL_CATALOGS",
    "CATALOG_MAP",
    "CARL_CATALOG",
    "GOTTMAN_CATALOG",
    "MONROE_CATALOG",
    "PAR_CATALOG",
    "RADICAL_CANDOR_CATALOG",
    "SBI_CATALOG",
    "SCQA_CATALOG",
    "SPARKLINE_CATALOG",
    "STAR_CATALOG",
    "STATE_CATALOG",
    "VOSS_CATALOG",
]
