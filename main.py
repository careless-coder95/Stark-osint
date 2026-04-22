import logging
import asyncio
from pyrogram import Client

from config import BOT_TOKEN, API_ID, API_HASH
from database.db import init_db
from handlers.start import register_start_handlers
from handlers.menu import register_menu_handlers
from handlers.api_handler import register_api_handlers
from handlers.extra import register_extra_handlers

# ─── LOGGING SETUP ──────────────────────────────────────────
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

# ─── BOT CLIENT ─────────────────────────────────────────────
app = Client(
    name="osint_lookup_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
)


def register_all_handlers():
    """Register all handlers in correct priority order."""
    register_start_handlers(app)
    register_menu_handlers(app)
    register_extra_handlers(app)
    register_api_handlers(app)   # Must be last — has catch-all text handler


async def main():
    logger.info("Initialising database...")
    init_db()

    logger.info("Registering handlers...")
    register_all_handlers()

    logger.info("Starting OSINT Lookup Bot...")
    async with app:
        me = await app.get_me()
        logger.info(f"Bot is running as @{me.username} (ID: {me.id})")
        logger.info("Press Ctrl+C to stop.")
        await asyncio.Event().wait()   # Keep running until interrupted


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
