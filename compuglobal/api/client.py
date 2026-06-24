"""Module for handling API requests to CGHMC APIs."""

import logging
from http import HTTPStatus
from typing import Any

from aiohttp import ClientSession

from compuglobal.api.endpoint import PreparedRequest, RequestMethod
from compuglobal.errors import APIPageStatusError

log = logging.getLogger(__name__)


class CompuGlobalAPIClient:
    """Client for handling API requests to CompuGlobal APIs.

    Parameters
    ----------
    base_url : str
        The base URL of the API (e.g. https://frinkiac.com)
    session : ClientSession
        The client session to use for all API requests

    """

    def __init__(self, base_url: str, session: ClientSession) -> None:
        self.base_url = base_url
        self.session = session

    async def get(self, url: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        """Get the JSON response from the API using the given url, and params.

        Parameters
        ----------
        url : str
            The url to use in the request
        params : dict[str, Any] | None, optional
            The query params to use in the request

        Returns
        -------
        dict[str, Any] | list[Any]
            A json response from the API

        Raises
        ------
        APIPageStatusError
            Raises an error if a non 2xx HTTP status code is received from the API

        """
        async with self.session.get(url, params=params) as response:
            if HTTPStatus.OK <= response.status < HTTPStatus.MULTIPLE_CHOICES:
                log.debug("Response %s | GET %s", response.status, url)
                return await response.json()

            log.error("Non-2xx response %s | POST %s | Headers %s", response.status, url, response.headers)
            raise APIPageStatusError(response.status, self.base_url)

    async def post_data(self, url: str, json: dict[str, Any] | list[Any] | None) -> str:
        """Post some json data to the given API url.

        Parameters
        ----------
        url : str
            The url to use in the request
        json : dict[str, Any] | list[Any] | None
            The body of the json request to post

        Returns
        -------
        str
            The api response as text

        Raises
        ------
        APIPageStatusError
            Raises an error if a non 2xx HTTP status code is received from the API

        """
        async with self.session.post(url, json=json) as response:
            if HTTPStatus.OK <= response.status < HTTPStatus.MULTIPLE_CHOICES:
                log.debug("Response %s | POST %s", response.status, url)
                return await response.text()

            log.error("Non-2xx response %s | POST %s | Headers %s", response.status, url, response.headers)
            raise APIPageStatusError(response.status, self.base_url)

    async def handle_request(self, request: PreparedRequest) -> str | dict[str, Any] | list[Any]:
        """Handle given prepared request with appropriate method (GET/POST).

        Parameters
        ----------
        request : PreparedRequest
            The request to perform

        Returns
        -------
        str | dict[str, Any] | list[Any]
            The json response from the API

        """
        log.debug("%s %s | params=%s | body=%s", request.method.value, request.url, request.params, request.body)
        if request.method == RequestMethod.POST:
            return await self.post_data(request.url, json=request.body)

        return await self.get(request.url, params=request.params)
