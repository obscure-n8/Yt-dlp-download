import os
import asyncio
from pyrogram import Client, idle
from config import BOT_TOKEN, API_ID, API_HASH, DOWNLOAD_DIR
from uploader import start_clients, stop_clients

# Global bot instance (ekhane plugins=dict() thakbe na)
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

async def main():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    await start_clients()
    
    # প্লাগইনগুলোকে জোর করে লোড করা হচ্ছে
    from plugins import start, leech, bsetting
    start.register_handlers(bot)
    leech.register_handlers(bot)
    bsetting.register_handlers(bot)

    await bot.start()
    me = await bot.get_me()
    print(f"✅ Bot started: @{me.username} with plugins loaded.")
    try:
        await idle()
    finally:
        await bot.stop()
        await stop_clients()

if __name__ == "__main__":
    asyncio.run(main())
