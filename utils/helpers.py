import time
import logging
import re
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import BUTTON_NAMES, FORCE_JOIN_CHANNELS

logger = logging.getLogger(__name__)

# ─── COOLDOWN STORE ─────────────────────────────────────────
_cooldown: dict[int, float] = {}


def is_on_cooldown(user_id: int, seconds: int) -> bool:
    """Return True if user is still within cooldown window."""
    last = _cooldown.get(user_id, 0)
    return (time.time() - last) < seconds


def set_cooldown(user_id: int):
    """Record the current timestamp for the user."""
    _cooldown[user_id] = time.time()


def cooldown_remaining(user_id: int, seconds: int) -> int:
    """Return remaining cooldown seconds."""
    last = _cooldown.get(user_id, 0)
    remaining = seconds - (time.time() - last)
    return max(0, int(remaining))


# ─── KEYBOARDS ──────────────────────────────────────────────

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Build the main reply keyboard from config button names."""
    bn = BUTTON_NAMES
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(bn["btn1"]), KeyboardButton(bn["btn2"])],
            [KeyboardButton(bn["btn3"]), KeyboardButton(bn["btn4"])],
            [KeyboardButton(bn["btn5"])],
            [KeyboardButton(bn["support"]), KeyboardButton(bn["updates"])],
            [KeyboardButton(bn["group"]), KeyboardButton(bn["account"])],
        ],
        resize_keyboard=True,
    )


def cancel_keyboard() -> ReplyKeyboardMarkup:
    """Keyboard shown while waiting for number input."""
    return ReplyKeyboardMarkup(
        [[KeyboardButton("❌ Cancel")]],
        resize_keyboard=True,
    )


def force_join_keyboard() -> InlineKeyboardMarkup:
    """Dynamically build inline join buttons + verify button."""
    rows = []
    for ch in FORCE_JOIN_CHANNELS:
        rows.append([InlineKeyboardButton(f"➕ {ch['name']}", url=ch["link"])])
    rows.append([InlineKeyboardButton("✅ Verify Membership", callback_data="verify_join")])
    return InlineKeyboardMarkup(rows)


def link_keyboard(text: str, url: str) -> InlineKeyboardMarkup:
    """Single inline button with a link."""
    return InlineKeyboardMarkup([[InlineKeyboardButton(text, url=url)]])


# ─── VALIDATORS ─────────────────────────────────────────────

def is_valid_phone(number: str) -> bool:
    """Basic E.164 phone number validation."""
    pattern = re.compile(r"^\+?[1-9]\d{6,14}$")
    return bool(pattern.match(number.strip()))


def clean_number(number: str) -> str:
    """Strip spaces and normalise number."""
    return number.strip().replace(" ", "").replace("-", "")


# ─── RESPONSE PARSER ────────────────────────────────────────

def parse_api_response(api_name: str, data: dict) -> dict:
    """
    Normalise API responses from different providers into
    a consistent dict: {valid, number, country, carrier, location, line_type}
    """
    result = {
        "valid": False,
        "number": "N/A",
        "country": "N/A",
        "carrier": "N/A",
        "location": "N/A",
        "line_type": "N/A",
    }

    try:
        if api_name == "NumVerify":
            result["valid"]     = data.get("valid", False)
            result["number"]    = data.get("international_format", "N/A")
            result["country"]   = data.get("country_name", "N/A")
            result["carrier"]   = data.get("carrier", "N/A")
            result["location"]  = data.get("location", "N/A")
            result["line_type"] = data.get("line_type", "N/A")

        elif api_name == "Abstract API":
            result["valid"]     = data.get("valid", False)
            result["number"]    = data.get("phone", "N/A")
            country             = data.get("country", {})
            result["country"]   = country.get("name", "N/A") if isinstance(country, dict) else str(country)
            result["carrier"]   = data.get("carrier", "N/A")
            result["location"]  = data.get("country", {}).get("calling_code", "N/A")
            result["line_type"] = data.get("type", "N/A")

        elif api_name == "NumLookupAPI":
            result["valid"]     = data.get("valid", False)
            result["number"]    = data.get("number", "N/A")
            result["country"]   = data.get("country_name", "N/A")
            result["carrier"]   = data.get("carrier", "N/A")
            result["location"]  = data.get("location", "N/A")
            result["line_type"] = data.get("line_type", "N/A")

        elif api_name == "Phone Validator":
            result["valid"]     = str(data.get("status", "")).lower() == "success"
            result["number"]    = data.get("phone_number", "N/A")
            result["country"]   = data.get("country", "N/A")
            result["carrier"]   = data.get("carrier", "N/A")
            result["location"]  = data.get("city", "N/A")
            result["line_type"] = data.get("phone_type", "N/A")

        elif api_name == "IP-API Phone":
            result["valid"]     = data.get("valid", False)
            result["number"]    = data.get("number", "N/A")
            result["country"]   = data.get("countryName", "N/A")
            result["carrier"]   = data.get("carrier", "N/A")
            result["location"]  = data.get("timezones", ["N/A"])[0] if data.get("timezones") else "N/A"
            result["line_type"] = data.get("lineType", "N/A")

        else:
            # Generic fallback
            for key in ("valid", "number", "country", "carrier", "location", "line_type"):
                if key in data:
                    result[key] = data[key]

    except Exception as e:
        logger.error(f"Error parsing {api_name} response: {e}")

    return result


def format_result(api_name: str, parsed: dict) -> str:
    """Format the parsed result into a premium HTML box."""
    valid_icon = "✅" if parsed["valid"] else "❌"
    return f"""<b>╔══════════════════════╗
║   📡 OSINT LOOKUP RESULT   ║
╚══════════════════════╝</b>

<b>🔌 Source :</b> <code>{api_name}</code>
<b>📞 Number :</b> <code>{parsed['number']}</code>
<b>✔️ Valid   :</b> {valid_icon} <code>{parsed['valid']}</code>

<b>┌─── 🌍 LOCATION INFO ───┐</b>
<b>  🗺️ Country  :</b> <code>{parsed['country']}</code>
<b>  📍 Region   :</b> <code>{parsed['location']}</code>
<b>└────────────────────────┘</b>

<b>┌─── 📶 CARRIER INFO ────┐</b>
<b>  📡 Carrier  :</b> <code>{parsed['carrier']}</code>
<b>  📲 Line Type:</b> <code>{parsed['line_type']}</code>
<b>└────────────────────────┘</b>

<i>🤖 Powered by OSINT Lookup Bot</i>"""
