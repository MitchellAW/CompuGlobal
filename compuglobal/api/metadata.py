"""All metadata endpoints of an CGHMC API."""

from dataclasses import dataclass

from .endpoint import Endpoint, RequestMethod


@dataclass
class MetadataAPI:
    """An object with the available metadata endpoints.

    Attributes
    ----------
    EPISODE: Endpoint
        The /api/episode endpoint of the API
    TRANSCRIPT: Endpoint
        The /api/transcript endpoint of the API

    """

    EPISODE = Endpoint(
        path="/api/episode/{key}/{start_timestamp}/{end_timestamp}",
        method=RequestMethod.GET,
    )

    TRANSCRIPT = Endpoint(
        path="/api/transcript",
        method=RequestMethod.GET,
        query_params=frozenset({"e", "t"}),
    )
