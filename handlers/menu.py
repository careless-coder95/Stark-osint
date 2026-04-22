import logging
from pyrogram import Client, filters
from pyrogram.types import Message

from handlers.forcejoin import check_force_join
from utils.helpers import main_menu_keyboard, force_join_keyboard

logger = logging.getLogger(__name__)

FORCE_JOIN_TEXT = """<b>⚠️ Access Restricted</b>

You must join all required channels to use this bot.

👇 Join and then press <b>✅ Verify</b>:"""


def register_menu_handlers(app: Client):

    @app.on_message(filters.private & filters.command("menu"))
    async def menu_command(client: Client, message: Message):
        user_id = message.from_user.id
        if not await check_force_join(client, user_id):
            await message.reply(FORCE_JOIN_TEXT, reply_markup=force_join_keyboard(), parse_mode="html")
            return
        await message.reply(
            "<b>📋 Main Menu</b>\n\nChoose an option below:",
            reply_markup=main_menu_keyboard(),
            parse_mode="html",
        )
