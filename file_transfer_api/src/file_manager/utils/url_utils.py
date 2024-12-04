from urllib.parse import urlparse, urlsplit


class URLPath:
    """Class to represent a URL path. This is a wrapper around the urllib.parse.urlparse function. That will allow easy
    access to the different parts of the URL."""

    def __init__(self, url: str):
        """Initialise the URLPath class.

        Args:
            url: URL to parse.
        """
        self.url = url
        self.parsed_url = urlparse(url)
        self.name = urlsplit(url).path.split("/")[-1]

    def __str__(self):
        return self.url

    def __repr__(self):
        return self.url
