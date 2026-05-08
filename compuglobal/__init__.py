"""Python wrapper for the CGHMC API (Frinkiac, Morbotron Master Of All Science and more!"""

from .aio import (
    AsyncCompuGlobalAPI,
    CapitalBeatUs,
    Frinkiac,
    MasterOfAllScience,
    Morbotron,
)
from .errors import APIPageStatusError, NoSearchResultsFound
from .models.comic import ComicStrip
from .models.episode import Episode
from .models.font import FontAlignment, FontColorRGB, FontFamily
from .models.frame import Frame
from .models.screencap import Screencap
from .models.subtitle import Subtitle
from .models.stream import StreamOverlay, Stream

__title__ = "compuglobal"
__author__ = "MitchellAW"
__license__ = "MIT"
__version__ = "0.3.0"

__all__ = [
    "APIPageStatusError",
    "NoSearchResultsFound",
    "ComicStrip",
    "Frame",
    "Screencap",
    "Episode",
    "FontAlignment",
    "FontColorRGB",
    "FontFamily",
    "Subtitle",
    "Stream",
    "StreamOverlay",
    "CapitalBeatUs",
    "Frinkiac",
    "MasterOfAllScience",
    "Morbotron",
    "AsyncCompuGlobalAPI",
]
