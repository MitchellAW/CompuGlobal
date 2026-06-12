"""All metadata endpoints of an CGHMC API."""

from .endpoint import Endpoint, RequestMethod


class MetadataAPI:
    """An object with the available metadata endpoints.

    Attributes
    ----------
    EPISODE : Endpoint
        The /api/episode endpoint of the API
    TRANSCRIPT : Endpoint
        The /api/transcript endpoint of the API

    """

    EPISODE: Endpoint = Endpoint(
        path="/api/episode/{key}/{start_timestamp}/{end_timestamp}",
        method=RequestMethod.GET,
    )

    TRANSCRIPT: Endpoint = Endpoint(
        path="/api/transcript",
        method=RequestMethod.GET,
        required_query_params=frozenset({"e", "t"}),
    )
