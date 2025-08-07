import random

from aiogram import types, Router
from aiogram.filters import Command

from ..enums import HeadsOrTails


router = Router()

@router.message(Command("flip"))
async def play_flip(msg: types.Message):
    await msg.reply(random.choice(list(HeadsOrTails)))
