import aiohttp

from .api.client import CompuGlobalAPIClient
from .api.config import CompuGlobalAPIConfig
from .api.discover import DiscoverAPI
from .api.media import MediaAPI
from .api.metadata import MetadataAPI
from .models.font import FontFamily

"""Contains the async API Wrappers used for accessing all the cghmc API
endpoints."""


class AsyncCompuGlobalAPI:
    BASE_URL: str
    TITLE: str
    DEFAULT_FONT: FontFamily

    def __init__(self, session: aiohttp.ClientSession | None = None, timeout: int = 15):
        client = CompuGlobalAPIClient(base_url=self.BASE_URL, session=session, timeout=timeout)
        config = CompuGlobalAPIConfig(title=self.TITLE, default_font=self.DEFAULT_FONT)

        endpoints = [
            DiscoverAPI(client=client, config=config),
            MediaAPI(client=client, config=config),
            MetadataAPI(client=client, config=config),
        ]

        self._attach_endpoint_methods(endpoints)

    def _attach_endpoint_methods(self, endpoints):
        for endpoint in endpoints:
            for name, method in endpoint._get_public_methods():
                if hasattr(self, name):
                    raise RuntimeError(f"Duplicate API method: {name}")

                # bind method to client
                setattr(self, name, method)


# West Wing Meme/GIF generator API
class CapitalBeatUs(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing CapitalBeatUs API endpoints (West Wing)."""

    BASE_URL = "https://capitalbeat.us"
    TITLE = "West Wing"
    DEFAULT_FONT = FontFamily.IMPACT


# Simpsons Meme/GIF generator API
class Frinkiac(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing Frinkiac API endpoints (The Simpsons)."""

    BASE_URL = "https://frinkiac.com"
    TITLE = "Simpsons"
    DEFAULT_FONT = FontFamily.AKBAR


# Rick and Morty Meme/GIF generator API
class MasterOfAllScience(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing MasterOfAllScience API endpoints
    (Rick and Morty)."""

    BASE_URL = "https://masterofallscience.com"
    TITLE = "Rick and Morty"
    DEFAULT_FONT = FontFamily.IMPACT


# Futurama Meme/GIF generator API
class Morbotron(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing Morbotron API endpoints (Futurama)."""

    BASE_URL = "https://morbotron.com"
    TITLE = "Futurama"
    DEFAULT_FONT = FontFamily.FR_BOLD
