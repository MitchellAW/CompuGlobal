"""Subtitles are used in Screencaps and Comic/Stream overlays."""

from pydantic import Field

from compuglobal.models.base import BaseCompuGlobalModel
from compuglobal.models.timestamp import Timestamp


class Subtitle(BaseCompuGlobalModel):
    """A Subtitle for a given period of time in a TV show.

    Attributes
    ----------
    id : int
        The unique identifier of the subtitle
    representative_timestamp : int
        The primary timestamp of the subtitle
    key : str
        The episode key (S01E01)
    start_timestamp : int
        The timestamp where the subtitle begins
    end_timestamp : int
        The timestamp where the subtitle ends
    content : str
        The content/text of the subtitle
    language : str
        The language of the subtitle

    """

    id: int = Field(alias="Id")
    representative_timestamp: int = Field(alias="RepresentativeTimestamp")
    key: str = Field(alias="Episode")
    start_timestamp: int = Field(alias="StartTimestamp", ge=0)
    end_timestamp: int = Field(alias="EndTimestamp", ge=0)
    content: str = Field(alias="Content")
    language: str = Field(alias="Language")

    @property
    def duration(self) -> int:
        """Get the duration of the subtitle in milliseconds.

        Returns
        -------
        int
            The duration in milliseconds.

        """
        return Timestamp.get_duration(start_timestamp=self.start_timestamp, end_timestamp=self.end_timestamp)

    @property
    def timecode(self) -> str:
        """A readable timecode for the subtitle's representative timestamp in format ``mm:ss``.

        Returns
        -------
        str
            A readable timecode in format ``mm:ss``

        """
        return Timestamp.get_timecode(self.representative_timestamp)
