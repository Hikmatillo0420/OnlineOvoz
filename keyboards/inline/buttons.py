from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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
