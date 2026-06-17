"""Definitions for fonts and text in Comic/Stream overlays."""

from enum import StrEnum

from pydantic import Field

from compuglobal.models.base import BaseCompuGlobalModel


class FontFamily(StrEnum):
    """An enumeration of font families."""

    #: The impact font family
    IMPACT = "impact"

    #: The Comic Neue font family
    COMIC_NEUE = "comicneue"

    #: The Jost font family
    JOST = "jost"

    #: The Pacifico font family
    PACIFICO = "pacifico"

    #: The Akbar font family (Frinkiac default)
    AKBAR = "akbar"

    #: The Fr Bold font family (Morbotron default)
    FR_BOLD = "fr"

    @staticmethod
    def universal_fonts() -> list["FontFamily"]:
        """Get a list of universal fonts that work across all APIs.

        Returns
        -------
        list[FontFamily]
            List of universal fonts

        """
        return [
            FontFamily.IMPACT,
            FontFamily.COMIC_NEUE,
            FontFamily.PACIFICO,
            FontFamily.JOST,
        ]


class FontAlignment(StrEnum):
    """An enumeration of font alignments."""

    #: Align the text to the left
    ALIGN_LEFT = "l"

    #: Align the text to the right
    ALIGN_RIGHT = "r"

    #: Align the text to the center
    ALIGN_CENTER = "c"


class FontColor(BaseCompuGlobalModel):
    """A color for a font.

    Attributes
    ----------
    red : int
        The amount of red in the color (0-255)
    green : int
        The amount of green in the color (0-255)
    blue : int
        The amount of blue in the color (0-255)
    alpha : int, optional
        The amount of alpha transparency in the color (0-255)

    """

    red: int = Field(alias="r", ge=0, le=255, default=255)
    green: int = Field(alias="g", ge=0, le=255, default=255)
    blue: int = Field(alias="b", ge=0, le=255, default=255)
    alpha: int = Field(alias="a", ge=0, le=255, default=255)

    @property
    def rgba(self) -> list[int]:
        """The font color as a list of the rgba values.

        Returns
        -------
        list[int]
            A list of the rgba values in that order [red, green, blue, alpha]

        """
        return [self.red, self.green, self.blue, self.alpha]

    @property
    def hex(self) -> str:
        """The font color as a hex string.

        Returns
        -------
        str
            The color hex code

        """
        return f"{self.red:02x}{self.green:02x}{self.blue:02x}{self.alpha:02x}"

    @classmethod
    def from_rgba(cls, r: int, g: int, b: int, a: int) -> "FontColor":
        """Create a FontColor from rgba.

        Parameters
        ----------
        r : int
            Red (0-255)
        g : int
            Green (0-255)
        b : int
            Blue (0-255)
        a : int
            Alpha (0-255)

        Returns
        -------
        FontColor
            The font color

        """
        return cls(red=r, green=g, blue=b, alpha=a)

    @classmethod
    def from_hex(cls, hex_str: str) -> "FontColor":
        """Create a FontColor from a hex string.

        Parameters
        ----------
        hex_str : str
            A hex color string, with or without a leading ``#``.
            Supports 6-character (RRGGBB) or 8-character (RRGGBBAA) formats.
            Alpha is 255 if not given.

        Returns
        -------
        FontColor
            The color represented by the hex string

        Raises
        ------
        ValueError
            If the hex string is not 6 or 8 characters (excluding ``#``)

        """
        hex_str = hex_str.lstrip("#")

        rgb_size = 6
        rgba_size = 8

        if len(hex_str) not in {rgb_size, rgba_size}:
            msg = f"Hex string must be 6 or 8 characters, got {len(hex_str)}"
            raise ValueError(msg)

        r, g, b = (int(hex_str[i : i + 2], 16) for i in (0, 2, 4))
        a = int(hex_str[rgb_size:rgba_size], 16) if len(hex_str) == rgba_size else 255

        return cls(red=r, green=g, blue=b, alpha=a)
