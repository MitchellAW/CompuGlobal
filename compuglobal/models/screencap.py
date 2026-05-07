from typing import List

from pydantic import Field

from .base import BaseCompuGlobalModel
from .comic import (
    ComicOverlay,
    ComicPanel,
    ComicStrip,
    build_overlay,
)
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
        frame: Frame
            The representative frame of the screencap.
        id: int
            The screencap ID.
        key: str
            The episode key (S01E01) of the screencap's representative frame.
        timestamp: int
            The timestamp of the screencap's represenative frame.
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
        caption: str
            The caption/subtitles during the screencap.
    """

    # Returns "" if empty string
    @staticmethod
    def get_value(value):
        if value == "":
            return ""

        else:
            return value.replace("\n", "")

    def get_real_timestamp(self):
        """Gets a readable timestamp for the frame in format "mm:ss"

        Returns
        -------
        str
            A readable timestamp for the frame in format `mm:ss`."""

        return self.frame.get_real_timestamp()

    def get_image_url(self):
        """Returns the direct image url for the screencap without any caption.

        Returns
        -------
        str
            The image url for the screencap without any caption."""

        path_params = {"key": self.frame.key, "timestamp": self.frame.timestamp}
        return self._api.endpoints.IMAGE.build_encoded_url(self._api.url, path_params=path_params)

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

        # if caption is None:
        #     caption = self.caption

        return self.frame.get_meme_url(caption)

    def get_comic_panel_url(self, subtitles: List[Subtitle] = []):
        if len(subtitles) == 0:
            subtitles = self.subtitles

        overlays = build_overlay(subtitles, font=self._api.default_font)
        panel = ComicPanel(e=self.frame.key, ts=self.frame.timestamp, o=overlays)

        params = {"b64": panel.get_encoded()}
        return self._api.endpoints.COMIC_PANEL.build_encoded_url(self._api.url, query=params)

    def get_comic_strip_url(self, subtitles: List[Subtitle] = []):
        if len(subtitles) == 0:
            subtitles = self.subtitles

        if len(subtitles) > 4:
            subtitles = subtitles[:4]

        panels = []
        for subtitle in subtitles:
            overlay = ComicOverlay(t=subtitle.content, f=self._api.default_font)
            panel = ComicPanel(e=subtitle.key, ts=subtitle.representative_timestamp, o=[overlay])
            panels.append(panel)

        comic_strip = ComicStrip(panels=panels)
        params = {"b64": comic_strip.get_encoded(), "layout": comic_strip.layout}
        return self._api.endpoints.COMIC_STRIP.build_encoded_url(self._api.url, query=params)

    def get_gif_url(self, caption=None, before=3000, after=4000):
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
        raise NotImplementedError("Coming soon.")

    # Gets the mp4 url for the screencap captioned with subtitles, defaults gif
    # length to < ~7000ms, before + after must not exceed 10,000ms (10 sec.)
    def get_mp4_url(self, caption=None, before=3000, after=4000):
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
        raise NotImplementedError("Coming soon.")

    def __str__(self):
        return str(self.frame) + ": " + self.frame.key + " (" + self.frame.get_real_timestamp() + ")"
