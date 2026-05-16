from dataclasses import dataclass

from compuglobal.models.font import FontFamily


@dataclass
class CompuGlobalAPIConfig:
    title: str
    default_font: FontFamily = FontFamily.IMPACT
