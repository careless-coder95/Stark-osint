import logging
import asyncio
from pyrogram import Client, idle

from config import BOT_TOKEN, API_ID, API_HASH
from database.db import init_db
from handlers.start import register_start_handlers
from handlers.menu import register_menu_handlers
from handlers.extra import register_extra_handlers
from handlers.api_handler import register_api_handlers

# ─── LOGGING ────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)

# ─── CLIENT ─────────────────────────────────────────────────
app = Client(
    name="osint_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
)


async def main():
    logger.info("Initialising database...")
    init_db()

    logger.info("Registering handlers...")
    # ORDER MATTERS — specific handlers first, catch-all last
    register_start_handlers(app)
    register_menu_handlers(app)
    register_extra_handlers(app)
    register_api_handlers(app)   # has catch-all text handler — always last

    logger.info("Starting bot...")
    await app.start()

    me = await app.get_me()
    logger.info(f"✅ Bot running as @{me.username} (ID: {me.id})")
    logger.info("Press Ctrl+C to stop.")

    await idle()

    await app.stop()
    logger.info("Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())
