"""Test all models in font module."""

import pytest
from pydantic import ValidationError

from compuglobal.models.font import FontColor

VALID_RGB_VALUES = [
    (0, 0, 0, 0),
    (50, 50, 50, 50),
    (100, 100, 100, 100),
    (150, 150, 150, 150),
    (200, 200, 200, 200),
    (255, 255, 255, 255),
]


INVALID_RGB_VALUES = [
    (-1, 0, 0, 0),
    (256, 0, 0, 0),
    (0, -1, 0, 0),
    (0, 256, 0, 0),
    (0, 0, -1, 0),
    (0, 0, 256, 0),
    (0, 0, 0, -1),
    (0, 0, 0, 256),
]

HEX_TO_RGBA_VALUES = [
    ("#ff0000", [255, 0, 0, 255]),
    ("#00ff00", [0, 255, 0, 255]),
    ("#0000ff", [0, 0, 255, 255]),
    ("#ff00ff", [255, 0, 255, 255]),
    ("#ffffff", [255, 255, 255, 255]),
    ("#000000", [0, 0, 0, 255]),
    ("#00000000", [0, 0, 0, 0]),
    ("#ffffff80", [255, 255, 255, 128]),
    ("#1a2b3c", [26, 43, 60, 255]),
    ("#deadbe", [222, 173, 190, 255]),
    ("#ff6600cc", [255, 102, 0, 204]),
]


@pytest.mark.parametrize(("red", "green", "blue", "alpha"), VALID_RGB_VALUES)
def test_font_color_rgb(red: int, green: int, blue: int, alpha: int) -> None:
    payload = {"r": red, "g": green, "b": blue, "a": alpha}
    color = FontColor.model_validate(payload)
    assert color.model_dump() == payload


@pytest.mark.parametrize(("red", "green", "blue", "alpha"), INVALID_RGB_VALUES)
def test_font_color_invalid_invalid_range(red: int, green: int, blue: int, alpha: int) -> None:
    invalid_payload = {"r": red, "g": green, "b": blue, "a": alpha}
    with pytest.raises(ValidationError):
        FontColor.model_validate(invalid_payload)


@pytest.mark.parametrize(("red", "green", "blue", "alpha"), VALID_RGB_VALUES)
def test_font_color_rgba(red: int, green: int, blue: int, alpha: int) -> None:
    color = FontColor(red=red, green=green, blue=blue, alpha=alpha)
    assert color.rgba == [red, green, blue, alpha]


@pytest.mark.parametrize(("hex_code", "expected"), HEX_TO_RGBA_VALUES)
def test_font_color_from_hex(hex_code: str, expected: list[int]) -> None:
    color = FontColor.from_hex(hex_code)
    assert color.rgba == expected
