from pyrogram import filters, Client
from pyrogram.types import Message
from Bot.bot import TGBot

@TGBot.on_message(filters.command("start") & filters.private)
async def start(bot: Client, message: Message):
    await message.reply_text(
        "Hi 16-06-2023",
        quote=True,
    )