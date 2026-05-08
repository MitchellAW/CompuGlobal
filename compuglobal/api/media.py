from ..models.stream import Stream
from .endpoint import Endpoint, RequestMethod


class MediaAPI:
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
