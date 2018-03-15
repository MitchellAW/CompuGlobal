from base64 import b64encode

import requests

from .errors import *
from .screencap import *

__title__ = 'compuglobal'
__author__ = 'MitchellAW'
__license__ = 'MIT'
__version__ = '0.1.7'


"""Contains the API Wrappers used for accessing all the cghmc API endpoints."""


class CompuGlobalAPI:
    """Represents an API Wrapper used for accessing the cghmc API endpoints.

    :param url: The url of the API. (https://frinkiac.com/)
    :type url: str
    :param title: The title of the tv show/movie/skit that the url leads to.
    :type title: str

    Attributes:
        random_url:
            Endpoint used for getting a random screencap
        caption_url:
            Endpoint for getting caption info using episode and timestamp
            (e = episode & t = timestamp)
        search_url:
            Endpoint for getting screencaps using a search query
            (q = search query)
        frames_url:
            Endpoint for getting all valid frames before & after an episode
            and timestamp
            (episode/timestamp/before/after)
        nearby_url:
            Endpoint for getting all valid frames nearby an episode and
            timestamp
            (e = episode & t = timestamp)
        episode_url:
            Endpoint for getting episode info and subtitles from start to
            end for episode
            (episode/start/end)"""

    def __init__(self, url, title):
        self.URL = url
        self.title = title

        # Initalise all API endpoints
        self.random_url = self.URL + 'api/random'
        self.caption_url = self.URL + 'api/caption?e={}&t={}'
        self.search_url = self.URL + 'api/search?q='
        self.frames_url = self.URL + 'api/frames/{}/{}/{}/{}'
        self.nearby_url = self.URL + 'api/nearby?e={}&t={}'
        self.episode_url = self.URL + 'api/episode/{}/{}/{}'

    def get_screencap(self, episode, timestamp):
        """Performs a GET request to the "api/caption?e={}&t={}" endpoint and
        gets a TV Show screencap using episode (e={}) and timestamp (t={})

        :param episode: The episode key of the screencap.
        :type episode: str
        :param timestamp: The timestamp of the screencap.
        :type timestamp: int

        :returns: A screencap object for the episode and timestamp.
        :rtype: Screencap

        :raises APIPageStatusError: Raises an exception if the status code
        of the request is not 200."""

        caption_url = self.caption_url.format(episode, timestamp)
        screen = requests.get(caption_url)
        if screen.status_code == 200:
            return Screencap(self, screen.json())

        else:
            raise APIPageStatusError(screen.status_code, self.URL)

    def get_random_screencap(self):
        """Performs a GET request to the "api/random" endpoint and gets a
        random TV Show screencap.

        :returns: A random screencap object.
        :rtype: Screencap

        :raises APIPageStatusError: Raises an exception if the status code
        of the request is not 200."""

        screen = requests.get(self.random_url)
        if screen.status_code == 200:
            return Screencap(self, screen.json())

        else:
            raise APIPageStatusError(screen.status_code, self.URL)

    def search(self, search_text):
        """Performs a GET request to the "api/search?q=" endpoint and gets a
        list of search results using the search text as the search query (q=)
        for the request.

        :param search_text: The text/quote to search for.
        :type search_text: str

        :returns search_results: A list of search results containing the
        id, episode and timestamp for each result.
        :rtype: list

        :raises APIPageStatusError: Raises an exception if the status code
        of the request is not 200.
        :raises NoSearchResultsFound: Raises an exception if there are no
        search results found using search_text."""

        search_url = self.search_url + search_text.replace(' ', '+')

        search = requests.get(search_url)
        if search.status_code == 200:
            search_results = search.json()

            if len(search_results) > 0:
                return search_results

            else:
                raise NoSearchResultsFound()

        else:
            raise APIPageStatusError(search.status_code, self.URL)

    def search_for_screencap(self, search_text):
        """Uses search() to get a list of search results using search_text
        and gets a screencap using the episode and timestamp of the first
        search result.

        :param search_text: The text/quote to search for.
        :type search_text: str

        :returns: A screencap object of the first search result found using
        search_text.
        :rtype: Screencap

        :raises APIPageStatusError: Raises an exception if the status code
        of the request is not 200.
        :raises NoSearchResultsFound: Raises an exception if there are no
        search results found using search_text."""

        search_results = self.search(search_text)
        if len(search_results) > 0:
            result = search_results[0]
            return self.get_screencap(result['Episode'], result['Timestamp'])

    def get_frames(self, episode, timestamp, before, after):
        """Gets all valid frames before and after the timestamp of the
        episode.

        :param episode: The episode key of the screencap.
        :type episode: str
        :param timestamp: The timestamp of the screencap.
        :type timestamp: int
        :param before: The number of milliseconds before the timestamp.
        :type before: int
        :param after: The number of millisecods after the timestamp.
        :type after: int

        :returns: A list of valid frames before and after the timestamp of
        the episode, containing the id, episode and timestamp for each frame.
        :rtype: list

        :raises APIPageStatusError: Raises an exception if the status code
        of the request is not 200."""

        frames_url = self.frames_url.format(episode, timestamp, before, after)
        frames = requests.get(frames_url)
        if frames.status_code == 200:
            return frames.json()

        else:
            raise APIPageStatusError(frames.status_code, self.URL)

    def encode_caption(self, caption, max_lines=4, max_chars=24, shorten=True):
        """Loops through the caption and formats it using max_lines and
        max_chars and finally encodes it in base64 for use in the url.

        :param caption: The caption to format and encode.
        :type caption: str
        :param max_lines: The maximum number of lines of captions allowed.
        :type max_lines: int
        :param max_chars: The maximum number of characters allowed per line.
        :type max_chars: int
        :param shorten: Whether or not to shorten the caption at its latest
        sentence ending.
        :type shorten: bool

        :returns: The formatted caption, encoded in base64.
        :rtype: str"""

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

        :param caption: The caption to shorten/trim.
        :type caption: str

        :returns caption: The shortened caption, ending at its latest
        sentence ending.
        :rtype: str"""

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

        :param subtitles_json: The json response containing the subtitles of
        the screencap.
        :type subtitles_json: dict

        :returns caption: The subtitles combined as a complete caption."""

        caption = ''
        for quote in subtitles_json['Subtitles']:
            caption += quote['Content'] + ' '

        return caption

    def generate_gif(self, gif_url):
        """Performs a GET request using gif_url and returns the direct url
        for the gif once it has been generated.

        :param gif_url: The url of the gif to generate.
        :type gif_url: str

        :returns: The direct url for the generated gif.
        :rtype: str

        :raises APIPageStatusError: Raises an exception if the status code
        of the request is not 200."""

        gif_loader = requests.get(gif_url)
        if gif_loader.status_code == 200:
            return gif_loader.url

        else:
            raise APIPageStatusError(gif_loader.status_code, self.URL)


# West Wing Meme/GIF generator API
class CapitalBeatUs(CompuGlobalAPI):
    """An API Wrapper for accessing CapitalBeatUs API endpoints (West Wing)."""
    def __init__(self):
        super().__init__('https://capitalbeat.us/', 'West Wing')


# Simpsons Meme/GIF generator API
class Frinkiac(CompuGlobalAPI):
    """An API Wrapper for accessing Frinkiac API endpoints (The Simpsons)."""
    def __init__(self):
        super().__init__('https://frinkiac.com/', 'The Simpsons')


# Steamed Hams Meme/GIF generator API
class FrinkiHams(CompuGlobalAPI):
    """An API Wrapper for accessing FriniHams API endpoints
    (The Simpsons - Steamed Hams Skit)."""
    def __init__(self):
        super().__init__('https://frinkihams.com/', 'Steamed Hams')


# 30 Rock Meme/GIF generator API
class GoodGodLemon(CompuGlobalAPI):
    """An API Wrapper for accessing GoodGodLemon API endpoints (30 Rock)."""
    def __init__(self):
        super().__init__('https://goodgodlemon.com/', '30 Rock')


# Rick and Morty Meme/GIF generator API
class MasterOfAllScience(CompuGlobalAPI):
    """An API Wrapper for accessing MasterOfAllScience API endpoints
    (Rick and Morty)."""
    def __init__(self):
        super().__init__('https://masterofallscience.com/', 'Rick and Morty')


# Futurama Meme/GIF generator API
class Morbotron(CompuGlobalAPI):
    """An API Wrapper for accessing Morbotron API endpoints
    (Futurama)."""
    def __init__(self):
        super().__init__('https://morbotron.com/', 'Futurama')
