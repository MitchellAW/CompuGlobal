"""Test metadata module endpoint definition match expected API contract."""

from inline_snapshot import snapshot

from compuglobal.api.endpoint import RequestMethod
from compuglobal.api.metadata import MetadataAPI


def test_metadata_endpoints_use_correct_methods() -> None:
    endpoints = [MetadataAPI.EPISODE, MetadataAPI.TRANSCRIPT]
    for endpoint in endpoints:
        assert endpoint.method == RequestMethod.GET


def test_metadata_endpoints_use_api_route() -> None:
    endpoints = [MetadataAPI.EPISODE, MetadataAPI.TRANSCRIPT]
    for endpoint in endpoints:
        assert endpoint.path.startswith("/api/")


def test_metadata_episode_has_expected_path() -> None:
    path = MetadataAPI.EPISODE.path
    assert path.startswith("/api/episode")
    assert path.endswith("/{key}/{start_timestamp}/{end_timestamp}")


def test_metadata_episode_has_expected_params() -> None:
    params = MetadataAPI.EPISODE.query_params
    assert params == frozenset()


def test_metadata_transcript_has_expected_path() -> None:
    path = MetadataAPI.TRANSCRIPT.path
    assert path == "/api/transcript"


def test_metadata_transcript_has_expected_params() -> None:
    params = MetadataAPI.TRANSCRIPT.query_params
    assert params == snapshot(frozenset({"e", "t"}))
