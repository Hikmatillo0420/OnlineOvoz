from aiogram import types
from aiogram.filters import BaseFilter


class isPrivate(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in (
            'private',
        )

