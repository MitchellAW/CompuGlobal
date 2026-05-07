from pydantic import Field

from .base import BaseCompuGlobalModel


class Frame(BaseCompuGlobalModel):

    id: int = Field(alias="Id")
    key: str = Field(alias="Episode")
    timestamp: int = Field(alias="Timestamp", ge=0)

    """Represents a single frame of a TVShow/Movie/Skit generated using an
    instance of CompuGlobalAPI.

    Parameters
    ----------
    api: CompuGlobalAPI
        The CompuGlobalAPI object that was used to generate the screencap.
    frame_json: dict
        The json response from the API for the screencap.

    Attributes
    ----------
        json: dict
            The json response used to create the frame.
        id: int
            The ID of the frame.
        key: str
            The episode key (S01E01) of the frame.
        timestamp: int
            The timestamp of the frame.
        image_url: str
            The direct url for the frame image.
    """

    @property
    def image_url(self) -> str:
        return self._api.image_url.format(self.key, self.timestamp)

    def get_meme_url(self, caption=None):
        """Encodes the caption with base64 and then returns the meme url for
        the frame with an embedded caption.

        Parameters
        ----------
        caption: str
            The caption to embed in the image.

        Returns
        -------
        str
            The meme url for the frame with an embedded caption."""
        raise NotImplementedError("Coming soon.")

    def get_real_timestamp(self):
        """Gets a readable timestamp for the frame in format "mm:ss"

        Returns
        -------
        str
            A readable timestamp for the frame in format `mm:ss`."""

        seconds = int(self.timestamp / 1000)
        minutes = int(seconds / 60)
        seconds -= int(minutes * 60)
        return "{}:{:02d}".format(minutes, seconds)

    def __str__(self):
        return self._api.title + " - " + self.key
