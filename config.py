# ============================================================
#              OSINT NUMBER LOOKUP BOT - CONFIG
# ============================================================

# ─── BOT CREDENTIALS ────────────────────────────────────────
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
API_ID    = 123456
API_HASH  = "your_api_hash_here"
OWNER_ID  = 123456789

# ============================================================
#   FORCE JOIN SETTINGS
# ============================================================

# Force join ON karna ho → True
# Force join OFF karna ho → False
FORCE_JOIN = True

# ─── CHANNELS / GROUPS LIST ─────────────────────────────────
#
#   PUBLIC channel/group:
#     "id"   → "@username"          (@ ke saath)
#     "link" → "https://t.me/username"
#
#   PRIVATE channel/group:
#     "id"   → -100xxxxxxxxxx       (numeric ID, integer)
#     "link" → "https://t.me/+xxxxxxxxxxxxxxxx"  (invite link)
#
#   IMPORTANT (Private ke liye):
#     Bot ko us channel/group ka ADMIN banana padega
#     tabhi wo membership check kar payega.
#
# ────────────────────────────────────────────────────────────

FORCE_JOIN_CHANNELS = [

    # ── Public Channel example ──────────────────────────────
    {
        "name": "Main Channel",
        "id":   "@yourchannel",                        # public username
        "link": "https://t.me/yourchannel",
    },

    # ── Private Channel example ─────────────────────────────
    {
        "name": "Private VIP Channel",
        "id":   -1001234567890,                        # numeric ID (integer)
        "link": "https://t.me/+abcdefghijklmnop",      # private invite link
    },

    # ── Private Group example ───────────────────────────────
    {
        "name": "Private Group",
        "id":   -1009876543210,                        # numeric ID (integer)
        "link": "https://t.me/+xxxxxxxxxxxxxxxxx",     # private invite link
    },

]

# ─── MENU BUTTON NAMES ──────────────────────────────────────
BUTTON_NAMES = {
    "btn1": "🔍 Lookup 1",
    "btn2": "📡 Lookup 2",
    "btn3": "🚗 Lookup 3",
    "btn4": "🌐 Lookup 4",
    "btn5": "🛰️ Lookup 5",
    "support": "💬 Support",
    "updates": "📢 Updates",
    "group":   "👥 OSINT Group",
    "account": "👤 My Account",
}

# ============================================================
#   API CONFIGURATIONS
#
#   Sirf yeh fields bharo — code nahi chhuna padega:
#
#   url           → Base API URL
#   input_param   → URL mein user input ka param naam (?num=, ?rc=, etc.)
#   key_param     → API key param naam (&api_key=) — blank agar key nahi
#   key_value     → Aapki actual API key — blank agar key nahi
#   input_label   → Bot user ko kya type karne ko bolega
#   input_example → Example jo bot dikhayega
# ============================================================

APIS = {

    "btn1": {
        "name":          "Lookup 1",
        "url":           "https://your-api-1.vercel.app/endpoint",
        "input_param":   "num",
        "key_param":     "",
        "key_value":     "",
        "input_label":   "phone number",
        "input_example": "+919876543210",
    },

    "btn2": {
        "name":          "Lookup 2",
        "url":           "https://your-api-2.vercel.app/endpoint",
        "input_param":   "rc",
        "key_param":     "api_key",
        "key_value":     "YOUR_KEY_HERE",
        "input_label":   "RC number",
        "input_example": "MH12AB1234",
    },

    "btn3": {
        "name":          "Lookup 3",
        "url":           "https://your-api-3.vercel.app/endpoint",
        "input_param":   "uid",
        "key_param":     "",
        "key_value":     "",
        "input_label":   "UID",
        "input_example": "12022250",
    },

    "btn4": {
        "name":          "Lookup 4",
        "url":           "",
        "input_param":   "",
        "key_param":     "",
        "key_value":     "",
        "input_label":   "value",
        "input_example": "",
    },

    "btn5": {
        "name":          "Lookup 5",
        "url":           "",
        "input_param":   "",
        "key_param":     "",
        "key_value":     "",
        "input_label":   "value",
        "input_example": "",
    },
}

# ─── EXTERNAL LINKS ─────────────────────────────────────────
SUPPORT_LINK  = "https://t.me/yoursupport"
UPDATES_LINK  = "https://t.me/yourupdates"
GROUP_LINK    = "https://t.me/yourosintgroup"

# ─── ANTI-SPAM COOLDOWN ─────────────────────────────────────
COOLDOWN_SECONDS = 5

# ─── DATABASE ───────────────────────────────────────────────
DB_PATH = "database/users.db"
