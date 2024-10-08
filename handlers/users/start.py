from aiogram.filters import CommandStart
from aiogram.types import InlineQueryResultCachedVoice

from keyboards.default.buttons import voice_bot
from keyboards.inline.buttons import boshlash
from loader import dp, db
from aiogram import types


@dp.message(CommandStart())
async def start_bot(message: types.Message):
    try:
        db.add_user(fullname=message.from_user.full_name, telegram_id=message.from_user.id)
    except Exception as e:
        print(e)
    await message.answer(f"Assalomu alaykum {message.from_user.full_name}!")
    await message.answer("Agar botdan foydalanishni boshlamoqchi bo'lsangiz, quyidagi tugmani bosing", reply_markup= await boshlash())

