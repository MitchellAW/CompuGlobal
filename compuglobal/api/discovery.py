"""All endpoints used for discovery/search/lookups of screencaps/frames."""

from compuglobal.api.endpoint import Endpoint, RequestMethod


class DiscoveryAPI:
    """Defines the available discovery endpoints for finding screencaps/frames.

    Attributes
    ----------
    CAPTION : Endpoint
        The /api/caption endpoint for looking up Screencaps
    DISCOVER : Endpoint
        The /api/discover endpoint for discovering random screencaps
    RANDOM : Endpoint
        The /api/random endpoint for getting a random screencap
    NAVIGATOR : Endpoint
        The /api/navigator endpoint for getting all available episode data
    SEARCH : Endpoint
        The /api/search endpoint for searching screencaps
    FRAMES : Endpoint
        The /api/frames endpoint for getting frames around a particular screencap

    """

    CAPTION: Endpoint = Endpoint(
        path="/api/caption",
        method=RequestMethod.GET,
        required_query_params=frozenset({"e", "t", "nearby"}),
    )

    DISCOVER: Endpoint = Endpoint(
        path="/api/discover",
        method=RequestMethod.GET,
    )

    RANDOM: Endpoint = Endpoint(
        path="/api/random",
        method=RequestMethod.GET,
        optional_query_params=frozenset({"smin", "smax"}),
    )

    NAVIGATOR: Endpoint = Endpoint(
        path="/api/navigator",
        method=RequestMethod.GET,
    )

    SEARCH: Endpoint = Endpoint(
        path="/api/search",
        method=RequestMethod.GET,
        required_query_params=frozenset({"q"}),
        optional_query_params=frozenset({"smin", "smax"}),
    )

    FRAMES: Endpoint = Endpoint(
        path="/api/frames/{key}/{timestamp}/{before}/{after}",
        method=RequestMethod.GET,
    )
