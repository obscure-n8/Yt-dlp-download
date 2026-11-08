from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import (
    OWNER_ID,
    DEFAULT_SPLIT_SIZE,
    PREMIUM_SPLIT_SIZE,
    BOT_API_SPLIT_SIZE,
    USER_SESSION_STRING,
    PREMIUM_SESSION_STRING,
)
from helpers import human_size


def _settings_text():
    # effective split size
    if PREMIUM_SESSION_STRING:
        eff = PREMIUM_SPLIT_SIZE
        eff_label = "Premium (4GB)"
    elif USER_SESSION_STRING:
        eff = DEFAULT_SPLIT_SIZE
        eff_label = "Non-premium (2GB)"
    else:
        eff = BOT_API_SPLIT_SIZE
        eff_label = "Bot API (50MB)"

    return (
        "**⚙️ Bot Settings**\n\n"
        f"**User Session:** {'✅ set' if USER_SESSION_STRING else '❌ not set'}\n"
        f"**Premium Session:** {'✅ set' if PREMIUM_SESSION_STRING else '❌ not set'}\n"
        f"**Effective Split Size:** `{human_size(eff)}` ({eff_label})\n\n"
        f"**Config Vars (defaults):**\n"
        f"`TG_SPLIT_SIZE` = `{human_size(DEFAULT_SPLIT_SIZE)}`\n"
        f"`PREMIUM_SPLIT_SIZE` = `{human_size(PREMIUM_SPLIT_SIZE)}`\n\n"
        "Heroku → **Settings → Config Vars** e value bodla, tarpor **Restart** koro."
    )


def _settings_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Config Variables", callback_data="cfg")],
        [InlineKeyboardButton("User_string_session", callback_data="uss")],
        [InlineKeyboardButton("File_split_size", callback_data="fss")],
        [InlineKeyboardButton("🔄 Reset to default", callback_data="reset")],
    ])


def _is_owner(user_id: int) -> bool:
    return OWNER_ID and user_id == OWNER_ID


@bot.on_message(filters.command("bsetting") & filters.private)
async def bsetting_handler(client, message):
    if not _is_owner(message.from_user.id):
        await message.reply("**❌ Ei command shudhu owner er jonno.**")
        return
    await message.reply(_settings_text(), reply_markup=_settings_kb())


@bot.on_callback_query(filters.regex("^(cfg|uss|fss|reset|open_bsetting)$"))
async def bsetting_cb(client, cb):
    # callback o owner check
    if not _is_owner(cb.from_user.id):
        await cb.answer("❌ Owner only.", show_alert=True)
        return

    data = cb.data

    if data == "open_bsetting":
        try:
            await cb.message.edit_text(_settings_text(), reply_markup=_settings_kb())
        except Exception:
            pass
        await cb.answer()
        return

    if data == "cfg":
        await cb.answer("Heroku → Settings → Config Vars", show_alert=True)
    elif data == "uss":
        await cb.answer(
            "USER_SESSION_STRING: non-premium (2GB)\n"
            "PREMIUM_SESSION_STRING: premium (4GB)\n\n"
            "Duita optional. Kono ta na dile 50MB split hobe.",
            show_alert=True,
        )
    elif data == "fss":
        await cb.answer(
            f"TG_SPLIT_SIZE = {human_size(DEFAULT_SPLIT_SIZE)}\n"
            f"PREMIUM_SPLIT_SIZE = {human_size(PREMIUM_SPLIT_SIZE)}\n\n"
            "Heroku Config Vars e bodla.",
            show_alert=True,
        )
    elif data == "reset":
        await cb.answer(
            "Reset korte Heroku Config Vars theke value gulo delete koro.\n"
            "Default: TG_SPLIT_SIZE=2GB, PREMIUM_SPLIT_SIZE=4GB",
            show_alert=True,
        )
