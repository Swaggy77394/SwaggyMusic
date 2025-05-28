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


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("String session not filled. Please fill at least one Pyrogram session.")
        exit()

    await sudo()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)

        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER(__name__).warning(f"Failed to fetch banned users: {e}")

    await app.start()

    for all_module in ALL_MODULES:
        importlib.import_module("SHUKLAMUSIC.plugins." + all_module)

    LOGGER("SHUKLAMUSIC.plugins").info("All features loaded successfully!")

    await userbot.start()
    await SHUKLA.start()

    try:
        await SHUKLA.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("SHUKLAMUSIC").error(
            "❌ Please start a voice chat in your log group/channel before running the bot."
        )
        exit()
    except Exception as e:
        LOGGER("SHUKLAMUSIC").warning(f"Stream call failed: {e}")

    await SHUKLA.decorators()

    LOGGER("SHUKLAMUSIC").info("🚀 Stranger Music Bot Started Successfully!")
    await idle()

    # Cleanup
    await app.stop()
    await userbot.stop()
    LOGGER("SHUKLAMUSIC").info("🛑 Stranger Music Bot Stopped.")


if __name__ == "__main__":
    import asyncio
    asyncio.run(init())
