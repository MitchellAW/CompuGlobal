class NoSearchResultsFoundError(Exception):
    """Raised when no search results are returned during a search query to the
    search endpoint of the API."""

    def __init__(self) -> None:
        super().__init__("No search results found.")


class APIPageStatusError(Exception):
    """Raised when the status code for the API is not 200.

    Parameters
    ----------
    page_status: int
        The page status number for the error.
    url: str
        The url page that encountered the error."""

    def __init__(self, page_status: int, url: str) -> None:
        super().__init__(f"Error {page_status}. {url} may be down.")
