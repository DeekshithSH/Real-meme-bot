from os import environ, cpu_count
from dotenv import load_dotenv

load_dotenv()

class Names(object):
    Device={
        "RMX1911(Old)": "📱 Realme 5(Old)",
        "RMX1925(Old)": "📱 Realme 5s(Old)",
        "RMX2030(Old)": "📱 Realme 5i(Old)",
        "r5x(Old)": "📱 Realme 5/5s/5i(Old)",
        "RMX1911": "📱 Realme 5",
        "RMX1925": "📱 Realme 5s",
        "RMX2030": "📱 Realme 5i",
        "R5X": "📱 Realme 5/5s/5i", 
        "Garnet": "📱 Poco X6/RN 13 Pro"
    }

    Type={
        "ROM":"📱💾 ROM",
        "Recovery":"📱🔧 Recovery",
        "Kernel":"📱🐧 Kernel"
    }

    Other=["⬅️ Back"]

class Command_Text:
    start=environ.get("start_text", "-")
    help=environ.get("help_text", "-")
    reply={
        "post_link": "Send Channel/Group message link where the Build was Posted",
        "type": "Send Build type \n<code>ROM</code>\n<code>Kernel</code>\n<code>Recovery</code>",
        "device": "Send Device code\nOnly send new device code name if the device does not exist in below text\nelse copy paste device code name",
        "name": "Send Build Name\nRom, Kernel or Recovery Name",
        "version": "send build version",
        "status": "Status\n<code>Official</code>\n<code>Community</code>\n<code>Unofficial</code>\n<code>Port</code>",
        "release_date": "Send Release Date\nformat: dd-mm-yyyy",
        "dev": "Send Developer username\neg: @DeekshithSH",
        "download_link": "Send Text which will Apear on The Download Button",
        "android_version": "Send ROM Android Version",
        "kernel_version": "Send Kernel Version",
    }

class Types(object):
    ROM=[
        "post_link",
        "type",
        "device",
        "name",
        "version",
        "android_version",
        "status",
        "release_date",
        "dev",
        "download_link",
    ]
    Recovery=[
        "post_link",
        "type",
        "device",
        "name",
        "version",
        "status",
        "release_date",
        "dev",
        "download_link",
    ]
    Kernel=[
        "post_link",
        "type",
        "device",
        "name",
        "version",
        "kernel_version",
        "status",
        "release_date",
        "dev",
        "download_link",
    ]
