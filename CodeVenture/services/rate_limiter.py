import time
from typing import Optional

from django.core.cache import cache
from django.http import HttpRequest


def _get_client_ip(request: HttpRequest) -> str:
    """
    Best-effort extraction of a client identifier.

    We prioritise X-Forwarded-For when present (e.g. when running
    behind a reverse proxy) and fall back to REMOTE_ADDR.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # The left‑most address is the original client.
        ip = x_forwarded_for.split(",")[0].strip()
        if ip:
            return ip

    ip = request.META.get("REMOTE_ADDR")
    return ip or "unknown"


def _is_over_limit(cache_key: str, limit: int, window_seconds: int) -> bool:
    """
    Simple per-key counter using Django's cache.

    We use `cache.add` + `cache.incr` to implement a sliding window
    starting from the first request. This is intentionally lightweight
    and good enough for a production demo environment.
    """
    # First request for this key within the window.
    if cache.add(cache_key, 1, timeout=window_seconds):
        return False

    try:
        current = cache.incr(cache_key)
    except ValueError:
        # Key disappeared between `add` and `incr`; start a new window.
        cache.set(cache_key, 1, timeout=window_seconds)
        return False

    return current > limit


def is_over_limit_for_request(
    request: HttpRequest,
    *,
    prefix: str = "judge0",
    limit: int = 3,
    window_seconds: int = 24 * 60 * 60,
) -> bool:
    """
    Returns True if the caller has exceeded the allowed number of requests.

    - `limit`: maximum number of allowed requests within `window_seconds`.
    - `window_seconds`: length of the sliding window for counting requests.

    The key space is intentionally coarse (per‑IP) because this is
    designed as a cost‑control guardrail for a public demo, not a
    security barrier.
    """
    client_id = _get_client_ip(request)
    cache_key = f"rl:{prefix}:{client_id}"
    return _is_over_limit(cache_key, limit, window_seconds)

