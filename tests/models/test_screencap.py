"""Test all models in screencap module."""

from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st
from inline_snapshot import snapshot
from pydantic import ValidationError

from compuglobal.models.screencap import Screencap, ScreencapMoment


def test_screencap_moment() -> None:
    moment = ScreencapMoment(
        episode="S01E02",
        timestamp=872288,
        content="what do you say we go out for a round of frosty chocolate milkshakes?",
        title="Bart the Genius",
    )
    assert moment.model_dump() == snapshot(
        {
            "Episode": "S01E02",
            "Timestamp": 872288,
            "Content": "what do you say we go out for a round of frosty chocolate milkshakes?",
            "Title": "Bart the Genius",
        },
    )


def test_screencap_moment_validate_dump(screencap_moment: dict[str, Any]) -> None:
    moment = ScreencapMoment.model_validate(screencap_moment)
    dump = moment.model_dump()
    expected = ScreencapMoment.model_validate(dump)
    assert moment == expected


@given(st.integers(max_value=-1))
def test_screencap_moment_invalid_timestamp(bad_timestamp: int) -> None:
    with pytest.raises(ValidationError):
        ScreencapMoment(episode="S01E01", timestamp=bad_timestamp, content="Content", Title="Title")


@given(st.integers(max_value=-1))
def test_screencap_moment_validate_invalid_timestamp(bad_timestamp: int) -> None:
    payload = {"Episode": "S01E01", "Timestamp": bad_timestamp, "Content": "Content", "Title": "Title"}
    with pytest.raises(ValidationError):
        ScreencapMoment.model_validate(payload)


def test_screencap_moment_timecode(screencap_moment: dict[str, Any]) -> None:
    moment = ScreencapMoment.model_validate(screencap_moment)
    assert moment.timecode == snapshot("18:38")


def test_screencap_validate_dump(screencap: Screencap) -> None:
    dump = screencap.model_dump()
    expected = Screencap.model_validate(dump)
    assert screencap == expected


def test_screencap_timecode(screencap: Screencap) -> None:
    assert screencap.timecode == snapshot("5:50")


def test_screencap_captions(screencap: Screencap) -> None:
    assert screencap.captions == [
        "Feels like I'm wearing nothing at all--",
        'Nothing at all-- Nothing at all!"',
        "Stupid, sexy Flanders!",
    ]


def test_screencap_caption(screencap: Screencap) -> None:
    assert screencap.caption == snapshot(
        "Feels like I'm wearing nothing at all-- Nothing at all-- Nothing at all!\" Stupid, sexy Flanders!",
    )


def test_screencap_duration(screencap: Screencap) -> None:
    assert screencap.duration == snapshot(7799)


def test_screencap_start(screencap: Screencap) -> None:
    assert screencap.start == 347055


def test_screencap_end(screencap: Screencap) -> None:
    assert screencap.end == 354854


def test_screencap_str(screencap: Screencap) -> None:
    assert str(screencap) == snapshot("S11E10 - 350725 (5:50)")
