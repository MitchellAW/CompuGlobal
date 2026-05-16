"""Python wrapper for the CGHMC API (Frinkiac, Morbotron Master Of All Science and more."""

from compuglobal.aio import (
    AsyncCompuGlobalAPI,
    CapitalBeatUs,
    Frinkiac,
    # pyrefly: ignore [deprecated]
    MasterOfAllScience,
    Morbotron,
)
from compuglobal.errors import APIPageStatusError, NoSearchResultsFoundError
from compuglobal.models.comic import ComicLayout, ComicOverlay, ComicPanel, ComicStrip
from compuglobal.models.episode import Episode, EpisodeMetadata, EpisodeSummary
from compuglobal.models.font import FontAlignment, FontColorRGB, FontFamily
from compuglobal.models.frame import Frame
from compuglobal.models.screencap import Screencap, ScreencapMoment
from compuglobal.models.stream import Stream, StreamOverlay
from compuglobal.models.subtitle import Subtitle

__title__ = "compuglobal"
__author__ = "MitchellAW"
__license__ = "MIT"
__version__ = "0.3.5"

__all__ = [
    "APIPageStatusError",
    "AsyncCompuGlobalAPI",
    "CapitalBeatUs",
    "ComicLayout",
    "ComicOverlay",
    "ComicPanel",
    "ComicStrip",
    "Episode",
    "EpisodeMetadata",
    "EpisodeSummary",
    "FontAlignment",
    "FontColorRGB",
    "FontFamily",
    "Frame",
    "Frinkiac",
    "MasterOfAllScience",
    "Morbotron",
    "NoSearchResultsFoundError",
    "Screencap",
    "ScreencapMoment",
    "Stream",
    "StreamOverlay",
    "Subtitle",
]
