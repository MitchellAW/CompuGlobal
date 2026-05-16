"""Module for handling API requests to CGHMC APIs."""

from http import HTTPStatus
from typing import Any

from aiohttp import ClientSession, ClientTimeout

from compuglobal.api.endpoint import PreparedRequest, RequestMethod
from compuglobal.errors import APIPageStatusError


class CompuGlobalAPIClient:
    """Client for handling API requests to CompuGlobal APIs."""

    def __init__(
        self,
        base_url: str,
        session: ClientSession | None = None,
        timeout: int = 15,
    ) -> None:
        """Define an API client for interacting with CGHMC APIs.

        Parameters
        ----------
        base_url : str
            The base URL of the API (e.g. https://frinkiac.com)
        session : ClientSession | None, optional
            The client session to use for all API requests
        timeout : int, optional
            The number of seconds to wait before raising a timeout error for each API request

        """
        self.base_url = base_url
        self.timeout = timeout

        self.timeout = ClientTimeout(total=timeout)

        self._is_auto_session = session is None

        if session is None:
            self.session = ClientSession(timeout=self.timeout)

        else:
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
                return await response.json()

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
                return await response.text()

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
        if request.method == RequestMethod.POST:
            return await self.post_data(request.url, json=request.body)

        return await self.get(request.url, params=request.params)

    async def close(self) -> None:
        """Close the http client session."""
        if self._is_auto_session:
            await self.session.close()
