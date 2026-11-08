import os
import re
import asyncio
from pyrogram import filters
from bot import bot
from config import UPLOAD_CHAT_ID, THUMB_PATH
from downloader import download_m3u8
from splitter import decide_split, get_split_size
from uploader import upload_parts
from helpers import edit_status, cleanup, human_size

URL_RE = re.compile(r"^https?://", re.IGNORECASE)


@bot.on_message(filters.text & filters.private & filters.regex(URL_RE))
async def leech_handler(client, message):
    url = message.text.strip()

    # 1. Status message
    status = await message.reply(f"`File is downloading...`\n\n`{url}`")

    file_path = None
    parts = []

    try:
        # 2. Download (blocking, thread e)
        file_path = await asyncio.to_thread(download_m3u8, url, status)

        size = os.path.getsize(file_path)
        limit = get_split_size()

        # 3. Split decide
        if size > limit:
            await edit_status(
                status,
                f"`File is splitting...`\n\n"
                f"Size: `{human_size(size)}`\n"
                f"Split size: `{human_size(limit)}`",
                force=True,
            )
            parts = await asyncio.to_thread(decide_split, file_path)
        else:
            parts = [file_path]

        # 4. Upload
        await edit_status(
            status,
            f"`File is uploading...`\n\n"
            f"Parts: `{len(parts)}`",
            force=True,
        )

        await upload_parts(
            bot_client=client,
            parts=parts,
            chat_id=UPLOAD_CHAT_ID,
            caption=url,
            thumb=THUMB_PATH,
            status_msg=status,
        )

        # 5. Done
        await edit_status(
            status,
            f"**File has uploaded.**\n\n`{url}`",
            force=True,
        )

    except Exception as e:
        await edit_status(
            status,
            f"**❌ Error:**\n`{e}`\n\n`{url}`",
            force=True,
        )
    finally:
        if file_path:
            cleanup(file_path)
        for p in parts:
            cleanup(p)
