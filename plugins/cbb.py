from pyrogram import Client 
from bot import Bot
from config import *
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.database import *
from pyrogram.types import InputMediaPhoto
from pyrogram.enums import ParseMode

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data

    if data == "help":
        await query.message.edit_media(
            media=InputMediaPhoto(
                media="https://i.ibb.co/dwmHC029/photo-2025-05-03-12-22-24-7500193791484100632.jpg",
                caption=HELP_TXT.format(first=query.from_user.first_name),
                parse_mode=ParseMode.HTML
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('« Bᴀᴄᴋ', callback_data='start'),
                 InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data='close')]
            ])
        )

    elif data == "about":
        await query.message.edit_media(
            media=InputMediaPhoto(
                media="https://i.ibb.co/8nt0LhjS/photo-2025-05-03-12-22-24-7500193804369002524.jpg",
                caption=ABOUT_TXT.format(first=query.from_user.first_name),
                parse_mode=ParseMode.HTML
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('« Bᴀᴄᴋ', callback_data='start'),
                 InlineKeyboardButton('Cʟᴏsᴇ ✖', callback_data='close')]
            ])
        )

    elif data == "start":
        await query.message.edit_media(
            media=InputMediaPhoto(
                media="https://i.ibb.co/m5CmBgZ8/photo-2025-05-01-08-09-59-7499386582445588496.jpg",
                caption=START_MSG.format(first=query.from_user.first_name),
                parse_mode=ParseMode.HTML
            ),
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Pʀᴇᴍɪᴜᴍ", callback_data="premium")
                ],
                [
                    InlineKeyboardButton("Aʙᴏᴜᴛ", callback_data="about"),
                    InlineKeyboardButton("Hᴇʟᴘ", callback_data="help")
                ]
            ])
        )


# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport
#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#


    elif data == "premium":
        await query.message.delete()
        await client.send_photo(
            chat_id=query.message.chat.id,
            photo=QR_PIC,
            caption=(
                f"<pre>›› Hᴇʏ ʙʀᴏ ᴏʀ sɪs!</pre>\n"
                f"<blockquote>❏ ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇ ʙᴇɴɪꜰɪᴛꜱ:</blockquote>\n"
                f"<blockquote>›› ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋꜱ\n❏ ɢᴇᴛ ᴅɪʀᴇᴄᴛ ғɪʟᴇs\n\n›› ᴀᴅ-ғʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ\n❏ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴅᴜʟᴛ ᴄᴏɴᴛᴇɴ</blockquote>\n"
                f"<b><blockquote>‼️ Aғᴛᴇʀ sᴇɴᴅɪɴɢ ᴀ sᴄʀᴇᴇɴsʜᴏᴛ ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴜs sᴏᴍᴇ ᴛɪᴍᴇ ᴛᴏ ᴀᴅᴅ ʏᴏᴜ ɪɴ ᴛʜᴇ ᴘʀᴇᴍɪᴜᴍ ʟɪsᴛ.</b></blockquote>"
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Cʜᴇᴄᴋ ᴏᴜᴛ ᴏᴜʀ ᴘʟᴀɴs", url=(SCREENSHOT_URL)
                        )
                    ],
                    [InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close")],
                ]
            )
        )



    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

    elif data.startswith("rfs_ch_"):
        cid = int(data.split("_")[2])
        try:
            chat = await client.get_chat(cid)
            mode = await db.get_channel_mode(cid)
            status = "🟢 ᴏɴ" if mode == "on" else "🔴 ᴏғғ"
            new_mode = "ᴏғғ" if mode == "on" else "on"
            buttons = [
                [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
                [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")]
            ]
            await query.message.edit_text(
                f"Channel: {chat.title}\nCurrent Force-Sub Mode: {status}",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception:
            await query.answer("Failed to fetch channel info", show_alert=True)

    elif data.startswith("rfs_toggle_"):
        cid, action = data.split("_")[2:]
        cid = int(cid)
        mode = "on" if action == "on" else "off"

        await db.set_channel_mode(cid, mode)
        await query.answer(f"Force-Sub set to {'ON' if mode == 'on' else 'OFF'}")

        # Refresh the same channel's mode view
        chat = await client.get_chat(cid)
        status = "🟢 ON" if mode == "on" else "🔴 OFF"
        new_mode = "off" if mode == "on" else "on"
        buttons = [
            [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
            [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")]
        ]
        await query.message.edit_text(
            f"Channel: {chat.title}\nCurrent Force-Sub Mode: {status}",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data == "fsub_back":
        channels = await db.show_channels()
        buttons = []
        for cid in channels:
            try:
                chat = await client.get_chat(cid)
                mode = await db.get_channel_mode(cid)
                status = "🟢" if mode == "on" else "🔴"
                buttons.append([InlineKeyboardButton(f"{status} {chat.title}", callback_data=f"rfs_ch_{cid}")])
            except:
                continue

        await query.message.edit_text(
            "sᴇʟᴇᴄᴛ ᴀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴛᴏɢɢʟᴇ ɪᴛs ғᴏʀᴄᴇ-sᴜʙ ᴍᴏᴅᴇ:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )


# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport
#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#
