from aiogram.types import CallbackQuery, InlineKeyboardMarkup, LinkPreviewOptions


async def safe_edit(
    callback: CallbackQuery,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
    parse_mode: str = "HTML",
    link_preview_options: LinkPreviewOptions | None = None,
) -> None:
    """
    Безопасно «редактирует» сообщение независимо от того, является ли оно
    текстом или фото с подписью. Если сообщение — фото, удаляет его
    и отправляет новое текстовое. Если сообщение — текст, просто редактирует.
    
    link_preview_options — нужен, чтобы отключать превью ссылок в инструкциях
    (иначе под текстом всплывает большая картинка первой ссылки).
    """
    if callback.message.photo:
        # Это сообщение с фото — нельзя редактировать как текст
        await callback.message.delete()
        await callback.message.answer(
            text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            link_preview_options=link_preview_options,
        )
    else:
        # Обычное текстовое сообщение — можно редактировать
        await callback.message.edit_text(
            text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            link_preview_options=link_preview_options,
        )
