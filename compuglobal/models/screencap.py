"""Models for  Screencaps and ScreencapMoments."""

from pydantic import Field

from compuglobal.models.base import BaseCompuGlobalModel
from compuglobal.models.episode import EpisodeMetadata
from compuglobal.models.frame import Frame
from compuglobal.models.subtitle import Subtitle
from compuglobal.models.timestamp import Timestamp


class ScreencapMoment(BaseCompuGlobalModel):
    """A moment from an episode with the episode title and a single subtitle.

    Attributes
    ----------
    episode : str
        The episode key (S01E01)
    timestamp : int
        The timestamp of the snapshot
    content : str
        The content of the subtitle
    title : str
        The title of the episode in the snapshot
    video_width : int
        The width of the video in pixels
    video_height : int
        The height of the video in pixels

    """

    episode: str = Field(alias="Episode")
    timestamp: int = Field(alias="Timestamp", ge=0)
    content: str = Field(alias="Content")
    title: str = Field(alias="Title")
    video_width: int = Field(alias="VideoWidth", ge=0, default=480)
    video_height: int = Field(alias="VideoHeight", ge=0, default=360)

    @property
    def key(self) -> str:
        """The episode key of the screencap (S01E01). Just an alias for episode.

        Returns
        -------
        str
            The episode key (S01E01)

        """
        return self.episode

    @property
    def timecode(self) -> str:
        """A readable timecode for the frame's timestamp in format ``mm:ss``.

        Returns
        -------
        str
            A readable timecode in format ``mm:ss``

        """
        return Timestamp.get_timecode(self.timestamp)


class Screencap(BaseCompuGlobalModel):
    """A Screencap of an episode at a point in time of a TV Show.

    Attributes
    ----------
    episode : EpisodeMetadata
        The metadata of the episode in the screencap
    frame : Frame
        The primary frame of the screencap
    subtitles : list[Subtitle]
        The subtitles of the screencap
    nearby : list[Frame]
        A list of nearby frames
    min_timestamp : int
        The minimum timestamp of the episode of the screencap
    max_timestamp : int
        The maximum timestamp of the episode of the screencap

    """

    episode: EpisodeMetadata = Field(alias="Episode")
    frame: Frame = Field(alias="Frame")
    subtitles: list[Subtitle] = Field(alias="Subtitles")
    nearby: list[Frame] = Field(alias="Nearby")
    min_timestamp: int = Field(alias="MinTimestamp", ge=0)
    max_timestamp: int = Field(alias="MaxTimestamp", ge=0)

    @property
    def key(self) -> str:
        """The episode key of the screencap (S01E01).

        Returns
        -------
        str
            The episode key (S01E01)

        """
        return self.frame.key

    @property
    def timestamp(self) -> int:
        """The timestamp of the screencap frame.

        Returns
        -------
        int
            The timestamp

        """
        return self.frame.timestamp

    @property
    def timecode(self) -> str:
        """A readable timecode for the frame's timestamp in format ``mm:ss``.

        Returns
        -------
        str
            A readable timecode in format ``mm:ss``.

        """
        return Timestamp.get_timecode(timestamp=self.frame.timestamp)

    @property
    def duration(self) -> int:
        """Duration of screencap subtitles in milliseconds.

        Returns
        -------
        int
            Duration in milliseconds

        """
        return Timestamp.get_subtitles_duration(self.subtitles)

    @property
    def captions(self) -> list[str]:
        """A list of captions for the screencap from all subtitles.

        Returns
        -------
        list[str]
            A list of captions from the subtitles

        """
        return [f"{subtitle.content}" for subtitle in self.subtitles]

    @property
    def caption(self) -> str:
        """The entire caption for the screencap from all subtitles as a string.

        Returns
        -------
        str
            The entire caption of the screencap

        """
        return " ".join(self.captions)

    @property
    def start(self) -> int:
        """The earliest start timestamp from the subtitles.

        Returns
        -------
        int
            The start timestamp

        """
        return min(subtitle.start_timestamp for subtitle in self.subtitles)

    @property
    def end(self) -> int:
        """The latest end timestamp from the subtitles.

        Returns
        -------
        int
            The end timestamp

        """
        return max(subtitle.end_timestamp for subtitle in self.subtitles)

    def __str__(self) -> str:
        """Get the string representation of the Screencap.

        Returns
        -------
        str
            The string representation of the Screencap.

        """
        return str(self.frame)
