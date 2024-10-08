from aiogram.types import InlineQuery, InlineQueryResultCachedVoice

from loader import dp, db


@dp.inline_query()
async def inline_search(query: InlineQuery):
    search_text = query.query.strip()  # Foydalanuvchi yozgan qidiruv matni
    if not search_text:
        # Hech narsa kiritilmagan bo'lsa, barcha ovozlarni qidiradi
        voices = db.search_voices()
    else:
        # Kiritilgan qidiruv matniga mos ovozlarni qidiradi
        voices = db.search_voices(search_text)

    results = []
    for voice in voices:
        results.append(
            InlineQueryResultCachedVoice(
                id=str(voice[0]),  # Noyob ID (database `id`)
                voice_file_id=voice[2],  # Telegramda saqlangan 'file_id' (voice_id ustuni)
                title=voice[1],  # Ovoz nomi (voice_name ustuni)
            )
        )

    # Inline queryga javob qaytarish
    await query.answer(results=results, cache_time=1)
