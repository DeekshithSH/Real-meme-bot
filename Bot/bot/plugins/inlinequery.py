from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery
from Bot.bot import TGBot
from Bot.utils.Translation import Names
from Bot.utils.database import Database
db = Database()

@TGBot.on_inline_query()
async def answer(client, inline_query: InlineQuery):
    print(inline_query.query)
    query=inline_query.query.split(" ", 1)
    device=await db.get_db_names()
    results=[]
    if (not query[0] in device):
        filtered_list = list(filter(lambda x: x.startswith(query[0]), device))
        for x in filtered_list:
            results.append(InlineQueryResultArticle(
                x,
                InputTextMessageContent(Names.Device.get(x,x)),
                None,
                None,
                Names.Device.get(x,x),
                InlineKeyboardMarkup([[InlineKeyboardButton(str(Names.Device.get(x, x)), f"div|{str(x)}")]])
                ))
        if not results:
            results.append(InlineQueryResultArticle(
                "Device Not Found",
                InputTextMessageContent("Select a Device"),
                None,
                None,
                "Device Not Found",
                InlineKeyboardMarkup([[InlineKeyboardButton("Device List", f"divl|1")]])
            ))
        return await inline_query.answer(results, cache_time=1)
    

    filtered_list = list(filter(lambda x: x.startswith(query[0]), device))

    results.append(InlineQueryResultArticle(
        "Something Else",
        InputTextMessageContent("Select a Device"),
        None,
        None,
        "Something Else",
        InlineKeyboardMarkup([[InlineKeyboardButton("Device", f"divl|1")]])
    ))
    return await inline_query.answer(results, cache_time=1)
    

    return await inline_query.answer(results, cache_time=1)
    await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                title="Installation",
                input_message_content=InputTextMessageContent(
                    "Here's how to install **Pyrogram**"
                ),
                url="https://docs.pyrogram.org/intro/install",
                description="How to install Pyrogram",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(
                            "Open website",
                            url="https://docs.pyrogram.org/intro/install"
                        )]
                    ]
                )
            ),
            InlineQueryResultArticle(
                title="Usage",
                input_message_content=InputTextMessageContent(
                    "Here's how to use **Pyrogram**"
                ),
                url="https://docs.pyrogram.org/start/invoking",
                description="How to use Pyrogram",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(
                            "Open website",
                            url="https://docs.pyrogram.org/start/invoking"
                        )]
                    ]
                )
            )
        ],
        cache_time=1
    )