from Bot.bot import TGBot
from Bot.vars import Var
from Bot.utils.database import Database
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums.parse_mode import ParseMode
db = Database()


@TGBot.on_callback_query()
async def cb_data(bot, update: CallbackQuery):
    cd = update.data.split("|")
    if (cd[0] == "by_ver"):
        data=await db.get_file_byid(cd[1], cd[2], cd[3])
        await update.edit_message_text(
            f"---\n[Goto Post](https://t.me/c/{str(data.get('channel_id')).removeprefix('-100')}/{data.get('msg_id')})\n---\n{data.get('name')}\nVersion{data.get('version')}\n{data.get('status')}\nby @{data.get('dev')}\nRelease Date {data.get('release_date')}\n",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(gen_dl_btn(data.get('download_link'))),
            parse_mode=ParseMode.MARKDOWN
            )

    elif (len(cd)==1):
        col_names=await db.get_col_names(cd[0])
        await update.edit_message_reply_markup(InlineKeyboardMarkup(get_btn(col_names,update.data)))
    
    elif (len(cd)==2):
        docs=await db.get_doc_names(cd[0], cd[1])
        await update.edit_message_reply_markup(InlineKeyboardMarkup(get_btn(docs,update.data)))

    elif (len(cd)==3):
        data=await db.get_file_byname (cd[0], cd[1], cd[2])
        await update.edit_message_reply_markup(InlineKeyboardMarkup(await get_ver_btn(data, cd)))


def get_btn(list_data, old_data):
    btn=[]
    for x in list_data:
        btn.append([InlineKeyboardButton(str(x), old_data+"|"+str(x))])
    return btn

async def get_ver_btn(data,old_data):
    btn=[]
    async for x in data:
        btn.append([InlineKeyboardButton(x.get("version"), f"by_ver|{old_data[0]}|{old_data[1]}|{x.get('_id')}")])
    return btn

def gen_dl_btn(data):
    btn=[]
    for x, y in data.items():
        btn.append([InlineKeyboardButton(str(x), url=str(y))])
    return btn