"""Used for interacting with and building CGHMC APIs."""

import json
from typing import overload
from warnings import deprecated

import aiohttp

from compuglobal.api.client import CompuGlobalAPIClient
from compuglobal.api.config import CompuGlobalAPIConfig
from compuglobal.api.discovery import DiscoveryAPI
from compuglobal.api.media import MediaAPI
from compuglobal.api.metadata import MetadataAPI
from compuglobal.errors import NoSearchResultsFoundError
from compuglobal.models.comic import ComicPanel, ComicStrip
from compuglobal.models.episode import Episode, EpisodeSummary
from compuglobal.models.font import FontFamily
from compuglobal.models.frame import Frame, FrameResult
from compuglobal.models.overlay import OverlayFormat
from compuglobal.models.screencap import Screencap, ScreencapMoment
from compuglobal.models.stream import Stream
from compuglobal.models.subtitle import Subtitle

"""Contains the async API Wrappers used for accessing all the cghmc API endpoints."""


class AsyncCompuGlobalAPI:
    """Represents a base API of the CGHMC family.

    Parameters
    ----------
    session : aiohttp.ClientSession, optional
        The client session to use for all API calls

    Attributes
    ----------
    BASE_URL : str
        The base url of the API
    TITLE : str
        The title of the API
    DEFAULT_FORMAT : OverlayFormat
        The default formatting to use in all comic/gif overlays
    discovery : DiscoveryAPI
        The discovery API with all discovery endpoints
    media : MediaAPI
        The media API with all media endpoints
    metadata : MetadataAPI
        The metadataAPI with all metadata endpoints

    """

    BASE_URL: str
    TITLE: str
    DEFAULT_FORMAT: OverlayFormat
    _MAX_ALLOWED_SUBTITLES = 4

    discovery: DiscoveryAPI = DiscoveryAPI()
    media: MediaAPI = MediaAPI()
    metadata: MetadataAPI = MetadataAPI()

    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.client = CompuGlobalAPIClient(base_url=self.BASE_URL, session=session)
        self.config = CompuGlobalAPIConfig(title=self.TITLE, default_format=self.DEFAULT_FORMAT)

    async def get_screencap(
        self,
        episode: str | None = None,
        timestamp: int | None = None,
        frame: Frame | None = None,
    ) -> Screencap:
        """Get the screencap for the given episode & timestamp, or a screencap of the Frame object.

        Parameters
        ----------
        episode : str | None, optional
            An episode key
        timestamp : int | None, optional
            A timestamp of the screencap
        frame : Frame | None, optional
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
            invalid_args_error = (
                f"Expected str and int or compuglobal.Frame, but received {type(episode)},"
                f" {type(timestamp)} and {type(frame)} instead"
            )
            raise TypeError(invalid_args_error)

        request = self.discovery.CAPTION.build_request(self.client.base_url, query=params)
        caption = await self.client.handle_request(request)
        return Screencap.model_validate(caption)

    async def search(
        self,
        search_text: str,
        season_minimum: int | None = None,
        season_maximum: int | None = None,
    ) -> list[FrameResult]:
        """Perform a search of the given search text and returns a list of all the Frames.

        Parameters
        ----------
        search_text : str
            The search text to query
        season_minimum : int | None, optional
            The minimum season allowed in the search results
        season_maximum : int | None, optional
            The maximum season allowed in the search results

        Returns
        -------
        list[FrameResult]
            A list of all frames found containing the search text.

        Raises
        ------
        NoSearchResultsFoundError
            Raises an error if no search results are found

        """
        optional_params = {"smin": season_minimum, "smax": season_maximum}
        query = {"q": search_text}
        query |= {k: v for k, v in optional_params.items() if v is not None}

        request = self.discovery.SEARCH.build_request(self.client.base_url, query=query)
        search_results = await self.client.handle_request(request)

        if len(search_results) > 0:
            return [FrameResult.model_validate(result) for result in search_results]

        raise NoSearchResultsFoundError

    async def search_for_screencap(
        self,
        search_text: str,
        season_minimum: int | None = None,
        season_maximum: int | None = None,
    ) -> Screencap:
        """Perform a search of the given search text and returns the top result.

        Parameters
        ----------
        search_text : str
            The search text to query
        season_minimum : int | None, optional
            The minimum season allowed in the search
        season_maximum : int | None, optional
            The maximum season allowed in the search

        Returns
        -------
        Screencap
            The screencap of the top search result

        """
        search_results = await self.search(search_text, season_minimum=season_minimum, season_maximum=season_maximum)
        result = search_results[0]
        return await self.get_screencap(result.key, result.timestamp)

    async def get_random_screencap(
        self,
        season_minimum: int | None = None,
        season_maximum: int | None = None,
    ) -> Screencap:
        """Get a random TV Show screencap.

        Parameters
        ----------
        season_minimum : int | None, optional
            Minimum season number allowed in random result
        season_maximum : int | None, optional
            Maximum season number allowed in random result

        Returns
        -------
        Screencap
            A random screencap object.

        """
        optional_params = {"smin": season_minimum, "smax": season_maximum}
        query = {k: v for k, v in optional_params.items() if v is not None}
        request = self.discovery.RANDOM.build_request(self.client.base_url, query=query)
        random = await self.client.handle_request(request)
        return Screencap.model_validate(random)

    async def browse_episode(self, episode: str) -> Episode:
        """Get all episode metadata and subtitles for a given episode.

        Parameters
        ----------
        episode : str
            Episode key (S01E01)

        Returns
        -------
        Episode
            The episode containing all metadata and subtitles

        """
        path_params = {"key": episode, "start_timestamp": 0, "end_timestamp": 99999999}
        request = self.metadata.EPISODE.build_request(self.client.base_url, path_params=path_params)
        episode_data = await self.client.handle_request(request)
        return Episode.model_validate(episode_data)

    async def get_transcript(self, episode: str, timestamp: int) -> list[Subtitle]:
        """Get a transcript of subtitles around the given episode key and timestamp.

        Parameters
        ----------
        episode : str
            Episode key (S01E01)
        timestamp : int
            Timestamp in the episode

        Returns
        -------
        list[Subtitle]
            The list of subtitles

        """
        params = {"e": episode, "t": timestamp}
        request = self.metadata.TRANSCRIPT.build_request(self.client.base_url, query=params)
        subtitles = await self.client.handle_request(request)
        return [Subtitle.model_validate(subtitle) for subtitle in subtitles]

    async def discover(self) -> list[ScreencapMoment]:
        """Discover random moments with their screencap and caption.

        Returns
        -------
        list[ScreencapMoment]
            List of random ``ScreencapMoment``s

        """
        request = self.discovery.DISCOVER.build_request(self.client.base_url)
        moments = await self.client.handle_request(request)
        return [ScreencapMoment.model_validate(moment) for moment in moments]

    async def navigator(self) -> list[EpisodeSummary]:
        """Get a summary for every single episode containing distributed frame IDs throughout the episode.

        Returns
        -------
        list[EpisodeSummary]
            A list of episode summaries

        """
        request = self.discovery.NAVIGATOR.build_request(self.client.base_url)
        summaries = await self.client.handle_request(request)
        return [EpisodeSummary.model_validate(summary) for summary in summaries]

    async def get_frames(self, key: str, timestamp: int, before: int, after: int) -> list[Frame]:
        """Get a list of all valid frames before and after the timestamp of the episode.

        Parameters
        ----------
        key : str
            The episode key of the screencap.
        timestamp : int
            The timestamp of the screencap.
        before : int
            The number of milliseconds before the timestamp.
        after : int
            The number of milliseconds after the timestamp.

        Returns
        -------
        list[Frame]
            A list of valid frames before and after the timestamp of
            the episode.

        """
        path_params = {"key": key, "timestamp": timestamp, "before": before, "after": after}

        request = self.discovery.FRAMES.build_request(self.client.base_url, path_params=path_params)
        frames = await self.client.handle_request(request)

        return [Frame.model_validate(frame_result) for frame_result in frames]

    async def get_image_url(self, screencap: Screencap) -> str:
        """Get the direct image url for the screencap without any caption.

        Parameters
        ----------
        screencap : Screencap
            The screencap to use for generating the image url

        Returns
        -------
        str
            The image url for the screencap without any caption.

        """
        path_params = {"key": screencap.frame.key, "timestamp": screencap.frame.timestamp}
        return self.media.IMAGE.build_encoded_url(self.client.base_url, path_params=path_params)

    async def get_comic_panel_url(
        self,
        screencap: Screencap,
        subtitles: list[Subtitle] | None = None,
        overlay_format: OverlayFormat | None = None,
    ) -> str:
        """Get the URL for a single comic panel showing the given screencap with subtitles.

        Parameters
        ----------
        screencap : Screencap
            The screencap to use in the comic panel
        subtitles : list[Subtitle] | None, optional
            A list of subtitles to overlay in the comic panel
        overlay_format : OverlayFormat | None, optional
            The formatting to use in the comic panel overlay (subtitle)

        Returns
        -------
        str
            The url of the comic panel

        """
        screencap, subtitles, overlay_format = self._resolve_overlay_inputs(screencap, subtitles, overlay_format)

        panel = ComicPanel.from_screencap(screencap=screencap, overlay_format=overlay_format)

        params = {"b64": panel.get_encoded()}
        return self.media.COMIC_PANEL.build_encoded_url(self.client.base_url, query=params)

    async def get_comic_strip_url(
        self,
        screencap: Screencap,
        subtitles: list[Subtitle] | None = None,
        overlay_format: OverlayFormat | list[OverlayFormat] | None = None,
    ) -> str:
        """Get the URL for a comic strip showing the given screencap with subtitles.

        Parameters
        ----------
        screencap : Screencap
            The screencap to use in the comic strip
        subtitles : list[Subtitle] | None, optional
            The subtitles to overlay in the comic strip
        overlay_format : OverlayFormat | list[OverlayFormat] | None, optional
            The formatting to use in the comic strip overlays (subtitleS). See :meth:`OverlayFormat.normalise` for
            full details on how formats are resolved.

        Returns
        -------
        str
            The url of the comic strip

        """
        screencap, subtitles, overlay_format = self._resolve_overlay_inputs(screencap, subtitles, overlay_format)

        comic_strip = ComicStrip.from_screencap(screencap=screencap, overlay_format=overlay_format)
        params = {"b64": comic_strip.get_encoded(), "layout": comic_strip.layout}
        return self.media.COMIC_STRIP.build_encoded_url(self.client.base_url, query=params)

    async def get_comic_maker_url(
        self,
        screencap: Screencap,
        subtitles: list[Subtitle] | None = None,
        overlay_format: OverlayFormat | list[OverlayFormat] | None = None,
    ) -> str:
        """Get a url for making a comic with the given screencap, subtitles, and overlay format(s).

        Parameters
        ----------
        screencap : Screencap
            The screencap to make the comic with
        subtitles : list[Subtitle] | None, optional
            The subtitles to override in the comic maker, by default None
        overlay_format : OverlayFormat | list[OverlayFormat] | None, optional
            The subtitle/overlay formatting to override in the comic maker, by default None

        Returns
        -------
        str
            The url for making the comic

        """
        screencap, subtitles, overlay_format = self._resolve_overlay_inputs(screencap, subtitles, overlay_format)
        path_params = {"key": screencap.frame.key, "timestamp": screencap.frame.timestamp}

        strip = ComicStrip.from_screencap(screencap=screencap, overlay_format=overlay_format)

        return self.media.COMIC_MAKER.build_encoded_url(
            base_url=self.BASE_URL,
            path_params=path_params,
            query={"b64": strip.get_encoded(), "layout": strip.layout},
        )

    async def get_gif_url(
        self,
        screencap: Screencap,
        subtitles: list[Subtitle] | None = None,
        overlay_format: OverlayFormat | list[OverlayFormat] | None = None,
    ) -> str:
        """Get the URL for a gif of the given screencap with default or given subtitles.

        Parameters
        ----------
        screencap : Screencap
            The screencap to use for the gif
        subtitles : list[Subtitle] | None, optional
            The subtitles to overlay in the gif
        overlay_format : OverlayFormat | list[OverlayFormat] | None, optional
            The formatting to use in the gif overlays (subtitles). See :meth:`OverlayFormat.normalise` for
            full details on how formats are resolved.

        Returns
        -------
        str
            The URL of the gif, or a comic strip as a fallback if gif rendering fails.

        """
        screencap, subtitles, overlay_format = self._resolve_overlay_inputs(screencap, subtitles, overlay_format)

        stream = Stream.from_screencap(screencap=screencap, overlay_format=overlay_format)

        request = self.media.RENDER_GIF.build_request(self.client.base_url, body=stream)
        request.body = [request.body]
        response = await self.client.handle_request(request)

        if isinstance(response, str):  # pragma: no branch
            for line in response.splitlines():
                data = json.loads(line)
                if "url" in data:
                    return f"{self.client.base_url}{data.get('url')}"

        return await self.get_comic_strip_url(screencap)

    async def get_gif_maker_url(
        self,
        screencap: Screencap,
        subtitles: list[Subtitle] | None = None,
        overlay_format: OverlayFormat | list[OverlayFormat] | None = None,
    ) -> str:
        """Get a url for making a comic with the given screencap, subtitles, and overlay format(s).

        Parameters
        ----------
        screencap : Screencap
            The screencap to make the comic with
        subtitles : list[Subtitle] | None, optional
            The subtitles to override in the comic maker, by default None
        overlay_format : OverlayFormat | list[OverlayFormat] | None, optional
            The subtitle/overlay formatting to override in the comic maker, by default None

        Returns
        -------
        str
            The url for making the comic

        """
        screencap, subtitles, overlay_format = self._resolve_overlay_inputs(screencap, subtitles, overlay_format)

        path_params = {
            "key": screencap.frame.key,
            "start_timestamp": screencap.get_start(),
            "end_timestamp": screencap.get_end(),
        }

        stream = Stream.from_screencap(screencap=screencap, overlay_format=overlay_format)

        return self.media.GIF_MAKER.build_encoded_url(
            base_url=self.BASE_URL,
            path_params=path_params,
            query={"b64": stream.get_encoded()},
        )

    @overload
    def _resolve_overlay_inputs(
        self,
        screencap: Screencap,
        subtitles: list[Subtitle] | None = None,
        overlay_format: OverlayFormat | None = None,
    ) -> tuple[Screencap, list[Subtitle], OverlayFormat]: ...

    @overload
    def _resolve_overlay_inputs(
        self,
        screencap: Screencap,
        subtitles: list[Subtitle] | None = None,
        overlay_format: OverlayFormat | list[OverlayFormat] | None = None,
    ) -> tuple[Screencap, list[Subtitle], OverlayFormat | list[OverlayFormat]]: ...

    def _resolve_overlay_inputs(
        self,
        screencap: Screencap,
        subtitles: list[Subtitle] | None = None,
        overlay_format: OverlayFormat | list[OverlayFormat] | None = None,
    ) -> tuple[Screencap, list[Subtitle], OverlayFormat | list[OverlayFormat]]:

        # Use default format if not given
        overlay_format = overlay_format or self.config.default_format

        # Use screencap subtitles if not given
        subtitles = subtitles or screencap.subtitles

        # Prevent too many subtitles being used
        subtitles = subtitles[: self._MAX_ALLOWED_SUBTITLES]

        # Change subtitles
        screencap = screencap.model_copy(update={"subtitles": subtitles})

        return screencap, subtitles, overlay_format


class CapitalBeatUs(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing CapitalBeatUs API endpoints (West Wing)."""

    BASE_URL = "https://capitalbeat.us"
    TITLE = "West Wing"
    DEFAULT_FORMAT = OverlayFormat(font_family=FontFamily.IMPACT)


class Frinkiac(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing Frinkiac API endpoints (The Simpsons)."""

    BASE_URL = "https://frinkiac.com"
    TITLE = "Simpsons"
    DEFAULT_FORMAT = OverlayFormat(font_family=FontFamily.AKBAR)


@deprecated("The MasterOfAllScience API is deprecated, and currently redirects to Frinkiac")
class MasterOfAllScience(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing MasterOfAllScience API endpoints (Rick and Morty)."""

    BASE_URL = "https://masterofallscience.com"
    TITLE = "Rick and Morty"
    DEFAULT_FORMAT = OverlayFormat(font_family=FontFamily.IMPACT)


class Morbotron(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing Morbotron API endpoints (Futurama)."""

    BASE_URL = "https://morbotron.com"
    TITLE = "Futurama"
    DEFAULT_FORMAT = OverlayFormat(font_family=FontFamily.FR_BOLD)
