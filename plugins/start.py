from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import bot
from config import OWNER_ID


@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    text = (
        "**Bot is alive now.**\n\n"
        "Paste your m3u8 link here."
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚙️ Settings", callback_data="open_bsetting")]
    ])
    await message.reply(text, reply_markup=kb)
