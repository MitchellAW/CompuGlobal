"""Test API config module."""

from compuglobal import FontAlignment
from compuglobal.api.config import CompuGlobalAPIConfig
from compuglobal.models.font import FontColor, FontFamily
from compuglobal.models.overlay import OverlayFormat


def test_compuglobal_config_defaults() -> None:
    config = CompuGlobalAPIConfig(title="Example")
    default_format = OverlayFormat(
        font_family=FontFamily.IMPACT,
        font_size=0,
        font_color=FontColor.from_rgba(255, 255, 255, 255),
        text_position_x=50,
        text_position_y=97,
        text_alignment=FontAlignment.ALIGN_CENTER,
        all_caps=True,
    )
    expected = CompuGlobalAPIConfig(title="Example", default_format=default_format)
    assert config == expected


def test_compuglobal_config_overrides() -> None:
    custom_format = OverlayFormat(
        font_family=FontFamily.JOST,
        font_size=12,
        font_color=FontColor.from_rgba(10, 20, 30, 40),
        text_position_x=120,
        text_position_y=80,
        text_alignment=FontAlignment.ALIGN_LEFT,
        all_caps=False,
    )
    config = CompuGlobalAPIConfig(
        title="Test",
        default_format=custom_format,
    )
    assert config.title == "Test"
    assert config.default_format == custom_format
