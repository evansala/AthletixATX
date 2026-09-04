import re

# Matches the 11-character YouTube video ID out of any common URL shape:
#   https://www.youtube.com/watch?v=VIDEOID
#   https://youtu.be/VIDEOID
#   https://www.youtube.com/embed/VIDEOID
#   https://www.youtube.com/shorts/VIDEOID
#   with or without extra query params / www / youtube-nocookie.com
_YOUTUBE_RE = re.compile(
    r"""(?:youtube(?:-nocookie)?\.com/                # youtube.com / youtube-nocookie.com
            (?:watch\?v=|embed/|shorts/|v/)
        |youtu\.be/                                    # short domain
        )
        (?P<id>[A-Za-z0-9_-]{11})
    """,
    re.VERBOSE,
)


def extract_youtube_id(url: str):
    """Return the 11-char YouTube video ID from a URL, or None if it can't be parsed."""
    if not url:
        return None
    match = _YOUTUBE_RE.search(url.strip())
    return match.group("id") if match else None
