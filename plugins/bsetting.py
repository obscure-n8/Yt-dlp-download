from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import bot
from config import (
    OWNER_ID,
    TG_SPLIT_SIZE if False else DEFAULT_SPLIT_SIZE,  # placeholder
    PREMIUM_SPLIT_SIZE,
    USER_SESSION_STRING,
    PREMIUM_SESSION_STRING,
)
