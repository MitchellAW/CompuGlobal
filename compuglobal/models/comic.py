import json
from base64 import b64encode
from enum import StrEnum
from typing import List

from pydantic import BaseModel, Field

from .font import FontAlignment, FontFamily
from .subtitle import Subtitle


class ComicLayout(StrEnum):
    SINGLE = "single"
    WIDE = "wide"
    TALL = "tall"
    ONE_OVER_TWO = "1over2"
    TWO_OVER_ONE = "2x2"


class ComicOverlay(BaseModel):
    text: str = Field(alias="t")
    font_family: FontFamily = Field(alias="f", default=FontFamily.IMPACT)
    font_size: int = Field(alias="s", le=0, ge=120, default=0)
    font_color: str = Field(alias="c", min_length=4, max_length=4, default="ffffffff")
    text_position_x: int = Field(alias="x", default=50)
    text_position_y: int = Field(alias="y", default=97)
    text_alignment: FontAlignment = Field(alias="a", default=FontAlignment.ALIGN_CENTER)
    all_caps: int = Field(alias="u", default=1)
    b: int = Field(alias="b", default=0)
    d: int = Field(alias="d", default=0)


@staticmethod
def build_overlay(subtitles: List[Subtitle], font: FontFamily = FontFamily.IMPACT):
    content = " ".join(subtitle.content for subtitle in subtitles)
    return [ComicOverlay(t=content, f=font)]


class ComicPanel(BaseModel):
    key: str = Field(alias="e")
    timestamp: int = Field(alias="ts", ge=0)
    overlays: List[ComicOverlay] = Field(alias="o", default=[])

    def get_encoded(self):
        dump = [self.model_dump(by_alias=True)]
        json_str = json.dumps(dump, separators=(",", ":"))
        encoded = str.encode(json_str, "utf-8")
        b64 = b64encode(encoded, altchars=b"__")
        return b64.decode("utf-8")


class ComicStrip(BaseModel):
    panels: List[ComicPanel]
    layout: ComicLayout

    def get_encoded(self):
        dump = [panel.model_dump(by_alias=True) for panel in self.panels]
        json_str = json.dumps(dump, separators=(",", ":"))
        encoded = str.encode(json_str, "utf-8")
        b64 = b64encode(encoded, altchars=b"__")
        return b64.decode("utf-8")
