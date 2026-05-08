from .endpoint import Endpoint, RequestMethod


class DiscoverAPI:
    CAPTION = Endpoint(
        path="/api/caption",
        method=RequestMethod.GET,
        query_params=frozenset({"e", "t", "nearby"}),
    )

    DISCOVER = Endpoint(
        path="/api/discover",
        method=RequestMethod.GET,
    )

    RANDOM = Endpoint(
        path="/api/random",
        method=RequestMethod.GET,
    )

    NAVIGATOR = Endpoint(
        path="/api/navigator",
        method=RequestMethod.GET,
    )

    SEARCH = Endpoint(
        path="/api/search",
        method=RequestMethod.GET,
        query_params=frozenset({"q"}),
    )

    FRAMES = Endpoint(
        path="/api/frames/{key}/{timestamp}/{before}/{after}",
        method=RequestMethod.GET,
    )
