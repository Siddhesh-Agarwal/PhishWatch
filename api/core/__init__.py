# type: ignore
from core.checks import (
    has_favicon,
    has_valid_dns_record,
    has_valid_ssl_certs,
    is_blacklisted,
    is_not_forwarding,
    is_registered_recently,
    is_using_free_hosting,
    uses_https,
)
from core.db import add_data, search_data
from core.utils import get_domain
