from aiogram import Bot, Dispatcher, types
from src.config import settings
import asyncio
from src.logger import get_logger






log = get_logger()
async def main():
    
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    
    log.info("Bot is polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())

    except (KeyboardInterrupt, SystemExit):
        log.info("Bot stopped!")