"""
api_handler.py  —  Generic API caller
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Config se URL + params padhta hai, khud URL banata hai,
call karta hai, aur JSON response ko saaf format mein
dikhata hai.  Code change karne ki zaroorat NAHI.
"""

import logging
import asyncio
import aiohttp
import re
from pyrogram import Client, filters
from pyrogram.types import Message

from config import APIS, BUTTON_NAMES, COOLDOWN_SECONDS
from database.db import increment_search
from handlers.forcejoin import check_force_join
from utils.helpers import (
    cancel_keyboard,
    main_menu_keyboard,
    force_join_keyboard,
    is_on_cooldown,
    set_cooldown,
    cooldown_remaining,
)

logger = logging.getLogger(__name__)

# ── Button text → API key ────────────────────────────────────
BUTTON_TO_API: dict[str, str] = {
    BUTTON_NAMES[k]: k for k in ("btn1", "btn2", "btn3", "btn4", "btn5")
}

# ── Per-user state ───────────────────────────────────────────
# { user_id: "btn1" | "btn2" | ... }
_waiting: dict[int, str] = {}

FORCE_JOIN_TEXT = (
    "<b>⚠️ Access Restricted</b>\n\n"
    "Join all required channels first, then press <b>✅ Verify</b>:"
)


# ────────────────────────────────────────────────────────────
#  URL builder  (pure function, no side effects)
# ────────────────────────────────────────────────────────────
def build_url(api_cfg: dict, user_input: str) -> str:
    """
    Builds final GET URL from config fields.

    Rules:
      • Always: url?input_param=user_input
      • If key_param and key_value are non-empty:
            append  &key_param=key_value
    """
    base        = api_cfg["url"].rstrip("?&")
    input_param = api_cfg["input_param"]
    key_param   = api_cfg.get("key_param", "")
    key_value   = api_cfg.get("key_value", "")

    url = f"{base}?{input_param}={user_input}"

    if key_param and key_value:
        url += f"&{key_param}={key_value}"

    return url


# ────────────────────────────────────────────────────────────
#  HTTP caller
# ────────────────────────────────────────────────────────────
async def fetch(url: str) -> dict | list | None:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=12),
                headers={"User-Agent": "OSINTBot/1.0"},
            ) as resp:
                logger.info(f"GET {url}  →  HTTP {resp.status}")
                if resp.status == 200:
                    return await resp.json(content_type=None)
                logger.warning(f"Non-200 response: {resp.status}")
    except asyncio.TimeoutError:
        logger.error(f"Timeout: {url}")
    except Exception as e:
        logger.error(f"Fetch error: {e}")
    return None


# ────────────────────────────────────────────────────────────
#  Response formatter  (works on ANY JSON shape)
# ────────────────────────────────────────────────────────────
def _flatten(data, prefix="") -> list[tuple[str, str]]:
    """
    Recursively flatten nested dict/list into (key, value) pairs.
    Skips None, empty strings, empty dicts/lists.
    Max depth: 3 levels.
    """
    pairs = []
    if isinstance(data, dict):
        for k, v in data.items():
            full_key = f"{prefix}.{k}" if prefix else str(k)
            if isinstance(v, (dict, list)):
                pairs.extend(_flatten(v, full_key))
            elif v not in (None, "", [], {}):
                pairs.append((full_key, str(v)))
    elif isinstance(data, list):
        for i, item in enumerate(data[:5]):   # max 5 list items
            pairs.extend(_flatten(item, f"{prefix}[{i}]"))
    return pairs


def format_response(api_name: str, user_input: str, data) -> str:
    """
    Formats any JSON response into a clean HTML box.
    Works regardless of API response structure.
    """
    if data is None:
        return (
            f"<b>❌ No Data Found</b>\n\n"
            f"API returned no result for: <code>{user_input}</code>"
        )

    pairs = _flatten(data)

    if not pairs:
        return (
            f"<b>⚠️ Empty Response</b>\n\n"
            f"API returned an empty result for: <code>{user_input}</code>"
        )

    # Build rows — clean up key names
    rows = []
    for raw_key, val in pairs[:25]:   # cap at 25 fields
        # Pretty-print key: remove dots/brackets, title-case
        display_key = re.sub(r"[\.\[\]_]", " ", raw_key).strip().title()
        rows.append(f"<b>  • {display_key} :</b> <code>{val}</code>")

    body = "\n".join(rows)

    return (
        f"<b>╔══════════════════════════╗\n"
        f"║   📡 {api_name:<22}║\n"
        f"╚══════════════════════════╝</b>\n\n"
        f"<b>🔎 Input :</b> <code>{user_input}</code>\n"
        f"<b>━━━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
        f"{body}\n"
        f"<b>━━━━━━━━━━━━━━━━━━━━━━━━━━</b>\n\n"
        f"<i>🤖 Powered by OSINT Lookup Bot</i>"
    )


# ────────────────────────────────────────────────────────────
#  Register handlers
# ────────────────────────────────────────────────────────────
def register_api_handlers(app: Client):

    # ── Step 1: User clicks API button ──────────────────────
    @app.on_message(
        filters.private & filters.text &
        filters.regex(
            "^(" + "|".join(re.escape(k) for k in BUTTON_TO_API) + ")$"
        )
    )
    async def api_button_clicked(client: Client, message: Message):
        user_id = message.from_user.id
        api_key = BUTTON_TO_API.get(message.text)
        if not api_key:
            return

        if not await check_force_join(client, user_id):
            await message.reply(
                FORCE_JOIN_TEXT, reply_markup=force_join_keyboard(), parse_mode="html"
            )
            return

        cfg   = APIS[api_key]
        label = cfg.get("input_label", "value")
        ex    = cfg.get("input_example", "...")

        _waiting[user_id] = api_key

        await message.reply(
            f"<b>🔍 {cfg['name']}</b>\n\n"
            f"📥 Send your <b>{label}</b>:\n\n"
            f"<b>Example:</b> <code>{ex}</code>\n\n"
            f"Press <b>❌ Cancel</b> to go back.",
            reply_markup=cancel_keyboard(),
            parse_mode="html",
        )

    # ── Step 2: User sends the input value ──────────────────
    @app.on_message(filters.private & filters.text)
    async def input_received(client: Client, message: Message):
        user_id = message.from_user.id
        text    = message.text.strip()

        # Cancel
        if text == "❌ Cancel":
            _waiting.pop(user_id, None)
            await message.reply(
                "<b>✅ Cancelled.</b> Returned to main menu.",
                reply_markup=main_menu_keyboard(),
                parse_mode="html",
            )
            return

        # Not in waiting state
        if user_id not in _waiting:
            return

        # Force join re-check
        if not await check_force_join(client, user_id):
            _waiting.pop(user_id, None)
            await message.reply(
                FORCE_JOIN_TEXT, reply_markup=force_join_keyboard(), parse_mode="html"
            )
            return

        # Cooldown check
        if is_on_cooldown(user_id, COOLDOWN_SECONDS):
            sec = cooldown_remaining(user_id, COOLDOWN_SECONDS)
            await message.reply(
                f"<b>⏳ Wait {sec}s before next request.</b>",
                parse_mode="html",
            )
            return

        api_key = _waiting.pop(user_id)
        cfg     = APIS[api_key]
        url     = build_url(cfg, text)

        set_cooldown(user_id)

        proc = await message.reply(
            f"<b>⏳ Querying {cfg['name']}...</b>",
            parse_mode="html",
        )

        data = await fetch(url)

        await proc.delete()

        result = format_response(cfg["name"], text, data)
        await message.reply(result, parse_mode="html")
        await message.reply(
            "📋 Use the menu below:", reply_markup=main_menu_keyboard()
        )

        increment_search(user_id)
        logger.info(f"User {user_id} | {cfg['name']} | input={text}")
