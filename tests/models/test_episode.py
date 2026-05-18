"""Test all models in episode module."""

from typing import Any

import pytest
from pydantic import ValidationError

from compuglobal.models.episode import Episode, EpisodeMetadata, EpisodeSummary


@pytest.fixture
def episode_metadata_json() -> dict[str, Any]:
    return {
        "Id": 571,
        "Key": "S11E10",
        "Season": 11,
        "EpisodeNumber": 10,
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


def test_episode_metadata_validate_dump(episode_metadata_json: dict[str, Any]) -> None:
    metadata = EpisodeMetadata.model_validate(episode_metadata_json)
    dump = metadata.model_dump()
    expected = EpisodeMetadata.model_validate(dump)
    assert metadata == expected


def test_episode_metadata_model_validate_invalid_season(episode_metadata_json: dict[str, Any]) -> None:
    invalid = episode_metadata_json | {"Season": -1}
    with pytest.raises(ValidationError, match="Input should be greater than or equal to 0"):
        EpisodeMetadata.model_validate(invalid)


def test_episode_metadata_dump(episode_metadata_json: dict[str, Any]) -> None:
    metadata = EpisodeMetadata(
        id=571,
        key="S11E10",
        season=11,
        episode_number=10,
        title="Little Big Mom",
        director="Mark Kirkland",
        writer="Carolyn Omine",
        original_air_date="2000-01-09",
        wiki_link="https://en.wikipedia.org/wiki/Little_Big_Mom",
    )
    assert metadata.model_dump() == episode_metadata_json


def test_episode_summary_model_validate_dump(episode_summary_json: dict[str, Any]) -> None:
    summary = EpisodeSummary.model_validate(episode_summary_json)
    dump = summary.model_dump()
    expected = EpisodeSummary.model_validate(dump)
    assert summary == expected


def test_episode_summary_model_validate_missing_fields() -> None:
    invalid = {}
    with pytest.raises(ValidationError, match="Field required"):
        EpisodeSummary.model_validate(invalid)


def test_episode_summary_model_validate_unexpected_fields(episode_summary_json: dict[str, Any]) -> None:
    invalid = episode_summary_json | {"INVALID": True}
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        EpisodeSummary.model_validate(invalid)


def test_episode_model_validate_dump(episode_json: dict[str, Any]) -> None:
    episode = Episode.model_validate(episode_json)
    dump = episode.model_dump()
    expected = Episode.model_validate(dump)
    assert episode == expected


def test_episode_model_validate_invalid_episode() -> None:
    invalid = {"Episode": "S11E11"}
    with pytest.raises(ValidationError, match="Input should be a valid dictionary or instance of EpisodeMetadata"):
        Episode.model_validate(invalid)


def test_episode_model_validate_invalid_subtitles() -> None:
    invalid = {"Subtitles": ["Test"]}
    with pytest.raises(ValidationError, match="Input should be a valid dictionary or instance of Subtitle"):
        Episode.model_validate(invalid)
