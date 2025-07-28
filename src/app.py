from aiogram import Bot, Dispatcher

from .config import bot_config
from .commands import router as keyboard_router
from .replies import router as replies_router


dp = Dispatcher()

bot = Bot(token=bot_config.token)

routers = [keyboard_router, replies_router]

dp.include_routers(*routers)