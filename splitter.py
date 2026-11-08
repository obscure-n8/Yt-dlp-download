import os
from config import (
    DEFAULT_SPLIT_SIZE,
    PREMIUM_SPLIT_SIZE,
    BOT_API_SPLIT_SIZE,
    USER_SESSION_STRING,
    PREMIUM_SESSION_STRING,
)


def get_split_size() -> int:
    """
    Koto size e split hobe seta decide kore.
    - Premium session thakle: PREMIUM_SPLIT_SIZE (4GB)
    - Non-premium session thakle: DEFAULT_SPLIT_SIZE (2GB)
    - Kono session na thakle: BOT_API_SPLIT_SIZE (50MB)
    """
    if PREMIUM_SESSION_STRING:
        return PREMIUM_SPLIT_SIZE
    if USER_SESSION_STRING:
        return DEFAULT_SPLIT_SIZE
    return BOT_API_SPLIT_SIZE


def decide_split(file_path: str) -> list:
    """
    File size dekhe split korbe kina decide kore.
    """
    size = os.path.getsize(file_path)
    limit = get_split_size()

    if size <= limit:
        return [file_path]

    return _split(file_path, limit)


def _split(file_path: str, limit_bytes: int) -> list:
    parts = []
    base, ext = os.path.splitext(file_path)

    with open(file_path, "rb") as f:
        i = 1
        while True:
            chunk = f.read(limit_bytes)
            if not chunk:
                break
            part = f"{base}.part{i}{ext}"
            with open(part, "wb") as out:
                out.write(chunk)
            parts.append(part)
            i += 1

    try:
        os.remove(file_path)
    except Exception:
        pass
    return parts
