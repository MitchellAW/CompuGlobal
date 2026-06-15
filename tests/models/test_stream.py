"""Test all models in stream module."""

import pytest
from inline_snapshot import snapshot
from pydantic import ValidationError

from compuglobal.models.font import FontAlignment, FontFamily
from compuglobal.models.overlay import OverlayFormat
from compuglobal.models.screencap import Screencap
from compuglobal.models.stream import Stream, StreamOverlay


def test_stream_overlay_default() -> None:
    overlay = StreamOverlay(text="Test", start=0, end=0)
    expected = StreamOverlay(
        text="Test",
        font_family=FontFamily.IMPACT,
        font_size=0,
        font_color=[255, 255, 255, 255],
        text_position_x=50,
        text_position_y=97,
        text_alignment=FontAlignment.ALIGN_CENTER,
        all_caps=True,
        start=0,
        end=0,
    )

    assert overlay == expected


def test_stream_overlay_overrides() -> None:
    overlay = StreamOverlay(
        text="Custom",
        font_family=FontFamily.AKBAR,
        font_size=50,
        font_color=[0, 50, 150, 250],
        text_position_x=100,
        text_position_y=120,
        text_alignment=FontAlignment.ALIGN_RIGHT,
        all_caps=False,
        start=10,
        end=30,
    )

    assert overlay.model_dump() == snapshot(
        {
            "text": "Custom",
            "font": FontFamily.AKBAR,
            "size": 50,
            "color": [0, 50, 150, 250],
            "x": 100,
            "y": 120,
            "text_align": FontAlignment.ALIGN_RIGHT,
            "all_caps": False,
            "start": 10,
            "end": 30,
        },
    )


@pytest.mark.parametrize(("font_size"), [-1, -150, -300])
def test_stream_overlay_invalid_font_size_negative(font_size: int) -> None:
    with pytest.raises(ValidationError, match="Input should be greater than or equal to 0"):
        StreamOverlay(text="Test", font_size=font_size, start=0, end=0)


@pytest.mark.parametrize(("font_size"), [121, 200, 300])
def test_stream_overlay_invalid_font_size_large(font_size: int) -> None:
    with pytest.raises(ValidationError, match="Input should be less than or equal to 120"):
        StreamOverlay(text="Test", font_size=font_size, start=0, end=0)


@pytest.mark.parametrize(("font_color"), [(0, 0, 0), (0, 0)])
def test_stream_overlay_invalid_font_color_missing_colors(font_color: list[int]) -> None:
    with pytest.raises(ValidationError, match="List should have at least 4 items"):
        StreamOverlay(text="Test", font_color=font_color, start=0, end=0)


@pytest.mark.parametrize(("font_color"), [(0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0, 0)])
def test_stream_overlay_invalid_font_color_too_many_colors(font_color: list[int]) -> None:
    with pytest.raises(ValidationError, match="List should have at most 4 items"):
        StreamOverlay(text="Test", font_color=font_color, start=0, end=0)


@pytest.mark.parametrize(("font_color"), [("X", 0, 0, 0), (0, "X", 0, 0), (0, 0, "X", 0), (0, 0, 0, "X")])
def test_stream_overlay_invalid_font_color_not_ints(font_color: list[int]) -> None:
    with pytest.raises(ValidationError, match="Input should be a valid integer"):
        StreamOverlay(text="Test", font_color=font_color, start=0, end=0)


@pytest.mark.parametrize(("start"), [-1, -150, -300])
def test_stream_overlay_invalid_start_negative(start: int) -> None:
    with pytest.raises(ValidationError, match="Input should be greater than or equal to 0"):
        StreamOverlay(text="Test", start=start, end=0)


@pytest.mark.parametrize(("end"), [-1, -150, -300])
def test_stream_overlay_invalid_end_negative(end: int) -> None:
    with pytest.raises(ValidationError, match="Input should be greater than or equal to 0"):
        StreamOverlay(text="Test", start=0, end=end)


def test_stream_dump() -> None:
    stream = Stream(key="S01E01", start=0, end=1000, overlays=[], check_only=False)
    assert stream.model_dump() == snapshot(
        {"episode": "S01E01", "start": 0, "end": 1000, "overlays": [], "check_only": False},
    )


def test_stream_dump_with_overlays() -> None:
    overlays = [StreamOverlay(text=f"Example text {i}", start=i - 1, end=i) for i in range(1, 3)]
    stream = Stream(key="S01E01", start=0, end=2, overlays=overlays, check_only=False)
    assert stream.model_dump() == snapshot(
        {
            "episode": "S01E01",
            "start": 0,
            "end": 2,
            "overlays": [
                {
                    "text": "Example text 1",
                    "font": FontFamily.IMPACT,
                    "size": 0,
                    "color": [255, 255, 255, 255],
                    "x": 50,
                    "y": 97,
                    "text_align": FontAlignment.ALIGN_CENTER,
                    "all_caps": True,
                    "start": 0,
                    "end": 1,
                },
                {
                    "text": "Example text 2",
                    "font": FontFamily.IMPACT,
                    "size": 0,
                    "color": [255, 255, 255, 255],
                    "x": 50,
                    "y": 97,
                    "text_align": FontAlignment.ALIGN_CENTER,
                    "all_caps": True,
                    "start": 1,
                    "end": 2,
                },
            ],
            "check_only": False,
        },
    )


def test_stream_from_screencap(screencap: Screencap) -> None:
    stream = Stream.from_screencap(screencap=screencap)
    assert stream.model_dump() == snapshot(
        {
            "episode": "S11E10",
            "start": 347055,
            "end": 354854,
            "overlays": [
                {
                    "text": "Feels like I'm wearing nothing at all--",
                    "font": FontFamily.IMPACT,
                    "size": 0,
                    "color": [255, 255, 255, 255],
                    "x": 50,
                    "y": 97,
                    "text_align": FontAlignment.ALIGN_CENTER,
                    "all_caps": True,
                    "start": 0,
                    "end": 2335,
                },
                {
                    "text": 'Nothing at all-- Nothing at all!"',
                    "font": FontFamily.IMPACT,
                    "size": 0,
                    "color": [255, 255, 255, 255],
                    "x": 50,
                    "y": 97,
                    "text_align": FontAlignment.ALIGN_CENTER,
                    "all_caps": True,
                    "start": 2419,
                    "end": 5005,
                },
                {
                    "text": "Stupid, sexy Flanders!",
                    "font": FontFamily.IMPACT,
                    "size": 0,
                    "color": [255, 255, 255, 255],
                    "x": 50,
                    "y": 97,
                    "text_align": FontAlignment.ALIGN_CENTER,
                    "all_caps": True,
                    "start": 5088,
                    "end": 7799,
                },
            ],
            "check_only": False,
        },
    )


def test_stream_build_stream_overlays(screencap: Screencap) -> None:
    overlays = Stream.build_stream_overlays(screencap)
    assert overlays == snapshot(
        [
            StreamOverlay(text="Feels like I'm wearing nothing at all--", start=0, end=2335),
            StreamOverlay(text='Nothing at all-- Nothing at all!"', start=2419, end=5005),
            StreamOverlay(text="Stupid, sexy Flanders!", start=5088, end=7799),
        ],
    )


def test_stream_build_stream_overlays_font(screencap: Screencap) -> None:
    overlays = Stream.build_stream_overlays(screencap, overlay_format=OverlayFormat(font_family=FontFamily.JOST))
    assert overlays == snapshot(
        [
            StreamOverlay(
                text="Feels like I'm wearing nothing at all--",
                font_family=FontFamily.JOST,
                start=0,
                end=2335,
            ),
            StreamOverlay(text='Nothing at all-- Nothing at all!"', font_family=FontFamily.JOST, start=2419, end=5005),
            StreamOverlay(text="Stupid, sexy Flanders!", font_family=FontFamily.JOST, start=5088, end=7799),
        ],
    )


def test_stream_caption() -> None:
    overlays = [StreamOverlay(text=f"Example text {i}!", start=i - 1, end=i) for i in range(1, 3)]
    stream = Stream(key="S01E01", start=0, end=2, overlays=overlays, check_only=False)
    assert stream.caption == snapshot("Example text 1! Example text 2!")
