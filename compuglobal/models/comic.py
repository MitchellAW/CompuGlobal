"""Models for building a comic panel, or comic strip."""

import json
from base64 import b64encode
from enum import IntEnum, StrEnum

from pydantic import Field, model_validator

from compuglobal.models.base import BaseCompuGlobalModel
from compuglobal.models.overlay import OverlayFormat

from .font import FontAlignment, FontFamily
from .screencap import Screencap
from .subtitle import Subtitle


class ComicLayout(StrEnum):
    """Defines a layout to be used by :class:`ComicStrip`."""

    #: A single comic panel only
    SINGLE = "single"

    #: All comic panels laid out horizontally
    WIDE = "wide"

    #: All comic panels laid out vertically
    TALL = "tall"

    #: The first panel will be laid out above the next two panels
    ONE_OVER_TWO = "1over2"

    #: The panels will be laid out in a 2x2 grid layout
    TWO_OVER_ONE = "2x2"


class _DefaultComicLayoutSize(IntEnum):
    SINGLE = 1
    WIDE = 2
    ONE_OVER_TWO = 3
    TWO_OVER_ONE = 4


class ComicOverlay(BaseCompuGlobalModel):
    """Defines an overlay to display text in a comic.

    Attributes
    ----------
    text : str
        Text to overlay in the comic
    font_family : FontFamily
        Font family to use for the text
    font_size : int
        Size of the font
    font_color : str
        Font color as a hex string
    text_position_x : int
        Position of the text overlay on the X-axis
    text_position_y : int
        Position of the text overlay on the Y-axis
    text_alignment : FontAlignment
        Alignment of the text overlay
    all_caps : int
        Whether to have overlay text in all uppercase
    b : int
        Unknown b attribute
    d : int
        Unknown d attribute

    """

    text: str = Field(alias="t", description="Text to overlay")
    font_family: FontFamily = Field(alias="f", description="Font style to use", default=FontFamily.IMPACT)
    font_size: int = Field(alias="s", description="Size of the font", ge=0, le=120, default=0)
    font_color: str = Field(alias="c", description="Font color to use", min_length=8, max_length=10, default="ffffffff")
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
    def build_with_format(cls, *, text: str, overlay_format: OverlayFormat) -> "ComicOverlay":
        """Build a ComicOverlay using an OverlayFormat.

        Parameters
        ----------
        text : str
            The content/text of the subtitle in the overlay
        overlay_format : OverlayFormat
            The format to use for all formatting in the overlay

        Returns
        -------
        ComicOverlay
            The comic overlay with the given formatting

        """
        return cls(
            text=text,
            font_family=overlay_format.font_family,
            font_color=overlay_format.font_color_hex,
            font_size=overlay_format.font_size,
            text_position_x=overlay_format.text_position_x,
            text_position_y=overlay_format.text_position_y,
            text_alignment=overlay_format.text_alignment,
            all_caps=int(overlay_format.all_caps),
        )

    @classmethod
    def from_subtitles(
        cls,
        *,
        subtitles: list[Subtitle],
        overlay_format: OverlayFormat | None = None,
    ) -> "ComicOverlay":
        """Build a comic overlay using a list of Subtitles.

        Parameters
        ----------
        subtitles : list[Subtitle]
            A list of subtitles
        overlay_format : OverlayFormat | None
            The format to use in the overlay

        Returns
        -------
        ComicOverlay
            The overlay to display on a ComicPanel

        """
        if overlay_format is None:
            overlay_format = OverlayFormat()

        text = " ".join(subtitle.content for subtitle in subtitles)
        return cls.build_with_format(text=text, overlay_format=overlay_format)


class ComicPanel(BaseCompuGlobalModel):
    """Defines a comic panel of a TV show.

    Attributes
    ----------
    key : str
        The episode key (S01E01)
    timestamp : int
        The timestamp of the panel
    overlays : list[ComicOverlay]
        The text overlays to use in the panel

    """

    key: str = Field(alias="e", description="The episode key of the panel")
    timestamp: int = Field(alias="ts", ge=0, description="The timestamp of the panel")
    overlays: list[ComicOverlay] = Field(alias="o", description="The text overlays for each panel", default=[])

    @classmethod
    def from_screencap(
        cls,
        *,
        screencap: Screencap,
        overlay_format: OverlayFormat | None = None,
    ) -> "ComicPanel":
        """Build a comic panel from a Screencap.

        Parameters
        ----------
        screencap : Screencap
            Screencap to use for the comic panel
        overlay_format : OverlayFormat | None
            The format to use in the comic panel overlay.

        Returns
        -------
        ComicPanel
            The comic panel of the screencap

        """
        overlays = [ComicOverlay.from_subtitles(subtitles=screencap.subtitles, overlay_format=overlay_format)]

        return cls(e=screencap.frame.key, ts=screencap.frame.timestamp, o=overlays)

    @property
    def encoded(self) -> str:
        """The base 64 encoded representation of this panel.

        Returns
        -------
        str
            A base 64 string

        """
        dump = [self.model_dump()]
        json_str = json.dumps(dump, separators=(",", ":"))
        encoded = str.encode(json_str, "utf-8")
        b64 = b64encode(encoded, altchars=b"__")
        return b64.decode("utf-8")


class ComicStrip(BaseCompuGlobalModel, frozen=False):
    """A comic strip composed of multiple comic panels in a given layout.

    Attributes
    ----------
    panels : list[ComicPanel]
        The list of ComicPanels to use in the comic strip
    layout : ComicLayout | None
        The layout to use when displaying the panels

    """

    panels: list[ComicPanel] = Field(alias="panels", description="The list of ComicPanels to use in the ComicStrip")
    layout: ComicLayout | None = Field(
        alias="layout",
        description="The layout to use when displaying the panels",
        default=None,
    )

    @classmethod
    def from_screencap(
        cls,
        *,
        screencap: Screencap,
        overlay_format: OverlayFormat | list[OverlayFormat] | None = None,
    ) -> "ComicStrip":
        """Build a comic strip from a Screencap object.

        Parameters
        ----------
        screencap : Screencap
            The screencap to use for the comic strip
        overlay_format : OverlayFormat | list[OverlayFormat] | None
            The format(s) to use in the overlays. See :meth:`OverlayFormat.normalise` for
            full details on how formats are resolved.

        Returns
        -------
        ComicStrip
            The comic strip depicting the given screencap

        """
        overlay_formats = OverlayFormat.normalise(overlay_format, len(screencap.subtitles))
        panels = [
            ComicPanel(
                e=screencap.frame.key,
                ts=subtitle.representative_timestamp,
                o=cls.build_comic_overlays([subtitle], overlay_format=overlay_format),
            )
            for subtitle, overlay_format in zip(screencap.subtitles, overlay_formats, strict=True)
        ]

        return cls(panels=panels)

    @staticmethod
    def build_comic_overlays(
        subtitles: list[Subtitle],
        overlay_format: OverlayFormat | list[OverlayFormat] | None = None,
    ) -> list[ComicOverlay]:
        """Build a list comic overlays using the given subtitles and font.

        Parameters
        ----------
        subtitles : list[Subtitle]
            The subtitles to use for the overlays
        overlay_format : OverlayFormat | list[OverlayFormat] | None
            The format(s) to use in the overlays. See :meth:`OverlayFormat.normalise` for
            full details on how formats are resolved.

        Returns
        -------
        list[ComicOverlay]
            A list of comic overlays

        """
        overlay_formats = OverlayFormat.normalise(overlay_format, len(subtitles))
        return [
            ComicOverlay.build_with_format(text=subtitle.content, overlay_format=overlay_format)
            for subtitle, overlay_format in zip(subtitles, overlay_formats, strict=True)
        ]

    @property
    def encoded(self) -> str:
        """The base 64 encoded representation of this comic strip.

        Returns
        -------
        str
            A base 64 string

        """
        dump = [panel.model_dump() for panel in self.panels]
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
        else:
            self.layout = ComicLayout.TWO_OVER_ONE
        return self
