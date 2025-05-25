# ============================
# CONFIG.PY – MAIN SETTINGS
# ============================

# Unique identifier for this E-Box
EBOX_NAME = "E-Box MC3"

# Window titles for detection
PLC_WINDOW_TITLE = "PLC Server"
AIRPORT_WINDOW_TITLE = "AIRPORT SYSTEM"

# Telegram bot token (from @BotFather)
BOT_TOKEN = "xxxx"

# Telegram chat IDs
CHAT_ID_PLC = "-100xxxx"          # Channel for PLC captures
CHAT_ID_AIRPORT = "-100xxxx"      # Channel for Airport captures
CHAT_ID_COMMANDS = "-100xxxx"     # Group for manual commands

# Active time window for automatic screenshots (hours and days)
ACTIVE_HOURS = {
    "start": "07:00",          # Start time (inclusive)
    "end": "15:30",            # End time (inclusive)
    "days": [0, 1, 2, 3, 4]    # Active days: 0 = Monday to 4 = Friday
}

# Screenshot frequency (in minutes) per application
CAPTURE_INTERVAL_PLC_MINUTES = 30
CAPTURE_INTERVAL_AIRPORT_MINUTES = 60
