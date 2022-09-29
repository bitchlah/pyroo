# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de
# Dam-PyroBot

from gpytranslate import Translator
from pyrogram import Client, filters
from pyrogram.types import Message
from Cilik.helpers.basic import edit_or_reply

from Cilik.modules.Ubot.help import add_command_help


@Client.on_message(filters.me & filters.command(["tr", "trt", "translate"], [".", "-", "^", "!", "?"]))
async def translate(client: Client, message: Message):
    trl = Translator()
    if message.reply_to_message and (
        message.reply_to_message.text or message.reply_to_message.caption
    ):
        input_str = (
            message.text.split(None, 1)[1]
            if len(
                message.command,
            )
            != 1
            else None
        )
        target = input_str or "id"
        if message.reply_to_message.text:
            text = message.reply_to_message.text
        else:
            text = message.reply_to_message.caption
        try:
            tekstr = await trl(text, targetlang=target)
        except ValueError as err:
            await message.reply(
                f"**ERROR:** `{str(err)}`", parse_mode="Markdown"
            )
            return
    else:
        input_str = (
            message.text.split(None, 2)[1]
            if len(
                message.command,
            )
            != 1
            else None
        )
        text = message.text.split(None, 2)[2]
        target = input_str or "id"
        try:
            tekstr = await trl(text, targetlang=target)
        except ValueError as err:
            await message.reply(
                "**ERROR:** `{}`".format(str(err)), parse_mode="Markdown"
            )
            return
    await message.reply(
        f"**-⋟ Translated:** `{target}`\n```{tekstr.text}```\n\n**-⋟ Lang:** `{(await trl.detect(text))}`",
        parse_mode="Markdown",
    )


add_command_help(
    "translate",
    [
        [
            ".tr <kode bahasa> <text/reply>",
            "Menerjemahkan teks ke bahasa yang disetel. (Default kode bahasa indonesia)",
        ],
    ],
)
