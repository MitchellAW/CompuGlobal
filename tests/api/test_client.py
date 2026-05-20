"""Test API client module used for all API requests."""

import aiohttp
import pytest
from aiointercept import aiointercept

from compuglobal import APIPageStatusError
from compuglobal.api.client import CompuGlobalAPIClient
from compuglobal.api.endpoint import PreparedRequest, RequestMethod


@pytest.mark.asyncio
async def test_compuglobal_api_defaults() -> None:
    async with aiohttp.ClientSession() as session:
        client = CompuGlobalAPIClient(base_url="https://example.com", session=session)
        assert client.base_url == "https://example.com"
        assert client.session == session


@pytest.mark.asyncio
async def test_compuglobal_api_client_get(mock_http: aiointercept) -> None:
    async with aiohttp.ClientSession() as session:
        url = "https://example.com/test"
        mock_http.get(url, payload={"ok": True})

        client = CompuGlobalAPIClient(base_url="https://example.com", session=session)
        resp = await client.get(url)
        assert resp == {"ok": True}


@pytest.mark.asyncio
async def test_compuglobal_api_client_get_error(mock_http: aiointercept) -> None:
    async with aiohttp.ClientSession() as session:
        url = "https://example.com/test"
        mock_http.get(url, status=400)

        client = CompuGlobalAPIClient(base_url="https://example.com", session=session)
        with pytest.raises(APIPageStatusError, match="Error 400"):
            await client.get(url)


@pytest.mark.asyncio
async def test_compuglobal_api_client_post(mock_http: aiointercept) -> None:
    async with aiohttp.ClientSession() as session:
        url = "https://example.com/test"
        mock_http.post(url, payload={"ok": True})

        client = CompuGlobalAPIClient(base_url="https://example.com", session=session)
        resp = await client.post_data(url=url, json={})
        assert resp == '{"ok": true}'


@pytest.mark.asyncio
async def test_compuglobal_api_client_post_error(mock_http: aiointercept) -> None:
    async with aiohttp.ClientSession() as session:
        url = "https://example.com/test"
        mock_http.post(url, status=500)

        client = CompuGlobalAPIClient(base_url="https://example.com", session=session)
        with pytest.raises(APIPageStatusError, match="Error 500"):
            await client.post_data(url=url, json={})


@pytest.mark.asyncio
async def test_compuglobal_api_client_handle_request_get(mock_http: aiointercept) -> None:
    async with aiohttp.ClientSession() as session:
        url = "https://example.com/test"
        mock_http.get(url, payload={"ok": True})

        client = CompuGlobalAPIClient(base_url="https://example.com", session=session)

        request = PreparedRequest(url=url, method=RequestMethod.GET)
        resp = await client.handle_request(request)
        assert resp == {"ok": True}


@pytest.mark.asyncio
async def test_compuglobal_api_client_handle_request_post(mock_http: aiointercept) -> None:
    async with aiohttp.ClientSession() as session:
        url = "https://example.com/test"
        mock_http.post(url, payload={"ok": True})

        client = CompuGlobalAPIClient(base_url="https://example.com", session=session)
        request = PreparedRequest(url=url, method=RequestMethod.POST)
        resp = await client.handle_request(request)
        assert resp == '{"ok": true}'
