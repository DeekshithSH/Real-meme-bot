import logging
import math
from datetime import datetime
from Bot.bot import TGBot
from Bot.utils.Translation import Names
from Bot.vars import Var
from Bot.utils.database import Database
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums.parse_mode import ParseMode
db = Database()


@TGBot.on_callback_query()
async def cb_data(bot, update: CallbackQuery):
    cd=update.data.split("|")
    if cd[0]=="NA":
        await update.answer("Not Available")

    elif cd[0]=="divl":
        await gen_device_list(update, int(cd[1]))

    elif cd[0]=="div":
        await gen_file_type_list(update, cd[1])

    elif cd[0]=="typ":
        await gen_file_list(update, cd[1], cd[2], int(cd[3]))

    elif cd[0]=="file":
        await gen_ver_list(update, cd[1], cd[2], cd[3],int(cd[4]))

    elif cd[0]=="version":
        await gen_message(update, cd[1],cd[2], cd[3])

    elif cd[0]=="old":
        await gen_oldbuild_list(update, int(cd[1]))

async def gen_device_list(update: CallbackQuery, page_no:int):
    device_names = [item for item in (await db.get_db_names()) if not item.endswith('(Old)')] 
    list_len=len(device_names)
    lrange=[((page_no-1)*10),(page_no*10)]
    device_names=device_names[lrange[0]:lrange[1]]
    btn=[]
    for x in device_names:
        btn.append([InlineKeyboardButton(str(Names.Device.get(x, x)), f"div|{str(x)}")])

    nav_btn=[
        InlineKeyboardButton("<<", "{}".format("divl|"+str(page_no-1) if page_no>1 else "NA")),
        InlineKeyboardButton(f"{page_no}/{math.ceil(list_len/10)}", "NA"),
        InlineKeyboardButton(">>", "{}".format("divl|"+str(page_no+1) if list_len>page_no*10 else "NA"))
    ]
    btn.append([InlineKeyboardButton("🕰️ Old Build", "old|1")])
    btn.append(nav_btn)
    await update.edit_message_text("Select Device", reply_markup=InlineKeyboardMarkup(btn))

async def gen_file_type_list(update:CallbackQuery, device):
    file_type=await db.get_col_names(device)
    btn=[]
    for x in file_type:
        btn.append([InlineKeyboardButton(str(Names.Type.get(x,x)), f"typ|{device}|{str(x)}|1")])
    btn.append([InlineKeyboardButton(Names.Other[0], "divl|1")])
    await update.edit_message_text(f"{device}\nSelect Type", reply_markup=InlineKeyboardMarkup(btn))

async def gen_file_list(update:CallbackQuery, device:str, file_type:str, page_no:int):
    files=await db.get_doc_names(device,file_type)
    list_len=len(files)
    lrange=[((page_no-1)*10),(page_no*10)]
    files=files[lrange[0]:lrange[1]]

    btn=[]
    for x in files:
        btn.append([InlineKeyboardButton(x, f"file|{device}|{file_type}|{str(x)}|1")])

    nav_btn=[
        InlineKeyboardButton("<<", "{}".format(f"typ|{device}|{file_type}|"+str(page_no-1) if page_no>1 else "NA")),
        InlineKeyboardButton(f"{page_no}/{math.ceil(list_len/10)}", "NA"),
        InlineKeyboardButton(">>", "{}".format(f"typ|{device}|{file_type}|"+str(page_no+1) if list_len>page_no*10 else "NA"))
    ]
    btn.append(nav_btn)
    btn.append([InlineKeyboardButton(Names.Other[0], f"div|{device}")])
    await update.edit_message_text(f"{device}\nSelect a {file_type}", reply_markup=InlineKeyboardMarkup(btn))

async def gen_ver_list(update:CallbackQuery,device:str, file_type:str, file:str, page_no:int):
    file_range=[page_no*10-10+1, page_no*10]
    versions, total_files=await db.get_file_byname(device, file_type, file, file_range)
    btn=[]
    async for x in versions:
        btn.append([InlineKeyboardButton(x.get("version"), callback_data=f"version|{device}|{file_type}|{x.get('_id')}")])
    btn.append(
        [
            InlineKeyboardButton("<<", callback_data="{}".format(f"file|{device}|{file_type}|{file}|"+str(page_no-1) if page_no > 1 else 'NA')),
            InlineKeyboardButton(f"{page_no}/{math.ceil(total_files/10)}", callback_data="NA"),
            InlineKeyboardButton(">>", callback_data="{}".format(f"file|{device}|{file_type}|{file}|"+str(page_no+1) if total_files > page_no*10 else 'NA'))
        ]
    )
    btn.append([InlineKeyboardButton(Names.Other[0], f"typ|{device}|{file_type}|1")])
    await update.edit_message_text(f"{device}\n{file_type}\nSelect a {file} Version\n{file_type}", reply_markup=InlineKeyboardMarkup(btn))

async def gen_message(update:CallbackQuery,device:str,file_type:str,_id:str):
    data=await db.get_file_byid(device,file_type,_id)
    date=datetime.strftime(data.get('release_date'), "%d-%m-%Y")
    message=f"""------------------
<a href=https://t.me/c/{str(data.get('channel_id')).removeprefix('-100')}/{data.get('msg_id')}>Post Link</a>
------------------
<b>{data.get('name')} | {data.get('version')} | {data.get('type')}</b>
<b>{data.get('status') if not (data.get('type')=='Kernel') else ''}</b>
<b>{'Android '+data.get('android_version') if data.get('android_version') else ''} {'Kernel '+data.get('kernel_version') if data.get('kernel_version') else ''}</b>
by @{data.get('dev')}
Release Date {date}
"""
    btn=[]
    for x,y in (data.get("download_link")).items():
        btn.append([InlineKeyboardButton(x, url=y)])
    await update.message.reply_text(message, None, ParseMode.HTML, None, True, reply_markup=InlineKeyboardMarkup(btn))
    await update.answer(data.get('name'))

async def gen_oldbuild_list(update: CallbackQuery, page_no:int):
    device_names = [item for item in (await db.get_db_names()) if item.endswith('(Old)')] 
    list_len=len(device_names)
    lrange=[((page_no-1)*10),(page_no*10)]
    device_names=device_names[lrange[0]:lrange[1]]
    btn=[]
    for x in device_names:
        btn.append([InlineKeyboardButton(str(Names.Device.get(x, x)), f"div|{str(x)}")])

    nav_btn=[
        InlineKeyboardButton("<<", "{}".format("divl|"+str(page_no-1) if page_no>1 else "NA")),
        InlineKeyboardButton(f"{page_no}/{math.ceil(list_len/10)}", "NA"),
        InlineKeyboardButton(">>", "{}".format("divl|"+str(page_no+1) if list_len>page_no*10 else "NA"))
    ]
    btn.append(nav_btn)
    btn.append([InlineKeyboardButton(Names.Other[0], f"divl|1")])
    await update.edit_message_text("Select Device", reply_markup=InlineKeyboardMarkup(btn))