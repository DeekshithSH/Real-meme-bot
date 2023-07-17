import re
import json
import logging
import math
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from Bot.vars import Var
from Bot.bot import TGBot
from Bot.utils.Translation import Names, Command_Text, Types
from Bot.utils.database import Database
db = Database()

@TGBot.on_message(filters.command("start") & filters.private)
async def start(bot: Client, message: Message):
    if not bool(await db.get_user(message.from_user.id)):
        await db.add_user(message.from_user.id)

    db_names = [item for item in (await db.get_db_names()) if not item.endswith('(Old)')]            
    await message.reply_text(
        f"Hi {message.from_user.mention()},\n{Command_Text.start}\nSelect a Device",
        quote=True,
        reply_markup=InlineKeyboardMarkup(await get_div_list(db_names)),
        disable_web_page_preview=True
    )

async def get_div_list(db_names):
    btn=[]
    for x in db_names[0:10]:
        btn.append([InlineKeyboardButton(str(Names.Device.get(x, x)), f"div|{str(x)}")])
    
    nav_btn=[
        InlineKeyboardButton("<<", "NA"),
        InlineKeyboardButton(f"1/{math.ceil(len(db_names)/10)}", "NA"),
        InlineKeyboardButton(">>", "{}".format("divl|2" if len(btn)>10 else "NA"))
    ]
    btn.append([InlineKeyboardButton("🕰️ Old Build", "old|1")])
    btn.append(nav_btn)
    return btn

# @TGBot.on_message(filters.command("update") & filters.private & filters.text & filters.user(Var.AUTH_USER))
# async def update(bot: Client, message: Message):
#     Var.UPDATE_STATUS=message.text.removeprefix("/update ")
#     await message.reply_text(Var.UPDATE_STATUS)

@TGBot.on_message(filters.command("help") & filters.private)
async def help(bot: Client, message: Message):
    await message.reply_text(Command_Text.help, disable_web_page_preview=True)

@TGBot.on_message(filters.command("add") & filters.private)
async def help(bot: Client, message: Message):
    await message.reply_text(
        "{}",
        reply_markup=ForceReply(placeholder="Post Link")
    )
    await message.reply_text("Send Channel/Group message link where the Build was Posted")

@TGBot.on_message(filters.private & filters.text & filters.reply)
async def reply_handler(bot: Client, message: Message):
    logging.debug("reply_handler start")
    try:
        data: dict =json.loads(message.reply_to_message.text)
        logging.debug("Decoded json")
    except json.JSONDecodeError:
        message.continue_propagation()

    build_type=str(data.get("type", None)).lower()
    if build_type == "rom":
        key_list=Types.ROM
    elif build_type == "kernel":
        key_list=Types.Kernel
    else:
        key_list=Types.Recovery

    missing_keys = []
    for key in key_list:
        if key not in data:
            missing_keys.append(key)

    if len(missing_keys)>1:
        data[missing_keys[0]]=message.text
        await message.reply_text(Command_Text.reply.get(missing_keys[1], "Something went wrong\nContact the Owner"))
        await message.reply_text(str(json.dumps(data, indent=2)), reply_markup=ForceReply(None, str(missing_keys[1])))
    else:
        if data.get("done", False):
            if message.text.lower() == "yes":
                return await post_process(message)
            else:
                await message.reply_text("There is now way to Edit the data<br>send <code>Yes</code> when yes to upload")
                return await message.reply_text(str(json.dumps(data, indent=2)), reply_markup=ForceReply(None, "Yes"))
            
        else:
            dl_links=data.get("download_link", False)
            if dl_links:
                for x, y in dl_links.items():
                    if x and not y:
                        dl_links[x]=message.text
                        await message.reply_text("Send Button Text Name")
                        await message.reply_text("Send Done if your done")
                        await message.reply_text(str(json.dumps(data, indent=2)), reply_markup=ForceReply(None, "Build Name"))
                    elif message.text.lower() == "done":
                        data["done"]=True
                        await message.reply_text("Send <code>yes</code> to Upload the Build to Database")
                        await message.reply_text(str(json.dumps(data, indent=2)), reply_markup=ForceReply(None, "Yes"))
                    else:
                        dl_links[message.text]=False
                        await message.reply_text("Send Download Link for {}".format(message.text))
                        await message.reply_text(str(json.dumps(data, indent=2)), reply_markup=ForceReply(None, "{} Link".format(message.text)))
            else:
                await message.reply_text("Now Send Download Link Button Text<br>First Send Text Apear on The Download Button")
                dl_links[message.text]=False
                await message.reply_text("Send Download Link for {}".format(message.text))
                await message.reply_text(str(json.dumps(data, indent=2)), reply_markup=ForceReply(None, "{} Link".format(message.text)))

async def post_process(message:Message):
    print(json.dumps(message.reply_to_message.text, indent=2))  
    #
@TGBot.on_message(filters.command("test") & filters.private)
async def start_handler(bot: Client, message: Message):
    await message.reply_text("Hi", reply_markup=ForceReply(None, "text"))
#----Post process----
# pattern = r"https:\/\/t\.me\/(?<username>[a-zA-Z0-9_-]+)\/\d+\/(?<message_id>\d+)|https:\/\/t\.me\/(?<username>[a-zA-Z0-9_-]+)\/(?<message_id>\d+)"
# match = re.match(pattern, message.text)

# if match:
#     channel_username = match.group("username")
#     msg_id = match.group("message_id")
#     channel_id=(await bot.get_chat(channel_username)).id


# def get_button(m:Message):
#     if m.reply_markup:
#         if m.reply_markup.inline_keyboard:
#             btn_data=[]
#             for x in m.reply_markup.inline_keyboard:
#                 for y in x:
#                     if y.callback_data:
#                         btn_data.append(y.callback_data)
#             return btn_data
#     return []

# def get_next_data(text:str):
#     steps=[
#         "msg_id"
#     ]
#     text=text.split("|")