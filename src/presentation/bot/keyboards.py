from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from .enums import (
    MainKeyboardButton, 
    EnterCloudKeyboardButton, 
    ResourcePath, 
    WriteAdminButton
)


def get_main_keyboard():
    kb = ReplyKeyboardBuilder()
    for button in MainKeyboardButton:
        kb.button(text=button)
    kb.adjust(len(MainKeyboardButton))
    return kb.as_markup()


def get_inline_cloud_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text=EnterCloudKeyboardButton.NEXTCLOUD, url=ResourcePath.CLOUD)
    kb.adjust(1)
    return kb.as_markup()


def get_inline_support_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text=WriteAdminButton.WRITE_ADMIN, url=ResourcePath.ADMIN_TG)
    kb.adjust(1)
    return kb.as_markup()