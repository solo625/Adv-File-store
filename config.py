import os
from os import environ,getenv
import logging
from logging.handlers import RotatingFileHandler

#--------------------------------------------
#Bot token @Botfather
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
APP_ID = int(os.environ.get("APP_ID", "20714788")) #Your API ID from my.telegram.org
API_HASH = os.environ.get("API_HASH", "25103f6394df6328a3ac776bf83f0e26") #Your API Hash from my.telegram.org
#--------------------------------------------

CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002650912983")) #Your db channel Id
OWNER = os.environ.get("OWNER", "otakusolo") # Owner username without @
OWNER_ID = int(os.environ.get("OWNER_ID", "7009595359")) # Owner id
#--------------------------------------------
PORT = os.environ.get("PORT", "8001")
#--------------------------------------------
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://filestore:BFsHO5KRZ7XJqYGk@cluster0.v21xlgp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DATABASE_NAME", "filestore")
#--------------------------------------------
FSUB_LINK_EXPIRY = int(os.getenv("FSUB_LINK_EXPIRY", "0"))  # 0 means no expiry
BAN_SUPPORT = os.environ.get("BAN_SUPPORT", "https://t.me/otakusolo")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "200"))
#--------------------------------------------
START_PIC = os.environ.get("START_PIC", "https://i.ibb.co/1tm9L912/photo-2025-05-05-12-34-06-7500938994079760412.jpg")
FORCE_PIC = os.environ.get("FORCE_PIC", "https://i.ibb.co/Wvd71Cj2/photo-2025-05-06-12-32-12-7501309572447993884.jpg")

#--------------------------------------------
SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "tnshort.net")
SHORTLINK_API = os.environ.get("SHORTLINK_API", "477f2cdf1b113fca45b9167fc0370f55c37dfc76")
TUT_VID = os.environ.get("TUT_VID","https://t.me/how_to_download_tamil/3")
SHORT_MSG = "<b><pre>👀 Hᴇʏ ʙʀᴏ/sɪs ,</pre>\n<blockquote>‼️ ɢᴇᴛ ᴀʟʟ ꜰɪʟᴇꜱ ɪɴ ᴀ ꜱɪɴɢʟᴇ ʟɪɴᴋ ‼️</blockquote>\n<blockquote>⌯ ʏᴏᴜʀ ʟɪɴᴋ ɪꜱ ʀᴇᴀᴅʏ, ᴋɪɴᴅʟʏ ᴄʟɪᴄᴋ ᴏɴ ᴏᴘᴇɴ ʟɪɴᴋ ʙᴜᴛᴛᴏɴ ⌯</blockquote></b>"

SHORTENER_PIC = os.environ.get("SHORTENER_PIC", "https://i.ibb.co/1tm9L912/photo-2025-05-05-12-34-06-7500938994079760412.jpg")
#--------------------------------------------

#--------------------------------------------
HELP_TXT = "<b><blockquote>ᴛʜɪs ɪs ᴀɴ ғɪʟᴇ ᴛᴏ ʟɪɴᴋ ʙᴏᴛ ᴡᴏʀᴋ ғᴏʀ @otakusolo\n\n❏ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs\n├ /start : sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n├ /about : ᴏᴜʀ Iɴғᴏʀᴍᴀᴛɪᴏɴ\n└ /help : ʜᴇʟᴘ ʀᴇʟᴀᴛᴇᴅ ᴛᴏ ʙᴏᴛ</blockquote></b>"
ABOUT_TXT = """<b><blockquote>
👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href='https://t.me/otakusolo'>ᴏᴡɴᴇʀ</a>  
📚 ʟɪʙʀᴀʀʏ : <a href='https://docs.pyrogram.org/'>ᴘʏʀᴏɢʀᴀᴍ</a>  
🐍 ʟᴀɴɢᴜᴀɢᴇ : <a href='https://www.python.org/download/releases/3.0/'>ᴘʏᴛʜᴏɴ 3</a>  
🗄️ ᴅᴀᴛᴀʙᴀsᴇ : <a href='https://www.mongodb.com/'>ᴍᴏɴɢᴏ ᴅʙ</a>  
☁️ ʙᴏᴛ sᴇʀᴠᴇʀ : <a href='https://heroku.com'>ʜᴇʀᴏᴋᴜ</a>  
📦 ʙᴜɪʟᴅ sᴛᴀᴛᴜs : ᴠ2.7.1 [sᴛᴀʙʟᴇ]  
💬 sᴜᴘᴘᴏʀᴛ : <a href='https://t.me/srkassistant'>@support</a>
</blockquote></b>"""


#--------------------------------------------
#--------------------------------------------
START_MSG = os.environ.get("START_MESSAGE", "oʀᴀ oʀᴀ.... ɪ ᴀᴍ ᴍᴀᴅᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ ғɪɴᴅ ᴡʜᴀᴛ ʏᴏᴜ'ʀᴇ ʟᴏᴏᴋɪɴɢ ꜰᴏʀ....")
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "oʀᴀ oʀa.....ʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ sᴜʙsᴄʀɪʙᴇ ɴᴏᴡ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ғɪʟᴇs.....")

CMD_TXT = """<blockquote><b>» 𝗔𝗗𝗠𝗜𝗡𝗦 𝗖𝗢𝗠𝗠𝗔𝗡𝗗</b></blockquote>
<b><blockquote expandable>›› /dlt_time :</b> sᴇᴛ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇ
<b>›› /check_dlt_time :</b> ᴄʜᴇᴄᴋ ᴄᴜʀʀᴇɴᴛ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇ
<b>›› /dbroadcast :</b> ʙʀᴏᴀᴅᴄᴀsᴛ ᴅᴏᴄᴜᴍᴇɴᴛ / ᴠɪᴅᴇᴏ
<b>›› /ban :</b> ʙᴀɴ ᴀ ᴜꜱᴇʀ
<b>›› /unban :</b> ᴜɴʙᴀɴ ᴀ ᴜꜱᴇʀ
<b>›› /banlist :</b> ɢᴇᴛ ʟɪsᴛ ᴏꜰ ʙᴀɴɴᴇᴅ ᴜꜱᴇʀs
<b>›› /addchnl :</b> ᴀᴅᴅ ꜰᴏʀᴄᴇ sᴜʙ ᴄʜᴀɴɴᴇʟ
<b>›› /delchnl :</b> ʀᴇᴍᴏᴠᴇ ꜰᴏʀᴄᴇ sᴜʙ ᴄʜᴀɴɴᴇʟ
<b>›› /listchnl :</b> ᴠɪᴇᴡ ᴀᴅᴅᴇᴅ ᴄʜᴀɴɴᴇʟs
<b>›› /fsub_mode :</b> ᴛᴏɢɢʟᴇ ꜰᴏʀᴄᴇ sᴜʙ ᴍᴏᴅᴇ
<b>›› /pbroadcast :</b> sᴇɴᴅ ᴘʜᴏᴛᴏ ᴛᴏ ᴀʟʟ ᴜꜱᴇʀs
<b>›› /add_admin :</b> ᴀᴅᴅ ᴀɴ ᴀᴅᴍɪɴ
<b>›› /deladmin :</b> ʀᴇᴍᴏᴠᴇ ᴀɴ ᴀᴅᴍɪɴ
<b>›› /admins :</b> ɢᴇᴛ ʟɪsᴛ ᴏꜰ ᴀᴅᴍɪɴs
<b>›› /addpremium :</b> ᴀᴅᴅ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ
<b>›› /premium_users :</b> ʟɪsᴛ ᴀʟʟ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀs
<b>›› /remove_premium :</b> ʀᴇᴍᴏᴠᴇ ᴘʀᴇᴍɪᴜᴍ ꜰʀᴏᴍ ᴀ ᴜꜱᴇʀ
<b>›› /myplan :</b> ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ sᴛᴀᴛᴜs
<b>›› /count :</b> ᴄᴏᴜɴᴛ</blockquote>
"""
#--------------------------------------------
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "") #set your Custom Caption here, Keep None for Disable Custom Caption
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False #set True if you want to prevent users from forwarding files from bot
#--------------------------------------------
#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'
#--------------------------------------------
BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "ʙᴀᴋᴋᴀ ! ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ꜱᴇɴᴘᴀɪ!!"

#==========================(BUY PREMIUM)====================#

#OWNER_TAG = os.environ.get("OWNER_TAG", "Weekends_Feedback_bot")
#UPI_ID = os.environ.get("UPI_ID", "Weekends_Feedback_bot")
#QR_PIC = os.environ.get("QR_PIC", "https://i.ibb.co/21yW232g/photo-2025-05-01-09-28-01-7499406687187501064.jpg")
#SCREENSHOT_URL = os.environ.get("SCREENSHOT_URL", f"https://t.me/+FRmXFSlecDI5NGJl")
#--------------------------------------------
#Time and its price
#7 Days
#PRICE1 = os.environ.get("PRICE1", "0 rs")
#1 Month
#PRICE2 = os.environ.get("PRICE2", "60 rs")
#3 Month
#PRICE3 = os.environ.get("PRICE3", "150 rs")
#6 Month
#PRICE4 = os.environ.get("PRICE4", "280 rs")
#1 Year
#PRICE5 = os.environ.get("PRICE5", "550 rs")

#===================(END)========================#

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
   
