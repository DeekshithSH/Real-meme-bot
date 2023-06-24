import pprint

from pyrogram.types import Message
from Bot.bot import TGBot
from Bot.utils.database import Database
db=Database()

async def update_file():
    channel_id="rmx_1911"

    message=await TGBot.get_messages(channel_id,list(range(1,200 +1)))
    for m in message:
        if m.empty:
            print(f"{m.id}: Empty")
            continue
        text=(m.text or m.caption)
        if not text:
            print(f"{m.id}: None")
            continue
        text=text.markdown
        text+=get_button(m)
        print(f"{'-'*60}\n{m.id}\n{'-'*60}")
        print(text)
        skip=input("Skip?: ")
        if not (skip == "n"):
            print("skiped")
            continue
        data={}
        data["msg_id"] = m.id
        data["channel_id"] = m.chat.id
        data["channel_username"] = m.chat.username
        data["device"] = input("Device(1-5 / 2-5s / 3-5i / ''-5/5S/5i): ")
        data["name"] = input("File Name: ")
        data["type"] = input("File Type(1-ROM / 2-Recovery / 3-Kernel): ")
        data["version"] = input("File version: ")
        data["status"] = input("File Status (1-Official / 2-Community / 3 - Port / ''-Unofficial): ")
        data["dev"] = input("Dev username: ")
        data["release_date"] = input("Release Date: ")
        data["download_link"] = {}

        if data["status"] == "1":
            data["status"]="Official"
        elif data["status"] == "2":
            data["status"]="Community"
        elif data["status"] == "3":
            data["status"]="Port"
        elif not (data["status"]):
            data["status"]="Unofficial"

        if data["device"] == "1":
            data["device"]="RMX1911"
        elif data["device"] == "2":
            data["device"]="RMX1925"
        elif data["device"] == "3":
            data["device"]="RMX2030"
        elif not (data["device"]):
            data["device"]="r5x"

        if data["type"] == "1":
            data["type"]="ROM"
        elif data["type"] == "2":
            data["type"]="Recovery"
        elif data["type"] == "3":
            data["type"]="Kernel"

        if data["type"] == "ROM":
            data["android_version"] = input("Android Version: ")
        elif data["type"] == "Kernel":
            data["kernel_version"] = input("kernel Version: ")
            if not (data["kernel_version"]):
                data["kernel_version"]=None

        while True:
            key = input("Enter Build Type (or 'done' to finish): ")
            if key.lower() == "done":
                break
            value = input("Enter Download Link: ")
            data["download_link"][key] = value

        print("*"*60)
        data["device"]=data["device"].split(" ")
        pprint.pprint(data, indent=4)
        for x in data["device"]:
            await db.add_file(data["device"], data["type"], data)
        print("*"*60)

def get_button(m:Message):
    if m.reply_markup:
        if m.reply_markup.inline_keyboard:
            text="\n\nButton\n----------"
            for x in m.reply_markup.inline_keyboard:
                for y in x:
                    if y.url:
                        text+=f"\n{y.text}: {y.url}"
            return text
    return ""