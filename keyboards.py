from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню (по команде /start)
main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🟡 Личный кабинет", callback_data="cabinet")],
        [InlineKeyboardButton(text="🟡 Подключиться", callback_data="connect")],
        [InlineKeyboardButton(text="🟡 Наш канал", url="https://t.me/RumbushVPN")] 
    ]
)

# Личный кабинет
cabinet_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🟡 Подписка и баланс", callback_data="sub_balance")],
        [InlineKeyboardButton(text="🟡 Подключиться", callback_data="connect")],
        [InlineKeyboardButton(text="🟡 Партнерская программа", callback_data="affiliate")],
        [InlineKeyboardButton(text="🟡 Промокоды", callback_data="promo")],
        [InlineKeyboardButton(text="🟡 Поддержка", url="https://t.me/RumbushVPN")], 
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
    ]
)

# Меню "Подключиться" 
connect_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="iOS", callback_data="os_ios"),
            InlineKeyboardButton(text="Android", callback_data="os_android")
        ],
        [
            InlineKeyboardButton(text="Windows 10+", callback_data="os_win10"),
            InlineKeyboardButton(text="Windows 7", callback_data="os_win7")
        ],
        [
            InlineKeyboardButton(text="Linux", callback_data="os_linux"),
            InlineKeyboardButton(text="Huawei", callback_data="os_huawei")
        ],
        [
            InlineKeyboardButton(text="Android TV", callback_data="os_android_tv"),
            InlineKeyboardButton(text="Apple TV", callback_data="os_apple_tv")
        ],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
    ]
)
# --- 4. Меню "Подписка и баланс" ---
sub_balance_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💳 Приобрести подписку", callback_data="buy_sub")],
        [InlineKeyboardButton(text="💰 Пополнить баланс", callback_data="top_up_balance")],
        # Мы используем callback_data="cabinet", так как у нас уже есть функция, которая его обрабатывает!
        [InlineKeyboardButton(text="⬅️ Вернуться в кабинет", callback_data="cabinet")] 
    ]
)
# --- 5. Выбор тарифа подписки ---
tariffs_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💥 7 дней", callback_data="tariff_7d")],
        [InlineKeyboardButton(text="✨ 1 месяц", callback_data="tariff_1m")],
        [InlineKeyboardButton(text="❤️‍🔥 3 месяца", callback_data="tariff_3m")],
        [InlineKeyboardButton(text="🔥 6 месяцев", callback_data="tariff_6m")],
        [InlineKeyboardButton(text="↩️ Вернуться назад", callback_data="sub_balance")] 
    ]
)