import asyncio
import logging
import sys
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.utils.i18n import I18n, FSMI18nMiddleware
from bot.handlers import dp
from config import Conf as CF
from db import db

TOKEN = CF.BOT.BOT_TOKEN

i18n = I18n(path="locales", default_locale=CF.BOT.DEFAULT_LANG)

async def all_middleware():
    dp.update.middleware(FSMI18nMiddleware(i18n))

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="/star", description="Start the bot!")
    ]

async def create_all():
    await db.create_all()

async def main() -> None:
    await create_all()
    await all_middleware()
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await set_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())