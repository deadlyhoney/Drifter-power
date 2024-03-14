import random
import asyncio
from platform import python_version as pyver

from pyrogram import __version__ as pver
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram import __version__ as lver
from telethon import __version__ as tver

from MukeshRobot import SUPPORT_CHAT, pbot,BOT_USERNAME, OWNER_ID,BOT_NAME,START_IMG

MISHI = [
    "https://mallucampaign.in/images/img_1709919340.jpg",
    "https://mallucampaign.in/images/img_1709919341.jpg",
    "https://mallucampaign.in/images/img_1709919343.jpg",
    "https://mallucampaign.in/images/img_1709919344.jpg",
    "https://mallucampaign.in/images/img_1709919630.jpg",
    "https://mallucampaign.in/images/img_1709919632.jpg",
    "https://mallucampaign.in/images/img_1709919631.jpg",
    "https://mallucampaign.in/images/img_1709919633.jpg"
    "https://mallucampaign.in/images/img_1709919638.jpg",
    "https://mallucampaign.in/images/img_1709919639.jpg",
    "https://mallucampaign.in/images/img_1709919807.jpg",
    "https://mallucampaign.in/images/img_1709919640.jpg",
    "https://mallucampaign.in/images/img_1709919811.jpg",
    "https://mallucampaign.in/images/img_1709919813.jpg",
    "https://mallucampaign.in/images/img_1709919877.jpg",
    "https://mallucampaign.in/images/img_1709919880.jpg",
    "https://mallucampaign.in/images/img_1709919881.jpg",
    "https://mallucampaign.in/images/img_1709919882.jpg",
]

Mukesh = [
    [
        InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇ", url=f"https://t.me/DRIFTERSNETWORK"),
        InlineKeyboardButton(text="ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
    ],
    [
        InlineKeyboardButton(
            text="✞︎sᴜᴍᴍᴏɴ ᴅʀɪғᴛᴇʀ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ✞︎",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
]



@pbot.on_message(filters.command("alive"))
async def restart(client, m: Message):
    await m.delete()
    accha = await m.reply("ʜᴇʏ sᴏʟᴅɪᴇʀ")
    await asyncio.sleep(0.4)
    await accha.edit("🔥")
    await asyncio.sleep(0.3)
    await accha.edit("𝐃𝐫𝐢𝐟𝐭𝐞𝐫࿐●🏎️")
    await asyncio.sleep(0.3)
    await accha.delete()
    await asyncio.sleep(0.3)
    umm = await m.reply_sticker(
        "CAACAgQAAxkBAAI7CGXt61oqVZJq3llh5jgaqdllLwzWAAIpEQAC0n1AUN9p9WsWoafcHgQ"
    )
    await umm.delete()
    await asyncio.sleep(0.2)
    await m.reply_photo(
        random.choice(MISHI),
        caption=f"""** ✦ ʜᴇʏ, ɪ ᴀᴍ [{BOT_NAME}](f"t.me/{BOT_USERNAME}") ✦**\n\n❍ **ʟɪʙʀᴀʀʏ ➛** `{lver}`\n❍ **ᴛᴇʟᴇᴛʜᴏɴ ➛** `{tver}`\n❍ **ᴘʏʀᴏɢʀᴀᴍ ➛** `{pver}`\n❍ **ᴘʏᴛʜᴏɴ ➛** `{pyver()}`\n\n❍ **ᴍᴀᴅᴇ ʙʏ ➛** [ᴀɴᴅʜᴋᴀᴀʀ](tg://user?id={OWNER_ID})""",
        reply_markup=InlineKeyboardMarkup(Mukesh),
    )
    
__mod_name__ = "ᴀʟɪᴠᴇ"
__help__ = """
 ❍ /alive ➛ ᴄʜᴇᴄᴋ ʙᴏᴛ ᴀʟɪᴠᴇ sᴛᴀᴛᴜs.
 ❍ /ping ➛ ᴄʜᴋ ᴘɪɴɢ sᴛᴀᴛᴜs.
 ❍ /pingall ➛ ᴄʜᴋ ᴘɪɴɢ sᴛᴀᴛᴜs ᴏғ ᴀʟʟ ᴍᴏᴅᴜʟᴇs.
 """
    
