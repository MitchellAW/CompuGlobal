import json
from base64 import b64encode
from enum import StrEnum
from typing import List

from pydantic import BaseModel, Field, model_validator

from .screencap import Screencap
from .font import FontAlignment, FontFamily
from .subtitle import Subtitle


class ComicLayout(StrEnum):
    """Defines a layout to be used by :class:`ComicStrip`"""

    SINGLE = "single"
    WIDE = "wide"
    TALL = "tall"
    ONE_OVER_TWO = "1over2"
    TWO_OVER_ONE = "2x2"


class ComicOverlay(BaseModel, frozen=True):
    """Defines an overlay to display text in a :class:`ComicPanel`"""

    text: str = Field(alias="t", description="Text to overlay")
    font_family: FontFamily = Field(alias="f", description="Font style to use", default=FontFamily.IMPACT)
    font_size: int = Field(alias="s", description="Size of the font", le=0, ge=120, default=0)
    font_color: str = Field(alias="c", description="Font color to use", min_length=4, max_length=4, default="ffffffff")
    text_position_x: int = Field(alias="x", description="The x position of the overlay", default=50)
    text_position_y: int = Field(alias="y", description="The y position of the overlay", default=97)
    text_alignment: FontAlignment = Field(
        alias="a", description="Alignment of the text overlay", default=FontAlignment.ALIGN_CENTER
    )
    all_caps: int = Field(alias="u", description="Display text in all uppercase", default=1)
    b: int = Field(alias="b", description="Time before (unused)", default=0)
    d: int = Field(alias="d", description="Duration (unused)", default=0)

    @classmethod
    def from_subtitles(cls, *, subtitles: List[Subtitle], font_family: FontFamily) -> "ComicOverlay":
        """Builds a comic overlay using a list of Subtitles.

        Parameters
        ----------
        subtitles : List[Subtitle]
            A list of subtitles
        font_family : FontFamily
            The family of font to use for the new overlay.

        Returns
        -------
        ComicOverlay
            The overlay to display on a ComicPanel
        """
        text = " ".join(subtitle.content for subtitle in subtitles)
        return cls(t=text, f=font_family)


class ComicPanel(BaseModel, frozen=True):
    key: str = Field(alias="e", description="The episode key of the panel")
    timestamp: int = Field(alias="ts", ge=0, description="The timestamp of the panel")
    overlays: List[ComicOverlay] = Field(alias="o", description="The text overlays for each panel", default=[])

    @classmethod
    def from_screencap(cls, *, screencap: Screencap, font: FontFamily = FontFamily.IMPACT) -> "ComicPanel":
        overlays = [ComicOverlay.from_subtitles(subtitles=screencap.subtitles, font_family=font)]

        return cls(e=screencap.frame.key, ts=screencap.frame.timestamp, o=overlays)

    def get_encoded(self) -> str:
        """get_encoded Gets the base 64 encoded representation of this panel

        Returns
        -------
        str
            A base 64 string
        """
        dump = [self.model_dump(by_alias=True)]
        json_str = json.dumps(dump, separators=(",", ":"))
        encoded = str.encode(json_str, "utf-8")
        b64 = b64encode(encoded, altchars=b"__")
        return b64.decode("utf-8")


class ComicStrip(BaseModel):
    panels: List[ComicPanel] = Field(alias="panels", description="The list of ComicPanels to use in the ComicStrip")
    layout: ComicLayout | None = Field(
        alias="layout", description="The layout to use when displaying the panels", default=None
    )

    @classmethod
    def from_screencap(cls, *, screencap: Screencap, font_family: FontFamily = FontFamily.IMPACT) -> "ComicStrip":
        """Build a comic strip from a Screencap object.

        Parameters
        ----------
        screencap : Screencap
            The screencap to use for the comic strip
        font_family : FontFamily, optional
            The font to use for all overlays in the comic strip

        Returns
        -------
        ComicStrip
            The comic strip depicting the given screencap
        """
        panels = [
            ComicPanel(
                e=screencap.frame.key,
                ts=screencap.frame.timestamp,
                o=cls.build_comic_overlays(screencap.subtitles, font_family=font_family),
            )
        ]

        return cls(panels=panels)

    @staticmethod
    def build_comic_overlays(
        subtitles: List[Subtitle], font_family: FontFamily = FontFamily.IMPACT
    ) -> List[ComicOverlay]:
        return [ComicOverlay(t=subtitle.content, f=font_family) for subtitle in subtitles]

    def get_encoded(self) -> str:
        """Gets the base 64 encoded representation of this comic strip

        Returns
        -------
        str
            A base 64 string
        """
        dump = [panel.model_dump(by_alias=True) for panel in self.panels]
        json_str = json.dumps(dump, separators=(",", ":"))
        encoded = str.encode(json_str, "utf-8")
        b64 = b64encode(encoded, altchars=b"__")
        return b64.decode("utf-8")

    @model_validator(mode="after")
    def set_default_layout(self):
        # If user explicitly set layout → keep it
        if self.layout is not None:
            return self

        panel_count = len(self.panels)
        if panel_count == 1:
            self.layout = ComicLayout.SINGLE
        elif panel_count == 2:
            self.layout = ComicLayout.WIDE
        elif panel_count == 3:
            self.layout = ComicLayout.ONE_OVER_TWO
        else:
            self.layout = ComicLayout.TWO_OVER_ONE
        return self
