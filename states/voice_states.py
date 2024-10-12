from aiogram.filters.state import State, StatesGroup


class voiceStates(StatesGroup):
    voice_name = State()
    voice_id = State()
    chekk = State()
    voice_delete_name = State()
    ask_ad_content =State()
    chat_id = State()
    waiting_for_channel_link = State()
