from dataclasses import dataclass

from .endpoint import Endpoint, RequestMethod


@dataclass
class MetadataAPI:
    EPISODE = Endpoint(
        path="/api/episode/{key}/{start_timestamp}/{end_timestamp}",
        method=RequestMethod.GET,
    )

    TRANSCRIPT = Endpoint(
        path="/api/transcript",
        method=RequestMethod.GET,
        query_params=frozenset({"e", "t"}),
    )
