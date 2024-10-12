from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import db


async def yes_no_button():
    button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Ha", callback_data="yes"),
             InlineKeyboardButton(text="Yo'q", callback_data="no")]]

    )
    return button


async def boshlash():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Boshlash",
                    switch_inline_query=" "  # Bu tanlash oynasini ochadi
                )
            ]
        ]
    )
    return keyboard

async def delete_channel_button():
    kanallar = db.get_all_channels()
    inline_keyboard = []

    for kanal in kanallar:
        tugma = InlineKeyboardButton(
            text=f"{kanal[2]}",  # 'url' maydoni
            callback_data=f"delete_channel_{kanal[1]}"  # 'chat_id' maydoni
        )
        inline_keyboard.append([tugma])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

async def subscription_button():
    channels = db.get_all_channels()
    buttons = []
    for channel in channels:
        url = channel['url']
        buttons.append([InlineKeyboardButton(text="Obuna bo'lish", url=url)])
    buttons.append([InlineKeyboardButton(text="✅ Obuna bo'ldim", callback_data="subscribe_true")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
