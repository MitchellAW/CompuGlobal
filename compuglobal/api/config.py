from dataclasses import dataclass

from ..models.font import FontFamily


@dataclass
class CompuGlobalAPIConfig:
    title: str
    default_font: FontFamily = FontFamily.IMPACT
