import json
from typing import List, Optional

import aiohttp

from .core import BaseCompuGlobalAPI
from .endpoints import PreparedRequest, RequestMethod
from .errors import APIPageStatusError, NoSearchResultsFound
from .models.comic import ComicOverlay, ComicPanel, ComicStrip, build_overlay
from .models.font import FontFamily
from .models.frame import Frame
from .models.screencap import Screencap
from .models.stream import Stream, build_stream_overlays
from .models.subtitle import Subtitle

"""Contains the async API Wrappers used for accessing all the cghmc API
endpoints."""


class AsyncCompuGlobalAPI(BaseCompuGlobalAPI):
    def __init__(
        self,
        url,
        title,
        default_font: FontFamily = FontFamily.IMPACT,
        session: Optional[aiohttp.ClientSession] = None,
        timeout=15,
    ):
        super().__init__(url, title, default_font=default_font)
        self.timeout = aiohttp.ClientTimeout(total=timeout)

        self._is_auto_session = session is None

        if session is None:
            self.session = aiohttp.ClientSession()

        else:
            self.session = session

    async def get(self, url, params=None):
        async with self.session.get(url, timeout=self.timeout, params=params) as response:
            if response.status == 200:
                return await response.json()

            else:
                raise APIPageStatusError(response.status, self.url)

    async def post_data(self, url, json=None):
        async with self.session.post(url, json=json) as response:
            if response.status == 200:
                return await response.text()

            else:
                raise APIPageStatusError(response.status, self.url)

    async def handle_request(self, request: PreparedRequest):
        if request.method == RequestMethod.POST:
            return await self.post_data(request.url, json=request.body)

        return await self.get(request.url, params=request.params)

    async def close(self):
        if self._is_auto_session:
            await self.session.close()

    async def get_screencap(self, episode=None, timestamp=None, frame=None):
        """Performs a GET request to the ``api/caption?e={}&t={}`` endpoint and
        gets a TV Show screencap using episode ``e={}`` and timestamp
        ``t={}``

        Parameters
        ----------
        episode: str
            The episode key of the screencap.
        timestamp: int
            The timestamp of the screencap.
        frame: compuglobal.Frame
            The frame of the screencap.

        Returns
        -------
        compuglobal.Screencap
            A `Screencap` objecct for the episode and timestamp.

        Raises
        ------
        APIPageStatusError
            Raises an exception if the status code of the request is not 200.
        TypeError
            Raises an exception if the constructor does not receive episode and
            timestamp, or compuglobal.Frame

        Note
        ----
        Used for getting the episode info and caption shown below each
        screencap."""

        if isinstance(episode, str) and isinstance(timestamp, int):
            params = {"e": episode, "t": timestamp, "nearby": 1}

        elif isinstance(frame, Frame):
            params = {"e": frame.key, "t": frame.timestamp, "nearby": 1}

        else:
            raise TypeError(
                "Expected str and int or compuglobal.Frame, but received "
                f"{type(episode)}, {type(timestamp)} and {type(frame)} instead"
            )

        request = self.endpoints.CAPTION.build_request(self.url, query=params)
        caption = await self.handle_request(request)
        return Screencap.model_validate(caption, context=self.context)

    async def get_random_screencap(self):
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
        request = self.endpoints.RANDOM.build_request(self.url)
        random = await self.handle_request(request)
        return Screencap.model_validate(random, context=self.context)

    async def search(self, search_text) -> List[Frame]:
        """Performs a GET request to the ``api/search?q=`` endpoint and gets a
        list of search results using the search text as the search query
        ``q={}`` for the request.

        Parameters
        ----------
        search_text: str
            The text/quote to search for.

        Returns
        -------
        search_results: list
            A list of search results containing the id, episode and timestamp
            for each result.

        Raises
        ------
        APIPageStatusError
            Raises an exception if the status code of the request is not 200.
        NoSearchResultsFound
            Raises an exception if there are no
            search results found using search_text.

        Note
        ----
        Used for displaying all the search results and their screencaps."""

        params = {"q": search_text}

        request = self.endpoints.SEARCH.build_request(self.url, query=params)
        search_results = await self.handle_request(request)

        if len(search_results) > 0:
            all_frames = []
            for result in search_results:
                all_frames.append(Frame.model_validate(result, context=self.context))

            return all_frames

        else:
            raise NoSearchResultsFound()

    async def search_for_screencap(self, search_text) -> Screencap:
        """Performs a GET request to the ``api/search?q=`` endpoint using
        :func:`search` to get a list of search results using search_text
        and gets a screencap using the episode and timestamp of the first
        search result.

        Parameters
        ----------
        search_text: str
            The text/quote to search for.

        Returns
        -------
        compuglobal.Screencap
            A screencap object of the first search result found using
            search_text.

        Raises
        ------
        APIPageStatusError
            Raises an exception if the status code of the request is not 200.
        NoSearchResultsFound
            Raises an exception if there are no
            search results found using search_text."""

        search_results = await self.search(search_text)
        result = search_results[0]
        return await self.get_screencap(result.key, result.timestamp)

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

        request = self.endpoints.FRAMES.build_request(self.url, path_params=path_params)
        frames = await self.handle_request(request)

        all_frames = []
        for frame_result in frames:
            all_frames.append(Frame.model_validate(frame_result))

        return all_frames

    def get_image_url(self, screencap: Screencap):
        """Returns the direct image url for the screencap without any caption.

        Returns
        -------
        str
            The image url for the screencap without any caption."""

        path_params = {"key": screencap.frame.key, "timestamp": screencap.frame.timestamp}
        return self.endpoints.IMAGE.build_encoded_url(self.url, path_params=path_params)

    def get_comic_panel_url(self, screencap: Screencap, subtitles: List[Subtitle] = []):
        if len(subtitles) == 0:
            subtitles = screencap.subtitles

        overlays = build_overlay(subtitles, font=self.default_font)
        panel = ComicPanel(e=screencap.frame.key, ts=screencap.frame.timestamp, o=overlays)

        params = {"b64": panel.get_encoded()}
        return self.endpoints.COMIC_PANEL.build_encoded_url(self.url, query=params)

    def get_comic_strip_url(self, screencap: Screencap, subtitles: List[Subtitle] = []):
        if len(subtitles) == 0:
            subtitles = screencap.subtitles

        if len(subtitles) > 4:
            subtitles = subtitles[:4]

        panels = []
        for subtitle in subtitles:
            overlay = ComicOverlay(t=subtitle.content, f=self.default_font)
            panel = ComicPanel(e=subtitle.key, ts=subtitle.representative_timestamp, o=[overlay])
            panels.append(panel)

        comic_strip = ComicStrip(panels=panels)
        params = {"b64": comic_strip.get_encoded(), "layout": comic_strip.layout}
        return self.endpoints.COMIC_STRIP.build_encoded_url(self.url, query=params)

    async def get_gif_url(self, screencap: Screencap, subtitles: List[Subtitle] = []):
        if len(subtitles) == 0:
            subtitles = screencap.subtitles

        if len(subtitles) > 4:
            subtitles = subtitles[:4]

        min_timestamp = min(subtitle.start_timestamp for subtitle in subtitles)
        max_timestamp = max(subtitle.end_timestamp for subtitle in subtitles)

        overlays = build_stream_overlays(subtitles, min_timestamp=min_timestamp, font=self.default_font)

        stream = Stream(
            episode=screencap.episode.key, start=min_timestamp, end=max_timestamp, overlays=overlays, check_only=False
        )

        request = self.endpoints.RENDER_GIF.build_request(self.url, body=stream)
        request.body = [request.body]
        response = await self.handle_request(request)

        for line in response.splitlines():
            data = json.loads(line)
            if "url" in data:
                return f"{self.url}/{data.get("url")}"

        raise APIPageStatusError(400, self.url)

    async def generate_gif(self, gif_url):
        """Performs a GET request using gif_url and returns the direct url
        for the gif once it has been generated.

        Parameters
        ----------
        gif_url: str
            The url of the gif to generate.

        Returns
        -------
        str
            The direct url for the generated gif

        Raises
        ------
        APIPageStatusError
            Raises an exception if the status code of the request is not 200."""

        raise NotImplementedError("Coming soon.")


# West Wing Meme/GIF generator API
class CapitalBeatUs(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing CapitalBeatUs API endpoints (West Wing)."""

    def __init__(
        self,
        default_font: FontFamily = FontFamily.IMPACT,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        super().__init__("https://capitalbeat.us", "West Wing", default_font=default_font, session=session)


# Simpsons Meme/GIF generator API
class Frinkiac(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing Frinkiac API endpoints (The Simpsons)."""

    def __init__(
        self,
        default_font: FontFamily = FontFamily.AKBAR,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        super().__init__("https://frinkiac.com", "The Simpsons", default_font=default_font, session=session)


# Steamed Hams Meme/GIF generator API
class FrinkiHams(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing FriniHams API endpoints
    (The Simpsons - Steamed Hams Skit)."""

    def __init__(
        self,
        default_font: FontFamily = FontFamily.AKBAR,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        super().__init__("https://frinkihams.com", "Steamed Hams", default_font=default_font, session=session)


# 30 Rock Meme/GIF generator API
class GoodGodLemon(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing GoodGodLemon API endpoints (30 Rock)."""

    def __init__(
        self,
        default_font: FontFamily = FontFamily.IMPACT,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        super().__init__("https://goodgodlemon.com", "30 Rock", default_font=default_font, session=session)


# Rick and Morty Meme/GIF generator API
class MasterOfAllScience(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing MasterOfAllScience API endpoints
    (Rick and Morty)."""

    def __init__(
        self,
        default_font: FontFamily = FontFamily.IMPACT,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        super().__init__(
            "https://masterofallscience.com", "Rick and Morty", default_font=default_font, session=session
        )


# Futurama Meme/GIF generator API
class Morbotron(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing Morbotron API endpoints (Futurama)."""

    def __init__(
        self,
        default_font: FontFamily = FontFamily.FR_BOLD,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        super().__init__("https://morbotron.com", "Futurama", default_font=default_font, session=session)
