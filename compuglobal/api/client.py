"""Module for handling API requests to CGHMC APIs."""

import asyncio
import logging
from http import HTTPStatus
from typing import Any

from aiohttp import ClientSession

from compuglobal.api.endpoint import PreparedRequest, RequestMethod
from compuglobal.errors import APIPageStatusError, MaximumRetriesExceededError

log = logging.getLogger(__name__)


class CompuGlobalAPIClient:
    """Client for handling API requests to CompuGlobal APIs.

    Parameters
    ----------
    base_url : str
        The base URL of the API (e.g. https://frinkiac.com)
    session : ClientSession
        The client session to use for all API requests
    max_retries : int, optional
        The maximum number of retries for each request before raising an :class:`APIPageStatusError`

    """

    def __init__(self, base_url: str, session: ClientSession, max_retries: int = 0) -> None:
        self.base_url = base_url
        self.session = session
        self.max_retries = max_retries

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

            if response.status == HTTPStatus.TOO_MANY_REQUESTS:
                retry_after = int(response.headers.get("Retry-After", 60))
                raise APIPageStatusError(response.status, self.base_url, retry_after=retry_after)

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
            if response.status == HTTPStatus.TOO_MANY_REQUESTS:
                retry_after = int(response.headers.get("Retry-After", 60))
                raise APIPageStatusError(response.status, self.base_url, retry_after=retry_after)

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

        Raises
        ------
        APIPageStatusError
            Raised immediately for non-2xx responses that are not retryable (e.g. anything other than a 429).
        MaximumRetriesExceededError
            Raised when the maximum number of retries is exceeded.

        """
        for attempt in range(self.max_retries + 1):
            try:
                log.debug(
                    "%s %s | params=%s | body=%s",
                    request.method.value,
                    request.url,
                    request.params,
                    request.body,
                )
                if request.method == RequestMethod.POST:
                    return await self.post_data(request.url, json=request.body)

                return await self.get(request.url, params=request.params)

            except APIPageStatusError as error:
                if error.page_status != HTTPStatus.TOO_MANY_REQUESTS or attempt >= self.max_retries:
                    raise

                log.warning(
                    "Rate limited (429) | %s %s | retrying in %.2fs (attempt %d/%d)",
                    request.method.value,
                    request.url,
                    error.retry_after,
                    attempt + 1,
                    self.max_retries + 1,
                )

                if error.retry_after is not None:
                    # Add a buffer of 50-1000ms depending on retry amount
                    buffer = max(0.05, min(1, error.retry_after * 0.02))
                    await asyncio.sleep(error.retry_after + buffer)

        raise MaximumRetriesExceededError
