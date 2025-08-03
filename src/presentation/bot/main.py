import asyncio

from aiogram import Bot, Dispatcher

from .config import bot_config
from .replies import router as replies_router
from .commands.start import router as start_router


dp = Dispatcher()
bot = Bot(token=bot_config.bot_token)
routers = [start_router, replies_router]
dp.include_routers(*routers)

async def start():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start())