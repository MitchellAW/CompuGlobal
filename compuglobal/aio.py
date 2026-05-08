import json
from typing import List
from warnings import deprecated

import aiohttp

from .api.client import CompuGlobalAPIClient
from .api.config import CompuGlobalAPIConfig
from .api.discover import DiscoverAPI
from .api.media import MediaAPI
from .api.metadata import MetadataAPI
from .errors import NoSearchResultsFound
from .models.comic import ComicOverlay, ComicPanel, ComicStrip, build_overlay
from .models.font import FontFamily
from .models.frame import Frame
from .models.screencap import Screencap
from .models.stream import Stream, build_stream_overlays
from .models.subtitle import Subtitle

"""Contains the async API Wrappers used for accessing all the cghmc API endpoints."""


class AsyncCompuGlobalAPI:
    BASE_URL: str
    TITLE: str
    DEFAULT_FONT: FontFamily

    discover: DiscoverAPI = DiscoverAPI()
    media: MediaAPI = MediaAPI()
    metadata: MetadataAPI = MetadataAPI()

    def __init__(self, session: aiohttp.ClientSession | None = None, timeout: int = 15):
        self.client = CompuGlobalAPIClient(base_url=self.BASE_URL, session=session, timeout=timeout)
        self.config = CompuGlobalAPIConfig(title=self.TITLE, default_font=self.DEFAULT_FONT)

    async def get_screencap(
        self, episode: str | None = None, timestamp: int | None = None, frame: Frame | None = None
    ) -> Screencap:
        """Gets the screencap for the given episode & timestamp, or a screencap of the Frame object.

        Parameters
        ----------
        episode : str, optional
            An episode key
        timestamp : int, optional
            A timestamp of the screencap
        frame : Frame, optional
            A Frame object

        Returns
        -------
        Screencap
            The screencap for the given episode key and timestamp.

        Raises
        ------
        TypeError
            Must give only episode + timestamp, or a Frame object.
        """
        if isinstance(episode, str) and isinstance(timestamp, int):
            params = {"e": episode, "t": timestamp, "nearby": 1}

        elif isinstance(frame, Frame):
            params = {"e": frame.key, "t": frame.timestamp, "nearby": 1}

        else:
            raise TypeError(
                "Expected str and int or compuglobal.Frame, but received "
                f"{type(episode)}, {type(timestamp)} and {type(frame)} instead"
            )

        request = self.discover.CAPTION.build_request(self.client.base_url, query=params)
        caption = await self.client.handle_request(request)
        return Screencap.model_validate(caption)

    async def search(self, search_text: str) -> List[Frame]:
        """Performs a search of the given search text and returns a list of all the Frames.

        Parameters
        ----------
        search_text : str
            The search text to query

        Returns
        -------
        List[Frame]
            A list of all frames found containing the search text.

        Raises
        ------
        NoSearchResultsFound
            _description_
        """
        params = {"q": search_text}

        request = self.discover.SEARCH.build_request(self.client.base_url, query=params)
        search_results = await self.client.handle_request(request)

        if len(search_results) > 0:
            all_frames = []
            for result in search_results:
                all_frames.append(Frame.model_validate(result))

            return all_frames

        else:
            raise NoSearchResultsFound()

    async def search_for_screencap(self, search_text: str) -> Screencap:
        """Performs a search of the given search text and returns the top result.

        Parameters
        ----------
        search_text : str
            The search text to query

        Returns
        -------
        Screencap
            The screencap of the top search result
        """
        search_results = await self.search(search_text)
        result = search_results[0]
        return await self.get_screencap(result.key, result.timestamp)

    async def get_random_screencap(self) -> Screencap:
        """Gets a random TV Show screencap.

        Returns
        -------
        compuglobal.Screencap
            A random screencap object.

        Raises
        ------
        APIPageStatusError
            Raises an exception if the status code of the request is not 200."""
        request = self.discover.RANDOM.build_request(self.client.base_url)
        random = await self.client.handle_request(request)
        return Screencap.model_validate(random)

    async def get_frames(self, episode: str, timestamp: int, before: int, after: int) -> List[Frame]:
        """Gets a list of all valid frames before and after the timestamp of the episode.

        Parameters
        ----------
        episode: str
            The episode key of the screencap.
        timestamp: int
            The timestamp of the screencap.
        before: int
            The number of milliseconds before the timestamp.
        after: int
            The number of milliseconds after the timestamp.

        Returns
        -------
        list
            A list of valid frames before and after the timestamp of
            the episode.

        Raises
        ------
        APIPageStatusError
            Raises an exception if the status code of the request is not 200."""

        path_params = {"episode": episode, "timestamp": timestamp, "before": before, "after": after}

        request = self.discover.FRAMES.build_request(self.client.base_url, path_params=path_params)
        frames = await self.client.handle_request(request)

        all_frames = []
        for frame_result in frames:
            all_frames.append(Frame.model_validate(frame_result))

        return all_frames

    async def get_image_url(self, screencap: Screencap) -> str:
        """Returns the direct image url for the screencap without any caption.

        Returns
        -------
        str
            The image url for the screencap without any caption."""

        path_params = {"key": screencap.frame.key, "timestamp": screencap.frame.timestamp}
        return self.media.IMAGE.build_encoded_url(self.client.base_url, path_params=path_params)

    async def get_comic_panel_url(self, screencap: Screencap, subtitles: List[Subtitle] = []) -> str:
        """Gets the URL for a single comic panel showing the given screencap with subtitles.

        Parameters
        ----------
        screencap : Screencap
            The screencap to use in the comic panel
        subtitles : List[Subtitle], optional
            A list of subtitles to overlay in the comic panel, by default []

        Returns
        -------
        str
            The url of the comic panel
        """
        if len(subtitles) == 0:
            subtitles = screencap.subtitles

        overlays = build_overlay(subtitles, font=self.config.default_font)
        panel = ComicPanel(e=screencap.frame.key, ts=screencap.frame.timestamp, o=overlays)

        params = {"b64": panel.get_encoded()}
        return self.media.COMIC_PANEL.build_encoded_url(self.client.base_url, query=params)

    async def get_comic_strip_url(self, screencap: Screencap, subtitles: List[Subtitle] = []) -> str:
        """Gets the URL for a comic strip showing the given screencap with subtitles.

        Parameters
        ----------
        screencap : Screencap
            The screencap to use in the comic strip
        subtitles : List[Subtitle], optional
            A list of subtitles to overlay in the comic strip, by default []

        Returns
        -------
        str
            The url of the comic strip
        """
        if len(subtitles) == 0:
            subtitles = screencap.subtitles

        if len(subtitles) > 4:
            subtitles = subtitles[:4]

        panels = []
        for subtitle in subtitles:
            overlay = ComicOverlay(t=subtitle.content, f=self.config.default_font)
            panel = ComicPanel(e=subtitle.key, ts=subtitle.representative_timestamp, o=[overlay])
            panels.append(panel)

        comic_strip = ComicStrip(panels=panels)
        params = {"b64": comic_strip.get_encoded(), "layout": comic_strip.layout}
        return self.media.COMIC_STRIP.build_encoded_url(self.client.base_url, query=params)

    async def get_gif_url(self, screencap: Screencap, subtitles: List[Subtitle] = []) -> str:
        """get_gif_url Gets the URL for a gif of the given screencap with subtitles.

        Parameters
        ----------
        screencap : Screencap
            The screencap to use for the gif
        subtitles : List[Subtitle], optional
            The subtitles to overlay in the gif, by default []

        Returns
        -------
        str
            The URL of the gif, or a comic strip as a fallback if gif rendering fails.
        """
        if len(subtitles) == 0:
            subtitles = screencap.subtitles

        if len(subtitles) > 4:
            subtitles = subtitles[:4]

        min_timestamp = min(subtitle.start_timestamp for subtitle in subtitles)
        max_timestamp = max(subtitle.end_timestamp for subtitle in subtitles)

        overlays = build_stream_overlays(subtitles, min_timestamp=min_timestamp, font=self.config.default_font)

        stream = Stream(
            episode=screencap.episode.key, start=min_timestamp, end=max_timestamp, overlays=overlays, check_only=False
        )

        request = self.media.RENDER_GIF.build_request(self.client.base_url, body=stream)
        request.body = [request.body]
        response = await self.client.handle_request(request)

        for line in response.splitlines():
            data = json.loads(line)
            if "url" in data:
                return f"{self.client.base_url}/{data.get("url")}"

        return await self.get_comic_strip_url(screencap)

    async def close(self):
        """Closes any client sessions used for performing API requests."""
        await self.client.close()


# West Wing Meme/GIF generator API
class CapitalBeatUs(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing CapitalBeatUs API endpoints (West Wing)."""

    BASE_URL = "https://capitalbeat.us"
    TITLE = "West Wing"
    DEFAULT_FONT = FontFamily.IMPACT


# Simpsons Meme/GIF generator API
class Frinkiac(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing Frinkiac API endpoints (The Simpsons)."""

    BASE_URL = "https://frinkiac.com"
    TITLE = "Simpsons"
    DEFAULT_FONT = FontFamily.AKBAR


# Rick and Morty Meme/GIF generator API
@deprecated("The MasterOfAllScience API is deprecated, and currently redirects to Frinkiac")
class MasterOfAllScience(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing MasterOfAllScience API endpoints
    (Rick and Morty)."""

    BASE_URL = "https://masterofallscience.com"
    TITLE = "Rick and Morty"
    DEFAULT_FONT = FontFamily.IMPACT


# Futurama Meme/GIF generator API
class Morbotron(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing Morbotron API endpoints (Futurama)."""

    BASE_URL = "https://morbotron.com"
    TITLE = "Futurama"
    DEFAULT_FONT = FontFamily.FR_BOLD
