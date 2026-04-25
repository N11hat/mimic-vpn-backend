import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import config
from handlers import user_handlers
from database.models import init_db

async def main():
    await init_db()
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.include_router(user_handlers.router)
    
    print("Бот запущен и готов к работе!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())