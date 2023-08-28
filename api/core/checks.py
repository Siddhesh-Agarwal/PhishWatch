import socket

import requests
import whois  # type: ignore

from core.utils import get_domain, resolve_url


def uses_https(url: str) -> bool:
    """Check if the URL is using HTTPS."""

    return str(url).startswith("https://")


def is_blacklisted(domain: str) -> bool:
    """
    is_blacklisted checks if the domain is blacklisted.

    Parameters
    ----------
    domain : str
        The domain to check.

    Returns
    -------
    bool
        True if the domain is blacklisted, False otherwise.

    Reference
    ---------
    https://github.com/Siddhesh-Agarwal/IP-DB/
    """

    # TODO: Check if the domain is blacklisted
    return False


def is_using_free_hosting(domain: str) -> bool:
    # TODO: Check if the domain is using a free hosting service
    return False


def is_registered_recently(domain: str, debug: bool = False) -> bool:
    """
    is_register_in_past_year checks if the domain is registered in the past year.

    Parameters
    ----------
    domain : str
        The domain to check.
    debug : bool, optional
        Whether to print debug information, by default False

    Returns
    -------
    bool
        True if the domain is registered in the past year, False otherwise.
    """
    try:
        domain_ = whois.whois(domain)  # type: ignore
        if domain_.creation_date is None:  # type: ignore
            return True
        if domain_.creation_date < 500:  # type: ignore
            return True
        return False
    except Exception as e:
        if debug:
            print("Failed to get whois record for domain: " + domain)
            print(e)
        return True


def has_valid_dns_record(domain: str, debug: bool = False) -> bool:
    """
    has_valid_dns_record checks if the domain has a valid DNS record.

    Parameters
    ----------
    domain : str
        The domain to check.
    debug : bool, optional
        Whether to print the debug information, by default False

    Returns
    -------
    bool
        True if the domain has a valid DNS record, False otherwise.
    """

    try:
        socket.gethostbyname(domain)
        return True
    except Exception as e:
        if debug:
            print(e)
        return False


def is_not_forwarding(url: str) -> bool:
    """
    is_forwarding checks if the domain is using a URL shortening service.

    Parameters
    ----------
    url : str
        The URL to check.

    Returns
    -------
    bool
        True if the domain is using a URL shortening service, False otherwise.
    """
    _, longurl = resolve_url(url)
    if longurl is None:
        return False
    return get_domain(url) == get_domain(longurl)


def has_valid_ssl_certs(url: str) -> bool:
    """
    has_valid_ssl_certs checks if the domain has valid SSL certificates.

    Parameters
    ----------
    url : str
        The URL to check.

    Returns
    -------
    bool
        True if the domain has valid SSL certificates, False otherwise.

    References
    ----------
    """
    try:
        return requests.get(url, verify=True).status_code == 200
    except:
        return False


def has_favicon(domain: str) -> bool:
    """
    has_favicon checks if the domain has a favicon.

    Parameters
    ----------
    domain : str
        The domain to check.

    Returns
    -------
    bool
        True if the domain has a favicon, False otherwise.
    """

    try:
        r: requests.Response = requests.get(
            f"https://{domain}/favicon.ico", verify=True
        )
        return r.status_code == 200
    except:
        return False
