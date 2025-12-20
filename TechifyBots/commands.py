import random
import re
import asyncio
from collections import defaultdict

from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, PeerIdInvalid, InputUserDeactivated
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from config import *
from Script import text
from .db import tb
from .fsub import get_fsub


# ---------------- BUTTON PARSER (FOR BROADCAST) ---------------- #

def parse_button_markup(text: str):
    lines = text.split("\n")
    buttons = []
    final_text_lines = []

    for line in lines:
        row = []
        parts = line.split("||")
        is_button_line = True

        for part in parts:
            match = re.fullmatch(r"\[(.+?)\]\((https?://[^\s]+)\)", part.strip())
            if match:
                row.append(InlineKeyboardButton(match[1], url=match[2]))
            else:
                is_button_line = False
                break

        if is_button_line and row:
            buttons.append(row)
        else:
            final_text_lines.append(line)

    return (
        InlineKeyboardMarkup(buttons) if buttons else None,
        "\n".join(final_text_lines).strip()
    )


# ---------------- START COMMAND ---------------- #

@Client.on_message(filters.command("start"))
async def start_cmd(client: Client, message: Message):

    # Save user
    if await tb.get_user(message.from_user.id) is None:
        await tb.add_user(message.from_user.id, message.from_user.first_name)

        bot = await client.get_me()
        await client.send_message(
            LOG_CHANNEL,
            text.LOG.format(
                message.from_user.id,
                getattr(message.from_user, "dc_id", "N/A"),
                message.from_user.first_name or "N/A",
                f"@{message.from_user.username}" if message.from_user.username else "N/A",
                bot.username
            )
        )

    # Force subscribe check
    if IS_FSUB and not await get_fsub(client, message):
        return

    bot = await client.get_me()
    BOT_USERNAME = bot.username

    await message.reply_photo(
        photo=random.choice(PICS),
        caption=text.START.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    '⇆ 𝖠𝖽𝖽 𝖬𝖾 𝖳𝗈 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉 ⇆',
                    url=f'https://t.me/{BOT_USERNAME}?startgroup=botstart'
                )
            ],
            [
                InlineKeyboardButton('ℹ️ 𝖠𝖻𝗈𝗎𝗍', callback_data='about'),
                InlineKeyboardButton('📚 𝖧𝖾𝗅𝗉', callback_data='help')
            ],
            [
                InlineKeyboardButton(
                    '⇆ 𝖠𝖽𝖽 𝖬𝖾 𝖳𝗈 𝖸𝗈𝗎𝗋 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 ⇆',
                    url=f'https://t.me/{BOT_USERNAME}?startchannel=botstart'
                )
            ]
        ])
    )


# ---------------- HELP COMMAND ---------------- #

@Client.on_message(filters.command("help") & filters.private)
async def help_cmd(client: Client, message: Message):
    reply = await message.reply(
        text=(
            "❓ <b>𝘏𝘢𝘷𝘪𝘯𝘨 𝘛𝘳𝘰𝘶𝘣𝘭𝘦?</b>\n\n"
            "𝘐𝘧 𝘺𝘰𝘶'𝘳𝘦 𝘧𝘢𝘤𝘪𝘯𝘨 𝘢𝘯𝘺 𝘱𝘳𝘰𝘣𝘭𝘦𝘮 𝘸𝘩𝘪𝘭𝘦 𝘶𝘴𝘪𝘯𝘨 𝘵𝘩𝘦 𝘣𝘰𝘵 "
            "𝘰𝘳 𝘪𝘵𝘴 𝘤𝘰𝘮𝘮𝘢𝘯𝘥𝘴, 𝘱𝘭𝘦𝘢𝘴𝘦 𝘸𝘢𝘵𝘤𝘩 "
            "𝘵𝘩𝘦 𝘵𝘶𝘵𝘰𝘳𝘪𝘢𝘭 𝘷𝘪𝘥𝘦𝘰 𝘣𝘦𝘭𝘰𝘸.\n\n"
            "🎥 𝘛𝘩𝘦 𝘷𝘪𝘥𝘦𝘰 𝘸𝘪𝘭𝘭 𝘤𝘭𝘦𝘢𝘳𝘭𝘺 "
            "𝘦𝘹𝘱𝘭𝘢𝘪𝘯 𝘩𝘰𝘸 𝘵𝘰 𝘶𝘴𝘦 "
            "𝘦𝘢𝘤𝘩 𝘧𝘦𝘢𝘵𝘶𝘳𝘦.\n\n"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎬 𝘞𝘢𝘵𝘤𝘩 𝘛𝘶𝘵𝘰𝘳𝘪𝘢𝘭", url="https://youtu.be/")]
        ])
    )

    await asyncio.sleep(300)
    await reply.delete()
    try:
        await message.delete()
    except:
        pass


# ---------------- STATS COMMAND ---------------- #

@Client.on_message(filters.command("stats") & filters.private & filters.user(ADMIN))
async def total_users(client: Client, message: Message):
    users = await tb.get_all_users()
    await message.reply_text(
        f"👥 Total Users: {len(users)}",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🎭 Close", callback_data="close")]]
        )
    )


# ---------------- AUTO REACTION ---------------- #

@Client.on_message(filters.group | filters.channel)
async def send_reaction(client: Client, msg: Message):
    try:
        await msg.react(random.choice(EMOJIS))
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await msg.react(random.choice(EMOJIS))
    except Exception as e:
        print("Reaction error:", e)


# ---------------- BROADCAST ---------------- #

@Client.on_message(filters.command("broadcast") & filters.private & filters.user(ADMIN))
async def broadcasting_func(client: Client, message: Message):

    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast.")

    msg = await message.reply("📢 Starting broadcast...")
    to_copy = message.reply_to_message

    users = await tb.get_all_users()
    total = len(users)

    success = set()
    failed = 0

    raw_text = to_copy.caption or to_copy.text or ""
    reply_markup, clean_text = parse_button_markup(raw_text)

    for i, user in enumerate(users, start=1):
        uid = user.get("user_id")

        try:
            uid = int(uid)
            await to_copy.copy(uid, caption=clean_text, reply_markup=reply_markup)
            success.add(uid)

        except (UserIsBlocked, PeerIdInvalid, InputUserDeactivated):
            await tb.delete_user(uid)
            failed += 1

        except FloodWait as e:
            await asyncio.sleep(e.value)

        except Exception:
            await tb.delete_user(uid)
            failed += 1

        if i % 20 == 0:
            await msg.edit(
                f"Broadcasting...\n\n"
                f"Total: {total}\n"
                f"Success: {len(success)}\n"
                f"Failed: {failed}\n"
                f"Progress: {i}/{total}"
            )

        await asyncio.sleep(0.05)

    await msg.edit(
        f"Broadcast Completed\n\n"
        f"Total: {total}\n"
        f"Success: {len(success)}\n"
        f"Failed: {failed}",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🎭 Close", callback_data="close")]]
        )
    )
