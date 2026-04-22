import time
import logging
import re
from pyrogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
)
from config import BUTTON_NAMES, FORCE_JOIN_CHANNELS, FORCE_JOIN

logger = logging.getLogger(__name__)

# ─── COOLDOWN ───────────────────────────────────────────────
_cooldown: dict[int, float] = {}

def is_on_cooldown(user_id: int, seconds: int) -> bool:
    return (time.time() - _cooldown.get(user_id, 0)) < seconds

def set_cooldown(user_id: int):
    _cooldown[user_id] = time.time()

def cooldown_remaining(user_id: int, seconds: int) -> int:
    return max(0, int(seconds - (time.time() - _cooldown.get(user_id, 0))))


# ─── KEYBOARDS ──────────────────────────────────────────────

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    bn = BUTTON_NAMES
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(bn["btn1"]), KeyboardButton(bn["btn2"])],
            [KeyboardButton(bn["btn3"]), KeyboardButton(bn["btn4"])],
            [KeyboardButton(bn["btn5"])],
            [KeyboardButton(bn["support"]), KeyboardButton(bn["updates"])],
            [KeyboardButton(bn["group"]),   KeyboardButton(bn["account"])],
        ],
        resize_keyboard=True,
    )


def cancel_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton("❌ Cancel")]],
        resize_keyboard=True,
    )


def force_join_keyboard() -> InlineKeyboardMarkup:
    """
    Dynamically builds join buttons for ALL channels in config.
    Works for both public (@username) and private (invite link).
    """
    rows = []
    for ch in FORCE_JOIN_CHANNELS:
        name = ch.get("name", "Channel")
        link = ch.get("link", "")
        if link:
            rows.append([InlineKeyboardButton(f"➕ {name}", url=link)])

    rows.append([InlineKeyboardButton("✅ Verify Membership", callback_data="verify_join")])
    return InlineKeyboardMarkup(rows)


def link_keyboard(text: str, url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton(text, url=url)]])
