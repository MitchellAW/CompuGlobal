from pydantic import BaseModel, Field


class Frame(BaseModel, frozen=True):
    """A single frame of an episode at a point in time of a TV Show.

    Attributes
    ----------
    id: int
        The unique identifier of the frame
    key: str
        The episode key (S01E01)
    timestamp: int
        The timestamp of the frame
    """

    id: int = Field(alias="Id")
    key: str = Field(alias="Episode")
    timestamp: int = Field(alias="Timestamp", ge=0)

    def get_real_timestamp(self):
        """Gets a readable timestamp for the frame in format "mm:ss"

        Returns
        -------
        str
            A readable timestamp for the frame in format `mm:ss`."""

        seconds = int(self.timestamp / 1000)
        minutes = int(seconds / 60)
        seconds -= int(minutes * 60)
        return f"{minutes}:{seconds:02d}"

    def __str__(self):
        return f"{self.key} - {self.timestamp} ({self.get_real_timestamp()})"
