"""Used for interacting with and building CGHMC APIs."""

import dataclasses
import json
import logging
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

log = logging.getLogger(__name__)

"""Contains the async API Wrappers used for accessing all the cghmc API endpoints."""


class AsyncCompuGlobalAPI:
    """Represents a base API of the CGHMC family.

    Parameters
    ----------
    session : aiohttp.ClientSession
        The client session to use for all API calls
    default_format : OverlayFormat | None
        The default overlay format to use for all overlays/subtitles
    max_retries : int
        The maximum number of retries for all API requests

    Attributes
    ----------
    BASE_URL : str
        The base url of the API
    TITLE : str
        The title of the API
    EXTRA_FONTS : frozenset[FontFamily]
        A frozenset of any extra fonts permitted by the API
    discovery : DiscoveryAPI
        The discovery API with all discovery endpoints
    media : MediaAPI
        The media API with all media endpoints
    metadata : MetadataAPI
        The metadataAPI with all metadata endpoints

    """

    BASE_URL: str
    TITLE: str
    EXTRA_FONTS: frozenset[FontFamily] = frozenset()
    _MAX_ALLOWED_SUBTITLES = 4

    discovery: DiscoveryAPI = DiscoveryAPI()
    media: MediaAPI = MediaAPI()
    metadata: MetadataAPI = MetadataAPI()

    def __init__(
        self,
        session: aiohttp.ClientSession,
        default_format: OverlayFormat | None = None,
        max_retries: int = 0,
    ) -> None:
        extra_fonts = list(self.EXTRA_FONTS)
        if default_format is None:
            chosen_font = extra_fonts[0] if len(extra_fonts) > 0 else FontFamily.IMPACT
            default_format = OverlayFormat(font_family=chosen_font)

        allowed_fonts = extra_fonts + FontFamily.universal_fonts()

        self.config = CompuGlobalAPIConfig(
            title=self.TITLE,
            allowed_fonts=allowed_fonts,
            default_format=default_format,
        )
        self.client = CompuGlobalAPIClient(base_url=self.BASE_URL, session=session, max_retries=max_retries)

    async def get_screencap(
        self,
        *,
        episode: str | None = None,
        timestamp: int | None = None,
    ) -> Screencap:
        """Get the screencap for the given episode & timestamp.

        Parameters
        ----------
        episode : str | None
            An episode key
        timestamp : int | None
            A timestamp of the screencap

        Returns
        -------
        Screencap
            The screencap for the given episode key and timestamp.

        """
        params = {"e": episode, "t": timestamp, "nearby": 1}

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
        season_minimum : int | None
            The minimum season allowed in the search results
        season_maximum : int | None
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

        log.debug(
            "No search results found | base_url=%s | search_text=%s | season_minimum=%s | season_maximum=%s",
            self.BASE_URL,
            search_text,
            season_minimum,
            season_maximum,
        )
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
        season_minimum : int | None
            The minimum season allowed in the search
        season_maximum : int | None
            The maximum season allowed in the search

        Returns
        -------
        Screencap
            The screencap of the top search result

        """
        search_results = await self.search(search_text, season_minimum=season_minimum, season_maximum=season_maximum)
        result = search_results[0]
        return await self.get_screencap(episode=result.key, timestamp=result.timestamp)

    async def get_random_screencap(
        self,
        season_minimum: int | None = None,
        season_maximum: int | None = None,
    ) -> Screencap:
        """Get a random TV Show screencap.

        Parameters
        ----------
        season_minimum : int | None
            Minimum season number allowed in random result
        season_maximum : int | None
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
            List of random screencap moments

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
        subtitles : list[Subtitle] | None
            A list of subtitles to overlay in the comic panel
        overlay_format : OverlayFormat | None
            The formatting to use in the comic panel overlay (subtitle)

        Returns
        -------
        str
            The url of the comic panel

        """
        screencap, subtitles, overlay_format = self._resolve_overlay_inputs(screencap, subtitles, overlay_format)

        panel = ComicPanel.from_screencap(screencap=screencap, overlay_format=overlay_format)

        params = {"b64": panel.encoded}
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
        subtitles : list[Subtitle] | None
            The subtitles to overlay in the comic strip
        overlay_format : OverlayFormat | list[OverlayFormat] | None
            The formatting to use in the comic strip overlays (subtitleS). See :meth:`OverlayFormat.normalise` for
            full details on how formats are resolved.

        Returns
        -------
        str
            The url of the comic strip

        """
        screencap, subtitles, overlay_format = self._resolve_overlay_inputs(screencap, subtitles, overlay_format)

        comic_strip = ComicStrip.from_screencap(screencap=screencap, overlay_format=overlay_format)
        params = {"b64": comic_strip.encoded, "layout": comic_strip.layout}
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
        subtitles : list[Subtitle] | None
            The subtitles to override in the comic maker, by default None
        overlay_format : OverlayFormat | list[OverlayFormat] | None
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
            query={"b64": strip.encoded, "layout": strip.layout},
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
        subtitles : list[Subtitle] | None
            The subtitles to overlay in the gif
        overlay_format : OverlayFormat | list[OverlayFormat] | None
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
        subtitles : list[Subtitle] | None
            The subtitles to override in the comic maker, by default None
        overlay_format : OverlayFormat | list[OverlayFormat] | None
            The subtitle/overlay formatting to override in the comic maker, by default None

        Returns
        -------
        str
            The url for making the comic

        """
        screencap, subtitles, overlay_format = self._resolve_overlay_inputs(screencap, subtitles, overlay_format)

        path_params = {
            "key": screencap.frame.key,
            "start_timestamp": screencap.start,
            "end_timestamp": screencap.end,
        }

        stream = Stream.from_screencap(screencap=screencap, overlay_format=overlay_format)

        return self.media.GIF_MAKER.build_encoded_url(
            base_url=self.BASE_URL,
            path_params=path_params,
            query={"b64": stream.encoded},
        )

    def _resolve_font(self, overlay_format: OverlayFormat) -> OverlayFormat:
        if overlay_format.font_family in self.config.allowed_fonts:
            return overlay_format

        log.warning(
            "Font family %s is not allowed for %s, using IMPACT font instead | overlay_format=%s",
            overlay_format.font_family,
            self.config.title,
            overlay_format,
        )
        return dataclasses.replace(overlay_format, font_family=FontFamily.IMPACT)

    def _resolve_fonts(self, overlay_formats: list[OverlayFormat]) -> list[OverlayFormat]:
        return [self._resolve_font(overlay_format) for overlay_format in overlay_formats]

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
        if overlay_format != self.config.default_format:
            log.debug("Using custom overlay format | screencap=%s | overlay_format=%s", screencap, overlay_format)

        # Resolve any disallowed fonts in the format(s)
        if isinstance(overlay_format, list):
            overlay_format = self._resolve_fonts(overlay_format)
        else:
            overlay_format = self._resolve_font(overlay_format)

        # Use screencap subtitles if not given
        subtitles = subtitles or screencap.subtitles
        if subtitles != screencap.subtitles:
            log.debug("Using custom subtitles | screencap=%s | subtitles=%s", screencap, subtitles)

        # Prevent too many subtitles being used
        subtitles = subtitles[: self._MAX_ALLOWED_SUBTITLES]

        # Change subtitles
        screencap = screencap.model_copy(update={"subtitles": subtitles})

        return screencap, subtitles, overlay_format


class CapitalBeatUs(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing CapitalBeatUs API endpoints (West Wing)."""

    BASE_URL = "https://capitalbeat.us"
    TITLE = "West Wing"


class Frinkiac(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing Frinkiac API endpoints (The Simpsons)."""

    BASE_URL = "https://frinkiac.com"
    TITLE = "Simpsons"
    EXTRA_FONTS = frozenset({FontFamily.AKBAR})


@deprecated("The MasterOfAllScience API is deprecated, and currently redirects to Frinkiac")
class MasterOfAllScience(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing MasterOfAllScience API endpoints (Rick and Morty)."""

    BASE_URL = "https://masterofallscience.com"
    TITLE = "Rick and Morty"


class Morbotron(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing Morbotron API endpoints (Futurama)."""

    BASE_URL = "https://morbotron.com"
    TITLE = "Futurama"
    EXTRA_FONTS = frozenset({FontFamily.FR_BOLD})
