import os
from typing import List

API_ID = os.environ.get("API_ID", "37891385")
API_HASH = os.environ.get("API_HASH", "2d14a3ad7a0ea5ec9167fb1623f56fa2")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN = int(os.environ.get("ADMIN", "8420494874"))
PICS = (os.environ.get("PICS", "")).split()

LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1003386051877"))

DB_URI = os.environ.get("DB_URI", "")
DB_NAME = os.environ.get("DB_NAME", "RoyalityBots")

IS_FSUB = os.environ.get("IS_FSUB", "False").lower() == "true"  # Set "True" For Enable Force Subscribe
AUTH_CHANNELS = list(map(int, os.environ.get("AUTH_CHANNEL", "-100******** -100*********").split())) # Add Multiple channel ids

EMOJIS = [
    "👍", "❤️", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "😢",
    "🎉", "🤩", "🙏", "👌", "🕊", "🤡", "🥱", "🥴", "😍", "🤷‍♂️",
    "❤️‍🔥", "🌚", "💯", "🤣", "⚡", "🏆", "🗿", "😐", "🤨", "🍾",
    "💋", "😈", "😴", "😭", "🤓", "👻", "👨‍💻", "👀", "🙈", "🤷‍♀️",
    "😇", "🤝", "✍️", "🤗", "🫡", "😨", "🧑‍🎄", "🎄", "⛄", "🤪",
    "🆒", "💘", "🙊", "🦄", "😘", "🙉", "💊", "😎", "👾", "🤷"
]
