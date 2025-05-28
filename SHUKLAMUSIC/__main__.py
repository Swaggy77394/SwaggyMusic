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


async def startup():
    if not any([config.STRING1, config.STRING2, config.STRING3, config.STRING4, config.STRING5]):
        LOGGER(__name__).error("String session missing. Please fill at least one Pyrogram session.")
        exit(1)

    await sudo()

    try:
        users = await get_gbanned()
        BANNED_USERS.update(users)
        users = await get_banned_users()
        BANNED_USERS.update(users)
    except Exception as e:
        LOGGER(__name__).warning(f"Failed to fetch banned users: {e}")

    await app.start()
    for module in ALL_MODULES:
        importlib.import_module("SHUKLAMUSIC.plugins." + module)
    LOGGER("SHUKLAMUSIC.plugins").info("All features loaded successfully.")
    
    await userbot.start()
    await SHUKLA.start()

    try:
        await SHUKLA.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("SHUKLAMUSIC").error("Please start a voice chat in the log group/channel.")
        exit(1)
    except Exception as e:
        LOGGER("SHUKLAMUSIC").warning(f"Stream call failed: {e}")

    await SHUKLA.decorators()
    LOGGER("SHUKLAMUSIC").info("Bot started successfully!")


async def shutdown():
    LOGGER("SHUKLAMUSIC").info("Stopping bot...")
    await SHUKLA.stop()
    await userbot.stop()
    await app.stop()
    LOGGER("SHUKLAMUSIC").info("Bot stopped.")


async def main():
    await startup()
    try:
        await idle()
    finally:
        await shutdown()


if __name__ == "__main__":
    asyncio.run(main())
