from http import HTTPStatus

from aiohttp import ClientSession, ClientTimeout

from ..errors import APIPageStatusError
from .endpoint import PreparedRequest, RequestMethod


class CompuGlobalAPIClient:
    def __init__(
        self,
        base_url: str,
        session: ClientSession | None = None,
        timeout: int = 15,
    ):
        self.base_url = base_url
        self.timeout = timeout

        self.timeout = ClientTimeout(total=timeout)

        self._is_auto_session = session is None

        if session is None:
            self.session = ClientSession(timeout=self.timeout)

        else:
            self.session = session

    async def get(self, url, params=None):
        async with self.session.get(url, params=params) as response:
            if HTTPStatus.OK <= response.status < HTTPStatus.MULTIPLE_CHOICES:
                return await response.json()

            else:
                raise APIPageStatusError(response.status, self.base_url)

    async def post_data(self, url, json=None):
        async with self.session.post(url, json=json) as response:
            if HTTPStatus.OK <= response.status < HTTPStatus.MULTIPLE_CHOICES:
                return await response.text()

            else:
                raise APIPageStatusError(response.status, self.base_url)

    async def handle_request(self, request: PreparedRequest):
        if request.method == RequestMethod.POST:
            return await self.post_data(request.url, json=request.body)

        return await self.get(request.url, params=request.params)

    async def close(self):
        if self._is_auto_session:
            await self.session.close()
