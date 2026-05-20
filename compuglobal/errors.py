"""All errors/exceptions returned by CompuGlobal APIs."""


class NoSearchResultsFoundError(Exception):
    """Raised when no search results are found."""

    def __init__(self, message: str = "No search results found.") -> None:
        """Raise an error related to no search results being found."""
        super().__init__(message)


class APIPageStatusError(Exception):
    """Raised when the status code for the API is not 200."""

    def __init__(self, page_status: int, url: str) -> None:
        """Raise an error related to the page status of an API.

        Parameters
        ----------
        page_status : int
            The page status code returned by the API.
        url : str
            The base url that raised the error.

        """
        super().__init__(f"Error {page_status}. {url} may be down.")
