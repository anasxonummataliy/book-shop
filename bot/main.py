import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from config import BOT_TOKEN, BOT_NAME, BOT_DESCRIPTION, BOT_SHORT_DESCRIPTION
from database.base import init_db, async_session
from handlers import start
from middlewares.base import DatabaseMiddleware


async def set_bot_info(bot: Bot):
    await bot.set_my_name(BOT_NAME)
    await bot.set_my_description(BOT_DESCRIPTION)
    await bot.set_my_short_description(BOT_SHORT_DESCRIPTION)

    commands = [
        BotCommand(command="start", description="Botni ishga tushirish"),
        BotCommand(command="help", description="Yordam"),
        BotCommand(command="profile", description="Mening profilim"),
        BotCommand(command="catalog", description="Kitoblar katalogi"),
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.update.middleware(DatabaseMiddleware(async_session))

    dp.include_router(start.router)

    await init_db()

    await set_bot_info(bot)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
