from . import aio, api
from .aio_screencap import AIOScreencap
from .errors import APIPageStatusError, NoSearchResultsFound
from .frame import Frame
from .screencap import Screencap

__title__ = "compuglobal"
__author__ = "MitchellAW"
__license__ = "MIT"
__version__ = "0.2.7"

__all__ = [
    "api",
    "aio",
    "AIOScreencap",
    "APIPageStatusError",
    "NoSearchResultsFound",
    "Frame",
    "Screencap",
]
