"""Test overlay module."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from compuglobal.models.font import FontFamily
from compuglobal.models.overlay import OverlayFormat


def test_overlay_format_invalid_rgba_length_too_few() -> None:
    with pytest.raises(ValueError, match="must have exactly 4 values"):
        # pyrefly: ignore [bad-argument-type]
        OverlayFormat(font_color=())


def test_overlay_format_invalid_rgba_length_too_many() -> None:
    with pytest.raises(ValueError, match="must have exactly 4 values"):
        # pyrefly: ignore [bad-argument-type]
        OverlayFormat(font_color=(255, 255, 255, 255, 255))


@given(st.integers(max_value=-1))
def test_overlay_format_invalid_colors_low(bad_color: int) -> None:
    with pytest.raises(ValueError, match="values must be between 0 and 255"):
        OverlayFormat(font_color=(1, 1, 1, bad_color))


@given(st.integers(min_value=256))
def test_overlay_format_invalid_colors_high(bad_color: int) -> None:
    with pytest.raises(ValueError, match="values must be between 0 and 255"):
        OverlayFormat(font_color=(1, 1, 1, bad_color))


def test_overlay_format_normalise_default() -> None:
    normalised = OverlayFormat.normalise(None, 1)
    assert len(normalised) == 1
    assert normalised[0] == OverlayFormat()


def test_overlay_format_normalise_given() -> None:
    given = OverlayFormat(font_family=FontFamily.AKBAR)
    normalised = OverlayFormat.normalise(given, 1)
    assert normalised == [given]


def test_overlay_format_normalise_given_fewer() -> None:
    given = OverlayFormat(font_family=FontFamily.AKBAR)
    default = OverlayFormat()
    normalised = OverlayFormat.normalise([given], 4)
    assert normalised == [given, default, default, default]


def test_overlay_format_normalise_given_extras() -> None:
    given = OverlayFormat(font_family=FontFamily.AKBAR)
    normalised = OverlayFormat.normalise([given] * 10, 4)
    assert normalised == [given, given, given, given]
