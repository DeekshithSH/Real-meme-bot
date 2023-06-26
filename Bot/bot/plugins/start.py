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
    for x in db_names:
        btn.append([InlineKeyboardButton(str(x), str(x))])
    return btn
