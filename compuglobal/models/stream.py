"""Streams are posted to the CGHMC APIs for generating gifs/mp4s."""

from pydantic import Field

from compuglobal.models.base import BaseCompuGlobalModel
from compuglobal.models.font import FontAlignment, FontFamily
from compuglobal.models.overlay import OverlayFormat
from compuglobal.models.screencap import Screencap


class StreamOverlay(BaseCompuGlobalModel):
    """A subtitle overlay to use in a gif for a given period of time in a TV show.

    Attributes
    ----------
    text : str
        The content/text of the subtitle in the overlay
    font_family : FontFamily
        The font to use for the text in the overlay
    font_size : int
        The size of the font in the overlay
    font_color : list[int]
        The color of the font as an RGB list [0-255, 0-255, 0-255]
    text_position_x : int
        The position of the text on the X-axis
    text_position_y : int
        The position of the text on the Y-axis
    text_alignment : FontAlignment
        How to align the text of the overlay
    all_caps : bool
        Whether to have all text in uppercase
    start : int
        The time where the overlay begins
    end : int
        The time where the overlay ends

    """

    text: str = Field(alias="text")
    font_family: FontFamily = Field(alias="font", default=FontFamily.IMPACT)
    font_size: int = Field(alias="size", ge=0, le=120, default=0)
    font_color: list[int] = Field(alias="color", min_length=4, max_length=4, default=[255, 255, 255, 255])
    text_position_x: int = Field(alias="x", default=50)
    text_position_y: int = Field(alias="y", default=97)
    text_alignment: FontAlignment = Field(alias="text_align", default=FontAlignment.ALIGN_CENTER)
    all_caps: bool = Field(alias="all_caps", default=True)
    start: int = Field(alias="start", ge=0)
    end: int = Field(alias="end", ge=0)

    @classmethod
    def build_with_format(
        cls,
        *,
        text: str,
        start: int,
        end: int,
        overlay_format: OverlayFormat,
    ) -> "StreamOverlay":
        """Build a StreamOverlay using an OverlayFormat.

        Parameters
        ----------
        text : str
            The content/text of the subtitle in the overlay
        start : int
            The time where the overlay begins
        end : int
            The time where the overlay ends
        overlay_format : OverlayFormat
            The format to use for all formatting in the overlay

        Returns
        -------
        StreamOverlay
            The overlay with the given formatting

        """
        return cls(
            text=text,
            start=start,
            end=end,
            font_family=overlay_format.font_family,
            font_color=overlay_format.font_color,
            font_size=overlay_format.font_size,
            text_position_x=overlay_format.text_position_x,
            text_position_y=overlay_format.text_position_y,
            text_alignment=overlay_format.text_alignment,
            all_caps=overlay_format.all_caps,
        )


class Stream(BaseCompuGlobalModel):
    """A stream/gif of a TV show.

    Attributes
    ----------
    key : str
        The episode key (S01E01)
    start : int
        The timestamp of the start the stream
    end : int
        The timestamp of the end of the stream
    overlays : list[StreamOverlay]
        A list of stream overlays to use throughout the stream
    check_only : bool
        Whether to only check locally, or render the stream for others

    """

    key: str = Field(alias="episode")
    start: int = Field(alias="start", ge=0)
    end: int = Field(alias="end", ge=0)
    overlays: list[StreamOverlay] = Field(alias="overlays")
    check_only: bool = Field(alias="check_only")

    @classmethod
    def from_screencap(
        cls,
        *,
        screencap: Screencap,
        overlay_format: OverlayFormat | list[OverlayFormat] | None = None,
    ) -> "Stream":
        """Build a stream using a screencap object.

        Parameters
        ----------
        screencap : Screencap
            The screencap to use for the Stream
        overlay_format : OverlayFormat | list[OverlayFormat] | None, optional
            The format(s) to use in the overlays. See :meth:`OverlayFormat.normalise` for
            full details on how formats are resolved.

        Returns
        -------
        Stream
            The stream with overlays for the given screencap.

        """
        overlays = cls.build_stream_overlays(screencap, overlay_format)

        return cls(
            episode=screencap.episode.key,
            start=screencap.get_start(),
            end=screencap.get_end(),
            overlays=overlays,
            check_only=False,
        )

    @staticmethod
    def build_stream_overlays(
        screencap: Screencap,
        overlay_format: OverlayFormat | list[OverlayFormat] | None = None,
    ) -> list[StreamOverlay]:
        """Build stream overlays with the given screencap, subtitles, timestamp, and font.

        Parameters
        ----------
        screencap : Screencap
            The screencap to use for the overlays
        overlay_format : OverlayFormat | list[OverlayFormat] | None, optional
            The format(s) to use in the overlays. See :meth:`OverlayFormat.normalise` for
            full details on how formats are resolved.

        Returns
        -------
        list[StreamOverlay]
            The built list of overlays for the stream

        """
        overlay_format = OverlayFormat.normalise(overlay_format, len(screencap.subtitles))

        return [
            StreamOverlay.build_with_format(
                text=subtitle.content,
                start=subtitle.start_timestamp - screencap.get_start(),
                end=subtitle.end_timestamp - screencap.get_start(),
                overlay_format=overlay_format,
            )
            for subtitle, overlay_format in zip(screencap.subtitles, overlay_format, strict=True)
        ]

    def get_caption(self) -> str:
        """Get the entire caption of the Stream (all overlays) as a string.

        Returns
        -------
        str
            The entire caption of the stream

        """
        return " ".join(f"{overlay.text}" for overlay in self.overlays)
