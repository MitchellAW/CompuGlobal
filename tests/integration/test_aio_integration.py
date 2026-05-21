"""Test all API endpoints using aio module with live external APIs (no mocking)."""

import asyncio
from collections.abc import AsyncGenerator

import aiohttp
import pytest
import pytest_asyncio

from compuglobal.aio import AsyncCompuGlobalAPI, CapitalBeatUs, Frinkiac, Morbotron
from compuglobal.models.episode import Episode, EpisodeSummary
from compuglobal.models.frame import Frame, FrameResult
from compuglobal.models.screencap import Screencap, ScreencapMoment
from compuglobal.models.subtitle import Subtitle

API_CLASSES = [Frinkiac, Morbotron, CapitalBeatUs]
_screencap_cache: dict[str, Screencap] = {}


# Sleep between all tests to avoid flooding API
@pytest_asyncio.fixture(autouse=True)
async def wait_between_calls() -> None:
    await asyncio.sleep(1)


@pytest_asyncio.fixture(params=API_CLASSES, ids=lambda cls: cls.__name__)
async def api(request: pytest.FixtureRequest) -> AsyncGenerator[AsyncCompuGlobalAPI]:
    api_class = request.param
    async with aiohttp.ClientSession() as session:
        yield api_class(session=session)


@pytest_asyncio.fixture
async def random_screencap(api: AsyncCompuGlobalAPI) -> Screencap:
    class_name = type(api).__name__
    if class_name not in _screencap_cache:
        random_screencap = await api.get_random_screencap()
        _screencap_cache[class_name] = random_screencap

    return _screencap_cache[class_name]


@pytest_asyncio.fixture
async def random_customised_screencap(api: AsyncCompuGlobalAPI) -> Screencap:
    class_name = type(api).__name__
    if class_name not in _screencap_cache:
        random_screencap = await api.get_random_screencap()
        _screencap_cache[class_name] = random_screencap

    screencap = _screencap_cache[class_name]
    subtitles = [
        subtitle.model_copy(update={"content": f"Line {i + 1}: {subtitle.content}"})
        for i, subtitle in enumerate(screencap.subtitles)
    ]
    return screencap.model_copy(update={"subtitles": subtitles})


@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_get_random_screencap(api: AsyncCompuGlobalAPI) -> None:
    random_screencap = await api.get_random_screencap()
    assert isinstance(random_screencap, Screencap)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_get_screencap_episode_timestamp(api: AsyncCompuGlobalAPI, random_screencap: Screencap) -> None:
    screencap = await api.get_screencap(episode=random_screencap.frame.key, timestamp=random_screencap.frame.timestamp)
    assert random_screencap == screencap


@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_get_screencap_frame(api: AsyncCompuGlobalAPI, random_screencap: Screencap) -> None:
    screencap = await api.get_screencap(frame=random_screencap.frame)
    assert random_screencap == screencap


@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_search(api: AsyncCompuGlobalAPI) -> None:
    results = await api.search("test")
    assert len(results) > 0
    for result in results:
        assert isinstance(result, FrameResult)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_search_for_screencap(api: AsyncCompuGlobalAPI) -> None:
    result = await api.search_for_screencap("test")
    assert isinstance(result, Screencap)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_browse_episode(api: AsyncCompuGlobalAPI) -> None:
    episode = await api.browse_episode("S01E01")
    assert isinstance(episode, Episode)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_get_transcript(api: AsyncCompuGlobalAPI, random_screencap: Screencap) -> None:
    transcript = await api.get_transcript(
        episode=random_screencap.frame.key,
        timestamp=random_screencap.frame.timestamp,
    )
    assert len(transcript) > 0
    for caption in transcript:
        assert isinstance(caption, Subtitle)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_discover(api: AsyncCompuGlobalAPI) -> None:
    moments = await api.discover()
    assert len(moments) > 0
    for moment in moments:
        assert isinstance(moment, ScreencapMoment)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_navigator(api: AsyncCompuGlobalAPI) -> None:
    summaries = await api.navigator()
    assert len(summaries) > 0
    for summary in summaries:
        assert isinstance(summary, EpisodeSummary)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_get_frames(api: AsyncCompuGlobalAPI, random_screencap: Screencap) -> None:
    frames = await api.get_frames(
        key=random_screencap.frame.key,
        timestamp=random_screencap.frame.timestamp,
        before=0,
        after=99999999,
    )
    assert len(frames) > 0
    for frame in frames:
        assert isinstance(frame, Frame)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_get_image_url(api: AsyncCompuGlobalAPI, random_screencap: Screencap) -> None:
    image_url = await api.get_image_url(random_screencap)
    assert image_url.endswith(".jpg")
    async with api.client.session.head(image_url, allow_redirects=True) as response:
        assert response.status == 200
        content_type = response.headers.get("Content-Type", "")
        assert "image/jpeg" in content_type


@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_get_comic_panel_url(api: AsyncCompuGlobalAPI, random_screencap: Screencap) -> None:
    comic_panel_url = await api.get_comic_panel_url(random_screencap)
    assert "comic" in comic_panel_url
    assert "layout" not in comic_panel_url
    async with api.client.session.head(comic_panel_url, allow_redirects=True) as response:
        assert response.status == 200
        content_type = response.headers.get("Content-Type", "")
        assert "image/jpeg" in content_type


@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_get_comic_panel_url_custom_subtitles(
    api: AsyncCompuGlobalAPI,
    random_customised_screencap: Screencap,
) -> None:
    comic_panel_url = await api.get_comic_panel_url(random_customised_screencap)
    assert "comic" in comic_panel_url
    assert "layout" not in comic_panel_url
    async with api.client.session.head(comic_panel_url, allow_redirects=True) as response:
        assert response.status == 200
        content_type = response.headers.get("Content-Type", "")
        assert "image/jpeg" in content_type


@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_get_comic_strip_url(api: AsyncCompuGlobalAPI, random_screencap: Screencap) -> None:
    comic_strip_url = await api.get_comic_strip_url(random_screencap)
    assert "comic" in comic_strip_url
    assert "layout" in comic_strip_url
    async with api.client.session.head(comic_strip_url, allow_redirects=True) as response:
        assert response.status == 200
        content_type = response.headers.get("Content-Type", "")
        assert "image/jpeg" in content_type


@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_get_comic_strip_url_custom_subtitles(
    api: AsyncCompuGlobalAPI,
    random_customised_screencap: Screencap,
) -> None:
    comic_strip_url = await api.get_comic_strip_url(random_customised_screencap)
    assert "comic" in comic_strip_url
    assert "layout" in comic_strip_url
    async with api.client.session.head(comic_strip_url, allow_redirects=True) as response:
        assert response.status == 200
        content_type = response.headers.get("Content-Type", "")
        assert "image/jpeg" in content_type


@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_get_gif_url(api: AsyncCompuGlobalAPI, random_screencap: Screencap) -> None:
    gif_url = await api.get_gif_url(random_screencap)
    assert "gif" in gif_url
    async with api.client.session.head(gif_url, allow_redirects=True) as response:
        assert response.status == 200
        content_type = response.headers.get("Content-Type", "")
        assert "image/gif" in content_type


@pytest.mark.asyncio
@pytest.mark.integration
async def test_api_get_gif_url_custom_subtitles(
    api: AsyncCompuGlobalAPI,
    random_customised_screencap: Screencap,
) -> None:
    gif_url = await api.get_gif_url(random_customised_screencap)
    assert "gif" in gif_url
    async with api.client.session.head(gif_url, allow_redirects=True) as response:
        assert response.status == 200
        content_type = response.headers.get("Content-Type", "")
        assert "image/gif" in content_type
