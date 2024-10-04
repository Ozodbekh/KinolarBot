from os import getenv
from dotenv import load_dotenv
load_dotenv()

class BotConf:
    BOT_TOKEN = getenv("BOT_TOKEN")
    DEFAULT_LANG = getenv("DEFAULT_LANG")


class DbConf:
    DB_NAME = getenv("DB_NAME")
    DB_USER = getenv("DB_USER")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_HOST = getenv("DB_HOST")
    DB_PORT = getenv("DB_PORT")

class WebConf:
    ADMIN_USERNAME = getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = getenv("ADMIN_PASSWORD")



class Conf:
    BOT = BotConf()
    DB = DbConf()
    WEB = WebConf()