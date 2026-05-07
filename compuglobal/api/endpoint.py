from dataclasses import dataclass
from enum import StrEnum
from functools import cached_property
from string import Formatter
from typing import Any, FrozenSet, Type
from urllib.parse import urlencode

from pydantic import BaseModel


class RequestMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"


@dataclass
class PreparedRequest:
    url: str
    method: RequestMethod = RequestMethod.GET
    params: dict[str, Any] | None = None
    body: dict[str, Any] | list[Any] | None = None
    is_async: bool = True


@dataclass(frozen=True)
class Endpoint:
    path: str
    method: RequestMethod = RequestMethod.GET
    query_params: FrozenSet[str] = frozenset()
    body_model: Type[BaseModel] | None = None
    is_async: bool = True

    def build_url(
        self,
        base_url: str,
        query: dict[str, Any],
        path_params: dict[str, Any],
    ):
        # Validate that query and path params match what is expected
        self.validate_query(query)
        self.validate_path_params(path_params)

        # Form url with path params
        new_url = base_url + self.path.format(**path_params)
        return new_url

    def build_encoded_url(
        self,
        base_url: str,
        query: dict[str, Any] | None = None,
        path_params: dict[str, Any] | None = None,
    ):
        query = query or {}
        path_params = path_params or {}
        url = self.build_url(base_url, query, path_params)

        if len(query.keys()) > 0:
            return f"{url}?{urlencode(query, doseq=True)}"

        else:
            return url

    def build_request(
        self,
        base_url: str,
        query: dict[str, Any] | None = None,
        path_params: dict[str, Any] | None = None,
        body: BaseModel | None = None,
    ):
        query = query or {}
        path_params = path_params or {}
        new_url = self.build_url(base_url, query, path_params)

        # Get body data
        body_data = body.model_dump(by_alias=True) if body is not None else None

        return PreparedRequest(url=new_url, method=self.method, params=query, body=body_data)

    def validate_query(self, query: dict[str, Any]):
        missing = self.query_params - query.keys()
        unexpected = query.keys() - self.query_params

        if missing:
            raise ValueError(f"Missing the following query params: {missing}")
        if unexpected:
            raise ValueError(f"Unexpected query params: {unexpected}")

    def validate_path_params(self, path_params: dict[str, Any]):
        missing = self.required_path_params - path_params.keys()
        unexpected = path_params.keys() - self.required_path_params

        if missing:
            raise ValueError(f"Missing path params: {missing}")

        if unexpected:
            raise ValueError(f"Unexpected path params: {unexpected}")

    @cached_property
    def required_path_params(self) -> set[str]:
        return {field_name for _, field_name, _, _ in Formatter().parse(self.path) if field_name is not None}
