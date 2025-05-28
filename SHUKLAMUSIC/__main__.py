import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from SHUKLAMUSIC import LOGGER, app, userbot
from SHUKLAMUSIC.core.call import SHUKLA
from SHUKLAMUSIC.misc import sudo
from SHUKLAMUSIC.plugins import ALL_MODULES
from SHUKLAMUSIC.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

async def main():
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER(__name__).error("String session not filled. Please fill at least one STRINGx.")
        return

    await sudo()

    try:
        gbanned_users = await get_gbanned()
        banned_users = await get_banned_users()
        for user_id in gbanned_users + banned_users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER(__name__).warning(f"Error fetching banned users: {e}")

    await app.start()

    for module in ALL_MODULES:
        importlib.import_module("SHUKLAMUSIC.plugins." + module)

    LOGGER("SHUKLAMUSIC.plugins").info("All features loaded successfully.")

    await userbot.start()
    await SHUKLA.start()

    try:
        await SHUKLA.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("SHUKLAMUSIC").error(
            "Please start a voice chat in your log group/channel.\n\nBot cannot start streaming."
        )
        return
    except Exception as e:
        LOGGER("SHUKLAMUSIC").warning(f"Stream call error: {e}")

    await SHUKLA.decorators()

    LOGGER("SHUKLAMUSIC").info("╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎ MADE BY MR SHIVANSH\n╚═════ஜ۩۞۩ஜ════╝")

    try:
        await idle()
    finally:
        await SHUKLA.stop()
        await userbot.stop()
        await app.stop()
        LOGGER("SHUKLAMUSIC").info("Bot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped manually.")
