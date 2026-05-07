from .endpoints import Endpoints
from .models.font import FontFamily


class BaseCompuGlobalAPI:
    """Represents an API Wrapper used for accessing the cghmc API endpoints.

    Parameters
    ----------
    url: str
        The url of the API.
    title: str
        The title of the tv show/movie/skit that the url leads to.

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

    def __init__(self, url, title, default_font: FontFamily = FontFamily.IMPACT):
        self.url = url
        self.title = title
        self.context = {"_api": self}

        # All API endpoints
        self.endpoints = Endpoints()

        # Default font to use for text overlays on comics/gifs
        self.default_font = default_font
