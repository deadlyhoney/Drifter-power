import importlib
import re
import time
import asyncio
from platform import python_version as y
from sys import argv

from pyrogram import __version__ as pyrover
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import __version__ as telever
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown
from telethon import __version__ as tlhver

import MukeshRobot.modules.no_sql.users_db as sql
from MukeshRobot import (
    BOT_NAME,
    BOT_USERNAME,
    LOGGER,
    OWNER_ID,
    START_IMG,
    SUPPORT_CHAT,
    TOKEN,
    StartTime,
    dispatcher,
    pbot,
    telethn,
    updater,
)
from MukeshRobot.modules import ALL_MODULES
from MukeshRobot.modules.helper_funcs.chat_status import is_user_admin
from MukeshRobot.modules.helper_funcs.misc import paginate_modules


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time
PM_START_TEX = """ 
 ᴡᴇʟᴄᴏᴍᴇ {}  
""" 
 
 
PM_START_TEXT = """  
 
ʜᴇʏ {} , [❤️‍🔥]({}) 
 
──────「Gᴀʀᴏᴜ ガロウ」────── 
 
⌥ ɪ ᴀᴍ ɢᴀʀᴏᴜ, ᴀ ғᴀsᴛ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ᴀɴᴅ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ᴀᴅᴠᴀɴᴄᴇ ʙᴏᴛ ᴀʟʟ ᴛɪᴍᴇ ᴡɪᴛʜ ɴᴏ ʟᴀɢ.

▸ ɪ ʜᴀᴠᴇ ᴄʜᴀʀᴀᴄᴛᴇʀ ɢᴜᴇss ғᴇᴀᴛᴜʀᴇ ᴀʟsᴏ ᴀɴᴅ ᴄʜᴀᴛɢᴘᴛ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀʀᴛɪғɪᴄɪᴀʟ ɪɴᴛᴇʟʟɪɢᴇɴᴄᴇ ғᴇᴀᴛᴜʀᴇs. !
 
๏ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴍʏ ᴍᴏᴅᴜʟᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs ᴏғ Gᴀʀᴏᴜ ガロウ.
""" 

buttons = [ 
    [ 
        InlineKeyboardButton( 
            text=" ⛩ ᴀᴅᴅ ɢᴀʀᴏᴜ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ⛩ ", 
            url=f"https://t.me/{dispatcher.bot.username}?startgroup=true", 
        ), 
    ], 
    [ 
        InlineKeyboardButton(text=" 👾ʜᴇʟᴘ👾 ", callback_data="help_back"), 
        InlineKeyboardButton(text=" 🎵 Mᴜsɪᴄ 🎵 ", callback_data="no_back"), 
    ], 
    [ 
        InlineKeyboardButton(text=" 🍁sᴜᴘᴘᴏʀᴛ🍁 ", url=f"https://t.me/garou_support_chat"), 
        InlineKeyboardButton(text=" 🍁ᴜᴘᴅᴀᴛᴇs🍁 ", url=f"https://t.me/garou_updates"), 
    ], 
    [ 
        InlineKeyboardButton(text="", callback_data="gib_source"),  
        InlineKeyboardButton(text="", callback_data="Music_11"), 
], 
 
 
    [ 
        InlineKeyboardButton(text="ᴀʙᴏᴜᴛ ", callback_data="Radiux_"), 
    ], 
] 

HELP_STRINGS = f"""
» {BOT_NAME}  ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟʟᴏᴡ ᴛᴏ ɢᴇᴛ ᴅᴇsᴄʀɪᴘᴛɪᴏɴ ᴀʙᴏᴜᴛ sᴘᴇᴄɪғɪᴄs ᴄᴏᴍᴍᴀɴᴅ"""

DONATE_STRING = """ʜᴇʏ ʙᴀʙʏ,
  ʜᴀᴩᴩʏ ᴛᴏ ʜᴇᴀʀ ᴛʜᴀᴛ ʏᴏᴜ ᴡᴀɴɴᴀ ᴅᴏɴᴀᴛᴇ.

ʏᴏᴜ ᴄᴀɴ ᴅɪʀᴇᴄᴛʟʏ ᴄᴏɴᴛᴀᴄᴛ ᴍʏ [ᴅᴇᴠᴇʟᴏᴩᴇʀ](f"tg://user?id={OWNER_ID}") ғᴏʀ ᴅᴏɴᴀᴛɪɴɢ ᴏʀ ʏᴏᴜ ᴄᴀɴ ᴠɪsɪᴛ ᴍʏ [sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ](f"https://t.me/{SUPPORT_CHAT}") ᴀɴᴅ ᴀsᴋ ᴛʜᴇʀᴇ ᴀʙᴏᴜᴛ ᴅᴏɴᴀᴛɪᴏɴ."""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("MukeshRobot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


run_async
def test(update: Update, context: CallbackContext):
    # pprint(eval(str(update)))
    update.effective_message.reply_text(
        "Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN
    )
    update.effective_message.reply_text("This person edited a message")
    print(update.effective_message)


run_async
def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="𝐁𝙰𝙲𝙺", callback_data="help_back")]]
                    ),
                )

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            
            x=update.effective_message.reply_sticker(
"CAACAgQAAxkBAAIX9WXrJ89_2s1tx0B443tT7N2wDqoCAAKqCAACSUkZU0m0AAFDoqLaqTQE") 
            usr = update.effective_user 
            lol = update.effective_message.reply_text( 
                PM_START_TEX.format(usr.first_name), parse_mode=ParseMode.MARKDOWN 
            ) 
            time.sleep(0.6) 
            lol.edit_text("🔥")
            time.sleep(0.4)
            lol.edit_text("「Gᴀʀᴏᴜ ガロウ」") 
            time.sleep(0.6)
            lol.delete()
            
            update.effective_message.reply_text(
                PM_START_TEXT.format(escape_markdown(first_name), (START_IMG), BOT_NAME),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        update.effective_message.reply_photo(
            START_IMG,
            caption="ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴀʙʏ  !\n<b>ɪ ᴅɪᴅɴ'ᴛ sʟᴇᴘᴛ sɪɴᴄᴇ:</b> <code>{}</code>".format(
                uptime
            ),
            parse_mode=ParseMode.HTML,
        )


def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


run_async
def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "» *ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ* *{}* :\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="𝐁𝙰𝙲𝙺", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()

    except BadRequest:
        pass

            
    
run_async
def Iconic_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "Radiux_":
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(
            text=f"""
            𝐇𝙴𝚈 ᴅᴇᴀʀ,

ᴛʜɪs ɪs ɢᴀʀᴏᴜ , ᴀɴᴅ ɪᴛ's ɪᴄᴏɴɪᴄ ɪɴ ᴛʜᴇ ʀᴇᴀʟ sᴇɴsᴇ ᴀs ɪᴛ ɪs ᴀɴᴅ ɪɴᴛᴇʟʟɪɢᴇɴᴛ + ᴏʙᴇᴅɪᴇɴᴛ ʙᴏᴛ !!  
 
Iᴛ ʜᴀs ᴀ ʟᴏᴛ ᴏғ ғᴇᴀᴛᴜʀᴇs ᴡʜɪᴄʜ ɪs ᴛʜᴇ ʀᴇsᴜʟᴛ ᴏғ ᴀᴍᴀᴢɪɴɢ ʜᴀʀᴅᴡᴏʀᴋ ʙʏ ᴏᴜʀ ᴛᴇᴀᴍ ᴅᴇᴠᴇʟᴏᴘᴇʀ's...  
 
Oᴜᴛ ᴏғ ᴍᴀɴʏ ғᴇᴀᴛᴜʀᴇs, ᴛʜɪs ʙᴏᴛ ɪs ʙᴀsᴇᴅ ᴏɴ ᴛʜᴇ ɪᴍᴀɢɪɴᴀʀʏ.  
          """  , 
            parse_mode=ParseMode.MARKDOWN, 
            disable_web_page_preview=True, 
            reply_markup=InlineKeyboardMarkup( 
                [ 
                    [ 
                        InlineKeyboardButton( 
                            text="𝐎𝚆𝙽𝙴𝚁", url=f"https://t.me/who_am_i_think" 
                        ), 
                        InlineKeyboardButton( 
                            text="𝐒𝚄𝙿𝙿𝙾𝚁𝚃",  
                            url="https://t.me/garou_support_chat", 
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="𝐁𝙰𝙲𝙺", callback_data="Radiux_back"),
                    ],
                ]
            ),
        )
    elif query.data == "Radiux_back":
        first_name = update.effective_user.first_name 
        query.message.edit_text(
            PM_START_TEXT.format(escape_markdown(first_name), (START_IMG), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=False,
        )


run_async
def Music_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "Music_":
        query.message.edit_text(
            text=f"""
 ♥️ 𝐇𝙴𝚈 𝐁𝙰𝙱𝚈 ♥️ 
 
❍ *ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ「Gᴀʀᴏᴜ ガロウ」* 
 
❍ *ʜᴇʀᴇ ɪs ʏᴏᴜʀ ᴍᴜsɪᴄ ᴀʟʟ ғᴇᴀᴛᴜʀᴇs ᴏғ ɢᴀʀᴏᴜ. ɪ ᴀʟsᴏ ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴡɪᴛʜ ᴄʜᴀᴛɢᴘᴛ ғᴜɴᴄᴛɪᴏɴs ᴀʟsᴏ*  
 
❍ *𝟸𝟺x𝟽 ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ sᴍᴏᴏᴛʜʏ ᴏɴ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴀɴᴅ ᴘʀᴏᴠɪᴅᴇ ʙᴀᴅᴀss ǫᴜᴀʟɪᴛʏ*  
 
❍ *ᴀʟsᴏ ɢᴜᴇss ᴡᴀɪғᴜ ᴀɴᴅ ʜᴜsʙᴀɴᴅᴏᴏ ɴᴀᴍᴇ ᴀɴᴅ ᴀᴅᴅ ɪɴ ʏᴏᴜʀ ʜᴀʀᴇᴍ*  
""", 
           
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        
                InlineKeyboardButton(
                    text="𝐀𝙳𝙼𝙸𝙽",
                    callback_data="Music_1",
                ),
                        InlineKeyboardButton(text="𝐔𝚂𝙴𝚁𝚂", callback_data="Music_2"),
              ],
                 
                [
                        InlineKeyboardButton(text="𝐁𝙰𝙲𝙺", callback_data="Radiux_back"),
                    ],
                ]
           ),
        )
    elif query.data == "Music_1":
        query.message.edit_text(
            text=f"*❣️ Ꭺ𝙳𝙼𝙸𝙽'𝚂 Ꮯ𝙾𝙼𝙼𝙰𝙽𝙳𝚂 ❣️*"
            f"""

❀ ʜᴇʀᴇ ᴀʀᴇ ᴀʟʟ ᴍᴜsɪᴄ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs. ❀ 
 
*/pause* : ᴘᴀᴜsᴇ ᴛʜᴇ ᴏɴɢᴏɪɴɢ ᴍᴜsɪᴄ sᴛʀᴇᴀᴍ. 
 
*/resume* : ᴄᴏɴᴛɪɴᴜᴇs ᴛʜᴇ ᴘʀᴇᴠɪᴏᴜsʟʏ ᴏɴɢᴏɪɴɢ. 
 
*/skip* : sᴋɪᴘ ᴀ ᴄᴜʀʀᴇɴᴛ ᴛʀᴀᴄᴋ ᴏɴ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ. 
 
*/end* 𝐨𝐫 */stop* : sᴛᴏᴘ sᴏɴɢ ᴏɴ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ. 
 
*/player* : ᴅɪsᴘʟᴀʏs ᴛʜᴇ ᴜsᴇʀ-ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ ᴍᴜsɪᴄ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ. 
 
*/queue* : Uᴘᴄᴏᴍɪɴɢ ᴛʀᴀᴄᴋ ʟɪsᴛ.  

❀ [ɢᴀʀᴏᴜ ᴜᴘᴅᴀᴛᴇs](https://t.me/garou_updates) ❀ 
""", 
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="𝐁𝙰𝙲𝙺", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_2":
        query.message.edit_text(
             text=f"❀ *ᴜsᴇʀ ᴄᴀᴍᴍᴀɴᴅs* ❀" 
            f""" 
 
❍ */mstart* ➩ sᴛᴀʀᴛ ᴛʜᴇ ᴍᴜsɪᴄ ʙᴏᴛ. 
 
❍ */mhelp* ➩ Gᴇᴛ ʜᴇʟᴘ ᴄᴀᴍᴍᴀɴᴅs ғᴏʀ ʏᴏᴜ. 
 
❍ */addplaylist <song>* ➩ ᴀᴅᴅ sᴏɴɢ ɪɴ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ. 
 
❍ */playplaylist* ➩ ᴘʟᴀʏ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ. 
 
❍ */delplaylist* ➩ ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ᴘʟᴀʏʟɪsᴛ. 
 
߷ Gʀᴏᴜᴘ Sᴇᴛᴛɪɴɢs ߷ 
 
𖤓 */settings* ➙ ɢᴇᴛ ᴀ ᴄᴏᴍᴘʟᴇᴛᴇ ɢʀᴏᴜᴘ sᴇᴛᴛɪɴɢs ᴡɪᴛʜ ᴀʟʟ ɪɴʟɪɴᴇ ʙᴜᴛᴛᴏɴs 
 
❀ [ɢᴀʀᴏᴜ sᴜᴘᴘᴏʀᴛ](https://t.me/garou_support_chat) ❀ 
""", 
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="𝐁𝙰𝙲𝙺", callback_data="Music_"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_3":
        query.message.edit_text(
            text=
            f""" 

✿ ʜᴇʀᴇ ɪs ᴀʟʟ ᴀɴɪᴍᴇ ʀᴀɴᴅᴏᴍ ᴄᴏᴍᴍᴀɴᴅs.\n\n❍ /gecg ➛ sᴇɴᴅ ʀᴀɴᴅᴏᴍ ɢᴇᴄɢ ɪᴍɢ.\n❍ /avatar ➛ sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴀᴠᴀᴛᴀʀ ɪᴍɢ.\n❍ /foxgirl ➛ sᴇɴᴅs ʀᴀɴᴅᴏᴍ ғᴏxɢɪʀʟ sᴏᴜʀᴄᴇ ɪᴍᴀɢᴇs.\n❍ /waifus ➛ sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴡᴀɪғᴜ ɪᴍɢ.\n❍ /neko ➛ sᴇɴᴅs ʀᴀɴᴅᴏᴍ sғᴡ ɴᴇᴋᴏ sᴏᴜʀᴄᴇ ɪᴍᴀɢᴇs.\n❍ /gasm ➛ sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴏʀɢᴀsᴍ ɪᴍɢ.\n❍ /cuddle ➛ sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴄᴜᴅᴅʟᴇ ɪᴍɢ.\n❍ /shinobu ➛ sᴇɴᴅ ʀᴀɴᴅᴏᴍ sʜɪɴᴏʙᴜ ɪᴍɢ.\n❍ /megumin ➛ sᴇɴᴅ ʀᴀɴᴅᴏᴍ ᴍᴇɢᴜᴍɪɴ ɪᴍɢ.\n❍ /bully ➛ sᴇɴᴅ ʀᴀɴᴅᴏᴍ ʙᴜʟʟʏ ɪᴍɢ.\n❍ /cry ➛ sᴇɴᴅ ʀᴀɴᴅᴏᴍ ᴄʀʏ ɪᴍɢ.\n❍ /awoo ➛ sᴇɴᴅ ʀᴀɴᴅᴏᴍ ᴀᴡᴏᴏ ɪᴍɢ.

❀ [ɢᴀʀᴏᴜ ᴜᴘᴅᴀᴛᴇs](https://t.me/garou_updates) ❀ 
""", 
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="𝐁𝙰𝙲𝙺", callback_data="Music_5"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_4":
        query.message.edit_text(
            text=
            f"""
✿ ʜᴇʀᴇ ɪs ᴀʟʟ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴄᴀᴛᴄʜᴇʀ ( ɢᴀʙʙᴀʀ ʜᴇʀᴇᴍ ) ᴀɴɪᴍᴇ ᴄᴏᴍᴍᴀɴᴅs.\n\n❍ /guess ➛ ᴛᴏ ɢᴜᴇss ᴄʜᴀʀᴀᴄᴛᴇʀ.\n❍ /fav ➛ ᴀᴅᴅ ʏᴏᴜʀ ғᴀᴠʀᴀᴛᴇ.\n❍ /trade ➛ ᴛᴏ ᴛʀᴀᴅᴇ ᴄʜᴀʀᴀᴄᴛᴇʀs.\n❍ /gift ➛ ɢɪᴠᴇ ᴀɴʏ ᴄʜᴀʀᴀᴄᴛᴇʀ ғʀᴏᴍ ʏᴏᴜʀ ᴄᴏʟʟᴇᴄᴛɪᴏɴ ᴛᴏ ᴀɴᴏᴛʜᴇʀ ᴜsᴇʀ.\n❍ /collection ➛ ᴛᴏ sᴇᴇ ʏᴏᴜʀ ᴄᴏʟʟᴇᴄᴛɪᴏɴ.\n❍ /topgroups ➛ sᴇᴇ ᴛᴏᴘ ɢʀᴏᴜᴘs, ᴘᴘʟ ɢᴜᴇssᴇs ᴍᴏsᴛ ɪɴ ᴛʜᴀᴛ ɢʀᴏᴜᴘs.\n❍ /top ➛ ᴛᴏᴏ sᴇᴇ ᴛᴏᴘ ᴜsᴇʀs.\n❍ /ctop ➛ ʏᴏᴜʀ ᴄʜᴀᴛ ᴛᴏᴘ.\n❍ /changetime ➛ ᴄʜᴀɴɢᴇ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴀᴘᴘᴇᴀʀ ᴛɪᴍᴇ .\n❍ /herem ➛ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴄʜᴀᴛᴄʜ.

 [ɢᴀʀᴏᴜ sᴜᴘᴘᴏʀᴛ](https://t.me/garou_support-chat)  
 """,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="𝐁𝙰𝙲𝙺", callback_data="Music_5"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_5":
        query.message.edit_text(
            text=
            f"""
✿ Hᴇʀᴇ ᴀʀᴇ ʏᴏᴜʀ ᴀɴɪᴍᴇ ʀᴇʟᴀᴛᴇᴅ ᴍᴏᴅᴇs, ᴄʜᴏsᴇ ᴀɴʏ ᴏғ ᴛʜᴇᴍ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ  
 
✿ Aʟsᴏ, ᴛʜᴇʀᴇ ᴀʀᴇ ᴍᴀɴʏ ᴍᴏᴅᴜʟᴇs ɪɴ ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs ғᴏʀ ᴀɴɪᴍᴇ ʟᴏᴠᴇʀs !  
 
✿ Usᴇ /help ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴄʜᴇᴄᴋ ᴀʟʟ ᴏғ ᴛʜᴇᴍ  
 

[ɢᴀʀᴏᴜ sᴜᴘᴘᴏʀᴛ](https://t.me/garou_support-chat)  
""", 
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text = "ᴡᴀɪғᴜ-ʜᴜsʙᴀɴᴅᴏ", callback_data="Music_3"),
                        InlineKeyboardButton(text= "🍁ʜᴀʀᴇᴍ🍁", callback_data="Music_4"),
                    ],
                    [
                        InlineKeyboardButton(text="𝐁𝙰𝙲𝙺", callback_data="Music_11"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_6":
        query.message.edit_text(
            text=
            f"""
ᥫᩣ ʕ˖͜͡˖ʔ 𝐇𝙴𝚁𝙴 𝐈𝚂 𝐘𝙾𝚄𝚁 𝐇𝙴𝙻𝙿 & 𝐂𝙾𝙼𝙼𝙰𝙽𝙳𝚂 𝐑𝙴𝙻𝙰𝚃𝙴𝙳 𝐓𝙾 𝐑𝙰𝙸𝙳 𝐅𝙴𝙰𝚃𝚄𝚁𝙴 𝐈𝙽 𝐈𝙲𝙾𝙽𝙸𝙲 𝐑𝙾𝙱𝙾𝚃 ʕ˖͜͡˖ʔ ᥫᩣ


➩ Spam a message multiple times in the chat.

➩ /spam <count> <message>


❣️ [𒆜 𝐈𝙲𝙾𝙽𝙸𝙲 𝐁𝙾𝚃 ๖ۣ•҉ ᭄](https://t.me/iconic_robot) ❣️
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="𝐁𝙰𝙲𝙺", callback_data="Music_9"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_7":
        query.message.edit_text(
            text=
            f"""
𒈒 𝐇𝙴𝚁𝙴 𝐈𝚂 𝐘𝙾𝚄𝚁 𝐇𝙴𝙻𝙿 & 𝐂𝙾𝙼𝙼𝙰𝙽𝙳𝚂 𝐑𝙴𝙻𝙰𝚃𝙴𝙳 𝐓𝙾 𝐑𝙰𝙸𝙳 𝐅𝙴𝙰𝚃𝚄𝚁𝙴 𝐈𝙽 𝐈𝙲𝙾𝙽𝙸𝙲 𝐑𝙾𝙱𝙾𝚃 𒈒

➩ /raid <count> <@username>: *Spam raid messages tagging the specified user.*

➩ /mraid <count> <@username>: *Spam Mraid messages tagging the specified user.*

➩ /sraid <count> <@username>: *Spam Sraid messages tagging the specified user.*

➩ /rraid start: *Start reply raid on the user you're replying to. Every message they send will be auto-replied with a random message.*

➩ /rraid stop: *Stop the reply raid in the current chat.*


❣️ [𒆜 𝐈𝙲𝙾𝙽𝙸𝙲 𝐁𝙾𝚃 ๖ۣ•҉ ᭄](https://t.me/iconic_robot) ❣️
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="𝐁𝙰𝙲𝙺", callback_data="Music_9"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_8":
        query.message.edit_text(
            text=
            f"""

ᰔᩚ **Usᴇ `/chatbot on` ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴜsᴇ Iᴄᴏɴɪᴄ Bᴏᴛ's Cʜᴀᴛʙᴏᴛ ɪɴ ʏᴏᴜʀ ʀᴇsᴘᴇᴄᴛɪᴠᴇ ɢʀᴏᴜᴘs !!** ᰔᩚ

━━━━━━━━━━━━━━━━━━━━
💕 𝐈𝚃'𝚂 𝐁𝙰𝚂𝙴𝙳 𝐎𝙽 𝐈𝙼𝙰𝙶𝙸𝙽𝙰𝚁𝚈 𝐂𝙷𝙰𝚁𝙰𝙲𝚃𝙴𝚁`𝐈𝙲𝙲𝙷𝙰 𝐁𝙾𝚂𝙴` 𝐖𝙷𝙾 𝐖𝙸𝙻𝙻 𝐂𝙷𝙰𝚃 𝐖𝙸𝚃𝙷 𝐘𝙾𝚄 𝐀𝙽𝚈𝚃𝙸𝙼𝙴 𝐀𝙲𝙲𝙾𝚁𝙳𝙸𝙽𝙶 𝐓𝙾 𝐘𝙾𝚄𝚁 𝐎𝚁𝙳𝙴𝚁𝚂 !!! 💕

💓 𝐉𝚄𝚂𝚃 𝐓𝚈𝙿𝙴 𝙰 𝐌𝙴𝚂𝚂𝙰𝙶𝙴 𝐑𝙴𝙿𝙻𝚈𝙸𝙽𝙶 𝙾𝚁 𝐓𝙰𝙶𝙶𝙸𝙽𝙶 𝐈𝙲𝙾𝙽𝙸𝙲, 𝐀𝙽𝙳 𝐘𝙾𝚄 𝐖𝙸𝙻𝙻 𝐆𝙴𝚃 𝐀 𝐒𝚄𝙿𝙴𝚁𝙵𝙰𝚂𝚃 𝐑𝙴𝚂𝙿𝙾𝙽𝚂𝙴 𝐅𝚁𝙾𝙼 𝐈𝙲𝙲𝙷𝙰. 💓


❣️ [𒆜 𝐈𝙲𝙾𝙽𝙸𝙲 𝐁𝙾𝚃 ๖ۣ•҉ ᭄](https://t.me/iconic_robot) ❣️
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="𝐁𝙰𝙲𝙺", callback_data="Music_11"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_9":
        query.message.edit_text(
            text=
            f"""
✿ ʜᴇʀᴇ ɪꜱ ʜᴇʟᴘ ᴍᴇɴᴜ ꜰᴏʀ ꜱᴘᴀᴍ ʀᴀɪᴅ ✿

**𝐍𝐎𝐓𝐄 ➩ 𝐓𝙾 𝐔𝚂𝙴 𝐓𝙷𝙴𝚂𝙴 𝐂𝙾𝙼𝙼𝙰𝙽𝙳𝚂 𝐘𝙾𝚄 𝐌𝚄𝚂𝚃 𝐁𝙴 𝐎𝚆𝙽𝙴𝚁 𝐎𝚁 𝐀𝙳𝙼𝙸𝙽 𝐎𝙵 𝐀 𝐏𝙾𝙿𝚄𝙻𝙰𝚁 𝐂𝙷𝙰𝚃 𝐎𝚁 𝐂𝙷𝙰𝙽𝙽𝙴𝙻,**

**𝐈𝙵 𝐘𝙾𝚄 𝐀𝚁𝙴 𝐀𝙿𝙿𝙻𝙸𝙲𝙰𝙱𝙻𝙴, 𝐉𝙾𝙸𝙽 ➩ [𝐑𝙰𝙳𝙸𝚄𝚇 𝐒𝚄𝙿𝙿𝙾𝚁𝚃](https://t.me/The_Radiux_Support) 𝐀𝙽𝙳 𝐓𝙰𝙺𝙴 𝐒𝚄𝙳𝙾 𝐅𝚁𝙾𝙼 𝐓𝙷𝙴𝚁𝙴 !!**


❣️ [𒆜 𝐈𝙲𝙾𝙽𝙸𝙲 𝐁𝙾𝚃 ๖ۣ•҉ ᭄](https://t.me/iconic_robot) ❣️
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="𝐑𝙰𝙸𝙳", callback_data="Music_7"),
                        InlineKeyboardButton(text="𝐒𝙿𝙰𝙼", callback_data="Music_6"),
                    ],
                    [
                        InlineKeyboardButton(text="𝐁𝙰𝙲𝙺", callback_data="Music_11"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_10":
        query.message.edit_text(
            text=
            f"""
━━━━━━━━━━━━━━━━━━━━
➳ 𝐂ᴏᴍᴍᴀɴᴅ: /ask

💘 𝐀ʙᴏᴜᴛ: ᴜꜱᴇ ᴛʜᴇ /ask ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ɪɴᴛᴇʀᴀᴄᴛ ᴡɪᴛʜ ᴛʜᴇ ᴀᴅᴠᴀɴᴄᴇᴅ 𝙲𝙷𝙰𝚃 𝙶𝙿𝚃-𝟺 ᴍᴏᴅᴇʟ ꜰᴏʀ ᴀɴ ᴇɴʜᴀɴᴄᴇᴅ ᴄʜᴀᴛ ᴇxᴘᴇʀɪᴇɴᴄᴇ. ᴛʜɪꜱ ɪꜱ ᴀ ɴᴇᴡ ꜰᴇᴀᴛᴜʀᴇ, ᴀɴᴅ ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ɪᴛ ᴜɴʟɪᴍɪᴛᴇᴅʟʏ...

💗 𝐅ᴇᴀᴛᴜʀᴇꜱ: /ask ყσυɾ ɱεssαցҽ -- ɪɴɪᴛɪᴀᴛᴇ ᴀ ᴄᴏɴᴠᴇʀꜱɪᴏɴ ᴡɪᴛʜ 𝙲𝙷𝙰𝚃 𝙶𝙿𝚃-𝟺, ᴀɴᴅ ɪᴛ ᴡɪʟʟ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴏᴜɢʜᴛꜰᴜʟ ᴀɴᴅ ᴄᴏɴᴛᴇxᴛᴡᴀʀᴇ ʀᴇꜱᴘᴏɴꜱᴇꜱ.

╰┈➤𝐍ᴏᴛᴇ : 𝚃𝙷𝙸𝚂 𝙵𝙴𝙰𝚃𝚄𝚁𝙴 𝙸𝚂 𝙰𝚅𝙰𝙸𝙻𝙰𝙱𝙻𝙴 𝙵𝙾𝚁 𝙰𝙻𝙻 𝚄𝚂𝙴𝚁𝚂, 𝙰𝙽𝙳 𝙸𝚃 𝙰𝙳𝙳 𝙰 𝙿𝙾𝚆𝙴𝚁𝙵𝚄𝙻 𝙳𝙸𝙼𝙴𝙽𝚂𝙸𝙾𝙽 𝚃𝙾 𝚈𝙾𝚄𝚁 𝙲𝙷𝙰𝚃 𝙸𝙽𝚃𝙴𝚁𝙰𝙲𝚃𝙸𝙾𝙽𝚂. 𝙴𝙽𝙹𝙾𝚈 𝚃𝙷𝙴 𝚄𝙿𝙶𝚁𝙰𝙳𝙴𝙳 𝙲𝙰𝙿𝙰𝙱𝙸𝙻𝙸𝚃𝙸𝙴𝚂 ᴏғ  𝐂𝐇𝐀𝐓 𝐆𝐏𝐓-𝟒 𝚂𝙴𝙰𝙼𝙻𝙴𝚂𝚂𝙻𝚈!

━━━━━━━━━━━━━━━━━━━━

❣️ [𒆜 𝐈𝙲𝙾𝙽𝙸𝙲 𝐁𝙾𝚃 ๖ۣ•҉ ᭄](https://t.me/iconic_robot) ❣️
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="𝐁𝙰𝙲𝙺", callback_data="Music_11"),
                    ]
                ]
            ),
        )
    elif query.data == "Music_11":
        query.message.edit_text(
            text=f"*߷︎ 𝐂𝙷𝙾𝚂𝙴 𝐀𝙽𝚈 𝐎𝙵 𝐓𝙷𝙴 𝐌𝙾𝙳𝙴𝚂 𝐓𝙾 𝐂𝙾𝙽𝚃𝙸𝙽𝚄𝙴 ߷︎*"
            f"""


❣️ [𒆜 𝐈𝙲𝙾𝙽𝙸𝙲 𝐁𝙾𝚃 ๖ۣ•҉ ᭄](https://t.me/iconic_robot) ❣️ """,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="𝐒𝙿𝙰𝙼-𝐌𝙴𝙽𝚄", callback_data="Music_9"),
                        InlineKeyboardButton(text="𝐈𝙲𝙲𝙷𝙰-𝐂𝙷𝙰𝚃-𝐁𝙾𝚃", callback_data="Music_8"),
                    ],
                    [
                        InlineKeyboardButton(text="𝐂𝙷𝙰𝚃 𝐆𝙿𝚃", callback_data="Music_10"),
                        InlineKeyboardButton(text="𝐀𝙽𝙸𝙼𝙴", callback_data="Music_5"),
                    ],

                        [
                        InlineKeyboardButton(text="𝐁𝙰𝙲𝙺", callback_data="Radiux_back"),
                    ],
                ]
            ),
        )
    elif query.data == "Music_back":
        first_name = update.effective_user.first_name
        query.message.edit_text(
            PM_START_TEXT.format(escape_markdown(first_name), (START_IMG), BOT_NAME),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=False,
        )


run_async
def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_text(
                f"Contact me in PM to get help of {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="𝐇𝙴𝙻𝙿 ",
                                url="t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_text(
            "ᥫᩣ 𝐂𝙷𝙾𝚂𝙴 𝐀𝙽 𝐎𝙿𝚃𝙸𝙾𝙽 𝐅𝙾𝚁 𝐆𝙴𝚃𝚃𝙸𝙽𝙶 𝐇𝙴𝙻𝙿 ᰔᩚ",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="𝐒𝚃𝙰𝚁𝚃 𝐈𝙽 𝐏𝚁𝙸𝚅𝙰𝚃𝙴",
                            url="https://t.me/{}?start=help".format(
                                context.bot.username
                            ),
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="𝐎𝙿𝙴𝙽 𝐇𝙴𝚁𝙴",
                            callback_data="help_back",
                        )
                    ],
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="𝐁𝙰𝙲𝙺", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="Which module would you like to check {}'s settings for?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any chat settings available :'(\nSend this "
                "in a group chat you're admin in to find its current settings!",
                parse_mode=ParseMode.MARKDOWN,
            )


run_async
def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="◁",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                text="Hi there! There are quite a few settings for {} - go ahead and pick what "
                "you're interested in.".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Message is not modified",
            "Query_id_invalid",
            "Message can't be deleted",
        ]:
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))


run_async
def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "Click here to get this chat's settings, as well as yours."
            msg.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="𝐒𝙴𝚃𝚃𝙸𝙽𝙶𝚂",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "Click here to check your settings."

    else:
        send_settings(chat.id, user.id, True)


run_async
def donate(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    bot = context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )

        if OWNER_ID != {OWNER_ID} and DONATION_LINK:
            update.effective_message.reply_text(
                f"» ᴛʜᴇ ᴅᴇᴠᴇʟᴏᴩᴇʀ ᴏғ {dispatcher.bot.first_name} sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ɪs [VIP BOY](https://t.me/Queen_sakhi)"
                f"\n\nʙᴜᴛ ʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴅᴏɴᴀᴛᴇ ᴛᴏ ᴛʜᴇ ᴩᴇʀsᴏɴ ᴄᴜʀʀᴇɴᴛʟʏ ʀᴜɴɴɪɴɢ ᴍᴇ : [ʜᴇʀᴇ]({DONATION_LINK})",
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )

    else:
        try:
            bot.send_message(
                user.id,
                DONATE_STRING,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )

            update.effective_message.reply_text(
                "ɪ'ᴠᴇ ᴘᴍ'ᴇᴅ ʏᴏᴜ ᴀʙᴏᴜᴛ ᴅᴏɴᴀᴛɪɴɢ ᴛᴏ ᴍʏ ᴄʀᴇᴀᴛᴏʀ!"
            )
        except Unauthorized:
            update.effective_message.reply_text(
                "ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ ᴘᴍ ғɪʀsᴛ ᴛᴏ ɢᴇᴛ ᴅᴏɴᴀᴛɪᴏɴ ɪɴғᴏʀᴍᴀᴛɪᴏɴ."
            )


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def main():

    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
           dispatcher.bot.send_photo(
                f"@{SUPPORT_CHAT}",
                photo=f"{START_IMG}",
                caption=f"""
✿ {BOT_NAME} ɪs ᴀʟɪᴠᴇ ʙᴀʙʏ 
     ━━━━━━━𒈒✿𒈒━━━━━━━
**ᰔᩚ ᴍᴀᴅᴇ ʙʏ ➵ ʀᴀᴅɪᴜx**
**ᰔᩚ ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ ➵** `{y()}`
**ᰔᩚ ʟɪʙʀᴀʀʏ ᴠᴇʀsɪᴏɴ ➵** `{telever}`
**ᰔᩚ ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀsɪᴏɴ ➵** `{tlhver}`
**ᰔᩚ ᴩʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ ➵** `{pyrover}`
     ━━━━━━━𒈒✿𒈒━━━━━━━
""",
                parse_mode=ParseMode.MARKDOWN,
            )
        except Unauthorized:
            LOGGER.warning(
                f"Bot isn't able to send message to @{SUPPORT_CHAT}, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)

    CommandHandler("test", test)
    start_handler = CommandHandler("start", start)

    help_handler = CommandHandler("help", get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_.*")

    settings_handler = CommandHandler("settings", get_settings)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_")

    about_callback_handler = CallbackQueryHandler(
        Iconic_about_callback, pattern=r"Radiux_"
    )
    Music_callback_handler = CallbackQueryHandler(
        Music_about_callback, pattern=r"Music_"
    )

    donate_handler = CommandHandler("donate", donate)
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)

    # dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(Music_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)

    dispatcher.add_error_handler(error_callback)

    LOGGER.info("💝 𝐁𝙾𝚃 𝐒𝚃𝙰𝚁𝚃𝙴𝙳 𝐒𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 💝\n\n╔═════ᥫᩣ۩ღ۩ᥫᩣ════╗\n\n➟ ๏ 𝐈𝐂𝐎𝐍𝐈𝐂 💕\n\n╚═════ᥫᩣ۩ღ۩ᥫᩣ════╝")
    updater.start_polling(timeout=15, read_latency=4, drop_pending_updates=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    telethn.start(bot_token=TOKEN)
    pbot.start()
    main()
