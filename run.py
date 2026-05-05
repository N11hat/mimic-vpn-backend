import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN    
from handlers import user_handlers
from database.models import init_db
from handlers import user_handlers
from handlers import admin_handlers


async def main():
    await init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(user_handlers.router)
    dp.include_router(admin_handlers.router)

    print("Бот запущен и готов к работе!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
