from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- 1. Главное меню (по команде /start) ---
main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🗂 Личный кабинет", callback_data="cabinet")],
        [InlineKeyboardButton(text="🔌 Подключиться", callback_data="connect")],
        [InlineKeyboardButton(text="Наш канал", url="https://t.me/RumbushVPN")]
    ]
)

# --- 2. Личный кабинет ---
cabinet_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💳 Подписка и баланс", callback_data="sub_balance")],
        [InlineKeyboardButton(text="🔌 Подключиться", callback_data="connect")],
        [InlineKeyboardButton(text="🤝 Партнёрская программа", callback_data="partner")],
        [InlineKeyboardButton(text="🎟 Промокоды", callback_data="promo")],
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
    ]
)

# --- 3. Меню "Подключиться" (выбор устройства) ---
connect_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🍏iOS", callback_data="os_ios"),
            InlineKeyboardButton(text="🤖Android", callback_data="os_android")
        ],
        [
            InlineKeyboardButton(text="🖥Windows 10+", callback_data="os_win10"),
            InlineKeyboardButton(text="🪟Windows 7", callback_data="os_win7")
        ],
        [
            InlineKeyboardButton(text="🐧 Linux", callback_data="os_linux"),
            InlineKeyboardButton(text="📱 Huawei", callback_data="os_huawei")
        ],
        [
            InlineKeyboardButton(text="📺Android TV", callback_data="os_android_tv"),
            InlineKeyboardButton(text="🍎Apple TV", callback_data="os_apple_tv")
        ],
        [
            InlineKeyboardButton(text="🖥MacOS", callback_data="os_macos")
        ],
        [InlineKeyboardButton(text="🔙 Вернуться назад", callback_data="cabinet")]
    ]
)
