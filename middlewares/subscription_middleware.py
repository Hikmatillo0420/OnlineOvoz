import time
from typing import Any, Awaitable, Callable, cast, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from handlers.users.start import is_user_subscribed
from keyboards.inline.buttons import subscription_button


class UserCheckMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # print("Middleware ishladi")
        event = cast(Update, event)
        user_id = None

        if event.message:
            # print("Eventda message bor")
            user = event.message.from_user
            user_id = user.id
            message = event.message
        elif event.callback_query:
            # print("Eventda callback_query bor")
            user = event.callback_query.from_user
            user_id = user.id
            message = event.callback_query.message
        else:
            # print("Eventda message ham, callback_query ham yo'q")
            return await handler(event, data)

        if not await is_user_subscribed(user_id):
            # print(f"Foydalanuvchi {user_id} obuna emas")
            await message.answer(
                "⚠️ Botdan foydalanish uchun, quyidagi kanallarga obuna bo'ling:",
                reply_markup=await subscription_button()
            )
            return

        return await handler(event, data)
