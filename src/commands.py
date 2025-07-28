from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram import types

from .constants import START_MSG, CONNECT_WIFI, ENTER_CLOUD


router = Router(name='Commands Router')

@router.message(CommandStart())
async def start(msg: types.Message):
    keyboard = [
        [
            types.KeyboardButton(text=CONNECT_WIFI),
            types.KeyboardButton(text=ENTER_CLOUD)
        ],
    ]

    keyboard_markup = types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        input_field_placeholder="Выберите пункт"
    )

    await msg.answer(START_MSG, reply_markup=keyboard_markup)