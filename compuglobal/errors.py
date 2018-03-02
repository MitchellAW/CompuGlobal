# Raised when no search results are found
class NoSearchResultsFound(Exception):
    def __init__(self):
        super().__init__('No search results found.')


# Raised when page status 404s etc.
class APIPageStatusError(Exception):
    def __init__(self, page_status, url):
        super().__init__('Error {}. {} may be down.'.format(page_status, url))
