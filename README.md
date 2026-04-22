# 🕵️ OSINT Number Lookup Bot

A production-ready Telegram bot built with **Python + Pyrogram** that performs phone number OSINT lookups using 5 different APIs. Features force-join protection, anti-spam cooldown, SQLite user tracking, and a clean premium UI.

---

## 📁 Project Structure

```
osint_bot/
├── main.py                  # Entry point
├── config.py                # All configuration (edit this!)
├── requirements.txt
├── README.md
├── bot.log                  # Auto-generated at runtime
├── handlers/
│   ├── __init__.py
│   ├── start.py             # /start command + verify callback
│   ├── forcejoin.py         # Force join checker
│   ├── menu.py              # /menu command
│   ├── api_handler.py       # Phone lookup (5 APIs)
│   └── extra.py             # Support / Updates / Group / My Account
├── database/
│   ├── __init__.py
│   ├── db.py                # SQLite operations
│   └── users.db             # Auto-created at runtime
└── utils/
    ├── __init__.py
    └── helpers.py           # Keyboards, validators, formatters, cooldown
```

---

## ⚙️ Configuration (`config.py`)

Open `config.py` and fill in the following:

### 1. Bot Credentials

```python
BOT_TOKEN = "123456:ABC-DEF..."   # From @BotFather on Telegram
API_ID    = 123456                 # From https://my.telegram.org
API_HASH  = "abcdef1234567890"     # From https://my.telegram.org
OWNER_ID  = 123456789             # Your personal Telegram user ID
```

**How to get them:**
- **BOT_TOKEN** → Open Telegram → search `@BotFather` → `/newbot`
- **API_ID / API_HASH** → Go to https://my.telegram.org → Log in → "API Development Tools"
- **OWNER_ID** → Message `@userinfobot` on Telegram

---

### 2. Force Join Channels

```python
FORCE_JOIN_CHANNELS = [
    {
        "name": "Main Channel",
        "username": "@yourchannel",
        "link": "https://t.me/yourchannel"
    },
    # Add more channels as needed
]
```

> ⚠️ **Important:** Add your bot as an **admin** to each channel (at least "Add Members" permission) so it can check membership.

---

### 3. API Keys

Register and obtain free/paid keys from:

| Button | API Provider | Registration |
|--------|-------------|--------------|
| btn1 | NumVerify | https://numverify.com |
| btn2 | Abstract API | https://www.abstractapi.com/phone-validation-api |
| btn3 | NumLookupAPI | https://numlookupapi.com |
| btn4 | Phone Validator | https://www.phonevalidator.com |
| btn5 | IP-API Phone | https://phoneapi.net |

```python
APIS = {
    "btn1": { "key": "YOUR_NUMVERIFY_KEY", ... },
    "btn2": { "key": "YOUR_ABSTRACTAPI_KEY", ... },
    # etc.
}
```

---

### 4. Button Names (optional)

```python
BUTTON_NAMES = {
    "btn1": "🔍 NumVerify Lookup",
    "btn2": "📡 Abstract API Lookup",
    # Change to any display name you want
}
```

---

### 5. External Links

```python
SUPPORT_LINK  = "https://t.me/yoursupport"
UPDATES_LINK  = "https://t.me/yourupdates"
GROUP_LINK    = "https://t.me/yourosintgroup"
```

---

## 🚀 Setup & Running

### Local (Development)

```bash
# 1. Clone or download the project
git clone https://github.com/yourname/osint-bot.git
cd osint-bot

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Edit config
nano config.py   # Fill in all values

# 5. Run
python main.py
```

---

### VPS (Production — systemd)

```bash
# 1. Upload project to VPS (e.g. via SCP or git clone)
# 2. Install Python 3.11+
sudo apt update && sudo apt install python3 python3-pip python3-venv -y

# 3. Set up virtualenv and install deps
cd /opt/osint_bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Edit config.py with your credentials

# 5. Create systemd service
sudo nano /etc/systemd/system/osintbot.service
```

Paste this into the service file:

```ini
[Unit]
Description=OSINT Number Lookup Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/osint_bot
ExecStart=/opt/osint_bot/venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
# 6. Enable and start
sudo systemctl daemon-reload
sudo systemctl enable osintbot
sudo systemctl start osintbot

# 7. Check status
sudo systemctl status osintbot

# 8. View live logs
sudo journalctl -u osintbot -f
```

---

### VPS (Production — screen/tmux)

```bash
# Using screen
screen -S osintbot
source venv/bin/activate
python main.py
# Detach: Ctrl+A then D

# Using tmux
tmux new -s osintbot
source venv/bin/activate
python main.py
# Detach: Ctrl+B then D
```

---

## 🔁 How It Works

### Force Join Flow

```
User sends /start
       │
       ▼
Check all FORCE_JOIN_CHANNELS
       │
  ┌────┴────┐
  │ Joined? │
  └────┬────┘
       │ No → Show join buttons + Verify button
       │ Yes → Show welcome + main menu
       │
  User clicks Verify
       │
       ▼
Recheck channels
  Not joined → Show error again
  All joined → Show welcome + menu
```

> Force join is checked on **every** button press and search, not just /start.

---

### API Lookup Flow

```
User clicks API button (btn1–btn5)
    → Bot shows "Send number with country code"
    → User sends +919876543210
    → Bot validates format
    → Bot calls the selected API
    → Response is parsed and normalised
    → Result shown in formatted box
    → Search count incremented in DB
```

---

## 🗄️ Database

SQLite database auto-created at `database/users.db`.

**Schema:**
```sql
CREATE TABLE users (
    user_id      INTEGER PRIMARY KEY,
    name         TEXT,
    username     TEXT,
    search_count INTEGER DEFAULT 0,
    joined_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🛡️ Security Features

| Feature | Detail |
|---------|--------|
| Force Join | Checked on every interaction |
| Anti-Spam | Configurable cooldown (`COOLDOWN_SECONDS` in config.py) |
| Input Validation | E.164 phone format enforced |
| Exception Handling | All API calls wrapped in try/except |
| Logging | Full request + error logging to `bot.log` |

---

## 📦 Dependencies

```
pyrogram==2.0.106   # Telegram MTProto client
TgCrypto==1.2.5     # Crypto acceleration for Pyrogram
aiohttp==3.9.5      # Async HTTP for API calls
```

---

## 🧰 Troubleshooting

**Bot not responding:**
- Check `bot.log` for errors
- Ensure `BOT_TOKEN`, `API_ID`, `API_HASH` are correct

**Force join not working:**
- Make sure the bot is an admin in each channel
- Verify channel usernames are correct (with or without `@`)

**API returning no data:**
- Check API key validity
- Some APIs require number in E.164 format (`+CC...`)
- Verify your API plan hasn't expired

**`UserNotParticipant` error in logs:**
- Normal — it means the user hasn't joined the channel yet

---

## 📝 License

MIT License — free to use, modify, and distribute.
