import logging
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from database.db import upsert_user
from handlers.forcejoin import check_force_join
from utils.helpers import main_menu_keyboard, force_join_keyboard

logger = logging.getLogger(__name__)

WELCOME_TEXT = """<b>╔══════════════════════════╗
║   🕵️ OSINT NUMBER LOOKUP BOT   ║
╚══════════════════════════╝</b>

👋 Welcome, <b>{name}</b>!

🔍 <b>What can I do?</b>
┣ 📞 Lookup any phone number globally
┣ 🌍 Get carrier, country & location info
┣ 📡 Multiple OSINT API sources
┗ 🛡️ Fast, clean and accurate results

<b>━━━━━━━━━━━━━━━━━━━━━━━━━━</b>
📲 <i>Use the menu below to get started!</i>
<b>━━━━━━━━━━━━━━━━━━━━━━━━━━</b>"""

FORCE_JOIN_TEXT = """<b>⚠️ Access Restricted</b>

You must join <b>all required channels</b> before using this bot.

👇 Click the buttons below to join, then press <b>✅ Verify</b>:"""

VERIFY_FAIL_TEXT = """<b>❌ Verification Failed</b>

You haven't joined all required channels yet.

Please join <b>all channels</b> and then press <b>✅ Verify</b> again."""


def register_start_handlers(app: Client):

    @app.on_message(filters.command("start") & filters.private)
    async def start_command(client: Client, message: Message):
        user = message.from_user
        try:
            upsert_user(user.id, user.first_name, user.username)
        except Exception as e:
            logger.error(f"DB upsert error: {e}")

        try:
            joined = await check_force_join(client, user.id)
        except Exception as e:
            logger.error(f"Force join check error: {e}")
            joined = True  # fallback: allow if check fails

        if not joined:
            await message.reply_text(
                FORCE_JOIN_TEXT,
                reply_markup=force_join_keyboard(),
                parse_mode="html",
            )
            return

        await message.reply_text(
            WELCOME_TEXT.format(name=user.first_name),
            reply_markup=main_menu_keyboard(),
            parse_mode="html",
        )

    @app.on_callback_query(filters.regex("^verify_join$"))
    async def verify_join_callback(client: Client, callback: CallbackQuery):
        user = callback.from_user
        try:
            upsert_user(user.id, user.first_name, user.username)
        except Exception as e:
            logger.error(f"DB upsert error: {e}")

        try:
            joined = await check_force_join(client, user.id)
        except Exception as e:
            logger.error(f"Force join check error: {e}")
            joined = True

        if not joined:
            await callback.answer("❌ You haven't joined all channels yet!", show_alert=True)
            try:
                await callback.message.edit_text(
                    VERIFY_FAIL_TEXT,
                    reply_markup=force_join_keyboard(),
                    parse_mode="html",
                )
            except Exception:
                pass
            return

        await callback.answer("✅ Verified! Welcome aboard.", show_alert=False)
        try:
            await callback.message.delete()
        except Exception:
            pass

        await client.send_message(
            user.id,
            WELCOME_TEXT.format(name=user.first_name),
            reply_markup=main_menu_keyboard(),
            parse_mode="html",
        )
