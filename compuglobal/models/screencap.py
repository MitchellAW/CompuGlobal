from typing import List

from pydantic import Field

from .base import BaseCompuGlobalModel
from .episode import Episode
from .frame import Frame
from .subtitle import Subtitle


class Screencap(BaseCompuGlobalModel):
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

    def __str__(self):
        return str(self.frame)
