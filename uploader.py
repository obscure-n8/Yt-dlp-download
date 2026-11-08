import os
from pyrogram import Client
from pyrogram.errors import FilePartMissing
from config import (
    API_ID, API_HASH,
    USER_SESSION_STRING, PREMIUM_SESSION_STRING,
    BOT_API_SPLIT_SIZE, DEFAULT_SPLIT_SIZE, PREMIUM_SPLIT_SIZE,
)

# --- Non-premium user client (optional) ---
user_client = None
if USER_SESSION_STRING:
    user_client = Client(
        "user_session",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=USER_SESSION_STRING,
        in_memory=True,
    )

# --- Premium client (optional) ---
premium_client = None
if PREMIUM_SESSION_STRING:
    premium_client = Client(
        "premium_session",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=PREMIUM_SESSION_STRING,
        in_memory=True,
    )


async def start_clients():
    if user_client:
        await user_client.start()
    if premium_client:
        await premium_client.start()


async def stop_clients():
    for c in (user_client, premium_client):
        if c:
            try:
                await c.stop()
            except Exception:
                pass


def _pick_uploader(bot_client):
    """
    Upload er jonno client pick kore.
    Priority: premium > non-premium > bot API
    """
    if premium_client:
        return premium_client, "premium"
    if user_client:
        return user_client, "user"
    return bot_client, "bot"


async def upload_parts(bot_client, parts: list, chat_id, caption: str,
                       thumb: str = None, status_msg=None):
    """
    File parts gulo chat_id te upload kore.
    """
    client, mode = _pick_uploader(bot_client)
    results = []
    total = len(parts)

    # Bot API te pathate hole 50MB er beshi gele error
    if mode == "bot":
        too_big = [p for p in parts if os.path.getsize(p) > BOT_API_SPLIT_SIZE]
        if too_big:
            raise ValueError(
                "Bot API diye 50MB er beshi upload hoy na. "
                "USER_SESSION_STRING ba PREMIUM_SESSION_STRING dao."
            )

    for idx, part in enumerate(parts, start=1):
        part_caption = caption if total == 1 else f"{caption}\n\n`Part {idx}/{total}`"

        kwargs = dict(
            chat_id=chat_id,
            caption=part_caption,
            supports_streaming=True,
            file_name=os.path.basename(part),
        )
        if thumb and os.path.exists(thumb):
            kwargs["thumb"] = thumb

        try:
            msg = await client.send_document(part, **kwargs)
        except FilePartMissing:
            # Retry once
            msg = await client.send_document(part, **kwargs)
        results.append(msg)

        try:
            os.remove(part)
        except Exception:
            pass

    return results
