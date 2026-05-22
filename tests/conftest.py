"""Shared pytest fixtures."""

from collections.abc import AsyncGenerator
from typing import Any

import pytest
import pytest_asyncio
from aiointercept import aiointercept

from compuglobal.models.screencap import Screencap


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--open-report",
        action="store_true",
        default=False,
        help="Automatically open the media report in the browser after the test run.",
    )


@pytest_asyncio.fixture
async def mock_http() -> AsyncGenerator[aiointercept]:
    async with aiointercept(mock_external_urls=True) as m:
        yield m


def frame(frame_id: int, episode: str, timestamp: int) -> dict[str, Any]:
    return {
        "Id": frame_id,
        "Episode": episode,
        "Timestamp": timestamp,
    }


def subtitle(subtitle_id: int, content: str, representative: int, start: int, end: int) -> dict[str, Any]:
    return {
        "Id": subtitle_id,
        "RepresentativeTimestamp": representative,
        "Episode": "S11E10",
        "StartTimestamp": start,
        "EndTimestamp": end,
        "Content": content,
        "Language": "en",
    }


def episode(season: int, episode: int) -> dict[str, Any]:
    return {
        "Id": 571,
        "Key": f"S{season}E{episode}",
        "Season": season,
        "EpisodeNumber": episode,
        "Title": "Little Big Mom",
        "Director": "Mark Kirkland",
        "Writer": "Carolyn Omine",
        "OriginalAirDate": "2000-01-09",
        "WikiLink": "https://en.wikipedia.org/wiki/Little_Big_Mom",
    }


@pytest.fixture
def episode_summary_json() -> dict[str, Any]:
    return {
        "Key": "S11E10",
        "Season": 11,
        "EpisodeNumber": 10,
        "Title": "Little Big Mom",
        "OriginalAirDate": "2000-01-09",
        "Frames": [
            65023,
            180347,
            240407,
            327577,
            413914,
            473348,
            545503,
            590548,
            642684,
            689814,
            740698,
            801384,
            857273,
            930680,
            981981,
            1038913,
            1090423,
            1139847,
            1177176,
            1246829,
        ],
    }


@pytest.fixture
def episode_json() -> dict[str, Any]:
    return {
        "Episode": {
            "Id": 571,
            "Key": "S11E10",
            "Season": 11,
            "EpisodeNumber": 10,
            "Title": "Little Big Mom",
            "Director": "Mark Kirkland",
            "Writer": "Carolyn Omine",
            "OriginalAirDate": "2000-01-09",
            "WikiLink": "https://en.wikipedia.org/wiki/Little_Big_Mom",
        },
        "Subtitles": [
            {
                "Id": 313546,
                "RepresentativeTimestamp": 4338,
                "Episode": "S11E10",
                "StartTimestamp": 3128,
                "EndTimestamp": 5797,
                "Content": "♪ The Simpsons ♪",
                "Language": "en",
            },
            {
                "Id": 313547,
                "RepresentativeTimestamp": 65023,
                "Episode": "S11E10",
                "StartTimestamp": 64314,
                "EndTimestamp": 66066,
                "Content": "D'oh!",
                "Language": "en",
            },
        ],
    }


@pytest.fixture
def screencap_moment() -> dict[str, Any]:
    return {
        "Episode": "S11E11",
        "Timestamp": 1118993,
        "Content": "- Now, does this hurt? - Aah!",
        "Title": "Faith Off",
    }


@pytest.fixture
def frame_json() -> dict[str, Any]:
    return frame(4555337, "S11E10", 350725)


@pytest.fixture
def episode_metadata_json() -> dict[str, Any]:
    return episode(season=11, episode=10)


def screencap_json() -> dict[str, Any]:
    return {
        "Episode": episode(season=11, episode=10),
        "Frame": frame(4555337, "S11E10", 350725),
        "Subtitles": [
            subtitle(313616, "Feels like I'm wearing nothing at all--", 348014, 347055, 349390),
            subtitle(313617, 'Nothing at all-- Nothing at all!"', 350517, 349474, 352060),
            subtitle(313618, "Stupid, sexy Flanders!", 353228, 352143, 354854),
        ],
        "Nearby": [frame(i, "S11E10", t) for i, t in enumerate(range(348223, 353228, 209), start=4555327)],
        "MinTimestamp": 1001,
        "MaxTimestamp": 1352977,
    }


@pytest.fixture
def screencap() -> Screencap:
    return Screencap.model_validate(screencap_json())


@pytest.fixture
def subtitle_json() -> dict[str, Any]:
    return subtitle(
        subtitle_id=313618,
        content="Stupid, sexy Flanders!",
        representative=353228,
        start=352143,
        end=354854,
    )
