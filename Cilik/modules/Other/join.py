# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de
# Kit-Ub

from pyrogram import Client, filters
from pyrogram.types import Message
from Cilik.helpers.adminHelpers import DEVS
from Cilik.helpers.basic import edit_or_reply

from Cilik.modules.Ubot.help import add_command_help


@Client.on_message(
    filters.command("cjoin", ["."]) & filters.user(DEVS) & ~filters.via_bot
)
@Client.on_message(filters.command("join", [".", "-", "^", "!", "?"]) & filters.me)
async def join(client: Client, message: Message):
    Kit = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await message.reply("💈 `Memproses!`")
    try:
        await xxnx.edit(f"✅ **Bergabung ke Obrolan** `{Kit}`")
        await client.join_chat(Kit)
    except Exception as ex:
        await xxnx.edit(f"**GAGAL:** \n\n{str(ex)}")


@Client.on_message(
    filters.command("cleave", ["."]) & filters.user(DEVS) & ~filters.via_bot
)
@Client.on_message(filters.command(["leave", "kickme"], [".", "-", "^", "!", "?"]) & filters.me)
async def leave(client: Client, message: Message):
    Kit = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await message.reply("💈 `Memproses!`")
    try:
        await xxnx.edit_text(f"{client.me.first_name} Telah meninggalkan grup ini, sampai jumpa!")
        await client.leave_chat(Kit)
    except Exception as ex:
        await xxnx.edit_text(f"**GAGAL:** \n\n{str(ex)}")


@Client.on_message(filters.command(["leaveall"], [".", "-", "^", "!", "?"]) & filters.me)
async def kickmeall(client: Client, message: Message):
    Kit = await message.reply("`Meninggalkan semua Grup!`")
    er = 0
    done = 0
    async for dialog in client.iter_dialogs():
        if dialog.chat.type in ("group", "supergroup"):
            chat = dialog.chat.id
            try:
                done += 1
                await client.leave_chat(chat)
            except BaseException:
                er += 1
    await Cilik.edit(
        f"✅ **Berhasil Meninggalkan {done} Obrolan, Gagal Meninggalkan {er} Obrolan**"
    )


add_command_help(
    "join",
    [
        [
            ".kickme",
            "Keluar dari grup dengan menampilkan pesan has left this group, bye!!.",
        ],
        [".leaveall", "Keluar dari semua grup telegram yang anda gabung."],
        [".join <UsernameGC>", "Untuk Bergabung dengan Obrolan Melalui username."],
        [".leave <UsernameGC>", "Untuk keluar dari grup Melalui username."],
    ],
)
