from typing import List

from pydantic import BaseModel, Field

from .episode import Episode
from .frame import Frame
from .subtitle import Subtitle


class Screencap(BaseModel, frozen=True):
    """A Screencap of an episode at a point in time of a TV Show.

    Attributes
    ----------
    episode: str
        The episode key (S01E01)
    frame: Frame
        The primary frame of the screencap
    subtitles: List[Subtitle]
        The subtitles of the screencap
    nearby: List[Frame]
        A list of nearby frames
    min_timestamp: int
        The minimum timestamp of the screencap
    max_timestamp: int
        The maximum timestamp of the screencap
    """

    episode: Episode = Field(alias="Episode")
    frame: Frame = Field(alias="Frame")
    subtitles: List[Subtitle] = Field(alias="Subtitles")
    nearby: List[Frame] = Field(alias="Nearby")
    min_timestamp: int = Field(alias="MinTimestamp", ge=0)
    max_timestamp: int = Field(alias="MaxTimestamp", ge=0)

    def get_real_timestamp(self):
        """Gets a readable timestamp for the frame in format "mm:ss"

        Returns
        -------
        str
            A readable timestamp for the frame in format `mm:ss`."""

        return self.frame.get_real_timestamp()

    def get_caption(self) -> str:
        """Gets the entire caption fo the screencap from all subtitles as a string.

        Returns
        -------
        str
            The entire caption of the screencap
        """
        return " ".join(f"{subtitle.content}" for subtitle in self.subtitles)

    def __str__(self):
        return str(self.frame)
