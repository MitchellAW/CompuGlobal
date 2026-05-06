from typing import Optional

import aiohttp

from .core import BaseCompuGlobalAPI
from .errors import APIPageStatusError, NoSearchResultsFound
from .models.aio_screencap import AIOScreencap
from .models.frame import Frame

"""Contains the async API Wrappers used for accessing all the cghmc API
endpoints."""


class AsyncCompuGlobalAPI(BaseCompuGlobalAPI):
    def __init__(self, url, title, session: Optional[aiohttp.ClientSession] = None, timeout=15):
        super().__init__(url, title)
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
                raise APIPageStatusError(response.status, self.URL)

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
            caption_url = self.caption_url.format(episode, timestamp)

        elif isinstance(frame, Frame):
            caption_url = self.caption_url.format(frame.key, frame.timestamp)

        else:
            raise TypeError(
                "Expected str and int or compuglobal.Frame, but received "
                f"{type(episode)}, {type(timestamp)} and {type(frame)} instead"
            )

        caption = await self.get(caption_url)
        return AIOScreencap.model_validate_json(caption, context=self.context)

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
        random = await self.get(self.random_url)
        return AIOScreencap.model_validate_json(random, context=self.context)

    async def search(self, search_text):
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

        params = {"q": search_text.replace(" ", "+")}

        search_results = await self.get(self.search_url, params=params)

        if len(search_results) > 0:
            all_frames = []
            for result in search_results:
                all_frames.append(Frame.model_validate_json(result, context=self.context))

            return all_frames

        else:
            raise NoSearchResultsFound()

    async def search_for_screencap(self, search_text) -> AIOScreencap:
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

        frames_url = self.frames_url.format(episode, timestamp, before, after)
        frames = await self.get(frames_url)

        all_frames = []
        for frame_result in frames:
            all_frames.append(Frame.model_validate_json(frame_result))

        return all_frames

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

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        super().__init__("https://capitalbeat.us", "West Wing")


# Simpsons Meme/GIF generator API
class Frinkiac(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing Frinkiac API endpoints (The Simpsons)."""

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        super().__init__("https://frinkiac.com", "The Simpsons")


# Steamed Hams Meme/GIF generator API
class FrinkiHams(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing FriniHams API endpoints
    (The Simpsons - Steamed Hams Skit)."""

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        super().__init__("https://frinkihams.com", "Steamed Hams")


# 30 Rock Meme/GIF generator API
class GoodGodLemon(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing GoodGodLemon API endpoints (30 Rock)."""

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        super().__init__("https://goodgodlemon.com", "30 Rock")


# Rick and Morty Meme/GIF generator API
class MasterOfAllScience(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing MasterOfAllScience API endpoints
    (Rick and Morty)."""

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        super().__init__("https://masterofallscience.com", "Rick and Morty")


# Futurama Meme/GIF generator API
class Morbotron(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing Morbotron API endpoints (Futurama)."""

    def __init__(self, session: Optional[aiohttp.ClientSession] = None):
        super().__init__("https://morbotron.com", "Futurama")
