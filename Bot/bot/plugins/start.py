from datetime import datetime
import re
import json
import logging
import math
import sys
from bson import ObjectId
import pymongo
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from Bot.bot import TGBot
from Bot.vars import Var
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

@TGBot.on_message(filters.command("help") & filters.private)
async def help(bot: Client, message: Message):
    await message.reply_text(Command_Text.help, disable_web_page_preview=True)

@TGBot.on_message(filters.command("add") & filters.private & filters.user(Var.ADMIN_ID))
async def help(bot: Client, message: Message):
    await message.reply_text(
        "{}",
        reply_markup=ForceReply(placeholder="Post Link")
    )
    await message.reply_text("Send Channel/Group message link where the Build was Posted")

@TGBot.on_message(filters.private & filters.text & filters.reply & filters.user(Var.ADMIN_ID))
async def reply_handler(bot: Client, message: Message):
    if message.text in ["/upload"]:
        message.continue_propagation()
    logging.debug("reply_handler start")
    try:
        data: dict =json.loads(message.reply_to_message.text)
        logging.debug("Decoded json")
    except json.JSONDecodeError:
        logging.debug(sys.exc_info())
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
        logging.debug("Missing Key: {}".format(missing_keys))
        logging.debug("Next Key:{}".format(missing_keys[1]))
        await message.reply_text(str(json.dumps(data, indent=2)), reply_markup=ForceReply(None, str(missing_keys[1])), disable_web_page_preview=True)
        await message.reply_text(Command_Text.reply.get(missing_keys[1]))
        if missing_keys[1] == "device":
            text="Devices:\n"
            for x in await db.get_db_names():
                logging.debug(x)
                text+=f"<code>{x}</code>\n"
            await message.reply_text(text)
        elif missing_keys[1] == "name":
            text="{}\n".format(data.get("type"))
            for x in await db.get_doc_names(data["device"], data["type"]):
                text+=f"<code>{x}</code>\n"
            await message.reply_text(text)
    else:
        if data.get("done", False):
            await message.reply_text(str(json.dumps(data, indent=2)), reply_markup=ForceReply(None, "/upload"), disable_web_page_preview=True)
            return await message.reply_text("Send /upload to Upload the Build to Database")
            
        else:
            dl_links=data.get("download_link", {})
            if dl_links:
                x,y=list(dl_links.keys())[-1], list(dl_links.values())[-1]

                if x and not y:
                    dl_links[x]=message.text
                    data["download_link"]=dl_links
                    await message.reply_text(str(json.dumps(data, indent=2)), reply_markup=ForceReply(None, "Build Name"), disable_web_page_preview=True)
                    await message.reply_text("Send Button Text Name")
                    return await message.reply_text("Send Done if your done")
                elif message.text.lower() == "done":
                    data["done"]=True
                    await message.reply_text(str(json.dumps(data, indent=2)), reply_markup=ForceReply(None, "/upload"), disable_web_page_preview=True)
                    return await message.reply_text("Send /upload to Upload the Build to Database")
                else:
                    dl_links[message.text]=False
                    data["download_link"]=dl_links
                    await message.reply_text(str(json.dumps(data, indent=2)), reply_markup=ForceReply(None, "{} Link".format(message.text)), disable_web_page_preview=True)
                    return await message.reply_text("Send Download Link for {}".format(message.text))
            else:
                dl_links[message.text]=False
                data["download_link"]=dl_links
                await message.reply_text(str(json.dumps(data, indent=2)), reply_markup=ForceReply(None, "{} Link".format(message.text)), disable_web_page_preview=True)
                return await message.reply_text("Send Download Link for {}".format(message.text))
            

@TGBot.on_message(filters.private & filters.reply & filters.command("upload") & filters.user(Var.ADMIN_ID))
async def post_process(bot: Client, message:Message):
    try:
        json_data: dict =json.loads(message.reply_to_message.text)
        logging.debug("Decoded json")
    except json.JSONDecodeError:
        logging.debug(sys.exc_info())
        message.continue_propagation()  
    
    pattern = r"https:\/\/t\.me\/(?P<username>[a-zA-Z0-9_-]+)\/(\d+\/)?(?P<message_id>\d+)"
    match = re.match(pattern, json_data.get("post_link"))

    data: dict={

    }
    
    if match:
        data["channel_username"] = match.group("username")
        data["msg_id"] = match.group("message_id")
        try:
            data["channel_id"] = (await bot.get_chat(data["channel_username"])).id
        except:
            data["channel_id"] = None
    else:
        data["post_link"] = json_data.get("post_link")

    device = list(str(json_data.get("device")).split(","))
    i=0
    for y in device:
        for x in await db.get_db_names():
            if str(x).casefold().replace(" ","") == str(y).casefold().replace(" ", ""):
                device[0]=x
        i+=1
    data["device"]=device

    data["type"] = str(json_data.get("type"))
    if data["type"].lower() == "rom":
        data["type"]="ROM"
    elif data["type"].lower() == "recovery":
        data["type"]="Recovery"
    elif data["type"].lower() == "kernel":
        data["type"]="Kernel"

    data["name"] = str(json_data.get("name"))
    for x in await db.get_doc_names(data["device"], data["type"]):
        if (data["name"].casefold().replace(" ", "")) == (str(x).casefold().replace(" ", "")):
            data["name"] = str(x)
    
    data["version"] = str(json_data.get("version"))

    data["status"] = str(json_data.get("status")).casefold().replace(" ","")
    if data["status"] == "official":
        data["status"]="Official"
    elif data["status"] == "community":
        data["status"]="Community"
    elif data["status"] == "port":
        data["status"]="Port"
    else:
        data["status"]="Unofficial"

    try:
        data["release_date"]=datetime.strptime(json_data.get("release_date"), "%d-%m-%Y")
    except:
        return await message.reply_text("Wrong Date Format")
    
    data["dev"]=json_data.get("dev").removeprefix("@")

    url_pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    dl_links={}
    for x,y in json_data.get("download_link").items():
        match = re.match(url_pattern, y)
        if match:
            dl_links[x]=match.groups()[0]
        else:
            return await message.reply_text("Invalid Download Link")
    data["download_link"]=dl_links

    if data["type"]=="ROM":
        data["android_version"]=json_data.get("android_version")
    elif data["type"]=="Kernel":
        data["kernel_version"]=json_data.get("kernel_version")
        if str(data["kernel_version"]).lower() == "none":
            data["kernel_version"]=None

    data["_id"] = ObjectId.from_datetime(data["release_date"])
    for x in data["device"]:
        await add_data(x, data)
    data["release_date"]=str(data["release_date"])
    data["_id"]=str(data["_id"])
    await message.reply_text(json.dumps(data, indent=2))

async def add_data(x:str, data):
    try:
        await db.add_file(str(x), data["type"], data)
    except pymongo.errors.DuplicateKeyError as e:
        logging.error("Error: Duplicate key")
        new_date_obj = data["release_date"].strftime("%d-%m-%Y") + " " + datetime.now().strftime("%H:%M")

        data["release_date"]=datetime.strptime(new_date_obj, "%d-%m-%Y %H:%M")
        data["_id"] = ObjectId.from_datetime(data["release_date"])  
        await add_data(x, data)