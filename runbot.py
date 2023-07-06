import asyncio
import sys
import logging
import logging.handlers as handlers
from pyrogram import idle
from Bot.bot import TGBot
from Bot.utils.update import update_file, fix_name

logging.basicConfig(
    level=logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(stream=sys.stdout),
              handlers.RotatingFileHandler("streambot.log", mode="a", maxBytes=104857600, backupCount=2, encoding="utf-8")],)

logging.getLogger("pyrogram").setLevel(logging.ERROR)

loop = asyncio.get_event_loop()

async def main():
    logging.info("Starting Bot")
    await TGBot.start()
    # await update_file()
    # await fix_name()
    await idle()
if __name__ == "__main__":
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    except Exception as err:
        logging.error(err.with_traceback(None))
    finally:
        loop.stop()
        logging.info("Stoped Bot")