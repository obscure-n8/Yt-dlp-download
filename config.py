import os

# ==================== Telegram ====================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID    = int(os.environ.get("API_ID", 0))
API_HASH  = os.environ.get("API_HASH")

# ==================== Owner ====================

OWNER_ID = int(os.environ.get("OWNER_ID", 0))

# ==================== User Sessions (optional) ====================

USER_SESSION_STRING    = os.environ.get("USER_SESSION_STRING") or None
# PREMIUM_SESSION_STRING: premium (4GB limit). Thakle 3.90GB split.
PREMIUM_SESSION_STRING = os.environ.get("PREMIUM_SESSION_STRING") or None

# ==================== Split Sizes (bytes) ====================
# Default: 1.95GB (2147483648 er kachakachi)
DEFAULT_SPLIT_SIZE = int(os.environ.get("TG_SPLIT_SIZE", 2 * 1024 * 1024 * 1024))
PREMIUM_SPLIT_SIZE = int(os.environ.get("PREMIUM_SPLIT_SIZE", 4 * 1024 * 1024 * 1024))

# Bot API limit (user session na thakle)
BOT_API_SPLIT_SIZE = 50 * 1024 * 1024  # 50 MB

# ==================== Download ====================
DOWNLOAD_DIR     = "/tmp/downloads"
FRAGMENT_WORKERS = int(os.environ.get("FRAGMENT_WORKERS", 16))  # yt-dlp -N


UPLOAD_CHAT_ID = os.environ.get("UPLOAD_CHAT_ID", "me")

# ==================== Thumbnail ====================
THUMB_PATH = os.environ.get("THUMB_PATH", "") or None
