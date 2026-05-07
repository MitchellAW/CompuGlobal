from typing import List

from ..errors import NoSearchResultsFound
from ..models.frame import Frame
from ..models.screencap import Screencap
from .base import EndpointBase
from .client import CompuGlobalAPIClient
from .config import CompuGlobalAPIConfig
from .endpoints import Endpoint, RequestMethod


class DiscoverAPI(EndpointBase):
    client: CompuGlobalAPIClient
    config: CompuGlobalAPIConfig

    CAPTION = Endpoint(
        path="/api/caption",
        method=RequestMethod.GET,
        query_params=frozenset({"e", "t", "nearby"}),
    )

    DISCOVER = Endpoint(
        path="/api/discover",
        method=RequestMethod.GET,
    )

    RANDOM = Endpoint(
        path="/api/random",
        method=RequestMethod.GET,
    )

    NAVIGATOR = Endpoint(
        path="/api/navigator",
        method=RequestMethod.GET,
    )

    SEARCH = Endpoint(
        path="/api/search",
        method=RequestMethod.GET,
        query_params=frozenset({"q"}),
    )

    FRAMES = Endpoint(
        path="/api/frames/{key}/{timestamp}/{before}/{after}",
        method=RequestMethod.GET,
    )

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

        request = self.CAPTION.build_request(self.client.base_url, query=params)
        caption = await self.client.handle_request(request)
        return Screencap.model_validate(caption)

    async def search(self, search_text) -> List[Frame]:
        params = {"q": search_text}

        request = self.SEARCH.build_request(self.client.base_url, query=params)
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
        request = self.RANDOM.build_request(self.client.base_url)
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

        request = self.FRAMES.build_request(self.client.base_url, path_params=path_params)
        frames = await self.client.handle_request(request)

        all_frames = []
        for frame_result in frames:
            all_frames.append(Frame.model_validate(frame_result))

        return all_frames
