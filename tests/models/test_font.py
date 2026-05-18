"""Test all models in font module."""

import pytest
from pydantic import ValidationError

from compuglobal.models.font import FontColorRGB

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


@pytest.mark.parametrize(("red", "green", "blue", "alpha"), VALID_RGB_VALUES)
def test_font_color_rgb(red: int, green: int, blue: int, alpha: int) -> None:
    payload = {"r": red, "g": green, "b": blue, "a": alpha}
    rgba = FontColorRGB.model_validate(payload)
    assert rgba.model_dump() == payload


@pytest.mark.parametrize(("red", "green", "blue", "alpha"), INVALID_RGB_VALUES)
def test_font_color_invalid_invalid_range(red: int, green: int, blue: int, alpha: int) -> None:
    invalid_payload = {"r": red, "g": green, "b": blue, "a": alpha}
    with pytest.raises(ValidationError):
        FontColorRGB.model_validate(invalid_payload)


@pytest.mark.parametrize(("red", "green", "blue", "alpha"), VALID_RGB_VALUES)
def test_font_color_get_rgba(red: int, green: int, blue: int, alpha: int) -> None:
    rgba = FontColorRGB(red=red, green=green, blue=blue, alpha=alpha)
    assert rgba.get_rgba() == [red, green, blue, alpha]
