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
from compuglobal.models.font import FontAlignment, FontColor, FontFamily
from compuglobal.models.frame import Frame, FrameResult
from compuglobal.models.overlay import OverlayFormat
from compuglobal.models.screencap import Screencap, ScreencapMoment
from compuglobal.models.stream import Stream, StreamOverlay
from compuglobal.models.subtitle import Subtitle
from compuglobal.models.timestamp import Timestamp

__title__ = "compuglobal"
__author__ = "MitchellAW"
__license__ = "MIT"
__version__ = "0.4.1"

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
    "FontColor",
    "FontFamily",
    "Frame",
    "FrameResult",
    "Frinkiac",
    "MasterOfAllScience",
    "Morbotron",
    "NoSearchResultsFoundError",
    "OverlayFormat",
    "Screencap",
    "ScreencapMoment",
    "Stream",
    "StreamOverlay",
    "Subtitle",
    "Timestamp",
]
