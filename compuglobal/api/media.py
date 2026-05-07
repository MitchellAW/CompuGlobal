import json
from typing import List

from ..errors import APIPageStatusError
from ..models.comic import ComicOverlay, ComicPanel, ComicStrip, build_overlay
from ..models.screencap import Screencap
from ..models.stream import Stream, build_stream_overlays
from ..models.subtitle import Subtitle
from .base import EndpointBase
from .endpoint import Endpoint, RequestMethod


class MediaAPI(EndpointBase):
    IMAGE = Endpoint(
        path="/img/{key}/{timestamp}.jpg",
        method=RequestMethod.GET,
    )

    COMIC_PANEL = Endpoint(
        path="/comic/img",
        method=RequestMethod.GET,
        query_params=frozenset({"b64"}),
    )

    COMIC_STRIP = Endpoint(
        path="/comic/img",
        method=RequestMethod.GET,
        query_params=frozenset({"b64", "layout"}),
    )

    RENDER_GIF = Endpoint(
        path="/api/render/gif/stream",
        method=RequestMethod.POST,
        body_model=Stream,
    )
    RENDER_MP4 = Endpoint(
        path="/api/render/mp4",
        method=RequestMethod.POST,
        body_model=Stream,
    )

    DETECT_LOOP = Endpoint(
        path="/api/detect-loop",
        method=RequestMethod.GET,
        query_params=frozenset(
            {"episode", "start", "end"},
        ),
    )

    def get_image_url(self, screencap: Screencap):
        """Returns the direct image url for the screencap without any caption.

        Returns
        -------
        str
            The image url for the screencap without any caption."""

        path_params = {"key": screencap.frame.key, "timestamp": screencap.frame.timestamp}
        return self.IMAGE.build_encoded_url(self.client.base_url, path_params=path_params)

    def get_comic_panel_url(self, screencap: Screencap, subtitles: List[Subtitle] = []):
        if len(subtitles) == 0:
            subtitles = screencap.subtitles

        overlays = build_overlay(subtitles, font=self.config.default_font)
        panel = ComicPanel(e=screencap.frame.key, ts=screencap.frame.timestamp, o=overlays)

        params = {"b64": panel.get_encoded()}
        return self.COMIC_PANEL.build_encoded_url(self.client.base_url, query=params)

    def get_comic_strip_url(self, screencap: Screencap, subtitles: List[Subtitle] = []):
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
        return self.COMIC_STRIP.build_encoded_url(self.client.base_url, query=params)

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

        request = self.RENDER_GIF.build_request(self.client.base_url, body=stream)
        request.body = [request.body]
        response = await self.client.handle_request(request)

        for line in response.splitlines():
            data = json.loads(line)
            if "url" in data:
                return f"{self.client.base_url}/{data.get("url")}"

        raise APIPageStatusError(400, self.client.base_url)
