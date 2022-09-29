# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de
# Kit-Ub

from pyrogram import idle
from uvloop import install

from config import BOT_VER
from Cilik import BOTLOG_CHATID, LOGGER, LOOP, aiosession, bots
from Cilik.helpers.misc import git, heroku

MSG_ON = """
✅ **KitUb Activated.**

**🤖 Userbot Version -** `{}`
**Ketik** `.kit` **untuk Mengecheck Bot**
"""


async def main():
    for bot in bots:
        try:
            await bot.start()
            bot.me = await bot.get_me()
            await bot.join_chat("bebasterserahya")
            await bot.join_chat("killuaroom")
            await bot.join_chat("diarydam")
            await bot.send_message(BOTLOG_CHATID, MSG_ON.format(BOT_VER))
        except Exception as a:
            LOGGER("main").warning(a)
    await idle()
    await aiosession.close()


if __name__ == "__main__":
    LOGGER("Kit").info("Starting KitUb")
    LOGGER("Kit").info(f"Total Clients = {len(bots)} Users")
    install()
    git()
    heroku()
    LOGGER("Kit").info(f"KitUb v{BOT_VER} ⚙️[⚡ Activated ⚡]")
    LOOP.run_until_complete(main())
