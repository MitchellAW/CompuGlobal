import json
from typing import List
from warnings import deprecated

import aiohttp

from .api.client import CompuGlobalAPIClient
from .api.config import CompuGlobalAPIConfig
from .api.discover import DiscoverAPI
from .api.media import MediaAPI
from .api.metadata import MetadataAPI
from .errors import APIPageStatusError, NoSearchResultsFound
from .models.comic import ComicOverlay, ComicPanel, ComicStrip, build_overlay
from .models.font import FontFamily
from .models.frame import Frame
from .models.screencap import Screencap
from .models.stream import Stream, build_stream_overlays
from .models.subtitle import Subtitle

"""Contains the async API Wrappers used for accessing all the cghmc API
endpoints."""


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

    async def close(self):
        await self.client.close()

    async def get_screencap(self, episode=None, timestamp=None, frame=None) -> Screencap:
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

    async def search(self, search_text) -> List[Frame]:
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

    async def search_for_screencap(self, search_text) -> Screencap:
        search_results = await self.search(search_text)
        result = search_results[0]
        return await self.get_screencap(result.key, result.timestamp)

    async def get_random_screencap(self) -> Screencap:
        """Performs a GET request to the ``api/random`` endpoint and gets a
        random TV Show screencap.

        Returns
        -------
        compuglobal.Screencap
            A random screencap object.

        Raises
        ------
        APIPageStatusError
            Raises an exception if the status code of the request is not 200.

        Note
        ----
        Used for getting a random screencap when clicking the "RANDOM"
        button."""
        request = self.discover.RANDOM.build_request(self.client.base_url)
        random = await self.client.handle_request(request)
        return Screencap.model_validate(random)

    async def get_frames(self, episode, timestamp, before, after):
        """Performs a GET request to the
        ``api/frames/{episode}/{timestamp}/{before}/{after}`` endpoint and
        gets a list of all valid frames before and after the timestamp of the
        episode.

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
            the episode, containing the id, episode and timestamp for each
            frame.

        Raises
        ------
        APIPageStatusError
            Raises an exception if the status code of the request is not 200.

        Note
        ----
        Used for displaying the valid frames available for the gifmaker."""

        path_params = {"episode": episode, "timestamp": timestamp, "before": before, "after": after}

        request = self.discover.FRAMES.build_request(self.client.base_url, path_params=path_params)
        frames = await self.client.handle_request(request)

        all_frames = []
        for frame_result in frames:
            all_frames.append(Frame.model_validate(frame_result))

        return all_frames

    async def get_image_url(self, screencap: Screencap):
        """Returns the direct image url for the screencap without any caption.

        Returns
        -------
        str
            The image url for the screencap without any caption."""

        path_params = {"key": screencap.frame.key, "timestamp": screencap.frame.timestamp}
        return self.media.IMAGE.build_encoded_url(self.client.base_url, path_params=path_params)

    async def get_comic_panel_url(self, screencap: Screencap, subtitles: List[Subtitle] = []):
        if len(subtitles) == 0:
            subtitles = screencap.subtitles

        overlays = build_overlay(subtitles, font=self.config.default_font)
        panel = ComicPanel(e=screencap.frame.key, ts=screencap.frame.timestamp, o=overlays)

        params = {"b64": panel.get_encoded()}
        return self.media.COMIC_PANEL.build_encoded_url(self.client.base_url, query=params)

    async def get_comic_strip_url(self, screencap: Screencap, subtitles: List[Subtitle] = []):
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

    async def get_gif_url(self, screencap: Screencap, subtitles: List[Subtitle] = []):
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

        raise APIPageStatusError(400, self.client.base_url)


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
