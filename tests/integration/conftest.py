"""Printing a test summary for integration tests."""

import datetime
import webbrowser
from collections import defaultdict
from pathlib import Path

import pytest
from jinja2 import Template

_default_media_urls: dict[str, list[dict[str, str]]] = defaultdict(list)

_customised_media_urls: dict[str, list[dict[str, str]]] = defaultdict(list)


def log_media_url(api_name: str, content_title: str, content_url: str, media_type: str) -> None:
    _default_media_urls[api_name].append({"title": content_title, "type": media_type, "url": content_url})


def log_customised_media_url(api_name: str, content_title: str, content_url: str, media_type: str) -> None:
    _customised_media_urls[api_name].append({"title": content_title, "type": media_type, "url": content_url})


def generate_html_report(path: Path) -> None:
    template_path = Path(__file__).parent / "report_template.jinja"
    template = Template(template_path.read_text())
    html = template.render(
        timestamp=datetime.datetime.now(tz=datetime.UTC).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        apis=_default_media_urls,
        custom_apis=_customised_media_urls,
    )

    path.write_text(html, encoding="utf-8")


def pytest_terminal_summary(terminalreporter: pytest.TerminalReporter, exitstatus: int, config: pytest.Config) -> None:  # ruff: ignore[unused-function-argument]
    if not _default_media_urls or not _customised_media_urls:
        return

    report_path = Path("media_report.html")
    generate_html_report(report_path)
    terminalreporter.write_line(f"\nHTML media report written to: {report_path.resolve()}")

    if config.getoption("--open-report"):
        webbrowser.open(report_path.resolve().as_uri())
