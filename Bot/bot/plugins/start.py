import math
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Bot.bot import TGBot
from Bot.utils.database import Database
db = Database()

@TGBot.on_message(filters.command("start") & filters.private)
async def start(bot: Client, message: Message):
    db_names = await db.get_db_names()
    await message.reply_text(
        "Hi 16-06-2023",
        quote=True,
        reply_markup=InlineKeyboardMarkup(await get_div_list(db_names))
    )

async def get_div_list(db_names):
    btn=[]
    for x in db_names[0:10]:
        btn.append([InlineKeyboardButton(str(x), f"div|{str(x)}")])
    
    nav_btn=[
        InlineKeyboardButton("<<", "NA"),
        InlineKeyboardButton(f"1/{math.ceil(len(db_names)/10)}", "NA"),
        InlineKeyboardButton(">>", "{}".format("divl|2" if len(btn)>10 else "NA"))
    ]
    btn.append(nav_btn)
    return btn
