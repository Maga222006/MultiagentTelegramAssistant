import os

from bot.keyboard_handlers import router as config_router

from aiogram import Bot, Dispatcher
from bot.handlers import router
import asyncio
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

dp.include_router(config_router)
dp.include_router(router)

async def main():
    print("Bot initialized...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())