from typing import List

from pydantic import BaseModel, Field

from .font import FontAlignment, FontFamily


class StreamOverlay(BaseModel):
    text: str = Field(alias="text")
    font_family: FontFamily = Field(alias="font", default=FontFamily.IMPACT)
    font_size: int = Field(alias="size", le=0, ge=120)
    font_color: List[int] = Field(alias="color", min_length=4, max_length=4, default=[255, 255, 255, 255])
    text_position_x: int = Field(alias="x")
    text_position_y: int = Field(alias="y")
    text_alignment: FontAlignment = Field(alias="text_align")
    all_caps: bool = Field(alias="all_caps")
    start: int = Field(alias="start", ge=0)
    end: int = Field(alias="end", ge=0)


class Stream(BaseModel):
    key: str = Field(alias="episode")
    start: int = Field(alias="start", ge=0)
    end: int = Field(alias="end", ge=0)
    overlays: List[StreamOverlay] = Field(alias="overlays")
    check_only: bool = Field(alias="check_only")
