from typing import List

from pydantic import BaseModel, Field

from .font import FontAlignment, FontFamily
from .subtitle import Subtitle


class StreamOverlay(BaseModel):
    text: str = Field(alias="text")
    font_family: FontFamily = Field(alias="font", default=FontFamily.IMPACT)
    font_size: int = Field(alias="size", le=0, ge=120, default=0)
    font_color: List[int] = Field(alias="color", min_length=4, max_length=4, default=[255, 255, 255, 255])
    text_position_x: int = Field(alias="x", default=50)
    text_position_y: int = Field(alias="y", default=97)
    text_alignment: FontAlignment = Field(alias="text_align", default=FontAlignment.ALIGN_CENTER)
    all_caps: bool = Field(alias="all_caps", default=True)
    start: int = Field(alias="start", ge=0)
    end: int = Field(alias="end", ge=0)


@staticmethod
def build_stream_overlays(subtitles: List[Subtitle], min_timestamp: int, font: FontFamily = FontFamily.IMPACT):
    return [
        StreamOverlay(
            text=subtitle.content,
            font=font,
            start=subtitle.start_timestamp - min_timestamp,
            end=subtitle.end_timestamp - min_timestamp,
        )
        for subtitle in subtitles
    ]


class Stream(BaseModel):
    key: str = Field(alias="episode")
    start: int = Field(alias="start", ge=0)
    end: int = Field(alias="end", ge=0)
    overlays: List[StreamOverlay] = Field(alias="overlays")
    check_only: bool = Field(alias="check_only")
