"""All errors/exceptions returned by CompuGlobal APIs."""

from http import HTTPStatus


class NoSearchResultsFoundError(Exception):
    """Raised when no search results are found."""

    def __init__(self, message: str = "No search results found.") -> None:
        super().__init__(message)


class MaximumRetriesExceededError(Exception):
    """Raised when the maximum number of retries is exceeded."""

    def __init__(self, message: str = "Maximum number of retries exceeded.") -> None:
        super().__init__(message)


class APIPageStatusError(Exception):
    """Raised when the status code for the API is not 200.

    Parameters
    ----------
    page_status : int
        The page status code returned by the API.
    url : str
        The base url that raised the error.
    retry_after : int | None
        Number of seconds to wait before retrying if error was a 429.

    """

    def __init__(self, page_status: int, url: str, retry_after: int | None = None) -> None:
        self.page_status = page_status
        self.url = url
        self.retry_after = retry_after

        msg = f"Error {page_status}. {url} may be down."
        if page_status == HTTPStatus.TOO_MANY_REQUESTS and self.retry_after is not None:
            msg += f" Retry after {retry_after} seconds."
        super().__init__(msg)
