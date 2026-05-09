from typing import List

from pydantic import BaseModel, Field

from .episode import EpisodeMetadata
from .frame import Frame
from .subtitle import Subtitle


class ScreencapMoment(BaseModel, frozen=True):
    """A moment from an episode with the episode title and a single subtitle.

    Attributes
    ----------
    episode: str
        The episode key (S01E01)
    timestamp: int
        The timestamp of the snapshot
    content: str
        The content of the subtitle
    title: str
        The title of the episode in the snapshot
    """

    episode: str = Field(alias="Episode")
    timestamp: int = Field(alias="Timestamp", ge=0)
    content: str = Field(alias="Content")
    title: str = Field(alias="Title")


class Screencap(BaseModel, frozen=True):
    """A Screencap of an episode at a point in time of a TV Show.

    Attributes
    ----------
    episode: EpisodeMetadata
        The metadata of the episode in the screencap
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

    episode: EpisodeMetadata = Field(alias="Episode")
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

    def captions(self) -> list[str]:
        """Gets a list of captions for the screencap from all subttiles.

        Returns
        -------
        list[str]
            A list of captions from the subtitles
        """
        return [f"{subtitle.content}" for subtitle in self.subtitles]

    def get_caption(self) -> str:
        """Gets the entire caption for the screencap from all subtitles as a string.

        Returns
        -------
        str
            The entire caption of the screencap
        """
        return " ".join(self.captions())

    def get_start(self) -> int:
        """Gets the earliest start timestamp from the subtitles.

        Returns
        -------
        int
            The start timestamp
        """
        return min(subtitle.start_timestamp for subtitle in self.subtitles)

    def get_end(self) -> int:
        """Gets the latest end timestamp from the subtitles.

        Returns
        -------
        int
            The end timestamp
        """
        return max(subtitle.end_timestamp for subtitle in self.subtitles)

    def __str__(self):
        return str(self.frame)
