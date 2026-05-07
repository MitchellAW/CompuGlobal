from . import aio, api
from .errors import APIPageStatusError, NoSearchResultsFound
from .models.frame import Frame
from .models.screencap import Screencap

__title__ = "compuglobal"
__author__ = "MitchellAW"
__license__ = "MIT"
__version__ = "0.2.7"

__all__ = [
    "api",
    "aio",
    "APIPageStatusError",
    "NoSearchResultsFound",
    "Frame",
    "Screencap",
]
