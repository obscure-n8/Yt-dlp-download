import os
import re
import asyncio
from pyrogram import filters
from config import UPLOAD_CHAT_ID, THUMB_PATH
from downloader import download_m3u8
from splitter import decide_split, get_split_size
from uploader import upload_parts
from helpers import edit_status, cleanup, human_size

URL_RE = re.compile(r"^https?://", re.IGNORECASE)

def register_handlers(app):
    @app.on_message(filters.text & filters.private & filters.regex(URL_RE))
    async def leech_handler(client, message):
        url = message.text.strip()
        status = await message.reply(f"`File is downloading...`\n\n`{url}`")

        file_path = None
        parts = []

        try:
            # Download
            file_path = await asyncio.to_thread(download_m3u8, url, status)

            size = os.path.getsize(file_path)
            limit = get_split_size()

            # Split Decide
            if size > limit:
                await edit_status(
                    status,
                    f"`File is splitting...`\n\nSize: `{human_size(size)}`\nSplit size: `{human_size(limit)}`",
                    force=True,
                )
                parts = await asyncio.to_thread(decide_split, file_path)
            else:
                parts = [file_path]

            # Upload
            await edit_status(
                status,
                f"`File is uploading...`\n\nParts: `{len(parts)}`",
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

            # Done
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
