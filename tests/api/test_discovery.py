"""Test discovery module endpoint definition match expected API contract."""

from inline_snapshot import snapshot

from compuglobal.api.discovery import DiscoveryAPI
from compuglobal.api.endpoint import RequestMethod


def test_discovery_endpoints_use_correct_methods() -> None:
    endpoints = [
        DiscoveryAPI.CAPTION,
        DiscoveryAPI.DISCOVER,
        DiscoveryAPI.RANDOM,
        DiscoveryAPI.NAVIGATOR,
        DiscoveryAPI.SEARCH,
        DiscoveryAPI.FRAMES,
    ]
    for endpoint in endpoints:
        assert endpoint.method == RequestMethod.GET


def test_discovery_endpoints_use_api_route() -> None:
    endpoints = [
        DiscoveryAPI.CAPTION,
        DiscoveryAPI.DISCOVER,
        DiscoveryAPI.RANDOM,
        DiscoveryAPI.NAVIGATOR,
        DiscoveryAPI.SEARCH,
        DiscoveryAPI.FRAMES,
    ]
    for endpoint in endpoints:
        assert endpoint.path.startswith("/api/")


def test_discovery_caption_expected_path() -> None:
    path = DiscoveryAPI.CAPTION.path
    assert path == "/api/caption"


def test_discovery_caption_expected_params() -> None:
    params = DiscoveryAPI.CAPTION.required_query_params
    assert params == snapshot(frozenset({"e", "nearby", "t"}))


def test_discovery_discover_expected_path() -> None:
    path = DiscoveryAPI.DISCOVER.path
    assert path == "/api/discover"


def test_discovery_discover_expected_params() -> None:
    params = DiscoveryAPI.DISCOVER.required_query_params
    assert params == frozenset()


def test_discovery_random_expected_path() -> None:
    path = DiscoveryAPI.RANDOM.path
    assert path == "/api/random"


def test_discovery_random_expected_params() -> None:
    params = DiscoveryAPI.RANDOM.required_query_params
    assert params == frozenset()


def test_discovery_random_optional_params() -> None:
    params = DiscoveryAPI.RANDOM.optional_query_params
    assert params == snapshot(frozenset({"smax", "smin"}))


def test_discovery_navigator_expected_path() -> None:
    path = DiscoveryAPI.NAVIGATOR.path
    assert path == "/api/navigator"


def test_discovery_navigator_expected_params() -> None:
    params = DiscoveryAPI.NAVIGATOR.required_query_params
    assert params == frozenset()


def test_discovery_search_expected_path() -> None:
    path = DiscoveryAPI.SEARCH.path
    assert path == "/api/search"


def test_discovery_search_expected_params() -> None:
    params = DiscoveryAPI.SEARCH.required_query_params
    assert params == snapshot(frozenset({"q"}))


def test_discovery_search_optional_params() -> None:
    params = DiscoveryAPI.SEARCH.optional_query_params
    assert params == snapshot(frozenset({"smax", "smin"}))


def test_discovery_frames_expected_path() -> None:
    path = DiscoveryAPI.FRAMES.path
    assert path.startswith("/api/frames")
    assert path.endswith("/{key}/{timestamp}/{before}/{after}")


def test_discovery_frames_expected_params() -> None:
    params = DiscoveryAPI.FRAMES.required_query_params
    assert params == frozenset()
