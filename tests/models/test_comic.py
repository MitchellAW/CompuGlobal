"""Test all models in comic module."""

from typing import Any

import pytest
from inline_snapshot import snapshot
from pydantic import ValidationError

from compuglobal.models.comic import ComicLayout, ComicOverlay, ComicPanel, ComicStrip
from compuglobal.models.font import FontAlignment, FontFamily
from compuglobal.models.overlay import OverlayFormat
from compuglobal.models.screencap import Screencap
from compuglobal.models.subtitle import Subtitle


def test_comic_overlay_with_defaults() -> None:
    overlay = ComicOverlay(text="First test")
    assert overlay.model_dump() == snapshot(
        {
            "t": "First test",
            "f": FontFamily.IMPACT,
            "s": 0,
            "c": "ffffffff",
            "x": 50,
            "y": 97,
            "a": FontAlignment.ALIGN_CENTER,
            "u": 1,
            "b": 0,
            "d": 0,
        },
    )


def test_comic_overlay_model_validates_with_defaults() -> None:
    payload = {"t": "Second test"}
    overlay = ComicOverlay.model_validate(payload)

    assert overlay.model_dump() == snapshot(
        {
            "t": "Second test",
            "f": FontFamily.IMPACT,
            "s": 0,
            "c": "ffffffff",
            "x": 50,
            "y": 97,
            "a": FontAlignment.ALIGN_CENTER,
            "u": 1,
            "b": 0,
            "d": 0,
        },
    )


def test_comic_overlay_model_with_overrides() -> None:
    overlay = ComicOverlay(
        text="Stupid, sexy Flanders!",
        font_family=FontFamily.AKBAR,
        font_size=50,
        font_color="00000000",
        text_position_x=100,
        text_position_y=100,
        text_alignment=FontAlignment.ALIGN_LEFT,
        all_caps=0,
        b=1,
        d=2,
    )
    assert overlay.model_dump() == snapshot(
        {
            "t": "Stupid, sexy Flanders!",
            "f": FontFamily.AKBAR,
            "s": 50,
            "c": "00000000",
            "x": 100,
            "y": 100,
            "a": FontAlignment.ALIGN_LEFT,
            "u": 0,
            "b": 1,
            "d": 2,
        },
    )


def test_comic_overlay_from_subtitles(subtitle_json: dict[str, Any]) -> None:
    subtitles = [Subtitle.model_validate(subtitle_json)]
    overlay = ComicOverlay.from_subtitles(
        subtitles=subtitles,
        overlay_format=OverlayFormat(font_family=FontFamily.AKBAR),
    )
    assert overlay.model_dump() == snapshot(
        {
            "t": "Stupid, sexy Flanders!",
            "f": FontFamily.AKBAR,
            "s": 0,
            "c": "ffffffff",
            "x": 50,
            "y": 97,
            "a": FontAlignment.ALIGN_CENTER,
            "u": 1,
            "b": 0,
            "d": 0,
        },
    )


def test_comic_panel_validate_dump_with_defaults() -> None:
    payload = {"e": "S01E01", "ts": 7777}
    panel = ComicPanel.model_validate(payload)
    assert panel.model_dump() == snapshot({"e": "S01E01", "ts": 7777, "o": []})


def test_comic_panel_validate_dump_with_overrides(subtitle_json: dict[str, Any]) -> None:
    subtitles = [Subtitle.model_validate(subtitle_json)]
    overlay = ComicOverlay.from_subtitles(
        subtitles=subtitles,
        overlay_format=OverlayFormat(font_family=FontFamily.AKBAR),
    )
    payload = {"e": "S01E01", "ts": 7777, "o": [overlay]}
    panel = ComicPanel.model_validate(payload)
    assert panel.model_dump() == snapshot(
        {
            "e": "S01E01",
            "ts": 7777,
            "o": [
                {
                    "t": "Stupid, sexy Flanders!",
                    "f": FontFamily.AKBAR,
                    "s": 0,
                    "c": "ffffffff",
                    "x": 50,
                    "y": 97,
                    "a": FontAlignment.ALIGN_CENTER,
                    "u": 1,
                    "b": 0,
                    "d": 0,
                },
            ],
        },
    )


def test_comic_panel_validate_invalid() -> None:
    payload = {"incorrect": "S01E01"}
    with pytest.raises(ValidationError):
        ComicPanel.model_validate(payload)


def test_comic_panel_from_screencap(screencap: Screencap) -> None:
    comic_panel = ComicPanel.from_screencap(screencap=screencap)
    assert comic_panel.model_dump() == snapshot(
        {
            "e": "S11E10",
            "ts": 350725,
            "o": [
                {
                    "t": (
                        "Feels like I'm wearing nothing at all-- Nothing at all--"
                        ' Nothing at all!" Stupid, sexy Flanders!'
                    ),
                    "f": FontFamily.IMPACT,
                    "s": 0,
                    "c": "ffffffff",
                    "x": 50,
                    "y": 97,
                    "a": FontAlignment.ALIGN_CENTER,
                    "u": 1,
                    "b": 0,
                    "d": 0,
                },
            ],
        },
    )


def test_comic_panel_from_screencap_custom_font(screencap: Screencap) -> None:
    comic_panel = ComicPanel.from_screencap(
        screencap=screencap,
        overlay_format=OverlayFormat(font_family=FontFamily.JOST),
    )
    assert comic_panel.model_dump() == snapshot(
        {
            "e": "S11E10",
            "ts": 350725,
            "o": [
                {
                    "t": (
                        "Feels like I'm wearing nothing at all-- Nothing at all--"
                        ' Nothing at all!" Stupid, sexy Flanders!'
                    ),
                    "f": FontFamily.JOST,
                    "s": 0,
                    "c": "ffffffff",
                    "x": 50,
                    "y": 97,
                    "a": FontAlignment.ALIGN_CENTER,
                    "u": 1,
                    "b": 0,
                    "d": 0,
                },
            ],
        },
    )


def test_comic_panel_encoded(subtitle_json: dict[str, Any]) -> None:
    subtitles = [Subtitle.model_validate(subtitle_json)]
    overlay = ComicOverlay.from_subtitles(
        subtitles=subtitles,
        overlay_format=OverlayFormat(font_family=FontFamily.AKBAR),
    )
    payload = {"e": "S01E01", "ts": 7777, "o": [overlay]}
    panel = ComicPanel.model_validate(payload)

    assert panel.encoded == snapshot(
        "W3siZSI6IlMwMUUwMSIsInRzIjo3Nzc3LCJvIjpbeyJ0IjoiU3R1cGlkLCBzZXh5IEZsYW5kZXJzISIsImYiOiJha2JhciIsInMiOjAs"
        "ImMiOiJmZmZmZmZmZiIsIngiOjUwLCJ5Ijo5NywiYSI6ImMiLCJ1IjoxLCJiIjowLCJkIjowfV19XQ==",
    )


def test_comic_strip(subtitle_json: dict[str, Any]) -> None:
    subtitles = [Subtitle.model_validate(subtitle_json)]
    overlay = ComicOverlay.from_subtitles(
        subtitles=subtitles,
        overlay_format=OverlayFormat(font_family=FontFamily.AKBAR),
    )
    payload = {"e": "S01E01", "ts": 7777, "o": [overlay]}
    panel = ComicPanel.model_validate(payload)
    panels = [panel.model_copy(update={"timestamp": panel.timestamp + 1000 * i}) for i in range(4)]
    strip = ComicStrip(panels=panels)
    assert strip.model_dump() == snapshot(
        {
            "panels": [
                {
                    "e": "S01E01",
                    "ts": 7777,
                    "o": [
                        {
                            "t": "Stupid, sexy Flanders!",
                            "f": FontFamily.AKBAR,
                            "s": 0,
                            "c": "ffffffff",
                            "x": 50,
                            "y": 97,
                            "a": FontAlignment.ALIGN_CENTER,
                            "u": 1,
                            "b": 0,
                            "d": 0,
                        },
                    ],
                },
                {
                    "e": "S01E01",
                    "ts": 8777,
                    "o": [
                        {
                            "t": "Stupid, sexy Flanders!",
                            "f": FontFamily.AKBAR,
                            "s": 0,
                            "c": "ffffffff",
                            "x": 50,
                            "y": 97,
                            "a": FontAlignment.ALIGN_CENTER,
                            "u": 1,
                            "b": 0,
                            "d": 0,
                        },
                    ],
                },
                {
                    "e": "S01E01",
                    "ts": 9777,
                    "o": [
                        {
                            "t": "Stupid, sexy Flanders!",
                            "f": FontFamily.AKBAR,
                            "s": 0,
                            "c": "ffffffff",
                            "x": 50,
                            "y": 97,
                            "a": FontAlignment.ALIGN_CENTER,
                            "u": 1,
                            "b": 0,
                            "d": 0,
                        },
                    ],
                },
                {
                    "e": "S01E01",
                    "ts": 10777,
                    "o": [
                        {
                            "t": "Stupid, sexy Flanders!",
                            "f": FontFamily.AKBAR,
                            "s": 0,
                            "c": "ffffffff",
                            "x": 50,
                            "y": 97,
                            "a": FontAlignment.ALIGN_CENTER,
                            "u": 1,
                            "b": 0,
                            "d": 0,
                        },
                    ],
                },
            ],
            "layout": ComicLayout.TWO_OVER_ONE,
        },
    )


def test_comic_strip_from_screencap(screencap: Screencap) -> None:
    comic_strip = ComicStrip.from_screencap(screencap=screencap)
    assert comic_strip.model_dump() == snapshot(
        {
            "panels": [
                {
                    "e": "S11E10",
                    "ts": 348014,
                    "o": [
                        {
                            "t": "Feels like I'm wearing nothing at all--",
                            "f": FontFamily.IMPACT,
                            "s": 0,
                            "c": "ffffffff",
                            "x": 50,
                            "y": 97,
                            "a": FontAlignment.ALIGN_CENTER,
                            "u": 1,
                            "b": 0,
                            "d": 0,
                        },
                    ],
                },
                {
                    "e": "S11E10",
                    "ts": 350517,
                    "o": [
                        {
                            "t": 'Nothing at all-- Nothing at all!"',
                            "f": FontFamily.IMPACT,
                            "s": 0,
                            "c": "ffffffff",
                            "x": 50,
                            "y": 97,
                            "a": FontAlignment.ALIGN_CENTER,
                            "u": 1,
                            "b": 0,
                            "d": 0,
                        },
                    ],
                },
                {
                    "e": "S11E10",
                    "ts": 353228,
                    "o": [
                        {
                            "t": "Stupid, sexy Flanders!",
                            "f": FontFamily.IMPACT,
                            "s": 0,
                            "c": "ffffffff",
                            "x": 50,
                            "y": 97,
                            "a": FontAlignment.ALIGN_CENTER,
                            "u": 1,
                            "b": 0,
                            "d": 0,
                        },
                    ],
                },
            ],
            "layout": ComicLayout.ONE_OVER_TWO,
        },
    )


def test_comic_strip_build_comic_overlays(subtitle_json: dict[str, Any]) -> None:
    subtitle = Subtitle.model_validate(subtitle_json)
    subtitles = [subtitle.model_copy(update={"content": f"{i} - {subtitle.content}"}) for i in range(1, 4)]
    overlays = ComicStrip.build_comic_overlays(subtitles=subtitles)
    assert overlays == snapshot(
        [
            ComicOverlay(text="1 - Stupid, sexy Flanders!"),
            ComicOverlay(text="2 - Stupid, sexy Flanders!"),
            ComicOverlay(text="3 - Stupid, sexy Flanders!"),
        ],
    )


def test_comic_strip_build_comic_overlays_with_font(subtitle_json: dict[str, Any]) -> None:
    subtitle = Subtitle.model_validate(subtitle_json)
    subtitles = [subtitle.model_copy(update={"content": f"{i} - {subtitle.content}"}) for i in range(1, 4)]
    overlays = ComicStrip.build_comic_overlays(
        subtitles=subtitles,
        overlay_format=OverlayFormat(font_family=FontFamily.JOST),
    )
    assert overlays == snapshot(
        [
            ComicOverlay(text="1 - Stupid, sexy Flanders!", font_family=FontFamily.JOST),
            ComicOverlay(text="2 - Stupid, sexy Flanders!", font_family=FontFamily.JOST),
            ComicOverlay(text="3 - Stupid, sexy Flanders!", font_family=FontFamily.JOST),
        ],
    )


def test_comic_strip_encoded(screencap: Screencap) -> None:
    comic_strip = ComicStrip.from_screencap(screencap=screencap)
    assert comic_strip.encoded == snapshot(
        "W3siZSI6IlMxMUUxMCIsInRzIjozNDgwMTQsIm8iOlt7InQiOiJGZWVscyBsaWtlIEknbSB3ZWFyaW5nIG5vdGhpbmcgYXQgYWxsLS0iLCJmIjoiaW1wYWN0IiwicyI6MCwiYyI6ImZmZmZmZmZmIiwieCI6NTAsInkiOjk3LCJhIjoiYyIsInUiOjEsImIiOjAsImQiOjB9XX0seyJlIjoiUzExRTEwIiwidHMiOjM1MDUxNywibyI6W3sidCI6Ik5vdGhpbmcgYXQgYWxsLS0gTm90aGluZyBhdCBhbGwhXCIiLCJmIjoiaW1wYWN0IiwicyI6MCwiYyI6ImZmZmZmZmZmIiwieCI6NTAsInkiOjk3LCJhIjoiYyIsInUiOjEsImIiOjAsImQiOjB9XX0seyJlIjoiUzExRTEwIiwidHMiOjM1MzIyOCwibyI6W3sidCI6IlN0dXBpZCwgc2V4eSBGbGFuZGVycyEiLCJmIjoiaW1wYWN0IiwicyI6MCwiYyI6ImZmZmZmZmZmIiwieCI6NTAsInkiOjk3LCJhIjoiYyIsInUiOjEsImIiOjAsImQiOjB9XX1d",
    )


@pytest.mark.parametrize(
    ("panel_count", "expected_layout"),
    [(1, ComicLayout.SINGLE), (2, ComicLayout.WIDE), (3, ComicLayout.ONE_OVER_TWO), (4, ComicLayout.TWO_OVER_ONE)],
)
def test_comic_strip_default_layouts(
    subtitle_json: dict[str, Any],
    panel_count: int,
    expected_layout: ComicLayout,
) -> None:
    subtitles = [Subtitle.model_validate(subtitle_json)]
    overlay = ComicOverlay.from_subtitles(
        subtitles=subtitles,
        overlay_format=OverlayFormat(font_family=FontFamily.AKBAR),
    )
    payload = {"e": "S01E01", "ts": 7777, "o": [overlay]}
    panel = ComicPanel.model_validate(payload)
    panels = [panel.model_copy(update={"timestamp": panel.timestamp + 1000 * i}) for i in range(panel_count)]
    strip = ComicStrip(panels=panels, layout=None)
    assert strip.layout == expected_layout


def test_comic_strip_custom_layout(
    subtitle_json: dict[str, Any],
) -> None:
    subtitles = [Subtitle.model_validate(subtitle_json)]
    overlay = ComicOverlay.from_subtitles(
        subtitles=subtitles,
        overlay_format=OverlayFormat(font_family=FontFamily.AKBAR),
    )
    payload = {"e": "S01E01", "ts": 7777, "o": [overlay]}
    panel = ComicPanel.model_validate(payload)
    panels = [panel.model_copy(update={"timestamp": panel.timestamp + 1000 * i}) for i in range(3)]
    strip = ComicStrip(panels=panels, layout=ComicLayout.WIDE)
    assert strip.layout == ComicLayout.WIDE
