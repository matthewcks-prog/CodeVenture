import re
from urllib.parse import urlparse, parse_qs
from typing import Optional


_YOUTUBE_VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def is_valid_video_id(value: str) -> bool:
    """Return True if the given value looks like a YouTube video ID."""
    return bool(value) and bool(_YOUTUBE_VIDEO_ID_RE.fullmatch(value))


def extract_video_id(raw_value: Optional[str]) -> Optional[str]:
    """
    Normalise a YouTube identifier into a bare video ID.

    Accepts:
    - A raw 11‑character video ID
    - A full YouTube URL (watch, share, embed, shorts)
    Returns the most likely video ID or None if nothing usable is found.
    """
    if not raw_value:
        return None

    value = raw_value.strip()

    # Already a plain video ID
    if is_valid_video_id(value):
        return value

    # Try to interpret as URL
    try:
        parsed = urlparse(value)
    except ValueError:
        # Not a URL, return as‑is so validation can flag it
        return value

    host = (parsed.hostname or "").lower()

    # Short URLs: https://youtu.be/<id>
    if host in {"youtu.be", "www.youtu.be"}:
        candidate = parsed.path.lstrip("/")
        if is_valid_video_id(candidate):
            return candidate

    # Standard YouTube URLs
    if "youtube.com" in host:
        # Watch URLs: https://www.youtube.com/watch?v=<id>
        query = parse_qs(parsed.query)
        if "v" in query:
            candidate = query["v"][0]
            if is_valid_video_id(candidate):
                return candidate

        # Embed / Shorts URLs: /embed/<id>, /shorts/<id>, etc.
        for part in reversed(parsed.path.split("/")):
            if is_valid_video_id(part):
                return part

    # Fallback: return the original trimmed value
    return value


def _normalised_id(raw_value: Optional[str]) -> Optional[str]:
    """
    Helper that returns a *validated* bare video ID or ``None``.
    """
    video_id = extract_video_id(raw_value)
    if not video_id or not is_valid_video_id(video_id):
        return None
    return video_id


def build_embed_url(raw_value: Optional[str]) -> Optional[str]:
    """
    Build a safe YouTube embed URL from an ID or URL.

    Returns None if no valid ID can be determined.
    """
    video_id = _normalised_id(raw_value)
    if not video_id:
        return None
    return f"https://www.youtube.com/embed/{video_id}"


def build_watch_url(raw_value: Optional[str]) -> Optional[str]:
    """
    Build a standard YouTube "watch" URL from an ID or URL.

    Useful for fallbacks when embedding is disabled by the video owner.
    """
    video_id = _normalised_id(raw_value)
    if not video_id:
        return None
    return f"https://www.youtube.com/watch?v={video_id}"


def build_thumbnail_url(raw_value: Optional[str], quality: str = "hqdefault") -> Optional[str]:
    """
    Build a thumbnail URL for the given YouTube video.

    Uses the public ``img.youtube.com`` endpoint which does not require
    any API keys and is very reliable in practice.

    The ``quality`` parameter corresponds to the standard thumbnail
    variants supported by YouTube (e.g. ``default``, ``mqdefault``,
    ``hqdefault``, ``sddefault``).
    """
    video_id = _normalised_id(raw_value)
    if not video_id:
        return None
    return f"https://img.youtube.com/vi/{video_id}/{quality}.jpg"

