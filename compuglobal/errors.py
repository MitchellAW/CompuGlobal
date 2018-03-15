class NoSearchResultsFound(Exception):
    """Raised when no search results are returned during a search query to the
    search endpoint of the API."""
    def __init__(self):
        super().__init__('No search results found.')


class APIPageStatusError(Exception):
    """Raised when the status code for the API is not 200.

    :param page_status: The page status number for the error.
    :param url: The url page that encountered the error."""
    def __init__(self, page_status, url):
        super().__init__('Error {}. {} may be down.'.format(page_status, url))
