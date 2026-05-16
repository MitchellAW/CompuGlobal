"""Definitions for fonts and text in Comic/Stream overlays."""

from enum import StrEnum

from pydantic import BaseModel, Field


class FontFamily(StrEnum):
    """An enumeration of font families."""

    IMPACT = "impact"
    COMIC_NEUE = "comicneue"
    JOST = "jost"
    PACIFICO = "pacifico"
    AKBAR = "akbar"
    FR_BOLD = "fr"


class FontAlignment(StrEnum):
    """An enumeration of font alignments."""

    ALIGN_LEFT = "l"
    ALIGN_RIGHT = "r"
    ALIGN_CENTER = "c"


class FontColorRGB(BaseModel):
    """A color for a font.

    Attributes
    ----------
    red: int
        The amount of red in the color (0-255)
    green: int
        The amount of green in the color (0-255)
    blue: int
        The amount of blue in the color (0-255)
    alpha: int
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
