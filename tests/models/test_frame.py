"""Test all models in frame module."""

import pytest
from hypothesis import given
from hypothesis import strategies as st
from inline_snapshot import snapshot
from pydantic import ValidationError

from compuglobal.models.frame import Frame

TIMESTAMP_CASES = [
    (1000, "0:01"),
    (7500, "0:07"),
    (35000, "0:35"),
    (123456, "2:03"),
    (1234567, "20:34"),
    (12345678, "205:45"),
]


def test_frame_model_dump() -> None:
    frame = Frame(id=9, key="S22E22", timestamp=7777)
    assert frame.model_dump() == snapshot(
        {"Id": 9, "Episode": "S22E22", "Timestamp": 7777, "VideoWidth": 480, "VideoHeight": 360},
    )


def test_frame_validate_dump() -> None:
    payload = {"Id": 1, "Episode": "S01E01", "Timestamp": 1000}
    frame = Frame.model_validate(payload)
    dump = frame.model_dump()
    expected = Frame.model_validate(dump)
    assert frame == expected


@given(st.integers(max_value=-1))
def test_frame_validate_invalid_timestamp(bad_timestamp: int) -> None:
    with pytest.raises(ValidationError):
        Frame(id="1", key="S01E01", timestamp=bad_timestamp)


@given(st.integers(max_value=-1))
def test_frame_validate_validate_invalid_timestamp(bad_timestamp: int) -> None:
    payload = {"Id": 1, "Episode": "S01E01", "Timestamp": bad_timestamp}
    with pytest.raises(ValidationError):
        Frame.model_validate(payload)


@pytest.mark.parametrize(("timestamp", "expected"), TIMESTAMP_CASES)
def test_frame_timecode(timestamp: int, expected: str) -> None:
    frame = Frame(id=1, key="S22E22", timestamp=timestamp)
    assert frame.timecode == expected


@pytest.mark.parametrize(("timestamp", "expected"), TIMESTAMP_CASES)
def test_frame_str(timestamp: int, expected: str) -> None:
    frame = Frame(id=1, key="S22E33", timestamp=timestamp)
    assert str(frame) == f"S22E33 - {timestamp} ({expected})"
