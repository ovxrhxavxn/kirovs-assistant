from aiogram import Router
from aiogram.filters.command import Command
from aiogram import types
from aiogram.fsm.context import FSMContext

from .logout import router as logout_router
from ..enums import Caption
from ..keyboards import get_main_keyboard, get_inline_support_keyboard
from ..fsms import AuthStates
from ....business_logic.dependencies import AuthenticatedUserService, LDAPService
from ....data_access.shemas import AuthenticatedUser


router = Router(name='Login Router')
router.include_router(logout_router)


@router.message(Command("login"))
async def command_login(message: types.Message, state: FSMContext):
    await state.set_state(AuthStates.waiting_for_username)
    await message.answer("Введите свой доменный логин:")


@router.message(AuthStates.waiting_for_username)
async def process_username(
        message: types.Message, 
        state: FSMContext, 
        auth_user_service: AuthenticatedUserService):

    user = await auth_user_service.get_by_domain_name(message.text)

    if user:
        await message.answer(Caption.UNUQUE_ERROR)
        return

    await state.update_data(username=message.text)
    await state.set_state(AuthStates.waiting_for_password)
    # Important: Tell user to delete password message for security
    await message.delete()
    await message.answer("Отлично. Теперь введите доменный пароль:")
    

@router.message(AuthStates.waiting_for_password)
async def process_password(
    message: types.Message, 
    state: FSMContext,
    ldap_service: LDAPService,
    auth_user_service: AuthenticatedUserService):

    user_data = await state.get_data()
    username = user_data.get("username")
    password = message.text
    await message.delete()
    verify_msg = await message.answer("Проверка данных...")

    # Perform the authentication check
    if await ldap_service.check_ad_credentials(username, password):
        await auth_user_service.add(AuthenticatedUser(nickname=message.from_user.username, domain_name=username))
        await message.answer(
            Caption.SUCCESS_AUTH,
            reply_markup=(get_main_keyboard())
        )
        support_msg = await  message.answer(Caption.SUPPORT_INFO, reply_markup=get_inline_support_keyboard())
        await verify_msg.delete()
        await support_msg.pin()
        await state.clear()
    else:
        await message.answer(
            "Аутентификация провалена. Попробуйте еще раз через /login",
        )
        await state.clear()