from enum import StrEnum
from typing import List

from pydantic import BaseModel, Field


class FontFamily(StrEnum):
    IMPACT = "impact"
    COMIC_NEUE = "comicneue"
    JOST = "jost"
    PACIFICO = "pacifico"
    AKBAR = "akbar"
    FR_BOLD = "fr"


class FontAlignment(StrEnum):
    ALIGN_LEFT = "l"
    ALIGN_RIGHT = "r"
    ALIGN_CENTER = "c"


class FontColorRGB(BaseModel):
    red: int = Field(alias="r", ge=0, le=255)
    green: int = Field(alias="g", ge=0, le=255)
    blue: int = Field(alias="b", ge=0, le=255)
    alpha: int = Field(alias="a", ge=0, le=255)

    def get_rgba(self) -> List[int]:
        return [self.red, self.green, self.blue, self.alpha]
