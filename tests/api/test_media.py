"""Test media module endpoint definition match expected API contract."""

from inline_snapshot import snapshot

from compuglobal.api.endpoint import RequestMethod
from compuglobal.api.media import MediaAPI
from compuglobal.models.stream import Stream


def test_media_get_endpoints_use_correct_method() -> None:
    endpoints = [MediaAPI.IMAGE, MediaAPI.COMIC_PANEL, MediaAPI.COMIC_STRIP, MediaAPI.DETECT_LOOP]
    for endpoint in endpoints:
        assert endpoint.method == RequestMethod.GET


def test_media_post_endpoints_use_correct_method() -> None:
    endpoints = [MediaAPI.RENDER_GIF, MediaAPI.RENDER_MP4]
    for endpoint in endpoints:
        assert endpoint.method == RequestMethod.POST


def test_media_api_endpoints_use_api_route() -> None:
    endpoints = [MediaAPI.RENDER_GIF, MediaAPI.RENDER_MP4, MediaAPI.DETECT_LOOP]
    for endpoint in endpoints:
        assert endpoint.path.startswith("/api/")


def test_media_comic_endpoints_use_comic_route() -> None:
    endpoints = [MediaAPI.COMIC_PANEL, MediaAPI.COMIC_STRIP]
    for endpoint in endpoints:
        assert endpoint.path.startswith("/comic/img")


def test_media_image_endpoints_use_img_route() -> None:
    endpoints = [MediaAPI.IMAGE]
    for endpoint in endpoints:
        assert endpoint.path.startswith("/img")


def test_media_image_expected_path() -> None:
    path = MediaAPI.IMAGE.path
    assert path.startswith("/img/")
    assert path.endswith("{key}/{timestamp}.jpg")


def test_media_image_expected_params() -> None:
    params = MediaAPI.IMAGE.required_query_params
    assert params == frozenset()


def test_media_comic_panel_expected_path() -> None:
    path = MediaAPI.COMIC_PANEL.path
    assert path == "/comic/img"


def test_media_comic_panel_expected_params() -> None:
    params = MediaAPI.COMIC_PANEL.required_query_params
    assert params == snapshot(frozenset({"b64"}))


def test_media_comic_strip_expected_path() -> None:
    path = MediaAPI.COMIC_STRIP.path
    assert path == "/comic/img"


def test_media_comic_strip_expected_params() -> None:
    params = MediaAPI.COMIC_STRIP.required_query_params
    assert params == snapshot(frozenset({"b64", "layout"}))


def test_media_render_gif_expected_path() -> None:
    path = MediaAPI.RENDER_GIF.path
    assert path == "/api/render/gif/stream"


def test_media_render_gif_expected_params() -> None:
    params = MediaAPI.RENDER_GIF.required_query_params
    assert params == frozenset()


def test_media_render_gif_expected_body() -> None:
    model = MediaAPI.RENDER_GIF.body_model
    assert model == Stream


def test_media_render_mp4_expected_path() -> None:
    path = MediaAPI.RENDER_MP4.path
    assert path == "/api/render/mp4"


def test_media_render_mp4_expected_params() -> None:
    params = MediaAPI.RENDER_MP4.required_query_params
    assert params == frozenset()


def test_media_render_mp4_expected_body_model() -> None:
    model = MediaAPI.RENDER_MP4.body_model
    assert model == Stream


def test_media_detect_loop_expected_path() -> None:
    path = MediaAPI.DETECT_LOOP.path
    assert path == "/api/detect-loop"


def test_media_detect_loop_expected_params() -> None:
    params = MediaAPI.DETECT_LOOP.required_query_params
    assert params == snapshot(frozenset({"end", "episode", "start"}))
