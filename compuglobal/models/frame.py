from pydantic import BaseModel, Field, model_validator

from compuglobal.core import BaseCompuGlobalAPI


class Frame(BaseModel):

    id: int = Field(alias="Id")
    key: str = Field("Episode")
    timestamp: int = Field(alias="Timestamp", ge=0)
    api: BaseCompuGlobalAPI
    image_url: str = ""

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

    @model_validator(mode="after")
    def set_image_url(self):
        self.image_url = f"{self.api.url}img/{self.key}/{self.timestamp}.jpg"
        return self

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
        return self.api.title + " - " + self.key
