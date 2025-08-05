from aiogram import types, BaseMiddleware

from ...business_logic.services import AuthenticatedUserService
from ...data_access.shemas import AuthenticatedUserFromDB
from .enums import MainKeyboardButton


class AuthMiddleware(BaseMiddleware):

    def __init__(self, auth_user_service: AuthenticatedUserService):
        self._auth_user_service = auth_user_service
        # Create a set of protected button texts for efficient lookup.
        # This is better than hardcoding strings!
        self._protected_keyboard_texts = {button.value for button in MainKeyboardButton}

    async def __call__(self, handler, event: types.Message, data: dict):
        if not event.from_user or not event.from_user.username:
            await event.answer("Для использования бота у вас должен быть установлен username в настройках Telegram.")
            return

        user: AuthenticatedUserFromDB | None = await self._auth_user_service.get(event.from_user.username)
        data['user'] = user

        # Public commands that are always allowed
        public_commands = {"/start", "/login"}

        # If the user is authenticated, we only need to prevent them from using /login again.
        if user:
            if event.text == "/login":
                await event.answer("Вы уже авторизованы.")
                return # Stop processing
            # Otherwise, let them do anything.
            return await handler(event, data)

        # --- If we reach here, the user is NOT authenticated ---

        # Let's check if they are trying to access a protected resource.
        is_command = event.text and event.text.startswith("/")
        is_protected = False

        if is_command:
            # It's a command, check if it's NOT in the public list
            if event.text not in public_commands:
                is_protected = True
        elif event.text in self._protected_keyboard_texts:
            # It's not a command, check if it's a protected keyboard button press
            is_protected = True

        # If the action is protected and the user is not authenticated, block them.
        if is_protected:
            await event.answer("Доступ запрещен. Пожалуйста, используйте /login для аутентификации.")
            return # Stop processing

        # If the action is not protected (e.g., /start, /login, or random text), let it pass.
        return await handler(event, data)