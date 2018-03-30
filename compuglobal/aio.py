import asyncio
from base64 import b64encode

import aiohttp

from .errors import *
from .aio_screencap import AIOScreencap
from .frame import Frame


"""Contains the async API Wrappers used for accessing all the cghmc API 
endpoints."""


class CompuGlobalAPI:
    """Represents an API Wrapper used for accessing the cghmc API endpoints.

    Parameters
    ----------
    url: str
        The url of the API.
    title: str
        The title of the tv show/movie/skit that the url leads to.
    timeout: float
        The timeout for websocket read.

    Attributes
    ----------
        random_url: str
            Endpoint used for getting a random screencap.
        caption_url: str
            Endpoint for getting caption info using episode and timestamp
            ``e = episode & t = timestamp``.
        search_url: str
            Endpoint for getting screencaps using a search query
            ``q = search query``.
        frames_url: str
            Endpoint for getting all valid frames before & after an episode
            and timestamp
            ``episode/timestamp/before/after``.
        nearby_url: str
            Endpoint for getting all valid frames nearby an episode and
            timestamp
            ``e = episode & t = timestamp``.
        episode_url: str
            Endpoint for getting episode info and subtitles from start to
            end for episode ``episode/start/end``.
        """
    def __init__(self, url, title, timeout):
        self.URL = url
        self.title = title
        self.timeout = timeout

        # Initalise all API endpoints
        self.random_url = self.URL + 'api/random'
        self.caption_url = self.URL + 'api/caption?e={}&t={}'
        self.search_url = self.URL + 'api/search?q='
        self.frames_url = self.URL + 'api/frames/{}/{}/{}/{}'
        self.nearby_url = self.URL + 'api/nearby?e={}&t={}'
        self.episode_url = self.URL + 'api/episode/{}/{}/{}'

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
            caption_url = self.caption_url.format(frame.key,
                                                  frame.timestamp)

        else:
            raise TypeError('Expected str and int or compuglobal.Frame, '
                            'but received {}, {} and {} instead'.
                            format(episode, timestamp, frame))

        async with aiohttp.ClientSession() as cs:
            async with cs.get(caption_url, timeout=self.timeout) as screen:
                if screen.status == 200:
                    return AIOScreencap(self, await screen.json())

                else:
                    raise APIPageStatusError(screen.status, self.URL)

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
        async with aiohttp.ClientSession() as cs:
            async with cs.get(self.random_url, timeout=self.timeout) as screen:
                if screen.status == 200:
                    return AIOScreencap(self, await screen.json())

                else:
                    raise APIPageStatusError(screen.status, self.URL)

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

        search_url = self.search_url + search_text.replace(' ', '+')
        async with aiohttp.ClientSession() as cs:
            async with cs.get(search_url, timeout=self.timeout) as search:
                if search.status == 200:
                    search_results = await search.json()

                    if len(search_results) > 0:
                        all_frames = []
                        for result in search_results:
                            all_frames.append(Frame(self, result))

                        return all_frames

                    else:
                        raise NoSearchResultsFound()

                else:
                    raise APIPageStatusError(search.status, self.URL)

    async def search_for_screencap(self, search_text):
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
        if len(search_results) > 0:
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
        async with aiohttp.ClientSession() as cs:
            async with cs.get(frames_url, timeout=self.timeout) as frames:
                if frames.status == 200:
                    all_frames = []
                    for frame_result in await frames.json():
                        all_frames.append(Frame(self, frame_result))

                    return all_frames

                else:
                    raise APIPageStatusError(frames.status, self.URL)

    def encode_caption(self, caption, max_lines=4, max_chars=24, shorten=True):
        """Loops through the caption and formats it using max_lines and
        max_chars and finally encodes it in base64 for use in the url.

        Parameters
        ----------
        caption: str
            The caption to format and encode.
        max_lines: int, optional
            The maximum number of lines of captions allowed.
        max_chars: int, optional
            The maximum number of characters allowed per line.
        shorten: bool, optional
            Whether or not to shorten the caption at its latest
            sentence ending.

        Returns
        -------
        str
            The formatted caption, encoded in base64."""

        char_count = 0
        line_count = 0
        formatted_caption = ''

        # Loop through and format to suit max_lines and max_chars per line
        for word in caption.split():
            char_count += len(word) + 1

            if char_count < max_chars and line_count < max_lines:
                formatted_caption += ' ' + word

            elif line_count < max_lines:
                char_count = len(word) + 1
                line_count += 1
                if line_count < max_lines:
                    formatted_caption += '\n' + ' ' + word

        # Shorten caption at end of sentences if set to True
        caption = formatted_caption
        if shorten:
            caption = self.shorten_caption(formatted_caption)
        encoded = b64encode(str.encode(caption, 'utf-8'), altchars=b'__')

        return encoded.decode('utf-8')

    @staticmethod
    def shorten_caption(caption):
        """Loops through the caption and trims it at its latest sentence
        ending (., !, ? or ♪).

        Parameters
        ----------
        caption: str
            The caption to shorten/trim.

        Returns
        -------
        caption: str
            The shortened caption, ending at its latest sentence ending."""
        for i in range(len(caption) - 1, 0, -1):
            if caption[i] == '.' or caption[i] == '!' or caption[i] == '?':
                return caption[:i + 1]

            elif caption[i] == '♪':
                return caption[:i]

        return caption

    @staticmethod
    def json_to_caption(subtitles_json):
        """Loops through the subtitles of the json response, concatenates all
        lines and returns all subtitles combined as a complete caption.

        Parameters
        ----------
        subtitles_json: dict
            The json response containing the subtitles of
            the screencap.

        Returns
        -------
        caption: str
            The subtitles combined as a complete caption."""
        caption = ''
        for quote in subtitles_json['Subtitles']:
            caption += quote['Content'] + ' '

        return caption

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

        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(gif_url, timeout=self.timeout) as gif_loader:
                    if gif_loader.status == 200:
                        return gif_loader.url

                    else:
                        raise APIPageStatusError(gif_loader.status, self.URL)

        except asyncio.TimeoutError:
            return gif_url


# West Wing Meme/GIF generator API
class CapitalBeatUs(CompuGlobalAPI):
    """An API Wrapper for accessing CapitalBeatUs API endpoints (West Wing)."""
    def __init__(self, timeout=15):
        super().__init__('https://capitalbeat.us/', 'West Wing', timeout)


# Simpsons Meme/GIF generator API
class Frinkiac(CompuGlobalAPI):
    """An API Wrapper for accessing Frinkiac API endpoints (The Simpsons)."""
    def __init__(self, timeout=15):
        super().__init__('https://frinkiac.com/', 'The Simpsons', timeout)


# Steamed Hams Meme/GIF generator API
class FrinkiHams(CompuGlobalAPI):
    """An API Wrapper for accessing FriniHams API endpoints
    (The Simpsons - Steamed Hams Skit)."""
    def __init__(self, timeout=15):
        super().__init__('https://frinkihams.com/', 'Steamed Hams', timeout)


# 30 Rock Meme/GIF generator API
class GoodGodLemon(CompuGlobalAPI):
    """An API Wrapper for accessing GoodGodLemon API endpoints (30 Rock)."""
    def __init__(self, timeout=15):
        super().__init__('https://goodgodlemon.com/', '30 Rock', timeout)


# Rick and Morty Meme/GIF generator API
class MasterOfAllScience(CompuGlobalAPI):
    """An API Wrapper for accessing MasterOfAllScience API endpoints
    (Rick and Morty)."""
    def __init__(self, timeout=15):
        super().__init__('https://masterofallscience.com/', 'Rick and Morty',
                         timeout)


# Futurama Meme/GIF generator API
class Morbotron(CompuGlobalAPI):
    """An API Wrapper for accessing Morbotron API endpoints (Futurama)."""
    def __init__(self, timeout=15):
        super().__init__('https://morbotron.com/', 'Futurama', timeout)
