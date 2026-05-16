"""The configuration for a CGHMC API (title + font)."""

from dataclasses import dataclass

from compuglobal.models.font import FontFamily


@dataclass
class CompuGlobalAPIConfig:
    """The configuration for a CompuGlobal API."""

    title: str
    default_font: FontFamily = FontFamily.IMPACT
