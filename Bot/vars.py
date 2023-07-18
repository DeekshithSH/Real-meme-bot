from os import environ, cpu_count
from dotenv import load_dotenv

load_dotenv()

class Var(object):
   API_ID:int = int(environ.get("API_ID"))
   API_HASH:str = str(environ.get("API_HASH"))
   SLEEP_THRESHOLD:int = int(environ.get("SLEEP_THRESHOLD", "60"))
   WORKERS:int = int(environ.get("", min(32, cpu_count() + 4)))
   DATABASE_URL:int = str(environ.get('DATABASE_URL'))
   BOT_TOKEN = str(environ.get("BOT_TOKEN"))
   AUTH_USER = list(set(int(x) for x in str(environ.get("AUTH_USER", "849816969")).split()))
   # UPDATE_STATUS=""
   STARTMSGID=int(environ.get("STARTMSGID", 1))
   ENDMSGID=environ.get("ENDMSGID", None)
   ENDMSGID=int(ENDMSGID) if ENDMSGID else int(STARTMSGID+200)

   PORT = int(environ.get("PORT", 8080))
   BIND_ADDRESS = str(environ.get("WEB_SERVER_BIND_ADDRESS", "0.0.0.0"))
   HAS_SSL = environ.get("HAS_SSL", False)
   HAS_SSL = True if str(HAS_SSL).lower() == "true" else False
   NO_PORT = environ.get("NO_PORT", False)
   NO_PORT = True if str(NO_PORT).lower() == "true" else False
   FQDN = str(environ.get("FQDN", BIND_ADDRESS))
   URL = "http{}://{}{}/".format(
            "s" if HAS_SSL else "", FQDN, "" if NO_PORT else ":" + str(PORT))
   OWNER_ID=list(set(int(x) for x in str(environ.get("OWNER_ID", "849816969")).split()))
   ADMIN_ID=list(set(int(x) for x in str(environ.get("ADMIN_ID", "849816969")).split()))
   ADMIN_ID.extend(OWNER_ID)