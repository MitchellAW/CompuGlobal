"""Test API config module."""

from compuglobal.api.config import CompuGlobalAPIConfig
from compuglobal.models.font import FontFamily


def test_compuglobal_config_defaults() -> None:
    config = CompuGlobalAPIConfig(title="Example")
    expected = CompuGlobalAPIConfig(title="Example", default_font=FontFamily.IMPACT)
    assert config == expected


def test_compuglobal_config_overrides() -> None:
    config = CompuGlobalAPIConfig(title="Test", default_font=FontFamily.AKBAR)
    assert config.title == "Test"
    assert config.default_font == FontFamily.AKBAR
