import asyncio

from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from filters.admin_bot import IsBotAdmin
from keyboards.default.buttons import voice_bot, majburiy_obuna, add_or_delete_voice
from keyboards.inline.buttons import yes_no_button
from loader import dp, db
from states.voice_states import voiceStates
from aiogram.filters import Command


@dp.message(Command('admin'), IsBotAdmin())
async def start_admin_bot(message: types.Message):
    await message.answer("🔝 Admin panel....", reply_markup=voice_bot())


@dp.message(F.text == "🛎 Obunachilar soni", IsBotAdmin())
async def member(message: types.Message):
    count_result = db.count_users()
    await message.answer(f"👥  Foydalanuvchilar soni: {count_result}")


@dp.message(F.text == "📤 Reklama yuborish", IsBotAdmin())
async def reklama_start(message: types.Message, state: FSMContext):
    await message.answer("Reklama yuborish uchun rasm, video yoki matn yuboring.")
    await state.set_state(voiceStates.ask_ad_content)

@dp.message(F.text == "🔊 Voice joylash / o'chrish", IsBotAdmin())
async def admin_addAnddelete_voice(message: types.Message, state: FSMContext):
    await message.answer("🔝 Voice bo'limi",reply_markup=add_or_delete_voice())




@dp.message(F.text == "📌Majburiy Obuna", IsBotAdmin())
async def force_channel(message: types.Message):
    await message.answer("🔝 Majburiy obunalar qo'shish bo'limi:", reply_markup=majburiy_obuna())



@dp.message(voiceStates.ask_ad_content)
async def send_ad_to_users(message: types.Message, state: FSMContext):
    await state.clear()
    users = db.select_all_users()
    count = 0
    for user in users:
        user_id = user[2]  # `user[2]` bo'lib, u `telegram_id` yoki `user_id`ni anglatadi.
        try:
            await message.send_copy(chat_id=user_id)
            count += 1
            await asyncio.sleep(0.05)
        except Exception as error:
            print(error)
    await message.answer(text=f"Reklama {count} ta foydalanuvchiga muvaffaqiyatli yuborildi.")


@dp.message(voiceStates.voice_delete_name)
async def film_check_code(message: types.Message, state: FSMContext):
    voice_delete_name = message.text
    if db.check_code_exists(voice_delete_name):
        await message.answer("🗑 Voice o'chirildi !")
        db.delete_voice_name(voice_delete_name)
    else:
        await message.answer("Bu nomda orqal hech qanday VOICE topilmadi !")
    await state.clear()

