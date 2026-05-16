from http import HTTPStatus
from typing import Any

from aiohttp import ClientSession, ClientTimeout

from compuglobal.api.endpoint import PreparedRequest, RequestMethod
from compuglobal.errors import APIPageStatusError


class CompuGlobalAPIClient:
    def __init__(
        self,
        base_url: str,
        session: ClientSession | None = None,
        timeout: int = 15,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout

        self.timeout = ClientTimeout(total=timeout)

        self._is_auto_session = session is None

        if session is None:
            self.session = ClientSession(timeout=self.timeout)

        else:
            self.session = session

    async def get(self, url: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        async with self.session.get(url, params=params) as response:
            if HTTPStatus.OK <= response.status < HTTPStatus.MULTIPLE_CHOICES:
                return await response.json()

            raise APIPageStatusError(response.status, self.base_url)

    async def post_data(self, url: str, json: dict[str, Any] | list[Any] | None) -> str:
        async with self.session.post(url, json=json) as response:
            if HTTPStatus.OK <= response.status < HTTPStatus.MULTIPLE_CHOICES:
                return await response.text()

            raise APIPageStatusError(response.status, self.base_url)

    async def handle_request(self, request: PreparedRequest) -> str | dict[str, Any] | list[Any]:
        if request.method == RequestMethod.POST:
            return await self.post_data(request.url, json=request.body)

        return await self.get(request.url, params=request.params)

    async def close(self) -> None:
        if self._is_auto_session:
            await self.session.close()
