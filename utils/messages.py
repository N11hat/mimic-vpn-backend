from aiogram.types import CallbackQuery, InlineKeyboardMarkup


async def safe_edit(
    callback: CallbackQuery,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
    parse_mode: str = "HTML",
) -> None:
    """
    Безопасно «редактирует» сообщение независимо от того, является ли оно
    текстом или фото с подписью. Если сообщение — фото, удаляет его
    и отправляет новое текстовое. Если сообщение — текст, просто редактирует.
    """
    if callback.message.photo:
        # Это сообщение с фото — нельзя редактировать как текст
        await callback.message.delete()
        await callback.message.answer(
            text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
        )
    else:
        # Обычное текстовое сообщение — можно редактировать
        await callback.message.edit_text(
            text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
        )
