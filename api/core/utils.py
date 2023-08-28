from urllib.parse import urlparse

import requests


def resolve_url(url: str) -> tuple[str, str | None]:
    """
    resolve_url resolves the URL to its final destination.

    Parameters
    ----------
    url : str
        The URL to resolve.

    Returns
    -------
    tuple[str, str | None]
        The first element is the original URL, the second element is the resolved URL.
    """

    try:
        r: requests.Response = requests.get(url)
    except requests.exceptions.RequestException:
        return (url, None)
    longurl = r.url if r.status_code == 200 else None
    return (url, longurl)


def get_domain(url: str) -> str:
    """get_domain returns the domain of the URL."""

    return urlparse(url).netloc
