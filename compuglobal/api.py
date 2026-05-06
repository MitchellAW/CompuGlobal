import requests

from .core import BaseCompuGlobalAPI
from .errors import APIPageStatusError, NoSearchResultsFound
from .models.frame import Frame
from .models.screencap import Screencap

"""Contains the API Wrappers used for accessing all the cghmc API endpoints."""


class CompuGlobalAPI(BaseCompuGlobalAPI):
    def get(self, url, params=None):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()

        else:
            raise APIPageStatusError(response.status_code, self.URL)

    def get_screencap(self, episode=None, timestamp=None, frame=None):
        """Performs a GET request to the ``api/caption?e={}&t={}`` endpoint and
        gets a TV Show screencap using episode ``e={}`` and timestamp
        ``t={} or a frame``

        Parameters
        ----------
        episode: str, optional
            The episode key of the screencap.
        timestamp: int, optional
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
                "Expected str and int or compuglobal.Frame, "
                "but received {}, {} and {} instead".format(episode, timestamp, frame)
            )

        screen = self.get(caption_url)
        return Screencap.model_validate_json(screen)

    def get_random_screencap(self):
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

        screen = self.get(self.random_url)
        return Screencap.model_validate_json(screen)

    def search(self, search_text):
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
            A list of search results containing the
            id, episode and timestamp for each result.

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

        search_url = self.search_url + search_text.replace(" ", "+")

        search_results = self.get(search_url)
        if len(search_results) > 0:
            all_frames = []
            for result in search_results:
                all_frames.append(Frame.model_validate_json(result, context=self.context))

            return all_frames

        else:
            raise NoSearchResultsFound()

    def search_for_screencap(self, search_text) -> Screencap:
        """Performs a GET request to the ``api/search?q=`` endpoint using
        `search` to get a list of search results using search_text
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

        search_results = self.search(search_text)
        result = search_results[0]
        return self.get_screencap(result.key, result.timestamp)

    def get_frames(self, episode, timestamp, before, after):
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
        frames = self.get(frames_url)
        all_frames = []
        for frame_result in frames.json():
            all_frames.append(Frame.model_validate_json(frame_result, context=self.context))

        return all_frames

    def view_episode(self, episode, start, end):
        """Performs a GET request to the ``api/episode/{episode}/{start}/{end}``
        endpoint and returns the json response containing episode information.

        Parameters
        ----------
        episode: str
            The episode key of the screencap.
        start: int
            The starting timestamp for the episode information.
        end: int
            The ending timestamp for the episode information.

        Returns
        -------
        dict
            The json response containing the episode information and
            subtitles for the timestamps.

        Note
        ----
        Used for displaying the rest of an episode when using the "View Episode"
        button next to each screencap."""

        episode_url = self.episode_url.format(episode, start, end)
        episode = self.get(episode_url)
        return episode

    def generate_gif(self, gif_url):
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
class CapitalBeatUs(CompuGlobalAPI):
    """An API Wrapper for accessing CapitalBeatUs API endpoints (West Wing)."""

    def __init__(self):
        super().__init__("https://capitalbeat.us", "West Wing")


# Simpsons Meme/GIF generator API
class Frinkiac(CompuGlobalAPI):
    """An API Wrapper for accessing Frinkiac API endpoints (The Simpsons)."""

    def __init__(self):
        super().__init__("https://frinkiac.com", "The Simpsons")


# Steamed Hams Meme/GIF generator API
class FrinkiHams(CompuGlobalAPI):
    """An API Wrapper for accessing FriniHams API endpoints
    (The Simpsons - Steamed Hams Skit)."""

    def __init__(self):
        super().__init__("https://frinkihams.com", "Steamed Hams")


# 30 Rock Meme/GIF generator API
class GoodGodLemon(CompuGlobalAPI):
    """An API Wrapper for accessing GoodGodLemon API endpoints (30 Rock)."""

    def __init__(self):
        super().__init__("https://goodgodlemon.com", "30 Rock")


# Rick and Morty Meme/GIF generator API
class MasterOfAllScience(CompuGlobalAPI):
    """An API Wrapper for accessing MasterOfAllScience API endpoints
    (Rick and Morty)."""

    def __init__(self):
        super().__init__("https://masterofallscience.com", "Rick and Morty")


# Futurama Meme/GIF generator API
class Morbotron(CompuGlobalAPI):
    """An API Wrapper for accessing Morbotron API endpoints
    (Futurama)."""

    def __init__(self):
        super().__init__("https://morbotron.com", "Futurama")
