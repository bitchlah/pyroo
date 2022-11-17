# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio
import time
from platform import python_version

from pyrogram import Client
from pyrogram import __version__ as versipyro
from pyrogram import filters
from pyrogram.types import Message

from config import ALIVE_EMOJI, ALIVE_LOGO, ALIVE_TEKS_CUSTOM, BOT_VER, CHANNEL
from config import GROUP
from Cilik import CMD_HELP, StartTime
from Cilik.helpers.basic import edit_or_reply
from Cilik.helpers.PyroHelpers import ReplyCheck
from Cilik.utils import get_readable_time

from .help import add_command_help

modules = CMD_HELP
emoji = ALIVE_EMOJI
alive_text = ALIVE_TEKS_CUSTOM


@Client.on_message(filters.command(["alive", "alby"], [".", "-", "^", "!", "?"]) & filters.me)
async def alive(client: Client, message: Message):
    xx = await message.reply("🕺")
    await asyncio.sleep(2)
    apa = client.send_video if ALIVE_LOGO.endswith(".mp4") else client.send_photo
    uptime = await get_readable_time((time.time() - StartTime))
    capt = (
        f"✘ [ALBY-Pyrobot](https://github.com/PunyaAlby/ALBY-Pyrobot) ✘\n\n"
        f"<b>{alive_text}</b>\n\n"
        f"✘ <b>Owner: </b> {client.me.mention} \n"
        f"✘ <b>Modul: </b> <code> Modules</code> \n"
        f"✘ <b>Bot Version: </b> <code>{BOT_VER}</code> \n"
        f"✘ <b>Python: </b> <code>{python_version()}</code> \n"
        f"✘ <b>Pyrogram: </b> <code>{versipyro}</code> \n"
        f"✘ <b>Support :</b> [Group](https://t.me/ruangdiskusikami) \n\n"
        f"✘ <b>Update :</b> [Channel](https://t.me/ruangprojects) \n\n"
    )
    await asyncio.gather(
        xx.delete(),
        apa(
            message.chat.id,
            ALIVE_LOGO,
            caption=capt,
            reply_to_message_id=ReplyCheck(message),
        ),
    )

add_command_help(
    "alive",
    [
        [".alby or .alive", "Perintah ini untuk memeriksa userbot anda berfungsi atau tidak."],
    ],
)
