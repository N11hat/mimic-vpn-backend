import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from config import BOT_TOKEN
from database.models import init_db
from handlers.user import router as user_router
from handlers import admin_handlers


async def set_bot_commands(bot: Bot):
    """Устанавливает список команд, который показывается в меню бота
    (синяя кнопка 'Меню' рядом с полем ввода)."""
    commands = [
        BotCommand(command="start", description="🏠 Главное меню"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


async def main():
    await init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(user_router)
    dp.include_router(admin_handlers.router)

    # Устанавливаем кнопку "Меню" с командами
    await set_bot_commands(bot)

    print("Бот запущен и готов к работе!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
