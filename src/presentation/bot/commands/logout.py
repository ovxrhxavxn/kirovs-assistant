from aiogram import types
from aiogram import Router
from aiogram.filters.command import Command

from ..enums import Caption
from ....business_logic.dependencies import get_auth_user_service


router = Router()

@router.message(Command("logout"))
async def logout(message: types.Message):
    auth_user_service = get_auth_user_service()
    username = message.from_user.username
    await auth_user_service.delete_by_nickname(username)
    sent_msg = await  message.answer(Caption.SUCCESS_LOGOUT, reply_markup=types.ReplyKeyboardRemove())
    await sent_msg.pin()