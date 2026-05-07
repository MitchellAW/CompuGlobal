from dataclasses import dataclass
from typing import Optional

import aiohttp

from .api.client import CompuGlobalAPIClient
from .api.config import CompuGlobalAPIConfig
from .api.discover import DiscoverAPI
from .api.media import MediaAPI
from .api.metadata import MetadataAPI
from .models.font import FontFamily

"""Contains the async API Wrappers used for accessing all the cghmc API
endpoints."""


@dataclass
class AsyncCompuGlobalAPI:
    client: CompuGlobalAPIClient
    config: CompuGlobalAPIConfig

    def __init__(self, client, config):
        endpoints = [
            DiscoverAPI(client=client, config=config),
            MediaAPI(client=client, config=config),
            MetadataAPI(client=client, config=config),
        ]

        self._attach_endpoint_methods(endpoints)

    def _attach_endpoint_methods(self, endpoints):
        for endpoint in endpoints:
            print(type(endpoint))
            for name, method in endpoint._get_public_methods():
                if hasattr(self, name):
                    raise RuntimeError(f"Duplicate API method: {name}")

                # bind method to client
                setattr(self, name, method)


# West Wing Meme/GIF generator API
class CapitalBeatUs(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing CapitalBeatUs API endpoints (West Wing)."""

    def __init__(
        self,
        session: Optional[aiohttp.ClientSession] = None,
        timeout: int = 15,
    ):
        client = CompuGlobalAPIClient(base_url="https://capitalbeat.us", session=session, timeout=timeout)
        config = CompuGlobalAPIConfig(title="West Wing", default_font=FontFamily.IMPACT)

        super().__init__(client=client, config=config)


# Simpsons Meme/GIF generator API
class Frinkiac(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing Frinkiac API endpoints (The Simpsons)."""

    def __init__(
        self,
        session: Optional[aiohttp.ClientSession] = None,
        timeout: int = 15,
    ):
        client = CompuGlobalAPIClient(base_url="https://frinkiac.com", session=session, timeout=timeout)
        config = CompuGlobalAPIConfig(title="The Simpsons", default_font=FontFamily.AKBAR)

        super().__init__(client=client, config=config)


# Rick and Morty Meme/GIF generator API
class MasterOfAllScience(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing MasterOfAllScience API endpoints
    (Rick and Morty)."""

    def __init__(
        self,
        session: Optional[aiohttp.ClientSession] = None,
        timeout: int = 15,
    ):
        client = CompuGlobalAPIClient(base_url="https://masterofallscience.com", session=session, timeout=timeout)
        config = CompuGlobalAPIConfig(title="Rick and Morty", default_font=FontFamily.IMPACT)

        super().__init__(client=client, config=config)


# Futurama Meme/GIF generator API
class Morbotron(AsyncCompuGlobalAPI):
    """An API Wrapper for accessing Morbotron API endpoints (Futurama)."""

    def __init__(
        self,
        session: Optional[aiohttp.ClientSession] = None,
        timeout: int = 15,
    ):
        client = CompuGlobalAPIClient(base_url="https://morbotron.com", session=session, timeout=timeout)
        config = CompuGlobalAPIConfig(title="Futurama", default_font=FontFamily.FR_BOLD)

        super().__init__(client=client, config=config)
