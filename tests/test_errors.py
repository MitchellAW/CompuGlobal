"""Test all exceptions in errors module."""

import re

import pytest

from compuglobal.errors import APIPageStatusError, NoSearchResultsFoundError


def test_no_search_results_found_error() -> None:
    with pytest.raises(NoSearchResultsFoundError, match="No search results found"):
        raise NoSearchResultsFoundError


def test_api_page_status_error() -> None:
    url = "https://example.com"
    status_code = 404
    with pytest.raises(APIPageStatusError, match=re.escape("Error 404. https://example.com may be down.")):
        raise APIPageStatusError(status_code, url)
