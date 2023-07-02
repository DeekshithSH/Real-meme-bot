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