from enum import StrEnum
from typing import List

from pydantic import BaseModel, Field


class FontFamily(StrEnum):
    AKBAR = "akbar"
    IMPACT = "impact"
    COMIC_NEUE = "comicneue"
    JOST = "jost"
    PACIFICO = "pacifico"


class TextAlignment(StrEnum):
    ALIGN_LEFT = "l"
    ALIGN_RIGHT = "r"
    ALIGN_CENTER = "c"


class Color(BaseModel):
    red: int = Field(alias="r", ge=0, le=255)
    green: int = Field(alias="g", ge=0, le=255)
    blue: int = Field(alias="b", ge=0, le=255)
    alpha: int = Field(alias="a", ge=0, le=255)

    def get_rgba(self) -> List[int]:
        return [self.red, self.green, self.blue, self.alpha]


class Overlay(BaseModel):
    text: str = Field(alias="text")
    font_family: FontFamily = Field(alias="font")
    font_size: int = Field(alias="size", le=0, ge=120)
    font_color: List[int] = Field(alias="color", min_length=4, max_length=4)
    text_position_x: int = Field(alias="x")
    text_position_y: int = Field(alias="y")
    text_alignment: TextAlignment = Field(alias="text_align")
    all_caps: bool = Field(alias="all_caps")
    start: int = Field(alias="start", ge=0)
    end: int = Field(alias="end", ge=0)


class Stream(BaseModel):
    key: str = Field(alias="episode")
    start: int = Field(alias="start", ge=0)
    end: int = Field(alias="end", ge=0)
    overlays: List[Overlay] = Field(alias="overlays")
    check_only: bool = Field(alias="check_only")
