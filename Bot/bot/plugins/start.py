import math
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Bot.vars import Var
from Bot.bot import TGBot
from Bot.utils.database import Database
db = Database()

@TGBot.on_message(filters.command("start") & filters.private)
async def start(bot: Client, message: Message):
    if not bool(await db.get_user(message.from_user.id)):
        await db.add_user(message.from_user.id)

    db_names = await db.get_db_names()
    await message.reply_text(
        f"Current Status [Message ID]({Var.UPDATE_STATUS})\nSelect a Device",
        quote=True,
        reply_markup=InlineKeyboardMarkup(await get_div_list(db_names)),
        disable_web_page_preview=True
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

@TGBot.on_message(filters.command("update") & filters.private & filters.text & filters.user(Var.AUTH_USER))
async def update(bot: Client, message: Message):
    Var.UPDATE_STATUS=message.text.removeprefix("/update ")
    await message.reply_text(Var.UPDATE_STATUS)