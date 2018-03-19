class Screencap:
    """Represents a screencap of a TVShow/Movie/Skit generated using an instance
    of CompuGlobalAPI.

    Parameters
    ----------
    api: CompuGlobalAPI
        The CompuGlobalAPI object that was used to generate the screencap.
    json: dict
        The json response from the API for the screencap.

    Attributes
    ----------
        id: int
            The ID of the screencap.
        key: str
            The episode key (S01E01) of the screencap.
        episode: int
            The episode number of the screencap.
        season: int
            The season number of the screencap.
        title: str
            The title of the episode.
        director: str
            The director(s) of the episode.
        writer: str
            The writer(s) of the episode.
        air_date: str
            The original air date of the episode.
        wiki_url: str
            Url to the wiki of the episode.
        timestamp: int
            The timestamp of the screencap.
        caption: str
            The caption/subtitles during the screencap.
        image_url: str
            The url format for the image.
        meme_url: str
            The meme url format for the image embedded with a caption.
        gif_url: str
            The gif url format for the screencap embedded with a caption.
        mp4_url: str
            The mp4 url format for the screencap embedded with a caption.
        """
    def __init__(self, api, json: dict):
        self.api = api
        self.json = json

        # Inititalise Episode Information, setting title, director, writer
        # and wiki url to None if they are empty
        self.id = self.json['Episode']['Id']
        self.key = self.json['Episode']['Key']
        self.episode = self.json['Episode']['EpisodeNumber']
        self.season = self.json['Episode']['Season']
        self.title = self.get_value(self.json['Episode']['Title'])
        self.director = self.get_value(self.json['Episode']['Director'])
        self.writer = self.get_value(self.json['Episode']['Writer'])
        self.air_date = self.json['Episode']['OriginalAirDate']
        self.wiki_url = self.get_value(self.json['Episode']['WikiLink'])
        self.timestamp = self.json['Frame']['Timestamp']

        # Initalise caption and urls
        self.caption = self.api.json_to_caption(self.json)
        self.image_url = self.api.URL + 'img/{}/{}.jpg'
        self.meme_url = self.api.URL + 'meme/{}/{}.jpg?b64lines={}'
        self.gif_url = self.api.URL + 'gif/{}/{}/{}.gif?b64lines={}'
        self.mp4_url = self.api.URL + 'mp4/{}/{}/{}.mp4?b64lines={}'

    # Returns none if empty string
    @staticmethod
    def get_value(value):
        if value == '':
            return None

        else:
            return value.replace('\n', '')

    def get_real_timestamp(self):
        """Gets a readable timestamp for the screencap in format "mm:ss"

        Returns
        -------
        str
            A readable timestamp for the screencap in format `mm:ss`."""

        seconds = int(self.timestamp / 1000)
        minutes = int(seconds / 60)
        seconds -= int(minutes * 60)
        return '{}:{:02d}'.format(minutes, seconds)

    def get_image_url(self):
        """Returns the direct image url for the screencap without any caption.

        Returns
        -------
        str
            The image url for the screencap without any caption."""
        return self.image_url.format(self.key, self.timestamp)

    def get_meme_url(self, caption=None):
        """Encodes the caption with base64 and then returns the meme url for
        the screencap with an embedded caption.

        Parameters
        ----------
        caption: str, optional
            The caption to embed in the image, if it is None, it will use the
            screencaps original caption.

        Returns
        -------
        str
            The meme url for the screencap with an embedded caption."""
        if caption is None:
            caption = self.caption

        b64_caption = self.api.encode_caption(caption)
        return self.meme_url.format(self.key, self.timestamp, b64_caption)

    async def get_gif_url(self, caption=None, before=3000, after=4000):
        """Gets the timestamps of the frames before and after the timestamp
        of the screencap using the frames endpoint for the screencap's API
        and returns the url for the gif with an embedded caption.

        Parameters
        ----------
        caption: str, optional
            The caption to embed in the gif, if it is None, it will use the
            screencaps original caption.
        before: int, optional
            The number of milliseconds before the screencap's timestamp to
            begin the gif, defaults to 3 seconds (3000ms).
        after: int, optional
            The number of milliseconds after the screencap's timestamp to
            begin the gif, defaults to 4 seconds (4000ms).

        Returns
        -------
        str
            The gif url for the screencap with an embedded caption.

        Note
        ----
        Defaults gif duration to  ~7 seconds (7000ms)."""

        if caption is None:
            caption = self.caption

        b64_caption = self.api.encode_caption(caption)

        # Get start and end frame numbers for gif
        frames = await self.api.get_frames(self.key, self.timestamp,
                                           int(before), int(after))
        start = frames[0]['Timestamp']
        end = frames[-1]['Timestamp']
        return self.gif_url.format(self.key, start, end, b64_caption)

    async def get_mp4_url(self, caption=None, before=3000, after=4000):
        """Gets the timestamps of the frames before and after the timestamp
        of the screencap using the frames endpoint for the screencap's API
        and returns the url for the mp4 with an embedded caption.

        Parameters
        ----------
        caption: str, optional
            The caption to embed in the mp4, if it is None, it will use the
            screencaps original caption.
        before: int, optional
            The number of milliseconds before the screencap's timestamp to
            begin the mp4, defaults to 3 seconds (3000ms).
        after: int, optional
            The number of milliseconds after the screencap's timestamp to
            begin the mp4, defaults to 4 seconds (4000ms).

        Returns
        -------
        str
            The mp4 url for the screencap with an embedded caption.

        Note
        ----
        Defaults mp4 duration to  ~7 seconds (7000ms)."""

        if caption is None:
            caption = self.caption

        b64_caption = self.api.encode_caption(caption)

        # Get start and end frame numbers for gif
        frames = await self.api.get_frames(self.key, self.timestamp,
                                           int(before), int(after))
        start = frames[0]['Timestamp']
        end = frames[-1]['Timestamp']
        return self.mp4_url.format(self.key, start, end, b64_caption)

    def __str__(self):
        return (self.api.title + ' - ' + self.key + ': ' + self.title +
                ' (' + self.get_real_timestamp() + ')')
