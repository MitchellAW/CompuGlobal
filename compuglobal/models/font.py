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


class FontAlignment(StrEnum):
    """An enumeration of font alignments."""

    #: Align the text to the left
    ALIGN_LEFT = "l"

    #: Align the text to the right
    ALIGN_RIGHT = "r"

    #: Align the text to the center
    ALIGN_CENTER = "c"


class FontColorRGB(BaseCompuGlobalModel):
    """A color for a font.

    Attributes
    ----------
    red : int
        The amount of red in the color (0-255)
    green : int
        The amount of green in the color (0-255)
    blue : int
        The amount of blue in the color (0-255)
    alpha : int
        The amount of alpha transparency in the color (0-255)

    """

    red: int = Field(alias="r", ge=0, le=255)
    green: int = Field(alias="g", ge=0, le=255)
    blue: int = Field(alias="b", ge=0, le=255)
    alpha: int = Field(alias="a", ge=0, le=255)

    def get_rgba(self) -> list[int]:
        """Get a list of the rgba values.

        Returns
        -------
        list[int]
            A list of the rgba values in that order [red, green, blue, alpha]

        """
        return [self.red, self.green, self.blue, self.alpha]
