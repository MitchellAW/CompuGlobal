"""Python wrapper for the CGHMC API (Frinkiac, Morbotron Master Of All Science and more!"""

from .aio import CapitalBeatUs, Frinkiac, MasterOfAllScience, Morbotron
from .errors import APIPageStatusError, NoSearchResultsFound
from .models.frame import Frame
from .models.screencap import Screencap

__title__ = "compuglobal"
__author__ = "MitchellAW"
__license__ = "MIT"
__version__ = "0.3.0"

__all__ = [
    "APIPageStatusError",
    "NoSearchResultsFound",
    "Frame",
    "Screencap",
    "CapitalBeatUs",
    "Frinkiac",
    "MasterOfAllScience",
    "Morbotron",
]
