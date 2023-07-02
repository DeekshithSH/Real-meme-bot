import logging
from pyrogram import Client
from Bot.vars import Var

TGBot=Client(
    "Bot_session",
    api_id=Var.API_ID,
    api_hash=Var.API_HASH,
    bot_token=Var.BOT_TOKEN,
    workdir="Bot",
    plugins={"root": "Bot/bot/plugins"},
    sleep_threshold=Var.SLEEP_THRESHOLD,
    workers=Var.WORKERS
    )