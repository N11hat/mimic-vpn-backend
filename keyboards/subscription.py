from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- 4. Меню "Подписка и баланс" ---
sub_balance_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💳 Приобрести подписку", callback_data="buy_sub")],
        [InlineKeyboardButton(text="💰 Пополнить баланс", callback_data="top_up_balance")],
        [InlineKeyboardButton(text="🔙 Вернуться назад", callback_data="cabinet")]
    ]
)

# --- 5. Выбор тарифа подписки ---
tariffs_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⚡ 7 дней", callback_data="tariff_7d")],
        [InlineKeyboardButton(text="✨ 1 месяц", callback_data="tariff_1m")],
        [InlineKeyboardButton(text="🔥 3 месяца", callback_data="tariff_3m")],
        [InlineKeyboardButton(text="🔥 6 месяцев", callback_data="tariff_6m")],
        [InlineKeyboardButton(text="🔙 Вернуться назад", callback_data="sub_balance")]
    ]
)
