from aiogram import types, BaseMiddleware

from ...business_logic.services import AuthenticatedUserService
from ...data_access.shemas import AuthenticatedUserFromDB


class AuthMiddleware(BaseMiddleware):

    # Use the standard Python constructor __init__
    def __init__(self, auth_user_service: AuthenticatedUserService):
        self._auth_user_service = auth_user_service

    # Use the required __call__ method for middleware
    async def __call__(self, handler, event: types.Message, data: dict):
        # --- 1. Get User and Add to Data ---
        # Do this once at the very beginning. This prevents crashes and code duplication.
        # It also ensures EVERY handler afterwards can reliably expect 'user' to be in data.
        if not event.from_user or not event.from_user.username:
            await event.answer("Для использования бота у вас должен быть установлен username в настройках Telegram.")
            return # Stop processing

        user: AuthenticatedUserFromDB | None = await self._auth_user_service.get(event.from_user.username)
        data['user'] = user

        # --- 2. Handle Guard Clauses (Early Exits) ---

        # Case: User is already authenticated and tries to /login again.
        if user and event.text == "/login":
            await event.answer("Вы уже авторизованы.")
            return # Stop processing, don't call the handler

        # Case: User is NOT authenticated and tries to use a protected command.
        is_protected_command = event.text and event.text.startswith("/") and event.text not in ["/start", "/login"]
        if not user and is_protected_command:
            await event.answer("Доступ запрещен. Пожалуйста, используйте /login для аутентификации.")
            return # Stop processing

        # --- 3. The "Happy Path" ---
        # If none of the guard clauses above were triggered, it means the user is allowed to proceed.
        # Just call the handler and let it do its job.
        return await handler(event, data)