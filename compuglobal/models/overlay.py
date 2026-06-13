"""Helper class for formatting of StreamOverlays and ComicOverlays."""

import dataclasses
from dataclasses import dataclass

from compuglobal.models.font import FontAlignment, FontFamily


@dataclass(frozen=True)
class OverlayFormat:
    """The formatting style to use in an overlay.

    Attributes
    ----------
    font_family : FontFamily
        The font to use for the text in the overlay
    font_size : int
        The size of the font in the overlay
    font_color : tuple[int, int, int, int]
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

    font_family: FontFamily = FontFamily.IMPACT
    font_size: int = 0
    font_color: tuple[int, int, int, int] = (255, 255, 255, 255)
    text_position_x: int = 50
    text_position_y: int = 97
    text_alignment: FontAlignment = FontAlignment.ALIGN_CENTER
    all_caps: bool = True

    def __post_init__(self) -> None:
        """Validate font_color is correct.

        Raises
        ------
        ValueError
            If font_colour does not contain 4 values, or any values are not between 0 and 255.

        """
        required_rgba_values = 4
        if len(self.font_color) != required_rgba_values:
            msg = f"font_color must have exactly 4 values (RGBA), got {len(self.font_color)}"
            raise ValueError(msg)

        min_color, max_color = 0, 255
        if not all(min_color <= color <= max_color for color in self.font_color):
            msg = f"font_color values must be between 0 and 255, got {self.font_color}"
            raise ValueError(msg)

    def _changed_fields(self) -> dict:
        return {f.name: getattr(self, f.name) for f in dataclasses.fields(self) if getattr(self, f.name) != f.default}

    def __str__(self) -> str:  # noqa: D105
        return str(self._changed_fields())

    @property
    def font_color_hex(self) -> str:
        """The font color as a hex string.

        Returns
        -------
        str
            The color hex code

        """
        r, g, b, a = self.font_color
        return f"{r:02x}{g:02x}{b:02x}{a:02x}"

    @classmethod
    def normalise(
        cls,
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
            return size * [cls()]

        if isinstance(overlay_format, cls):
            return size * [overlay_format]

        if len(overlay_format) < size:
            return overlay_format + [cls()] * (size - len(overlay_format))

        return overlay_format[:size]
