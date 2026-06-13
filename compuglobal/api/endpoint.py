"""Module of endpoint classes used for modelling an API endpoint."""

import logging
from dataclasses import dataclass
from enum import StrEnum
from functools import cached_property
from string import Formatter
from typing import Any
from urllib.parse import urlencode

from pydantic import BaseModel

log = logging.getLogger(__name__)


class RequestMethod(StrEnum):
    """An enum of HTTP request methods."""

    #: For GET requests
    GET = "GET"

    #: For POST requests
    POST = "POST"

    #: For PUT requests
    PUT = "PUT"


@dataclass
class PreparedRequest:
    """Defines request prepared for the given endpoint details.

    Attributes
    ----------
    url: str
        The url of the request
    method: RequestMethod, optional
        The HTTP RequestMethod for the request (GET/POST/PUT)
    params: dict[str, Any] | None, optional
        The query parameters to use in the request
    body: dict[str, Any] | list[Any] | None, optional
        The JSON request body to post

    """

    url: str
    method: RequestMethod = RequestMethod.GET
    params: dict[str, Any] | None = None
    body: dict[str, Any] | list[Any] | None = None


def _format_validation_error_message(message: str, values: set[str]) -> str:
    return f"{message}: {values}"


@dataclass(frozen=True)
class Endpoint:
    """Defines an endpoint of an API.

    Attributes
    ----------
    path : str
        The url path containing any path parameter names
    method : RequestMethod, optional
        The HTTP RequestMethod for the request (GET/POST/PUT)
    required_query_params : frozenset[str], optional
        The required query parameters to use in the request
    optional_query_params : frozenset[str], optional
        Optional query params that can be used in the request
    body_model : type[BaseModel] | None, optional
        The pydantic model for the json body

    """

    path: str
    method: RequestMethod = RequestMethod.GET
    required_query_params: frozenset[str] = frozenset()
    optional_query_params: frozenset[str] = frozenset()
    body_model: type[BaseModel] | None = None

    def build_url(
        self,
        base_url: str,
        query: dict[str, Any],
        path_params: dict[str, Any],
    ) -> str:
        """Build a url with the given base url, query params, and path params.

        Parameters
        ----------
        base_url : str
            The base url of the API
        query : dict[str, Any]
            The query params to use in the url
        path_params : dict[str, Any]
            The path params to use in the url

        Returns
        -------
        str
            The expected url to use

        """
        # Validate that query and path params match what is expected
        self.validate_query(query)
        self.validate_path_params(path_params)

        # Form url with path params
        return base_url + self.path.format(**path_params)

    def build_encoded_url(
        self,
        base_url: str,
        query: dict[str, Any] | None = None,
        path_params: dict[str, Any] | None = None,
    ) -> str:
        """Build an encoded url with the given base url, query params, and path params.

        Parameters
        ----------
        base_url : str
            The base url of the API
        query : dict[str, Any] | None, optional
            The query params to use in the url
        path_params : dict[str, Any] | None, optional
            The path params to use in the url

        Returns
        -------
        str
            The fully encoded expected url to use

        """
        query = query or {}
        path_params = path_params or {}
        url = self.build_url(base_url, query, path_params)

        if len(query.keys()) > 0:
            url = f"{url}?{urlencode(query, doseq=True)}"

        log.debug("Built encoded url %s | base_url=%s | query=%s | path_params=%s", url, base_url, query, path_params)
        return url

    def build_request(
        self,
        base_url: str,
        query: dict[str, Any] | None = None,
        path_params: dict[str, Any] | None = None,
        body: BaseModel | None = None,
    ) -> PreparedRequest:
        """Build a prepared request with the given base url, query params, path params, body model.

        Parameters
        ----------
        base_url : str
            The base url of the API
        query : dict[str, Any] | None, optional
            The query params to use in the params of the request
        path_params : dict[str, Any] | None, optional
            The path params to use in the path of the request
        body : BaseModel | None, optional
            The json body model to use in the request

        Returns
        -------
        PreparedRequest
            The request prepared using the given details

        """
        query = query or {}
        path_params = path_params or {}
        new_url = self.build_url(base_url, query, path_params)

        # Get body data
        body_data = body.model_dump() if body is not None else None

        log.debug(
            "Built %s request | path=%s | query=%s | path_params=%s | body=%s",
            self.method.value,
            self.path,
            query,
            path_params,
            body,
        )

        return PreparedRequest(url=new_url, method=self.method, params=query, body=body_data)

    def validate_query(self, query: dict[str, Any]) -> None:
        """Validate the query params against the expectation of the endpoint.

        Parameters
        ----------
        query : dict[str, Any]
            The query params to validate

        Raises
        ------
        ValueError
            Raises error if contains missing or unexpected params from the definition of the endpoint

        """
        missing = set(self.required_query_params - query.keys())
        unexpected = query.keys() - (self.required_query_params | self.optional_query_params)

        if missing:
            log.debug("Validation failed for %s | missing required params %s", self.path, missing)
            raise ValueError(
                _format_validation_error_message(message="Missing query params", values=missing),
            )
        if unexpected:
            log.debug("Validation failed for %s | unexpected params %s", self.path, unexpected)
            raise ValueError(
                _format_validation_error_message(message="Unexpected query params", values=unexpected),
            )

    def validate_path_params(self, path_params: dict[str, Any]) -> None:
        """Validate the path params against the expectation of the endpoint.

        Parameters
        ----------
        path_params : dict[str, Any]
            The path params to validate

        Raises
        ------
        ValueError
            Raises error if contains missing or unexpected path params from the definition of the endpoint

        """
        missing = self.required_path_params - path_params.keys()
        unexpected = path_params.keys() - self.required_path_params

        if missing:
            log.debug("Validation failed for %s | missing required path params %s", self.path, missing)
            raise ValueError(_format_validation_error_message(message="Missing path params", values=missing))

        if unexpected:
            log.debug("Validation failed for %s | unexpected path params %s", self.path, unexpected)
            raise ValueError(
                _format_validation_error_message(message="Unexpected path params", values=unexpected),
            )

    @cached_property
    def required_path_params(self) -> set[str]:
        """The path params required by the endpoint.

        Returns
        -------
        set[str]
            A set of strings representing each of the required path params

        """
        return {field_name for _, field_name, _, _ in Formatter().parse(self.path) if field_name is not None}
