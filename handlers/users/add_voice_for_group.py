from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from filters import isPrivate
from filters.admin_bot import IsBotAdmin
from keyboards.default.buttons import voice_bot
from keyboards.inline.buttons import yes_no_button
from loader import dp, db
from states.voice_states import voiceStates



