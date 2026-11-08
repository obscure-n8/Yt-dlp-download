import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
print(f"DEBUG: BOT_TOKEN loaded? {'Yes' if BOT_TOKEN else 'No'}")
print(f"DEBUG: API_ID = {API_ID}")
API_ID    = int(os.environ.get("API_ID", 0))
API_HASH  = os.environ.get("API_HASH")

OWNER_ID = int(os.environ.get("OWNER_ID", 0))

USER_SESSION_STRING    = os.environ.get("USER_SESSION_STRING") or None
PREMIUM_SESSION_STRING = os.environ.get("PREMIUM_SESSION_STRING") or None

DEFAULT_SPLIT_SIZE = int(os.environ.get("TG_SPLIT_SIZE", 2 * 1024 * 1024 * 1024))
PREMIUM_SPLIT_SIZE = int(os.environ.get("PREMIUM_SPLIT_SIZE", 4 * 1024 * 1024 * 1024))
BOT_API_SPLIT_SIZE = 50 * 1024 * 1024

DOWNLOAD_DIR     = "/tmp/downloads"
FRAGMENT_WORKERS = int(os.environ.get("FRAGMENT_WORKERS", 16))

UPLOAD_CHAT_ID = os.environ.get("UPLOAD_CHAT_ID", "me")
THUMB_PATH = os.environ.get("THUMB_PATH", "") or None
