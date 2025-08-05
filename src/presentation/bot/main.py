from aiogram import Bot, Dispatcher

from .config import bot_config
from .replies import router as replies_router
from .commands.start import router as start_router
from .commands.utils import router as utils_router
from ...business_logic.dependencies import (
    get_auth_user_service, 
    get_ldap_service, 
    get_weather_service
)
from .middlewares import AuthMiddleware


dp = Dispatcher()
bot = Bot(token=bot_config.bot_token)
routers = [start_router, replies_router, utils_router]
auth_service = get_auth_user_service()

async def start():
    dp.include_routers(*routers)
    dp.message.outer_middleware(AuthMiddleware(auth_service))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
            bot, 
            auth_user_service = auth_service,
            ldap_service = get_ldap_service(),
            weather_service = get_weather_service()
        )