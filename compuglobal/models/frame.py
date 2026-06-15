"""A single frame of a TV episode at a given point in time."""

from pydantic import Field

from compuglobal.models.base import BaseCompuGlobalModel
from compuglobal.models.timestamp import Timestamp


class Frame(BaseCompuGlobalModel):
    """A single frame of an episode at a point in time of a TV Show.

    Attributes
    ----------
    id : int
        The unique identifier of the frame
    key : str
        The episode key (S01E01)
    timestamp : int
        The timestamp of the frame

    """

    id: int = Field(alias="Id")
    key: str = Field(alias="Episode")
    timestamp: int = Field(alias="Timestamp", ge=0)

    @property
    def timecode(self) -> str:
        """A readable timecode for the frame's timestamp in format ``mm:ss``.

        Returns
        -------
        str
            A readable timecode in format ``mm:ss``

        """
        return Timestamp.get_timecode(timestamp=self.timestamp)

    def __str__(self) -> str:
        """Get the string representation of the Frame.

        Returns
        -------
        str
            The frame as a string e.g. S01E01 - 00000001 (00:01)

        """
        return f"{self.key} - {self.timestamp} ({self.timecode})"


class FrameResult(Frame):
    """Extend Frame with additional context from a search result.

    Attributes
    ----------
    content: str
        The subtitle content of the frame of this search result
    title: str
        The title of the episode for this frame

    """

    content: str = Field(alias="Content")
    title: str = Field(alias="Title")
