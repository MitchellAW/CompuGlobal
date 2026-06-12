"""All endpoints used for generating media (images/comics/gifs/mp4s)."""

from compuglobal.models.stream import Stream

from .endpoint import Endpoint, RequestMethod


class MediaAPI:
    """An object with the available media endpoints for dealing with images/comics/gifs/mp4s.

    Attributes
    ----------
    IMAGE : Endpoint
        The /img/*/*.jpg endpoint of the API
    COMIC_PANEL : Endpoint
        The /comic/img endpoint of the API for a comic panel
    COMIC_STRIP : Endpoint
        The /comic/img endpoint of the API for a comic strip
    RENDER_GIF : Endpoint
        The /api/render/gif/stream endpoint of the API for generating gifs
    RENDER_MP4 : Endpoint
        The /api/render/mp4 endpoint of the API for generating mp4s
    DETECT_LOOP : Endpoint
        The /api/detect-loop endpoint for detecting gif/mp4 loops

    """

    IMAGE: Endpoint = Endpoint(
        path="/img/{key}/{timestamp}.jpg",
        method=RequestMethod.GET,
    )

    COMIC_PANEL: Endpoint = Endpoint(
        path="/comic/img",
        method=RequestMethod.GET,
        required_query_params=frozenset({"b64"}),
    )

    COMIC_STRIP: Endpoint = Endpoint(
        path="/comic/img",
        method=RequestMethod.GET,
        required_query_params=frozenset({"b64", "layout"}),
    )

    RENDER_GIF: Endpoint = Endpoint(
        path="/api/render/gif/stream",
        method=RequestMethod.POST,
        body_model=Stream,
    )
    RENDER_MP4: Endpoint = Endpoint(
        path="/api/render/mp4",
        method=RequestMethod.POST,
        body_model=Stream,
    )

    DETECT_LOOP: Endpoint = Endpoint(
        path="/api/detect-loop",
        method=RequestMethod.GET,
        required_query_params=frozenset(
            {"episode", "start", "end"},
        ),
    )
