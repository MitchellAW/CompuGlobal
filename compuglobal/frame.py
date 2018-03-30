class Frame:
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
    def __init__(self, api, frame_json):
        self.json = frame_json
        self.api = api
        self.id = frame_json['Id']
        self.key = frame_json['Episode']
        self.timestamp = frame_json['Timestamp']
        self.image_url = api.URL + 'img/{}/{}.jpg'.format(self.key,
                                                          self.timestamp)

    def get_meme_url(self, caption):
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

        b64_caption = self.api.encode_caption(caption)
        return self.api.URL + 'meme/{}/{}.jpg?b64lines={}'.format(
            self.key, self.timestamp, b64_caption)

    def get_real_timestamp(self):
        """Gets a readable timestamp for the frame in format "mm:ss"

        Returns
        -------
        str
            A readable timestamp for the frame in format `mm:ss`."""

        seconds = int(self.timestamp / 1000)
        minutes = int(seconds / 60)
        seconds -= int(minutes * 60)
        return '{}:{:02d}'.format(minutes, seconds)

    def __str__(self):
        return self.api.title + ' - ' + self.key
