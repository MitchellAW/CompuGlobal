"""Test all models in subtitle module."""

from typing import Any

import pytest
from pydantic import ValidationError

from compuglobal.models.subtitle import Subtitle


def test_subtitle_dump(subtitle_json: dict[str, Any]) -> None:
    subtitle = Subtitle(
        id=313618,
        representative_timestamp=353228,
        key="S11E10",
        start_timestamp=352143,
        end_timestamp=354854,
        content="Stupid, sexy Flanders!",
        language="en",
    )
    assert subtitle.model_dump() == subtitle_json


def test_subtitle_validate_dump(subtitle_json: dict[str, Any]) -> None:
    subtitle = Subtitle.model_validate(subtitle_json)
    dump = subtitle.model_dump()
    expected = Subtitle.model_validate(dump)
    assert subtitle == expected


@pytest.mark.parametrize(("start_timestamp", "end_timestamp"), [(-1, 0), (0, -1), (-99, -99)])
def test_subtitle_invalid_timestamp(subtitle_json: dict[str, Any], start_timestamp: int, end_timestamp: int) -> None:
    subtitle = Subtitle.model_validate(subtitle_json)
    copy = subtitle.model_copy(update={"start_timestamp": start_timestamp, "end_timestamp": end_timestamp})
    copy_dump = copy.model_dump()
    with pytest.raises(ValidationError, match="Input should be greater than or equal to 0"):
        Subtitle.model_validate(copy_dump)


@pytest.mark.parametrize(
    ("start_timestamp", "end_timestamp", "expected"),
    [
        (1000, 1000, 0),
        (8000, 9000, 1000),
        (352143, 354854, 2711),
    ],
)
def test_subtitle_get_duration(
    subtitle_json: dict[str, Any],
    start_timestamp: int,
    end_timestamp: int,
    expected: int,
) -> None:
    subtitle = Subtitle.model_validate(subtitle_json)
    copy = subtitle.model_copy(update={"start_timestamp": start_timestamp, "end_timestamp": end_timestamp})
    assert copy.get_duration() == expected
