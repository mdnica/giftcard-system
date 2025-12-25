import time
from typing import Dict, Tuple

from .config import settings

# key: identifier (IP or user), value: (window_start_timestamp, count)
_request_store: Dict[str, Tuple[float, int]] = {}


def check_rate_limit(identifier: str, max_requests_per_minute: int = None) -> bool:
    """
    Returns True if allowed, False if rate limit exceeded.
    """
    max_requests = max_requests_per_minute or settings.MAX_REQUESTS_PER_MINUTE
    now = time.time()
    window = 60.0

    window_start, count = _request_store.get(identifier, (now, 0))

    if now - window_start > window:
        # reset window
        window_start, count = now, 0

    count += 1
    _request_store[identifier] = (window_start, count)

    return count <= max_requests
