"""Test AIO module used for all API endpoint requests."""

import random
from collections.abc import AsyncGenerator
from typing import Any

import aiohttp
import pytest
import pytest_asyncio
from aiointercept import aiointercept
from inline_snapshot import snapshot

from compuglobal.aio import AsyncCompuGlobalAPI
from compuglobal.api.config import CompuGlobalAPIConfig
from compuglobal.errors import NoSearchResultsFoundError
from compuglobal.models.font import FontFamily
from compuglobal.models.overlay import OverlayFormat
from compuglobal.models.screencap import Screencap, ScreencapMoment
from compuglobal.models.stream import Stream


class CustomCompuGlobalAPI(AsyncCompuGlobalAPI):
    """A test API wrapper."""

    BASE_URL = "https://example.com"
    TITLE = "Testing"


class _InvalidRequestJSONError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to validate request json.")


@pytest_asyncio.fixture
async def api() -> AsyncGenerator[CustomCompuGlobalAPI]:
    async with aiohttp.ClientSession() as session:
        yield CustomCompuGlobalAPI(session=session, default_format=OverlayFormat(font_family=FontFamily.JOST))


@pytest.fixture
def screencap_moment() -> ScreencapMoment:
    return ScreencapMoment(
        episode="S01E02",
        timestamp=872288,
        content="what do you say we go out for a round of frosty chocolate milkshakes?",
        title="Bart the Genius",
    )


def random_frame_results(quantity: int) -> list[dict[str, Any]]:
    return [
        {
            "Id": random.randint(1000000, 9999999),
            "Episode": f"S{random.randint(1, 20):0>2}E{random.randint(1, 20):0>2}",
            "Timestamp": random.randint(1000, 1200000),
            "Content": "Blah blah blah",
            "Title": "Random",
            "VideoWidth": 480,
            "VideoHeight": 360,
        }
        for _ in range(quantity)
    ]


@pytest.mark.asyncio
async def test_api_defaults() -> None:
    async with aiohttp.ClientSession() as session:
        api = CustomCompuGlobalAPI(session=session, default_format=OverlayFormat(font_family=FontFamily.JOST))
        assert api.config == CompuGlobalAPIConfig(
            title="Testing",
            allowed_fonts=FontFamily.universal_fonts(),
            default_format=OverlayFormat(font_family=FontFamily.JOST),
        )
        assert api.client.base_url == "https://example.com"


@pytest.mark.asyncio
async def test_api_get_screencap_episode_timestamp(
    api: CustomCompuGlobalAPI,
    mock_http: aiointercept,
    screencap: Screencap,
) -> None:
    params = {"e": "S11E10", "t": 350725, "nearby": 1}
    url = api.discovery.CAPTION.build_encoded_url(api.BASE_URL, query=params)
    mock_http.get(url, payload=screencap.model_dump())
    result = await api.get_screencap(episode="S11E10", timestamp=350725)
    assert result.model_dump() == screencap.model_dump()


@pytest.mark.asyncio
async def test_api_get_screencap_no_timestamp(api: CustomCompuGlobalAPI) -> None:
    with pytest.raises(TypeError):
        # pyrefly: ignore [missing-argument, unexpected-keyword]
        await api.get_screencap(episode="S01E01")


@pytest.mark.asyncio
async def test_api_get_screencap_no_episode(api: CustomCompuGlobalAPI) -> None:
    with pytest.raises(TypeError):
        # pyrefly: ignore [missing-argument, unexpected-keyword]
        await api.get_screencap(timestamp=1000)


@pytest.mark.asyncio
async def test_api_search(api: CustomCompuGlobalAPI, mock_http: aiointercept) -> None:
    url = api.discovery.SEARCH.build_encoded_url(api.BASE_URL, query={"q": "test"})
    expected_results = random_frame_results(3)
    mock_http.get(url, payload=expected_results)

    results = await api.search("test")
    for result, expected in zip(results, expected_results, strict=True):
        assert result.model_dump() == expected


@pytest.mark.asyncio
async def test_api_search_no_results_error(api: CustomCompuGlobalAPI, mock_http: aiointercept) -> None:
    url = api.discovery.SEARCH.build_encoded_url(api.BASE_URL, query={"q": "test"})

    mock_http.get(url, payload=[])

    with pytest.raises(NoSearchResultsFoundError):
        await api.search("test")


@pytest.mark.asyncio
async def test_api_search_for_screencap(
    api: CustomCompuGlobalAPI,
    mock_http: aiointercept,
    screencap: Screencap,
) -> None:
    expected_results = [
        {
            "Id": 4555337,
            "Episode": "S11E10",
            "Timestamp": 350725,
            "Content": 'Nothing at all-- Nothing at all!"',
            "Title": "Little Big Mom",
        },
        *random_frame_results(5),
    ]
    # First mock (search)
    url = api.discovery.SEARCH.build_encoded_url(api.BASE_URL, query={"q": "example"})
    mock_http.get(url, payload=expected_results)

    # Second mock (captions endpoint)
    params = {"e": "S11E10", "t": 350725, "nearby": 1}
    url = api.discovery.CAPTION.build_encoded_url(api.BASE_URL, query=params)
    mock_http.get(url, payload=screencap.model_dump())

    result = await api.search_for_screencap("example")
    assert result == screencap


@pytest.mark.asyncio
async def test_api_search_for_screencap_no_results_error(
    api: CustomCompuGlobalAPI,
    mock_http: aiointercept,
) -> None:
    # First mock (search)
    url = api.discovery.SEARCH.build_encoded_url(api.BASE_URL, query={"q": "example"})
    mock_http.get(url, payload=[])
    with pytest.raises(NoSearchResultsFoundError):
        await api.search_for_screencap("example")


@pytest.mark.asyncio
async def test_api_get_random_screencap(
    api: CustomCompuGlobalAPI,
    mock_http: aiointercept,
    screencap: Screencap,
) -> None:
    url = api.discovery.RANDOM.build_encoded_url(api.BASE_URL, query={}, path_params={})
    mock_http.get(url, payload=screencap.model_dump())
    random = await api.get_random_screencap()
    assert random == screencap


@pytest.mark.asyncio
async def test_api_browse_episode(
    api: CustomCompuGlobalAPI,
    mock_http: aiointercept,
    episode_json: dict[str, Any],
) -> None:
    path_params = {"key": "S11E10", "start_timestamp": 0, "end_timestamp": 99999999}
    url = api.metadata.EPISODE.build_encoded_url(api.BASE_URL, path_params=path_params)
    mock_http.get(url, payload=episode_json)

    episode = await api.browse_episode("S11E10")
    assert episode.model_dump() == episode_json


@pytest.mark.asyncio
async def test_api_get_transcript(
    api: CustomCompuGlobalAPI,
    mock_http: aiointercept,
    subtitle_json: dict[str, Any],
) -> None:
    params = {"e": "S11E10", "t": 353228}
    url = api.metadata.TRANSCRIPT.build_encoded_url(api.BASE_URL, query=params)

    mock_http.get(url, payload=[subtitle_json])

    transcript = await api.get_transcript("S11E10", 353228)
    assert transcript[0].model_dump() == subtitle_json


@pytest.mark.asyncio
async def test_api_discover(
    api: CustomCompuGlobalAPI,
    mock_http: aiointercept,
    screencap_moment: ScreencapMoment,
) -> None:
    moments = [screencap_moment.model_dump() for _ in range(5)]
    url = api.discovery.DISCOVER.build_encoded_url(api.BASE_URL)
    mock_http.get(url, payload=moments)
    results = await api.discover()
    for result in results:
        assert result == screencap_moment


@pytest.mark.asyncio
async def test_api_navigator(
    api: CustomCompuGlobalAPI,
    mock_http: aiointercept,
    episode_summary_json: dict[str, Any],
) -> None:
    summaries = [episode_summary_json for _ in range(5)]
    url = api.discovery.NAVIGATOR.build_encoded_url(api.BASE_URL)

    mock_http.get(url, payload=summaries)

    results = await api.navigator()
    assert len(results) == 5
    for result in results:
        assert result.model_dump() == episode_summary_json


@pytest.mark.asyncio
async def test_api_get_frames(
    api: CustomCompuGlobalAPI,
    mock_http: aiointercept,
    frame_json: dict[str, Any],
) -> None:
    frames = [frame_json for _ in range(5)]
    path_params = {"key": "S11E10", "timestamp": 350725, "before": 0, "after": 0}
    url = api.discovery.FRAMES.build_encoded_url(api.BASE_URL, path_params=path_params)

    mock_http.get(url, payload=frames)
    results = await api.get_frames(key="S11E10", timestamp=350725, before=0, after=0)
    assert len(results) == 5
    for result in results:
        assert result.model_dump() == frame_json


@pytest.mark.asyncio
async def test_api_get_image_url(api: CustomCompuGlobalAPI, screencap: Screencap) -> None:
    image_url = await api.get_image_url(screencap)
    assert image_url == "https://example.com/img/S11E10/350725.jpg"


@pytest.mark.asyncio
async def test_api_get_comic_panel_url(api: CustomCompuGlobalAPI, screencap: Screencap) -> None:
    comic_panel_url = await api.get_comic_panel_url(screencap)
    assert comic_panel_url == snapshot(
        "https://example.com/comic/img?b64=W3siZSI6IlMxMUUxMCIsInRzIjozNTA3MjUsIm8iOlt7InQiOiJGZWVscyBsaWtlIEknbSB3ZWFyaW5nIG5vdGhpbmcgYXQgYWxsLS0gTm90aGluZyBhdCBhbGwtLSBOb3RoaW5nIGF0IGFsbCFcIiBTdHVwaWQsIHNleHkgRmxhbmRlcnMhIiwiZiI6Impvc3QiLCJzIjowLCJjIjoiZmZmZmZmZmYiLCJ4Ijo1MCwieSI6OTcsImEiOiJjIiwidSI6MSwiYiI6MCwiZCI6MH1dfV0%3D",
    )


@pytest.mark.asyncio
async def test_api_get_comic_panel_url_custom_subtitles(
    api: CustomCompuGlobalAPI,
    screencap: Screencap,
) -> None:
    subtitles = [screencap.subtitles[1]]
    comic_panel_url = await api.get_comic_panel_url(screencap, subtitles=subtitles)
    assert comic_panel_url == snapshot(
        "https://example.com/comic/img?b64=W3siZSI6IlMxMUUxMCIsInRzIjozNTA3MjUsIm8iOlt7InQiOiJOb3RoaW5nIGF0IGFsbC0tIE5"
        "vdGhpbmcgYXQgYWxsIVwiIiwiZiI6Impvc3QiLCJzIjowLCJjIjoiZmZmZmZmZmYiLCJ4Ijo1MCwieSI6OTcsImEiOiJjIiwidSI6MSwiYiI6"
        "MCwiZCI6MH1dfV0%3D",
    )


@pytest.mark.asyncio
async def test_api_get_comic_strip_url(api: CustomCompuGlobalAPI, screencap: Screencap) -> None:
    comic_strip_url = await api.get_comic_strip_url(screencap)
    assert comic_strip_url == snapshot(
        "https://example.com/comic/img?b64=W3siZSI6IlMxMUUxMCIsInRzIjozNDgwMTQsIm8iOlt7InQiOiJGZWVscyBsaWtlIEknbSB3ZWFyaW5nIG5vdGhpbmcgYXQgYWxsLS0iLCJmIjoiam9zdCIsInMiOjAsImMiOiJmZmZmZmZmZiIsIngiOjUwLCJ5Ijo5NywiYSI6ImMiLCJ1IjoxLCJiIjowLCJkIjowfV19LHsiZSI6IlMxMUUxMCIsInRzIjozNTA1MTcsIm8iOlt7InQiOiJOb3RoaW5nIGF0IGFsbC0tIE5vdGhpbmcgYXQgYWxsIVwiIiwiZiI6Impvc3QiLCJzIjowLCJjIjoiZmZmZmZmZmYiLCJ4Ijo1MCwieSI6OTcsImEiOiJjIiwidSI6MSwiYiI6MCwiZCI6MH1dfSx7ImUiOiJTMTFFMTAiLCJ0cyI6MzUzMjI4LCJvIjpbeyJ0IjoiU3R1cGlkLCBzZXh5IEZsYW5kZXJzISIsImYiOiJqb3N0IiwicyI6MCwiYyI6ImZmZmZmZmZmIiwieCI6NTAsInkiOjk3LCJhIjoiYyIsInUiOjEsImIiOjAsImQiOjB9XX1d&layout=1over2",
    )


@pytest.mark.asyncio
async def test_api_get_comic_strip_url_custom_subtitles(api: CustomCompuGlobalAPI, screencap: Screencap) -> None:
    subtitles = [subtitle.model_copy(update={"content": f"Test {i}"}) for i, subtitle in enumerate(screencap.subtitles)]
    comic_strip_url = await api.get_comic_strip_url(screencap, subtitles=subtitles)
    assert comic_strip_url == snapshot(
        "https://example.com/comic/img?b64=W3siZSI6IlMxMUUxMCIsInRzIjozNDgwMTQsIm8iOlt7InQiOiJUZXN0IDAiLCJmIjoiam9zdCIsInMiOjAsImMiOiJmZmZmZmZmZiIsIngiOjUwLCJ5Ijo5NywiYSI6ImMiLCJ1IjoxLCJiIjowLCJkIjowfV19LHsiZSI6IlMxMUUxMCIsInRzIjozNTA1MTcsIm8iOlt7InQiOiJUZXN0IDEiLCJmIjoiam9zdCIsInMiOjAsImMiOiJmZmZmZmZmZiIsIngiOjUwLCJ5Ijo5NywiYSI6ImMiLCJ1IjoxLCJiIjowLCJkIjowfV19LHsiZSI6IlMxMUUxMCIsInRzIjozNTMyMjgsIm8iOlt7InQiOiJUZXN0IDIiLCJmIjoiam9zdCIsInMiOjAsImMiOiJmZmZmZmZmZiIsIngiOjUwLCJ5Ijo5NywiYSI6ImMiLCJ1IjoxLCJiIjowLCJkIjowfV19XQ%3D%3D&layout=1over2",
    )


@pytest.mark.asyncio
async def test_api_get_comic_strip_url_custom_subtitles_truncated_subtitles(
    api: CustomCompuGlobalAPI,
    screencap: Screencap,
) -> None:
    subtitles = [subtitle.model_copy(update={"content": f"Test {i}"}) for i, subtitle in enumerate(screencap.subtitles)]
    subtitles += subtitles
    comic_strip_url = await api.get_comic_strip_url(screencap, subtitles=subtitles)
    assert comic_strip_url == snapshot(
        "https://example.com/comic/img?b64=W3siZSI6IlMxMUUxMCIsInRzIjozNDgwMTQsIm8iOlt7InQiOiJUZXN0IDAiLCJmIjoiam9zdCIsInMiOjAsImMiOiJmZmZmZmZmZiIsIngiOjUwLCJ5Ijo5NywiYSI6ImMiLCJ1IjoxLCJiIjowLCJkIjowfV19LHsiZSI6IlMxMUUxMCIsInRzIjozNTA1MTcsIm8iOlt7InQiOiJUZXN0IDEiLCJmIjoiam9zdCIsInMiOjAsImMiOiJmZmZmZmZmZiIsIngiOjUwLCJ5Ijo5NywiYSI6ImMiLCJ1IjoxLCJiIjowLCJkIjowfV19LHsiZSI6IlMxMUUxMCIsInRzIjozNTMyMjgsIm8iOlt7InQiOiJUZXN0IDIiLCJmIjoiam9zdCIsInMiOjAsImMiOiJmZmZmZmZmZiIsIngiOjUwLCJ5Ijo5NywiYSI6ImMiLCJ1IjoxLCJiIjowLCJkIjowfV19LHsiZSI6IlMxMUUxMCIsInRzIjozNDgwMTQsIm8iOlt7InQiOiJUZXN0IDAiLCJmIjoiam9zdCIsInMiOjAsImMiOiJmZmZmZmZmZiIsIngiOjUwLCJ5Ijo5NywiYSI6ImMiLCJ1IjoxLCJiIjowLCJkIjowfV19XQ%3D%3D&layout=2x2",
    )


@pytest.mark.asyncio
async def test_api_get_gif_url(api: CustomCompuGlobalAPI, mock_http: aiointercept, screencap: Screencap) -> None:
    url = api.media.RENDER_GIF.build_encoded_url(api.BASE_URL)
    stream = Stream.from_screencap(screencap=screencap, overlay_format=api.config.default_format)
    payload = {
        "url": "/video/S02E01/CoCGOx7cJdlKOKjrZoE7S5_mXqw=.gif",
    }

    mock_http.post(url, payload=payload, status=200)
    gif_url = await api.get_gif_url(screencap)

    mock_http.assert_called_once_with(url, method="POST", json=[stream.model_dump()])
    assert gif_url == snapshot("https://example.com/video/S02E01/CoCGOx7cJdlKOKjrZoE7S5_mXqw=.gif")


@pytest.mark.asyncio
async def test_api_get_gif_url_custom_subtitles(
    api: CustomCompuGlobalAPI,
    mock_http: aiointercept,
    screencap: Screencap,
) -> None:
    subtitles = [subtitle.model_copy(update={"content": f"Test {i}"}) for i, subtitle in enumerate(screencap.subtitles)]
    url = api.media.RENDER_GIF.build_encoded_url(api.BASE_URL)

    stream_screencap = screencap.model_copy(update={"subtitles": subtitles})
    stream = Stream.from_screencap(screencap=stream_screencap, overlay_format=api.config.default_format)

    payload = {
        "url": "/video/S02E01/CoCGOx7cJdlKOKjrZoE7S5_mXqw=.gif",
    }

    mock_http.post(url, payload=payload, status=200)
    gif_url = await api.get_gif_url(screencap, subtitles=subtitles)

    mock_http.assert_called_once_with(url, method="POST", json=[stream.model_dump()])
    assert gif_url == snapshot("https://example.com/video/S02E01/CoCGOx7cJdlKOKjrZoE7S5_mXqw=.gif")


@pytest.mark.asyncio
async def test_api_get_gif_url_fallback_comic(
    api: CustomCompuGlobalAPI,
    mock_http: aiointercept,
    screencap: Screencap,
) -> None:
    url = api.media.RENDER_GIF.build_encoded_url(api.BASE_URL)
    stream = Stream.from_screencap(screencap=screencap, overlay_format=api.config.default_format)
    payload = {
        "progress": 0.044500000000000005,
    }

    mock_http.post(url, payload=payload, status=200)
    gif_url = await api.get_gif_url(screencap)

    mock_http.assert_called_once_with(url, method="POST", json=[stream.model_dump()])
    assert gif_url == snapshot(
        "https://example.com/comic/img?b64=W3siZSI6IlMxMUUxMCIsInRzIjozNDgwMTQsIm8iOlt7InQiOiJGZWVscyBsaWtlIEknbSB3ZWFyaW5nIG5vdGhpbmcgYXQgYWxsLS0iLCJmIjoiam9zdCIsInMiOjAsImMiOiJmZmZmZmZmZiIsIngiOjUwLCJ5Ijo5NywiYSI6ImMiLCJ1IjoxLCJiIjowLCJkIjowfV19LHsiZSI6IlMxMUUxMCIsInRzIjozNTA1MTcsIm8iOlt7InQiOiJOb3RoaW5nIGF0IGFsbC0tIE5vdGhpbmcgYXQgYWxsIVwiIiwiZiI6Impvc3QiLCJzIjowLCJjIjoiZmZmZmZmZmYiLCJ4Ijo1MCwieSI6OTcsImEiOiJjIiwidSI6MSwiYiI6MCwiZCI6MH1dfSx7ImUiOiJTMTFFMTAiLCJ0cyI6MzUzMjI4LCJvIjpbeyJ0IjoiU3R1cGlkLCBzZXh5IEZsYW5kZXJzISIsImYiOiJqb3N0IiwicyI6MCwiYyI6ImZmZmZmZmZmIiwieCI6NTAsInkiOjk3LCJhIjoiYyIsInUiOjEsImIiOjAsImQiOjB9XX1d&layout=1over2",
    )


@pytest.mark.asyncio
async def test_api_get_gif_url_truncated_subtitles(
    api: CustomCompuGlobalAPI,
    mock_http: aiointercept,
    screencap: Screencap,
) -> None:
    subtitles = [subtitle.model_copy(update={"content": f"Test {i}"}) for i, subtitle in enumerate(screencap.subtitles)]
    subtitles += subtitles
    url = api.media.RENDER_GIF.build_encoded_url(api.BASE_URL)

    stream_screencap = screencap.model_copy(update={"subtitles": subtitles[:4]})
    stream = Stream.from_screencap(screencap=stream_screencap, overlay_format=api.config.default_format)

    payload = {
        "url": "/video/S02E01/CoCGOx7cJdlKOKjrZoE7S5_mXqw=.gif",
    }

    mock_http.post(url, payload=payload, status=200)

    gif_url = await api.get_gif_url(screencap, subtitles=subtitles)

    mock_http.assert_called_once_with(url, method="POST", json=[stream.model_dump()])
    assert gif_url == snapshot("https://example.com/video/S02E01/CoCGOx7cJdlKOKjrZoE7S5_mXqw=.gif")
