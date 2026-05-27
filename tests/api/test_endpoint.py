"""Test endpoint module."""

import pytest
from pydantic import BaseModel

from compuglobal.api.endpoint import Endpoint, PreparedRequest, RequestMethod


def test_prepared_request_defaults() -> None:
    request = PreparedRequest(url="https://example.com")
    expected = PreparedRequest(url="https://example.com", method=RequestMethod.GET, params=None, body=None)
    assert request == expected


def test_prepared_request_overrides() -> None:
    request = PreparedRequest(
        url="https://example.com",
        method=RequestMethod.POST,
        params={"a": 1},
        body={"key": "value"},
    )

    assert request.url == "https://example.com"
    assert request.method == RequestMethod.POST
    assert request.params == {"a": 1}
    assert request.body == {"key": "value"}


def test_prepared_request_body_dict() -> None:
    request = PreparedRequest(url="https://example.com", body={"a": 1})
    assert isinstance(request.body, dict)


def test_prepared_request_body_list() -> None:
    request = PreparedRequest(url="https://example.com", body=[{"a": 1}, {"b": 2}])
    assert isinstance(request.body, list)


def test_params_empty_dict_vs_none() -> None:
    request = PreparedRequest(url="https://example.com", params={})
    assert request.params == {}


def test_prepared_request_params_is_none() -> None:
    request = PreparedRequest(url="https://example.com", params=None)
    assert request.params is None


def test_endpoint_defaults() -> None:
    endpoint = Endpoint(path="/example")
    expected = Endpoint(path="/example", method=RequestMethod.GET, required_query_params=frozenset(), body_model=None)
    assert endpoint == expected


def test_endpoint_overrides() -> None:
    class ExampleModel(BaseModel):
        pass

    endpoint = Endpoint(
        path="/example",
        method=RequestMethod.POST,
        required_query_params=frozenset({"foo"}),
        body_model=ExampleModel,
    )
    assert endpoint.path == "/example"
    assert endpoint.required_query_params == frozenset({"foo"})
    assert endpoint.body_model == ExampleModel


def test_endpoint_build_url() -> None:
    endpoint = Endpoint(path="/example", required_query_params=frozenset({"a"}))
    url = endpoint.build_url("https://example.com", query={"a": 1}, path_params={})
    assert url == "https://example.com/example"


def test_endpoint_build_url_path_params() -> None:
    endpoint = Endpoint(path="/example/{key}")
    url = endpoint.build_url("https://example.com", query={}, path_params={"key": 1})
    assert url == "https://example.com/example/1"


def test_endpoint_build_url_missing_or_unexpected_params() -> None:
    endpoint = Endpoint(path="/example", required_query_params=frozenset({"a"}))
    with pytest.raises(ValueError, match="Missing query params"):
        endpoint.build_url("https://example.com", query={"b": 1}, path_params={})

    with pytest.raises(ValueError, match="Unexpected query params"):
        endpoint.build_url("https://example.com", query={"a": 1, "b": 1}, path_params={})


def test_endpoint_build_url_missing_or_unexpected_path_params() -> None:
    endpoint = Endpoint(path="/example/{key}")
    with pytest.raises(ValueError, match="Missing path params"):
        endpoint.build_url("https://example.com", query={}, path_params={})

    with pytest.raises(ValueError, match="Unexpected path params"):
        endpoint.build_url("https://example.com", query={}, path_params={"key": 1, "unexpected": 2})


def test_endpoint_build_encoded_url() -> None:
    endpoint = Endpoint(path="/path/{key}", required_query_params=frozenset({"q"}))
    url = endpoint.build_encoded_url("https://example.com", query={"q": 1}, path_params={"key": "search"})
    assert url == "https://example.com/path/search?q=1"


def test_endpoint_build_encoded_url_exists() -> None:
    endpoint = Endpoint(path="/path/", required_query_params=frozenset())
    url = endpoint.build_encoded_url("https://example.com", query={}, path_params={})
    assert url is not None


def test_endpoint_build_encoded_url_missing_or_unexpected_params() -> None:
    endpoint = Endpoint(path="/example", required_query_params=frozenset({"a"}))
    with pytest.raises(ValueError, match="Missing query params"):
        endpoint.build_encoded_url("https://example.com", query={}, path_params={})

    with pytest.raises(ValueError, match="Unexpected query params"):
        endpoint.build_encoded_url("https://example.com", query={"a": 1, "b": 2})


def test_endpoint_build_encoded_url_missing_or_unexpected_path_params() -> None:
    endpoint = Endpoint(path="/example/{key}")
    with pytest.raises(ValueError, match="Missing path params"):
        endpoint.build_encoded_url("https://example.com", query={}, path_params={})

    with pytest.raises(ValueError, match="Unexpected path params"):
        endpoint.build_encoded_url("https://example.com", query={}, path_params={"key": 1, "unexpected": 2})


def test_endpoint_build_request() -> None:
    endpoint = Endpoint(path="/example")
    request = endpoint.build_request("https://example.com")
    expected = PreparedRequest(url="https://example.com/example", params={}, body=None)
    assert request == expected


def test_endpoint_build_request_overrides() -> None:
    endpoint = Endpoint(path="/path/{key}", required_query_params=frozenset({"q"}))
    request = endpoint.build_request("https://example.com", query={"q": 1}, path_params={"key": "search"})
    expected = PreparedRequest(url="https://example.com/path/search", params={"q": 1}, body=None)
    assert request == expected


def test_endpoint_build_request_missing_params() -> None:
    endpoint = Endpoint(path="/example", required_query_params=frozenset({"q"}))
    with pytest.raises(ValueError, match="Missing query params"):
        endpoint.build_request("https://example.com", query={}, path_params={})


def test_endpoint_build_request_unexpected_params() -> None:
    endpoint = Endpoint(path="/example", required_query_params=frozenset({"q"}))
    with pytest.raises(ValueError, match="Unexpected query params"):
        endpoint.build_request("https://example.com", query={"q": 1, "_unexpected_": True}, path_params={})


def test_endpoint_build_request_missing_path_params() -> None:
    endpoint = Endpoint(path="/example/{key}")
    with pytest.raises(ValueError, match="Missing path params"):
        endpoint.build_request("https://example.com", query={}, path_params={})


def test_endpoint_build_request_unexpected_path_params() -> None:
    endpoint = Endpoint(path="/example/{key}")
    with pytest.raises(ValueError, match="Unexpected path params"):
        endpoint.build_request("https://example.com", query={}, path_params={"key": 1, "unexpected": 2})


def test_endpoint_validate_query() -> None:
    endpoint = Endpoint(path="/example")
    assert endpoint.validate_query(query={}) is None


def test_endpoint_validate_query_missing_query_params() -> None:
    endpoint = Endpoint(path="/example", required_query_params=frozenset({"a"}))
    with pytest.raises(ValueError, match="Missing query params"):
        endpoint.validate_query(query={})


def test_endpoint_validate_query_unexpected_query_params() -> None:
    endpoint = Endpoint(path="/example", required_query_params=frozenset({"a"}))
    with pytest.raises(ValueError, match="Unexpected query params"):
        endpoint.validate_query(query={"a": 1, "b": 1})


def test_endpoint_validate_path_params_missing() -> None:
    endpoint = Endpoint(path="/example/{key}")
    with pytest.raises(ValueError, match="Missing path params"):
        endpoint.validate_path_params(path_params={})


def test_endpoint_validate_path_params_unexpected() -> None:
    endpoint = Endpoint(path="/example/{key}")
    with pytest.raises(ValueError, match="Unexpected path params"):
        endpoint.validate_path_params(path_params={"key": 1, "b": 1})


def test_endpoint_required_path_params() -> None:
    endpoint = Endpoint(path="/example/{key}/{value}/{id}")
    assert endpoint.required_path_params == {"id", "key", "value"}
