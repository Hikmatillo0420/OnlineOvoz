from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from filters import isPrivate
from filters.admin_bot import IsBotAdmin
from keyboards.default.buttons import voice_bot
from keyboards.inline.buttons import yes_no_button
from loader import dp, db
from states.voice_states import voiceStates

@dp.message(F.text == "🔙 Orqaga", IsBotAdmin(),isPrivate())
async def orqaga(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🔝 Asosiy Menyu", reply_markup=voice_bot())

@dp.message(F.text == "➕Voice", IsBotAdmin(),isPrivate())
async def admin_add_voice(message: types.Message, state: FSMContext):
    await message.answer("Voice'ni qisqa nomni yozing ! ")
    await state.set_state(voiceStates.voice_name)


@dp.message(F.text == "➖Voice", IsBotAdmin(),isPrivate())
async def admin_delete_voice(message: types.Message, state: FSMContext):
    await message.answer("voiceni nomni kiriting ! ")
    await state.set_state(voiceStates.voice_delete_name)


@dp.message(voiceStates.voice_name)
async def admin_voice_id(message: types.Message, state: FSMContext):
    voice_name = message.text
    await state.update_data({'voice_name': voice_name})
    await message.answer("endi voice'ni yuboring !")
    await state.set_state(voiceStates.voice_id)


@dp.message(voiceStates.voice_id)
async def admin(message: types.Message, state: FSMContext):
    voice_id = message.voice.file_id
    await state.update_data({'voice_id': voice_id})

    data = await state.get_data()
    text = (
        f"{data['voice_name']}"
    )
    await message.answer("Barcha ma'lumotlar to'g'rimi ?")
    await message.answer_voice(voice_id, caption=text, reply_markup=await yes_no_button(), parse_mode="HTML")

    await state.set_state(voiceStates.chekk)


@dp.callback_query(F.data == 'yes', voiceStates.chekk)
async def get_check_1(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    db.add_voice(data['voice_name'], data['voice_id'])

    await call.message.answer("Ma'lumotlari qabul qilindi\n")
    await call.message.delete()
    await state.clear()


@dp.callback_query(F.data == 'no', voiceStates.chekk)
async def get_check_0(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Kiritilgan ma'lumotlar o'chirib tashlandi !", reply_markup=voice_bot())
    await call.message.delete()
    await state.clear()
