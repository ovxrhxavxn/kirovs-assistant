from aiogram import types
from aiogram import Router
from aiogram.filters.command import CommandStart

from ..enums import Caption
from ..keyboards import get_inline_support_keyboard, get_main_keyboard
from ....data_access.shemas import AuthenticatedUserFromDB
from .login import router as login_router


router = Router()
router.include_router(login_router)

@router.message(CommandStart())
async def start(message: types.Message, user: AuthenticatedUserFromDB | None):
    if user:
        await message.answer(
            Caption.SUCCESS_AUTH, 
            reply_markup=(get_main_keyboard())
        )
        support_msg = await  message.answer(Caption.SUPPORT_INFO, reply_markup=get_inline_support_keyboard())
        await support_msg.pin()
    else:
        await message.answer(Caption.START_MSG)
