from bot.keyboard_handlers import router as config_router
from database.config import init_config_db
from database.user import init_user_db
from aiogram import Bot, Dispatcher
from bot.handlers import router
from config import TOKEN
import asyncio

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(config_router)
dp.include_router(router)

async def main():
    await init_config_db()
    await init_user_db()
    print("Bot initialized...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())