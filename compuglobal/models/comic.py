"""Models for building a comic panel, or comic strip."""

import json
from base64 import b64encode
from enum import IntEnum, StrEnum

from pydantic import BaseModel, Field, model_validator

from .font import FontAlignment, FontFamily
from .screencap import Screencap
from .subtitle import Subtitle


class ComicLayout(StrEnum):
    """Defines a layout to be used by :class:`ComicStrip`."""

    SINGLE = "single"
    WIDE = "wide"
    TALL = "tall"
    ONE_OVER_TWO = "1over2"
    TWO_OVER_ONE = "2x2"


class _DefaultComicLayoutSize(IntEnum):
    SINGLE = 1
    WIDE = 2
    ONE_OVER_TWO = 3
    TWO_OVER_ONE = 4


class ComicOverlay(BaseModel, frozen=True):
    """Defines an overlay to display text in a comic.

    Attributes
    ----------
    text: str
        Text to overlay in the comic
    font_family: FontFamily
        Font family to use for the text
    font_size: int
        Size of the font
    text_position_x: int
        Position of the text overlay on the X-axis
    text_position_y: int
        Position of the text overlay on the Y-axis
    text_alignment: FontAlignment
        Alignment of the text overlay

    """

    text: str = Field(alias="t", description="Text to overlay")
    font_family: FontFamily = Field(alias="f", description="Font style to use", default=FontFamily.IMPACT)
    font_size: int = Field(alias="s", description="Size of the font", ge=0, le=120, default=0)
    font_color: str = Field(alias="c", description="Font color to use", min_length=4, max_length=4, default="ffffffff")
    text_position_x: int = Field(alias="x", description="The x position of the overlay", default=50)
    text_position_y: int = Field(alias="y", description="The y position of the overlay", default=97)
    text_alignment: FontAlignment = Field(
        alias="a",
        description="Alignment of the text overlay",
        default=FontAlignment.ALIGN_CENTER,
    )
    all_caps: int = Field(alias="u", description="Display text in all uppercase", default=1)
    b: int = Field(alias="b", description="Time before (unused)", default=0)
    d: int = Field(alias="d", description="Duration (unused)", default=0)

    @classmethod
    def from_subtitles(
        cls,
        *,
        subtitles: list[Subtitle],
        font_family: FontFamily = FontFamily.IMPACT,
    ) -> "ComicOverlay":
        """Build a comic overlay using a list of Subtitles.

        Parameters
        ----------
        subtitles : List[Subtitle]
            A list of subtitles
        font_family : FontFamily, optional
            The family of font to use for the new overlay.

        Returns
        -------
        ComicOverlay
            The overlay to display on a ComicPanel

        """
        text = " ".join(subtitle.content for subtitle in subtitles)
        return cls(t=text, f=font_family)


class ComicPanel(BaseModel, frozen=True):
    """Defines a comic panel of a TV show.

    Attributes
    ----------
    key: str
        The episode key (S01E01)
    timestamp: int
        The timestamp of the panel
    overlays: List[ComicOverlay]
        The text overlays to use in the panel

    """

    key: str = Field(alias="e", description="The episode key of the panel")
    timestamp: int = Field(alias="ts", ge=0, description="The timestamp of the panel")
    overlays: list[ComicOverlay] = Field(alias="o", description="The text overlays for each panel", default=[])

    @classmethod
    def from_screencap(cls, *, screencap: Screencap, font: FontFamily = FontFamily.IMPACT) -> "ComicPanel":
        """Build a comic panel from a Screencap.

        Parameters
        ----------
        screencap : Screencap
            Screencap to use for the comic panel
        font : FontFamily, optional
            The font to use in the comic overlays

        Returns
        -------
        ComicPanel
            The comic panel of the screencap

        """
        overlays = [ComicOverlay.from_subtitles(subtitles=screencap.subtitles, font_family=font)]

        return cls(e=screencap.frame.key, ts=screencap.frame.timestamp, o=overlays)

    def get_encoded(self) -> str:
        """Get the base 64 encoded representation of this panel.

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
    """A comic strip composed of multiple comic panels in a given layout.

    Attributes
    ----------
    panels: List[ComicPanel]
        The list of ComicPanels to use in the comic strip
    layout: ComicLayout
        The layout to use when displaying the panels

    """

    panels: list[ComicPanel] = Field(alias="panels", description="The list of ComicPanels to use in the ComicStrip")
    layout: ComicLayout | None = Field(
        alias="layout",
        description="The layout to use when displaying the panels",
        default=None,
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
                ts=subtitle.representative_timestamp,
                o=cls.build_comic_overlays([subtitle], font_family=font_family),
            )
            for subtitle in screencap.subtitles
        ]

        return cls(panels=panels)

    @staticmethod
    def build_comic_overlays(
        subtitles: list[Subtitle],
        font_family: FontFamily = FontFamily.IMPACT,
    ) -> list[ComicOverlay]:
        """Build a list comic overlays using the given subtitles and font.

        Parameters
        ----------
        subtitles : List[Subtitle]
            The subtitles to use for the overlays
        font_family : FontFamily, optional
            The font to use in all the comic overlays

        Returns
        -------
        List[ComicOverlay]
            A list of comic overlays

        """
        return [ComicOverlay(t=subtitle.content, f=font_family) for subtitle in subtitles]

    def get_encoded(self) -> str:
        """Get the base 64 encoded representation of this comic strip.

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
    def set_default_layout(self) -> "ComicStrip":
        """Set the default layout for the comic strip based on the number of panels.

        Returns
        -------
        ComicStrip
            The comic strip with default layout.

        """
        # If user explicitly set layout → keep it
        if self.layout is not None:
            return self

        panel_count = len(self.panels)
        if panel_count == _DefaultComicLayoutSize.SINGLE:
            self.layout = ComicLayout.SINGLE
        elif panel_count == _DefaultComicLayoutSize.WIDE:
            self.layout = ComicLayout.WIDE
        elif panel_count == _DefaultComicLayoutSize.ONE_OVER_TWO:
            self.layout = ComicLayout.ONE_OVER_TWO
        elif panel_count == _DefaultComicLayoutSize.TWO_OVER_ONE:
            self.layout = ComicLayout.TWO_OVER_ONE
        else:
            self.layout = ComicLayout.TWO_OVER_ONE
        return self
