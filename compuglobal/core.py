from compuglobal.models.font import FontFamily


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
        self.context = {"api": self}

        # Initalise all API endpoints
        self.random_url = self.url + "api/random"
        self.caption_url = f"{self.url}/api/caption"  # api/caption?e=S01E01&t=9551&nearby=1
        self.search_url = f"{self.url}/api/search"
        self.episode_url = self.url + "api/episode"  # api/episode/S01E01/0/99999999
        self.navigator_url = f"{self.url}/api/navigator"
        self.transcript_url = f"{self.url}/api/transcript"  # api/transcript/?e=S01E01&t=9551
        self.render_gif_url = f"{self.url}/api/render/gif/stream"  # Stream-params
        self.render_mp4_url = f"{self.url}/api/render/mp4"  # Stream-params
        self.comic_url = f"{self.url}/comic/img"  # comic/img?b64=
        self.frames_url = self.url + "/{}/{}/{}"

        # Default font to use for text overlays on comics/gifs
        self.default_font = default_font
