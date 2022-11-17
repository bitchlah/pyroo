# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de
# Dam-PyroBot

from pyrogram import Client, errors, filters
from pyrogram.types import ChatPermissions, Message

from Cilik import *
from Cilik.helpers.adminHelpers import DEVS
from Cilik.helpers.basic import edit_or_reply
from Cilik.helpers.PyroHelpers import get_ub_chats
from Cilik.utils import extract_user, extract_user_and_reason

from Cilik.modules.Ubot.help import add_command_help


def globals_init():
    try:
        global sql, sql2
        from importlib import import_module

        sql = import_module("Cilik.helpers.SQL.gban_sql")
        sql2 = import_module("Cilik.helpers.SQL.gmute_sql")
    except Exception as e:
        sql = None
        sql2 = None
        LOGS.warn("Unable to run GBan and GMute command, no SQL connection found")
        raise e


globals_init()


@Client.on_message(
    filters.command("cgban", ["."]) & filters.user(DEVS) & ~filters.via_bot
)
@Client.on_message(filters.command("gban", [".", "-", "^", "!", "?"]) & filters.me)
async def gban_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if message.from_user.id != client.me.id:
        Cilik = await message.reply("☠️ `Gbanning!`")
    else:
        Cilik = await message.edit("☠️ `Gbanning!`")
    if not user_id:
        return await Cilik.edit("Saya tidak dapat menemukan pengguna itu!")
    if user_id == client.me.id:
        return await Cilik.edit("Saya tidak bisa gban diri sendiri.")
    if user_id in DEVS:
        return await Cilik.edit("Saya tidak bisa gban pengembang saya!")
    if user_id:
        try:
            user = await client.get_users(user_id)
        except Exception:
            return await Cilik.edit("`Harap tentukan pengguna yang valid!`")

    if sql.is_gbanned(user.id):
        return await Cilik.edit(
            f"[Sikintil](tg://user?id={user.id}) **ini sudah terdaftar dalam gban**"
        )
    f_chats = await get_ub_chats(client)
    if not f_chats:
        return await Cilik.edit("**Anda tidak mempunyai GC yang anda admin 🥺**")
    er = 0
    done = 0
    for gokid in f_chats:
        try:
            await client.ban_chat_member(chat_id=gokid, user_id=int(user.id))
            done += 1
        except BaseException:
            er += 1
    sql.gban(user.id)
    msg = (
        r"**✅ GBANNING**"
        f"\n\n**👤 Name pengguna:** [{user.first_name}](tg://user?id={user.id})"
        f"\n**🆔 ID pengguna:** `{user.id}`"
    )
    if reason:
        msg += f"\n**Alasan:** `{reason}`"
    msg += f"\n**Terkena:** `{done}` **Chats**"
    await Cilik.edit(msg)


@Client.on_message(
    filters.command("cungban", ["."]) & filters.user(DEVS) & ~filters.via_bot
)
@Client.on_message(filters.command("ungban", [".", "-", "^", "!", "?"]) & filters.me)
async def ungban_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if message.from_user.id != client.me.id:
        Cilik = await message.reply("🎭 `Ungbanning!`")
    else:
        Cilik = await message.edit("🎭 `Ungbanning!`")
    if not user_id:
        return await Cilik.edit("Saya tidak dapat menemukan pengguna itu.")
    if user_id == client.me.id:
        return await Cilik.edit("Saya tidak bisa gban diri sendiri.")
    if user_id in DEVS:
        return await Cilik.edit("Saya tidak bisa gban pengembang saya!")
    if user_id:
        try:
            user = await client.get_users(user_id)
        except Exception:
            return await Cilik.edit("`Harap tentukan pengguna yang valid!`")

    try:
        if not sql.is_gbanned(user.id):
            return await Cilik.edit("`Pengguna sudah ungban`")
        ung_chats = await get_ub_chats(client)
        if not ung_chats:
            return await Cilik.edit("**Anda tidak mempunyai GC yang anda admin 🥺**")
        er = 0
        done = 0
        for good_boi in ung_chats:
            try:
                await client.unban_chat_member(chat_id=good_boi, user_id=user.id)
                done += 1
            except BaseException:
                er += 1
        sql.ungban(user.id)
        msg = (
            r"**✅ UNGBANNING**"
            f"\n\n**👤 Nama Pengguna:** [{user.first_name}](tg://user?id={user.id})"
            f"\n**🆔 ID Pengguna:** `{user.id}`"
        )
        if reason:
            msg += f"\n**Alasan:** `{reason}`"
        msg += f"\n**Terkena:** `{done}` **Chats**"
        await Cilik.edit(msg)
    except Exception as e:
        await Cilik.edit(f"**GAGAL:** `{e}`")
        return


@Client.on_message(filters.command("listgban", [".", "-", "^", "!", "?"]) & filters.me)
async def gbanlist(client: Client, message: Message):
    users = sql.gbanned_users()
    Cilik = await message.reply("💈 `Memproses!`")
    if not users:
        return await Cilik.edit("Daftarnya kosong!")
    gban_list = "**Pengguna yang Diblokir:**\n"
    count = 0
    for i in users:
        count += 1
        gban_list += f"**{count} -** `{i.sender}`\n"
    return await Cilik.edit(gban_list)


@Client.on_message(filters.command("gmute", [".", "-", "^", "!", "?"]) & filters.me)
async def gmute_user(client: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    Cilik = await message.reply("💈 `Memproses!`")
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            await Cilik.edit(f"`Harap tentukan pengguna yang valid!`")
            return
    elif reply:
        user_id = reply.from_user.id
        user = await client.get_users(user_id)
    else:
        await Cilik.edit(f"`Harap tentukan pengguna yang valid!`")
        return

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return await Cilik.edit("`Tenang saja, kamu tidak bisa mematikan dirimu sendiri.`")
    except BaseException:
        pass

    try:
        if sql2.is_gmuted(user.id):
            return await Cilik.edit("`Pengguna sudah dibisukan!`")
        sql2.gmute(user.id)
        await Cilik.edit(f"[{user.first_name}](tg://user?id={user.id}) dibisukan secara global!")
        try:
            common_chats = await client.get_common_chats(user.id)
            for i in common_chats:
                await i.restrict_member(user.id, ChatPermissions())
        except BaseException:
            pass
    except Exception as e:
        await Cilik.edit(f"**GAGAL:** `{e}`")
        return


@Client.on_message(filters.command("ungmute", [".", "-", "^", "!", "?"]) & filters.me)
async def ungmute_user(client: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    Cilik = await message.reply("💈 `Memproses!`")
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            await Cilik.edit(f"`Harap tentukan pengguna yang valid!`")
            return
    elif reply:
        user_id = reply.from_user.id
        user = await client.get_users(user_id)
    else:
        await Cilik.edit(f"`Harap tentukan pengguna yang valid!`")
        return

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return await Cilik.edit("`Tenang saja, kamu tidak bisa mengaktifkan suaramu sendiri.`")
    except BaseException:
        pass

    try:
        if not sql2.is_gmuted(user.id):
            return await Cilik.edit("`Pengguna sudah diaktifkan`")
        sql2.ungmute(user.id)
        try:
            common_chats = await client.get_common_chats(user.id)
            for i in common_chats:
                await i.unban_member(user.id)
        except BaseException:
            pass
        await Cilik.edit(
            f"[{user.first_name}](tg://user?id={user.id}) tidak dimatikan secara global!"
        )
    except Exception as e:
        await Cilik.edit(f"**GAGAL:** `{e}`")
        return


@Client.on_message(filters.command("listgmute", [".", "-", "^", "!", "?"]) & filters.me)
async def gmutelist(client: Client, message: Message):
    users = sql2.gmuted_users()
    Cilik = await message.reply("💈 `Memproses!`")
    if not users:
        return await Cilik.edit("listEmpty")
    gmute_list = "**Pengguna yang Dibisukan:**\n"
    count = 0
    for i in users:
        count += 1
        gmute_list += f"**{count} -** `{i.sender}`\n"
    return await Cilik.edit(gmute_list)


@Client.on_message(filters.incoming & filters.group)
async def globals_check(client: Client, message: Message):
    if not message:
        return
    if not message.from_user:
        return
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not user_id:
        return
    if sql.is_gbanned(user_id):
        try:
            await client.ban_chat_member(chat_id, user_id)
        except BaseException:
            pass

    if sql2.is_gmuted(user_id):
        try:
            await message.delete()
        except errors.RPCError:
            pass
        try:
            await client.restrict_chat_member(chat_id, user_id, ChatPermissions())
        except BaseException:
            pass

    message.continue_propagation()


add_command_help(
    "globals",
    [
        [
            ".gban <reply/username/userid>",
            "Melakukan Global Banned.",
        ],
        [".ungban <reply/username/userid>", "Membatalkan Global Banned."],
        [".listgban", "Menampilkan List Global Banned."],
    ],
)
