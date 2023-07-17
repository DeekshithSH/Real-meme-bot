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
        "R5X": "📱 Realme 5/5s/5i"
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
        "type": "Send Build type <br><code>ROM</code><br><code>Kernel</code><br><code>Recovery</code>",
        "device": "Send Device code<br>Only send new device code name if the device does not exist in below text<br> else copy paste device code name",
        "name": "Send Build Name<br>Only send new Build name if the build name does not exist in below text<br> else copy paste build name name",
        "version": "send build version",
        "status": "Status<br><code>Official</code><br><code>Community</code><br><code>Unofficial</code>",
        "release_date": "Send Release Date",
        "dev": "Send Developer user name",
        "download_link": "Now Send Download Link Button Text<br>First Send Text Apear on The Download Button",
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
        "android_version"
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