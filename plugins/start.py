import asyncio
import os
import random
import sys
import re
import string 
import string as rohit
import time
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatInviteLink, ChatPrivileges
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from bot import Bot
from config import *
from helper_func import *
from database.database import *
from database.db_premium import *
from pyrogram.enums import ChatAction
import random
from pyrogram.enums import ParseMode



BAN_SUPPORT = f"{BAN_SUPPORT}"
TUT_VID = f"{TUT_VID}"

async def short_url(client: Client, message: Message, base64_string):
    try:
        prem_link = f"https://t.me/{client.username}?start=yu3elk{base64_string}"
        short_link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, prem_link)

        buttons = [
            [
                InlineKeyboardButton(text="Oᴘᴇɴ ʟɪɴᴋ", url=short_link),
                InlineKeyboardButton(text="Tᴜᴛᴏʀɪᴀʟ", url=TUT_VID)
            ],
            [
                InlineKeyboardButton("Main channel" , url="https://t.me/+gE8Utdmvn4kzZjE1")
            ]
        ]

        await message.reply_photo(
            photo=SHORTENER_PIC,
            caption=SHORT_MSG.format(
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    except IndexError:
        pass



@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    is_premium = await is_premium_user(user_id)

    welcome_text = "<i><blockquote>Wᴇʟᴄᴏᴍᴇ, ʙᴀʙʏ… ɪ’ᴠᴇ ʙᴇᴇɴ ᴄʀᴀᴠɪɴɢ ʏᴏᴜʀ ᴘʀᴇsᴇɴᴄᴇ ғᴇᴇʟs ᴘᴇʀғᴇᴄᴛ ɴᴏᴡ ᴛʜᴀᴛ ʏᴏᴜ’ʀᴇ ʜᴇʀᴇ.</blockquote></i>"

    stickers = [
        "CAACAgUAAxkBAAEOXBhoCoKZ76jevKX-Vc5v5SZhCeQAAXMAAh4KAALJrhlVZygbxFWWTLw2BA"
    ]

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    msg = await message.reply_text(welcome_text, parse_mode=ParseMode.HTML)
    await asyncio.sleep(0.1)

    await msg.edit_text("<b><i><pre>Sᴛᴀʀᴛɪɴɢ...</pre></i></b>", parse_mode=ParseMode.HTML)
    await asyncio.sleep(0.1)
    await msg.delete()

    await client.send_chat_action(message.chat.id, ChatAction.CHOOSE_STICKER)
    await message.reply_sticker(random.choice(stickers))

    # Check if user is banned
    banned_users = await db.get_ban_users()
    if user_id in banned_users:
        return await message.reply_text(
            "<b>⛔️ You are Bᴀɴɴᴇᴅ from using this bot.</b>\n\n"
            "<i>Cᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ ɪғ ʏᴏᴜ ᴛʜɪɴᴋ ᴛʜɪs ɪs ᴀ ᴍɪsᴛᴀᴋᴇ.</i>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Cᴏɴᴛᴀᴄᴛ sᴜᴘᴘᴏʀᴛ", url=BAN_SUPPORT)]]
            )
        )

    # ✅ Check Force Subscription
    if not await is_subscribed(client, user_id):
        return await not_joined(client, message)

    # File auto-delete time in seconds
    FILE_AUTO_DELETE = await db.get_del_timer()

    # Add user if not already present
    if not await db.present_user(user_id):
        try:
            await db.add_user(user_id)
        except:
            pass

    # Handle normal message flow
    text = message.text

    if len(text) > 7:
        try:
            basic = text.split(" ", 1)[1]
            if basic.startswith("yu3elk"):
                base64_string = basic[6:-1]
            else:
                base64_string = basic

            if not is_premium and user_id != OWNER_ID and not basic.startswith("yu3elk"):
                await short_url(client, message, base64_string)
                return

        except Exception as e:
            print(f"Error processing start payload: {e}")

        string = await decode(base64_string)
        argument = string.split("-")

        ids = []
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
            except Exception as e:
                print(f"Error decoding IDs: {e}")
                return

        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except Exception as e:
                print(f"Error decoding ID: {e}")
                return

        temp_msg = await message.reply("<b><pre>お待ちください</pre></b>")
        try:
            messages = await get_messages(client, ids)
        except Exception as e:
            await message.reply_text("Something went wrong!")
            print(f"Error getting messages: {e}")
            return
        finally:
            await temp_msg.delete()

        codeflix_msgs = []
        for msg in messages:
            caption = (CUSTOM_CAPTION.format(
                previouscaption="" if not msg.caption else msg.caption.html,
                filename=msg.document.file_name
            ) if bool(CUSTOM_CAPTION) and bool(msg.document) else ("" if not msg.caption else msg.caption.html))

            reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None

            try:
                copied_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT
                )
                codeflix_msgs.append(copied_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                copied_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT
                )
                codeflix_msgs.append(copied_msg)
            except Exception as e:
                print(f"Failed to send message: {e}")
                pass

        if FILE_AUTO_DELETE > 0:
            notification_msg = await message.reply(
                f"<b><blockquote>Tʜɪs Fɪʟᴇ ᴡɪʟʟ ʙᴇ Dᴇʟᴇᴛᴇᴅ ɪɴ  {get_exp_time(FILE_AUTO_DELETE)}.<b></blockquote>"
                f"<blockquote>Pʟᴇᴀsᴇ sᴀᴠᴇ ᴏʀ ғᴏʀᴡᴀʀᴅ ɪᴛ ᴛᴏ ʏᴏᴜʀ sᴀᴠᴇᴅ ᴍᴇssᴀɢᴇs ʙᴇғᴏʀᴇ ɪᴛ ɢᴇᴛs Dᴇʟᴇᴛᴇᴅ.</b></blockquote>"
            )

            await asyncio.sleep(FILE_AUTO_DELETE)

            for snt_msg in codeflix_msgs:
                if snt_msg:
                    try:
                        await snt_msg.delete()
                    except Exception as e:
                        print(f"Error deleting message {snt_msg.id}: {e}")

            try:
                reload_url = (
                    f"https://t.me/{client.username}?start={message.command[1]}"
                    if message.command and len(message.command) > 1 else None
                )
                keyboard = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("ɢᴇᴛ ғɪʟᴇ ᴀɢᴀɪɴ!", url=reload_url)]]
                ) if reload_url else None

                await notification_msg.edit(
                    "<b><pre>Pʀᴇᴠɪᴏᴜs Mᴇssᴀɢᴇ ᴡᴀs Dᴇʟᴇᴛᴇᴅ 🗑</pre></b>\n"
                    "<b><blockquote>Iғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɢᴇᴛ ᴛʜᴇ ғɪʟᴇs ᴀɢᴀɪɴ, ᴛʜᴇɴ ᴄʟɪᴄᴋ: ♻️ Cʟɪᴄᴋ Hᴇʀᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴇʟsᴇ ᴄʟᴏsᴇ ᴛʜɪs ᴍᴇssᴀɢᴇ.</blockquote></b>",
                    reply_markup=keyboard
                )
            except Exception as e:
                print(f"Error updating notification with 'Get File Again' button: {e}")

    else:
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("My channel", url="https://t.me/+gE8Utdmvn4kzZjE1")
            ],
            [
                InlineKeyboardButton("Aʙᴏᴜᴛ", callback_data="about"),
                InlineKeyboardButton("Hᴇʟᴘ", callback_data="help")
            ]
        ])

        await message.reply_photo(
            photo=START_PIC,
            caption=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            message_effect_id=5104841245755180586  # 🔥
        )

        return



#=====================================================================================##
# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport



# Create a global dictionary to store chat data
chat_data_cache = {}

async def not_joined(client: Client, message: Message):
    temp = await message.reply("<b><i><pre>Cʜᴇᴄᴋɪɴɢ sᴜʙsᴄʀɪᴘᴛɪᴏɴ...</pre></i></b>")

    user_id = message.from_user.id
    buttons = []
    count = 0

    try:
        all_channels = await db.show_channels()  # Should return list of (chat_id, mode) tuples
        for total, chat_id in enumerate(all_channels, start=1):
            mode = await db.get_channel_mode(chat_id)  # fetch mode 

            await message.reply_chat_action(ChatAction.TYPING)

            if not await is_sub(client, user_id, chat_id):
                try:
                    # Cache chat info
                    if chat_id in chat_data_cache:
                        data = chat_data_cache[chat_id]
                    else:
                        data = await client.get_chat(chat_id)
                        chat_data_cache[chat_id] = data

                    name = data.title

                    # Generate proper invite link based on the mode
                    if mode == "on" and not data.username:
                        invite = await client.create_chat_invite_link(
                            chat_id=chat_id,
                            creates_join_request=True,
                            expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None
                            )
                        link = invite.invite_link

                    else:
                        if data.username:
                            link = f"https://t.me/{data.username}"
                        else:
                            invite = await client.create_chat_invite_link(
                                chat_id=chat_id,
                                expire_date=datetime.utcnow() + timedelta(seconds=FSUB_LINK_EXPIRY) if FSUB_LINK_EXPIRY else None)
                            link = invite.invite_link

                    buttons.append([InlineKeyboardButton(text=name, url=link)])
                    count += 1
                    await temp.edit(f"<b>{'! ' * count}</b>")

                except Exception as e:
                    print(f"Error with chat {chat_id}: {e}")
                    return await temp.edit(
                        f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @RexySama</i></b>\n"
                        f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>"
                    )

        # Retry Button
        try:
            buttons.append([
                InlineKeyboardButton(
                    text='♻️ Tʀʏ Aɢᴀɪɴ',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ])
        except IndexError:
            pass

        await message.reply_photo(
            photo=FORCE_PIC,
            caption=FORCE_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id, 
                message_effect_id=5104841245755180586  # 🔥
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    except Exception as e:
        print(f"Final Error: {e}")
        await temp.edit(
            f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @RexySama</i></b>\n"
            f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>"
        )

#=====================================================================================##

@Client.on_message(filters.command('myplan') & filters.private)
async def check_plan(client: Client, message: Message):
    user = message.from_user
    user_id = user.id
    name = user.first_name
    username = f"@{user.username}" if user.username else "N/A"

    # Welcome message and animation
    welcome_text = (
        "<i><pre>"
        "Fᴇᴛᴄʜɪɴɢ ᴜsᴇʀ ɪɴғᴏ"
        "</pre></i>"
    )
    stickers = [
        "CAACAgUAAxkBAAEOXBhoCoKZ76jevKX-Vc5v5SZhCeQAAXMAAh4KAALJrhlVZygbxFWWTLw2BA"
    ]

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    msg = await message.reply_text(welcome_text, parse_mode=ParseMode.HTML)
    await asyncio.sleep(0.5)

    await msg.edit_text("<b><i><pre>Dᴏɴᴇ</pre></i></b>", parse_mode=ParseMode.HTML)
    await asyncio.sleep(0.5)
    await msg.delete()

    await client.send_chat_action(message.chat.id, ChatAction.CHOOSE_STICKER)
    await message.reply_sticker(random.choice(stickers))

    # Now fetch the user plan status
    status_message = await check_user_plan(user_id)

    image_url = "https://i.ibb.co/MxyCLGBf/photo-2025-01-16-11-21-46-7499433590862643216.jpg"
    url = "https://t.me/+FRmXFSlecDI5NGJl"

    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("Bᴜʏ ᴘʀᴇᴍɪᴜᴍ", url=url),
            InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close")
        ]]
    )

    caption = (
        f"<b><pre>𝗬𝗼𝘂𝗿 𝗣𝗹𝗮𝗻 𝗗𝗲𝘁𝗮𝗶𝗹𝘀 :</pre></b>\n"
        f"<b><blockquote>Nᴀᴍᴇ :</b> {name}\n"
        f"<b>Usᴇʀɴᴀᴍᴇ :</b> {username}\n"
        f"<b>Usᴇʀ ɪᴅ :</b> <code>{user_id}</code>\n"
        f"<b>Sᴛᴀᴛᴜs :</b> {status_message}</blockquote>"
    )

    await message.reply_photo(
        photo=image_url,
        caption=caption,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML, 
        message_effect_id=5104841245755180586  # 🔥
    )

#=====================================================================================##
# Command to add premium user
@Bot.on_message(filters.command('addpremium') & filters.private & admin)
async def add_premium_user_command(client, msg):
    if len(msg.command) != 4:
        await msg.reply_text(
            "<blockquote><b>Usᴇᴀɢᴇ: /addpaid <user_id> <time_value> <time_unit></b><blockquote>\n"
            "<blockquote>/addpremium 123456789 30 m → 30 minutes\n"
            "/addpremium 123456789 2 h → 2 hours\n"
            "/addpremium 123456789 1 d → 1 day\n"
            "/addpremium 123456789 1 y → 1 year</blockquote>"
        )
        return

    try:
        user_id = int(msg.command[1])
        time_value = int(msg.command[2])
        time_unit = msg.command[3].lower()  # supports: s, m, h, d, y

        # Call add_premium function
        expiration_time = await add_premium(user_id, time_value, time_unit)

        # Notify the admin with plain text and close button
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close2")]]
        )
        await msg.reply_text(
            f"✅ User `{user_id}` added as a premium user for {time_value} {time_unit}.\n"
            f"Expiration Time: `{expiration_time}`",
            reply_markup=keyboard
        )

        # Notify the user with image and button
        await client.send_photo(
            chat_id=user_id,
            photo="https://i.ibb.co/QFhKtfQH/photo-2025-05-03-13-06-15-7500205091543056408.jpg",
            caption=(
                f"<pre>🎉 Pʀᴇᴍɪᴜᴍ ᴀᴄᴛɪᴠᴀᴛᴇᴅ!</pre>\n"
                f"<blockquote>Yᴏᴜ ʜᴀᴠᴇ ʀᴇᴄᴇɪᴠᴇᴅ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss ғᴏʀ <b>{time_value} {time_unit}.</b></blockquote>\n"
                f"<blockquote>Exᴘɪʀᴇs ᴏɴ : <b>{expiration_time}</blockquote></b>"
            ),
            reply_markup=keyboard,
            message_effect_id=5104841245755180586  # 🔥
        )

    except ValueError:
        await msg.reply_text("❌ Invalid input. Please ensure user ID and time value are numbers.")
    except Exception as e:
        await msg.reply_text(f"⚠️ An error occurred: `{str(e)}`")


@Bot.on_callback_query()
async def on_callback_query(client, callback_query):
    if callback_query.data == "close2":
        await callback_query.message.delete()
        
#=====================================================================================##


#=====================================================================================##

# Command to remove premium user
@Bot.on_message(filters.command('remove_premium') & filters.private & admin)
async def pre_remove_user(client: Client, msg: Message):
    if len(msg.command) != 2:
        await msg.reply_text("<pre>Usᴇᴀɢᴇ: /remove_premium user_id</pre>")
        return
    try:
        user_id = int(msg.command[1])
        await remove_premium(user_id)
        await msg.reply_text(f"<blockquote>Usᴇʀ {user_id} ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ.</blockquote>")
    except ValueError:
        await msg.reply_text("<blockquote>Usᴇʀ_ɪᴅ ᴍᴜsᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ ᴏʀ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ.</blockquote>")

#=====================================================================================##

# Command to list active premium users
@Bot.on_message(filters.command('premium_users') & filters.private & admin)
async def list_premium_users_command(client, message):
    ist = timezone("Asia/Kolkata")
    premium_users_cursor = collection.find({})
    premium_user_list = ['<b>Active Premium Users in Database:</b>']
    current_time = datetime.now(ist)

    async for user in premium_users_cursor:
        user_id = user["user_id"]
        expiration_timestamp = user["expiration_timestamp"]

        try:
            expiration_time = datetime.fromisoformat(expiration_timestamp).astimezone(ist)
            remaining_time = expiration_time - current_time

            if remaining_time.total_seconds() <= 0:
                await collection.delete_one({"user_id": user_id})
                continue

            user_info = await client.get_users(user_id)
            username = user_info.username if user_info.username else "No Username"
            mention = user_info.mention

            days = remaining_time.days
            hours = remaining_time.seconds // 3600
            minutes = (remaining_time.seconds // 60) % 60
            seconds = remaining_time.seconds % 60
            expiry_info = f"{days}d {hours}h {minutes}m {seconds}s left"

            premium_user_list.append(
                f"<blockquote>Usᴇʀɪᴅ : <code>{user_id}</code>\n"
                f"Usᴇʀ : @{username}\n"
                f"Nᴀᴍᴇ : {mention}\n"
                f"Exᴘɪʀʏ : {expiry_info}</blockquote>"
            )
        except Exception as e:
            premium_user_list.append(
                f"UserID: <code>{user_id}</code>\n"
                f"Error: Unable to fetch user details ({str(e)})"
            )

    if len(premium_user_list) == 1:
        await message.reply_text("<pre>I ғᴏᴜɴᴅ 0 ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀs ɪɴ ᴍʏ ᴅʙ</pre>")
        return

    # Inline button to close the message
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close_premium_list")]]
    )

    # Send message with image and button
    await message.reply_photo(
        photo="https://i.ibb.co/V0kXYvxb/photo-2025-05-03-13-16-24-7500207702883172380.jpg",  # Replace with your image URL
        caption="\n\n".join(premium_user_list),
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML, 
        message_effect_id=5104841245755180586  # 🔥
    )

@Bot.on_callback_query(filters.regex("close_premium_list"))
async def close_callback(client, callback_query):
    await callback_query.message.delete()
    await callback_query.answer()


#=====================================================================================##

@Bot.on_message(filters.command("count") & filters.private & admin)
async def total_verify_count_cmd(client, message: Message):
    total = await db.get_total_verify_count()
    await message.reply_text(f"Tᴏᴛᴀʟ ᴠᴇʀɪғɪᴇᴅ ᴛᴏᴋᴇɴs ᴛᴏᴅᴀʏ: <b>{total}</b>")


#=====================================================================================##

@Bot.on_message(filters.command('commands') & filters.private & admin)
async def bcmd(bot: Bot, message: Message):        
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data = "close")]])
    await message.reply(text=CMD_TXT, reply_markup = reply_markup, quote= True)
