import logging
from pyrogram import Client, filters
from pyrogram.types import Message

from config import BUTTON_NAMES, SUPPORT_LINK, UPDATES_LINK, GROUP_LINK
from database.db import get_user, upsert_user
from handlers.forcejoin import check_force_join
from utils.helpers import main_menu_keyboard, force_join_keyboard, link_keyboard

logger = logging.getLogger(__name__)

FORCE_JOIN_TEXT = """<b>⚠️ Access Restricted</b>

You must join all required channels to use this bot.

👇 Join and then press <b>✅ Verify</b>:"""

SUPPORT_TEXT = """<b>💬 Support Center</b>

Having issues? Our support team is ready to help!

🕐 Response time: <b>Within 24 hours</b>
📩 Open a ticket in our support chat."""

UPDATES_TEXT = """<b>📢 Stay Updated</b>

Get the latest features, fixes, and announcements.

🔔 Join our updates channel to never miss anything!"""

GROUP_TEXT = """<b>👥 OSINT Community Group</b>

Join our active OSINT community!

🗣️ Discuss techniques, tools & findings with fellow researchers."""

ACCOUNT_TEXT = """<b>╔══════════════════════╗
║     👤 MY ACCOUNT      ║
╚══════════════════════╝</b>

<b>📛 Name      :</b> {name}
<b>🆔 User ID   :</b> <code>{user_id}</code>
<b>👤 Username  :</b> @{username}

<b>━━━━━━━━━━━━━━━━━━━━━━</b>
<b>🔍 Total Searches :</b> <code>{searches}</code>
<b>━━━━━━━━━━━━━━━━━━━━━━</b>

<i>Thank you for using OSINT Lookup Bot!</i>"""


def register_extra_handlers(app: Client):

    @app.on_message(filters.private & filters.regex(f"^{BUTTON_NAMES['support']}$"))
    async def support_handler(client: Client, message: Message):
        if not await check_force_join(client, message.from_user.id):
            await message.reply(FORCE_JOIN_TEXT, reply_markup=force_join_keyboard(), parse_mode="html")
            return
        await message.reply(
            SUPPORT_TEXT,
            reply_markup=link_keyboard("💬 Open Support Chat", SUPPORT_LINK),
            parse_mode="html",
        )

    @app.on_message(filters.private & filters.regex(f"^{BUTTON_NAMES['updates']}$"))
    async def updates_handler(client: Client, message: Message):
        if not await check_force_join(client, message.from_user.id):
            await message.reply(FORCE_JOIN_TEXT, reply_markup=force_join_keyboard(), parse_mode="html")
            return
        await message.reply(
            UPDATES_TEXT,
            reply_markup=link_keyboard("📢 Join Updates Channel", UPDATES_LINK),
            parse_mode="html",
        )

    @app.on_message(filters.private & filters.regex(f"^{BUTTON_NAMES['group']}$"))
    async def group_handler(client: Client, message: Message):
        if not await check_force_join(client, message.from_user.id):
            await message.reply(FORCE_JOIN_TEXT, reply_markup=force_join_keyboard(), parse_mode="html")
            return
        await message.reply(
            GROUP_TEXT,
            reply_markup=link_keyboard("👥 Join OSINT Group", GROUP_LINK),
            parse_mode="html",
        )

    @app.on_message(filters.private & filters.regex(f"^{BUTTON_NAMES['account']}$"))
    async def account_handler(client: Client, message: Message):
        user = message.from_user
        upsert_user(user.id, user.first_name, user.username)

        if not await check_force_join(client, user.id):
            await message.reply(FORCE_JOIN_TEXT, reply_markup=force_join_keyboard(), parse_mode="html")
            return

        db_user = get_user(user.id)
        searches = db_user["search_count"] if db_user else 0
        username = user.username or "N/A"

        await message.reply(
            ACCOUNT_TEXT.format(
                name=user.first_name,
                user_id=user.id,
                username=username,
                searches=searches,
            ),
            reply_markup=main_menu_keyboard(),
            parse_mode="html",
        )
