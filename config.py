# ============================================================
#              OSINT NUMBER LOOKUP BOT - CONFIG
# ============================================================

# ─── BOT CREDENTIALS ────────────────────────────────────────
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
API_ID    = 123456
API_HASH  = "your_api_hash_here"
OWNER_ID  = 123456789

# ─── FORCE JOIN CHANNELS ────────────────────────────────────
FORCE_JOIN_CHANNELS = [
    {
        "name": "Main Channel",
        "username": "@yourchannel1",
        "link": "https://t.me/yourchannel1"
    },
    {
        "name": "Updates Channel",
        "username": "@yourchannel2",
        "link": "https://t.me/yourchannel2"
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
#   API CONFIGURATIONS — FILL KARO, CODE NAHI CHHUNA PADEGA
#
#   Har API ke liye sirf 3 cheezein chahiye:
#
#   1. "url"        → Poora base URL (without input value)
#                     Example: "https://myapi.vercel.app/search"
#
#   2. "input_param"→ URL mein input ka parameter naam
#                     Example: "num", "rc", "uid", "q", "phone"
#                     Yahi user ka text is param mein jayega
#
#   3. "key_param"  → API key ka parameter naam
#                     Example: "api_key", "token", "access_key"
#                     Agar API mein key nahi chahiye → "" (blank)
#
#   4. "key_value"  → Aapki actual API key
#                     Agar key nahi chahiye → "" (blank)
#
#   5. "input_label"→ Bot user ko kya type karne ko bolega
#                     Example: "phone number", "RC number", "UID"
#
#   6. "input_example" → Example jo bot dikhayega
#                     Example: "+919876543210", "MH12AB1234"
#
# ─── URL KAISE BANTA HAI ────────────────────────────────────
#
#   Key NAHI hai:
#     Final URL = url + ? + input_param + = + <user_input>
#     Eg: https://xyz.vercel.app/?num=+919876543210
#
#   Key HAI:
#     Final URL = url + ? + input_param + = + <user_input>
#                     + & + key_param + = + key_value
#     Eg: https://api.example.com/check?rc=MH12&api_key=mykey
#
#   Key IN URL hai (not as query param):
#     Toh url mein hi likh do:
#     "url": "https://api.example.com/mykey/check"
#     "key_param": ""   ← blank rakho
#
# ============================================================

APIS = {

    "btn1": {
        "name":          "Lookup 1",            # Display naam
        "url":           "https://your-api-1.vercel.app/endpoint",
        "input_param":   "num",                 # ?num=<user_input>
        "key_param":     "",                    # key nahi hai → blank
        "key_value":     "",
        "input_label":   "phone number",        # bot message mein dikhega
        "input_example": "+919876543210",       # example dikhayega
    },

    "btn2": {
        "name":          "Lookup 2",
        "url":           "https://your-api-2.vercel.app/endpoint",
        "input_param":   "rc",                  # ?rc=<user_input>
        "key_param":     "api_key",             # &api_key=<key_value>
        "key_value":     "YOUR_API_KEY_HERE",
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
        "url":           "https://your-api-4.vercel.app/endpoint",
        "input_param":   "q",
        "key_param":     "token",
        "key_value":     "YOUR_TOKEN_HERE",
        "input_label":   "search query",
        "input_example": "anything",
    },

    "btn5": {
        "name":          "Lookup 5",
        "url":           "https://your-api-5.vercel.app/endpoint",
        "input_param":   "number",
        "key_param":     "",
        "key_value":     "",
        "input_label":   "number",
        "input_example": "+911234567890",
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
