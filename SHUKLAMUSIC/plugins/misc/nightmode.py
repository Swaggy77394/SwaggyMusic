import random
from pyrogram import filters, Client, enums
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    ChatPermissions
)
from SHUKLAMUSIC import app
from SHUKLAMUSIC.mongo.nightmodedb import (
    nightdb,
    nightmode_on,
    nightmode_off,
    get_nightchats
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Valid ChatPermissions config
CLOSE_CHAT = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False
)

OPEN_CHAT = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_add_web_page_previews=True,
    can_change_info=True,
    can_invite_users=True,
    can_pin_messages=True
)

# Buttons for reply markup
buttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("๏ ᴇɴᴀʙʟᴇ ๏", callback_data="add_night"),
            InlineKeyboardButton("๏ ᴅɪsᴀʙʟᴇ ๏", callback_data="rm_night")
        ]
    ]
)

# Command to show nightmode button
@app.on_message(filters.command("nightmode") & filters.group)
async def _nightmode(_, message):
    return await message.reply_photo(
        photo="https://telegra.ph//file/06649d4d0bbf4285238ee.jpg",
        caption="**ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ ᴏʀ ᴅɪsᴀʙʟᴇ ɴɪɢʜᴛᴍᴏᴅᴇ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.**",
        reply_markup=buttons
    )

# Handle button callbacks
@app.on_callback_query(filters.regex("^(add_night|rm_night)$"))
async def nightcb(_, query: CallbackQuery):
    data = query.data
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    check_night = await nightdb.find_one({"chat_id": chat_id})

    administrators = []
    async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        administrators.append(m.user.id)

    if user_id not in administrators:
        return await query.answer("Only admins can do this.", show_alert=True)

    if data == "add_night":
        if check_night:
            await query.message.edit_caption("**๏ ɴɪɢʜᴛᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.**")
        else:
            await nightmode_on(chat_id)
            await query.message.edit_caption(
                "**๏ ᴀᴅᴅᴇᴅ ᴄʜᴀᴛ ᴛᴏ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ . ᴛʜɪs ɢʀᴏᴜᴘ ᴡɪʟʟ ʙᴇ ᴄʟᴏsᴇᴅ ᴏɴ 𝟷𝟸ᴀᴍ [IST] ᴀɴᴅ ᴡɪʟʟ ᴏᴘᴇɴᴇᴅ ᴏɴ 𝟶𝟼ᴀᴍ [IST] .**"
            )
    elif data == "rm_night":
        if check_night:
            await nightmode_off(chat_id)
            await query.message.edit_caption("**๏ ɴɪɢʜᴛᴍᴏᴅᴇ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ !**")
        else:
            await query.message.edit_caption("**๏  ɴɪɢʜᴛᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ.**")

# Closing group at night
async def start_nightmode():
    chats = await get_nightchats()
    for chat in chats:
        try:
            chat_id = int(chat["chat_id"])
            await app.send_photo(
                chat_id,
                photo="https://telegra.ph//file/06649d4d0bbf4285238ee.jpg",
                caption="**ɢʀᴏᴜᴘ ɪs ᴄʟᴏsɪɴɢ. ɢᴏᴏᴅ ɴɪɢʜᴛ ᴇᴠᴇʀʏᴏɴᴇ !**"
            )
            await app.set_chat_permissions(chat_id, CLOSE_CHAT)
        except Exception as e:
            print(f"[ERROR] Failed to close chat {chat['chat_id']} - {e}")

# Reopening group in morning
async def close_nightmode():
    chats = await get_nightchats()
    for chat in chats:
        try:
            chat_id = int(chat["chat_id"])
            await app.send_photo(
                chat_id,
                photo="https://telegra.ph//file/14ec9c3ff42b59867040a.jpg",
                caption="**ɢʀᴏᴜᴘ ɪs ᴏᴘᴇɴɪɴɢ. ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ ᴇᴠᴇʀʏᴏɴᴇ !**"
            )
            await app.set_chat_permissions(chat_id, OPEN_CHAT)
        except Exception as e:
            print(f"[ERROR] Failed to open chat {chat['chat_id']} - {e}")

# Scheduler jobs
scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(start_nightmode, trigger="cron", hour=23, minute=59)
scheduler.add_job(close_nightmode, trigger="cron", hour=6, minute=1)
scheduler.start()
