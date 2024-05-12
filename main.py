# - *- coding: utf- 8 - *-
import asyncio
import os
import sys

import colorama
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from tgbot.data.config import BOT_TOKEN, BOT_SCHEDULER, get_admins
from tgbot.database.db_helper import create_dbx
from tgbot.middlewares import register_all_middlwares
from tgbot.routers import register_all_routers
from tgbot.services.api_session import AsyncRequestSession
from tgbot.utils.misc.bot_commands import set_commands
from tgbot.utils.misc.bot_logging import bot_logger
from tgbot.utils.misc_functions import autobackup_admin, startup_notify

colorama.init()


# Запуск шедулеров
async def scheduler_start(bot):
    BOT_SCHEDULER.add_job(autobackup_admin, trigger="cron", hour=00, args=(bot,))  # Ежедневный Автобэкап в 00:00


# Запуск бота и базовых функций
async def main():
    BOT_SCHEDULER.start()  # Запуск Шедулера
    dp = Dispatcher()  # Образ Диспетчера
    arSession = AsyncRequestSession()  # Пул асинхронной сессии запросов
    bot = Bot(  # Образ Бота
        token=BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode="HTML",
        ),
    )

    register_all_middlwares(dp)  # Регистрация всех мидлварей
    register_all_routers(dp)  # Регистрация всех роутеров

    try:
        await set_commands(bot)  # Установка пользовательских команд в боте
        await startup_notify(bot)  # Уведомление админов о запуске бота
        await scheduler_start(bot)  # Подключение шедулеров

        bot_logger.warning("BOT WAS STARTED")
        print(colorama.Fore.LIGHTYELLOW_EX + f"~~~~~ Bot was started - @{(await bot.get_me()).username} ~~~~~")
        print(colorama.Fore.LIGHTBLUE_EX + "~~~~~ TG developer - @djimbox ~~~~~")
        print(colorama.Fore.RESET)

        if len(get_admins()) == 0: print("***** ENTER ADMIN ID IN settings.ini *****")

        await bot.delete_webhook()  # Удаление вебхуков, если они имеются
        await bot.get_updates(offset=-1)  # Сброс пендинг апдейтов

        # Запуск бота (поллинга)
        await dp.start_polling(
            bot,
            arSession=arSession,
            allowed_updates=dp.resolve_used_update_types(),
        )
    finally:
        await arSession.close()  # Закрытие Асинхронной Сессии для прочих запросов
        await bot.session.close()  # Закрытие сессии бота


if __name__ == "__main__":
    create_dbx()  # Генерация Базы Данных и Таблиц

    try:
        if sys.platform == 'win32':  # Запуск на 32-х битных системах
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main())
        else:
            asyncio.run(main())  # Запуск на всех других системах
    except (KeyboardInterrupt, SystemExit):
        bot_logger.warning("Bot was stopped")
    finally:
        if sys.platform.startswith("win"):
            os.system("cls")
        else:
            os.system("clear")
