from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- 6. Основное меню пополнения ---
top_up_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💵 100₽", callback_data="pay_100"),
            InlineKeyboardButton(text="💵 200₽", callback_data="pay_200"),
            InlineKeyboardButton(text="💵 300₽", callback_data="pay_300")
        ],
        [
            InlineKeyboardButton(text="💵 500₽", callback_data="pay_500"),
            InlineKeyboardButton(text="💵 650₽", callback_data="pay_650")
        ],
        [
            InlineKeyboardButton(text="💵 850₽", callback_data="pay_850"),
            InlineKeyboardButton(text="💵 1500₽", callback_data="pay_1500"),
            InlineKeyboardButton(text="💵 2500₽", callback_data="pay_2500"),
            InlineKeyboardButton(text="💵 3500₽", callback_data="pay_3500")
        ],
        [InlineKeyboardButton(text="✏ Ввести сумму", callback_data="custom_amount")],
        [InlineKeyboardButton(text="🔙 Вернуться назад", callback_data="sub_balance")]
    ]
)

# --- 7. Меню при вводе кастомной суммы ---
top_up_presets_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💵 100₽", callback_data="pay_100"),
            InlineKeyboardButton(text="💵 200₽", callback_data="pay_200"),
            InlineKeyboardButton(text="💵 300₽", callback_data="pay_300")
        ],
        [
            InlineKeyboardButton(text="💵 500₽", callback_data="pay_500"),
            InlineKeyboardButton(text="💵 650₽", callback_data="pay_650")
        ],
        [
            InlineKeyboardButton(text="💵 850₽", callback_data="pay_850"),
            InlineKeyboardButton(text="💵 1500₽", callback_data="pay_1500"),
            InlineKeyboardButton(text="💵 2500₽", callback_data="pay_2500"),
            InlineKeyboardButton(text="💵 3500₽", callback_data="pay_3500")
        ],
        [InlineKeyboardButton(text="🔙 Вернуться назад", callback_data="top_up_balance")]
    ]
)
