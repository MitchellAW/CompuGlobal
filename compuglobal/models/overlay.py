"""Helper class for formatting of StreamOverlays and ComicOverlays."""

from pydantic import Field

from compuglobal.models.base import BaseCompuGlobalModel
from compuglobal.models.font import FontAlignment, FontColor, FontFamily


class OverlayFormat(BaseCompuGlobalModel):
    """The formatting style to use in an overlay.

    Attributes
    ----------
    font_family : FontFamily
        The font to use for the text in the overlay
    font_size : int
        The size of the font in the overlay
    font_color : FontColor
        The color of the font as an RGBA tuple (0-255, 0-255, 0-255, 0-255)
    text_position_x : int
        The position of the text on the X-axis
    text_position_y : int
        The position of the text on the Y-axis
    text_alignment : FontAlignment
        How to align the text of the overlay
    all_caps : bool
        Whether to have all text in uppercase

    """

    font_family: FontFamily = Field(default=FontFamily.IMPACT)
    font_size: int = Field(ge=0, le=120, default=0)
    font_color: FontColor = Field(default=FontColor())
    text_position_x: int = Field(default=50)
    text_position_y: int = Field(default=97)
    text_alignment: FontAlignment = Field(default=FontAlignment.ALIGN_CENTER)
    all_caps: bool = Field(default=True)

    def __str__(self) -> str:  # ruff: ignore[undocumented-magic-method]
        return str(self.model_dump(exclude_defaults=True))

    @property
    def font_color_hex(self) -> str:
        """The font color as a hex string.

        Returns
        -------
        str
            The color hex code

        """
        return self.font_color.hex

    @property
    def font_color_rgba(self) -> list[int]:
        """The font color as a a list of rgba values.

        Returns
        -------
        list[int]
            The color in rgba

        """
        return self.font_color.rgba

    @staticmethod
    def normalise(
        overlay_format: "OverlayFormat | list[OverlayFormat] | None",
        size: int,
    ) -> "list[OverlayFormat]":
        """Normalise the given overlay formats into a list of given size.

        Parameters
        ----------
        overlay_format : OverlayFormat | list[OverlayFormat] | None, optional
            The format(s) to use in the overlays:

            - If ``None``, default formatting is applied to all overlays
            - If a single :class:`OverlayFormat`, it is applied to all overlays
            - If a list, each format is applied to the corresponding overlay in order
            - If fewer formats are given than subtitles, default formatting is used for the remainder
            - If more formats are given than subtitles, the extras are ignored
        size : int
            The size of the desired list

        Returns
        -------
        list[OverlayFormat]
            The normalised list of formats with the given size

        """
        if overlay_format is None:
            return size * [OverlayFormat()]

        if isinstance(overlay_format, OverlayFormat):
            return size * [overlay_format]

        if len(overlay_format) < size:
            return overlay_format + [OverlayFormat()] * (size - len(overlay_format))

        return overlay_format[:size]
