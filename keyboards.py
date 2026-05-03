from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню (по команде /start)
main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Личный кабинет", callback_data="cabinet")],
        [InlineKeyboardButton(text="🔌 Подключиться", callback_data="connect")],
        [InlineKeyboardButton(text="Наш канал", url="https://t.me/RumbushVPN")] 
    ]
)

# Личный кабинет
cabinet_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💳 Подписка и баланс", callback_data="sub_balance")],
        [InlineKeyboardButton(text="🔌 Подключиться", callback_data="connect")],
        [InlineKeyboardButton(text="🤝 Партнерская программа", callback_data="partner")],
        [InlineKeyboardButton(text="🎁 Промокоды", callback_data="promo")],
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")], 
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
    ]
)

# Меню "Подключиться" 
connect_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🍏iOS", callback_data="os_ios"),
            InlineKeyboardButton(text="📲Android", callback_data="os_android")
        ],
        [
            InlineKeyboardButton(text="🖥Windows 10+", callback_data="os_win10"),
            InlineKeyboardButton(text="👴Windows 7", callback_data="os_win7")
        ],
        [
            InlineKeyboardButton(text="🐧Linux", callback_data="os_linux"),
            InlineKeyboardButton(text="📱Huawei", callback_data="os_huawei")
        ],
        [
            InlineKeyboardButton(text="📺Android TV", callback_data="os_android_tv"),
            InlineKeyboardButton(text="📺Apple TV", callback_data="os_apple_tv")
        ],
        [
            InlineKeyboardButton(text="💻MacOS", callback_data="os_macos") # <-- Добавили MacOS отдельным рядом
        ],
        [InlineKeyboardButton(text="↩️ Вернуться назад", callback_data="cabinet")]
    ]
)
# --- 4. Меню "Подписка и баланс" ---
sub_balance_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💳 Приобрести подписку", callback_data="buy_sub")],
        [InlineKeyboardButton(text="💰 Пополнить баланс", callback_data="top_up_balance")],
        # Мы используем callback_data="cabinet", так как у нас уже есть функция, которая его обрабатывает!
        [InlineKeyboardButton(text="↩️ Вернуться назад", callback_data="cabinet")] 
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
# --- 6. Клавиатуры для пополнения баланса ---

# Основное меню пополнения
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
        [InlineKeyboardButton(text="✏️ Ввести сумму", callback_data="custom_amount")],
        [InlineKeyboardButton(text="↩️ Вернуться назад", callback_data="sub_balance")]
    ]
)

# Меню при вводе кастомной суммы (кнопка "назад" возвращает в основное меню пополнения)
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
        [InlineKeyboardButton(text="↩️ Вернуться назад", callback_data="top_up_balance")]
    ]
)
# --- 7. Инструкция для Android ---
android_setup_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        # В кнопках-ссылках мы используем url="..." вместо callback_data="..."
        [InlineKeyboardButton(text="Шаг 1: Скачать приложение", url="https://play.google.com/store/apps/details?id=com.happproxy")], 
        [InlineKeyboardButton(text="Шаг 2: Подключиться", url="https://t.me/твоя_ссылка_на_подключение")], 
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")],
        [InlineKeyboardButton(text="↩️ Выбор устройства", callback_data="connect")]
    ]
)
# --- 8. Инструкция для iOS ---
ios_setup_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Шаг 1: Скачать приложение", url="https://apps.apple.com/ru/app/happ-proxy-utility-plus/id6746188973")], 
        [InlineKeyboardButton(text="Шаг 2: Подключиться", url="https://t.me/твоя_ссылка_на_подключение")], 
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")],
        [InlineKeyboardButton(text="↩️ Выбор устройства", callback_data="connect")]
    ]
)
# --- 9. Инструкция для Windows 10+ ---
win10_setup_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Шаг 1: Скачать приложение", url="https://clck.ru/3TP7C5")], 
        [InlineKeyboardButton(text="Шаг 2: Подключиться", url="https://t.me/твоя_ссылка_на_подключение")], 
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")],
        [InlineKeyboardButton(text="↩️ Выбор устройства", callback_data="connect")]
    ]
)
# --- 10. Инструкция для MacOS ---
macos_setup_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Шаг 1: Скачать приложение", url="https://apps.apple.com/ru/app/happ-proxy-utility-plus/id6746188973")], 
        [InlineKeyboardButton(text="Шаг 2: Подключиться", url="https://t.me/твоя_ссылка_на_подключение")], 
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")],
        [InlineKeyboardButton(text="↩️ Выбор устройства", callback_data="connect")]
    ]
)
# --- 11. Инструкция для Windows 7 ---
win7_setup_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Шаг 1: Скачать приложение", url="https://clck.ru/3TPmJV")], 
        [InlineKeyboardButton(text="Шаг 2: Подключиться", url="https://t.me/твоя_ссылка_на_подключение")], 
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")],
        [InlineKeyboardButton(text="↩️ Выбор устройства", callback_data="connect")]
    ]
)
# --- 12. Инструкция для Linux ---
linux_setup_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Шаг 1: Скачать приложение", url="https://clck.ru/3TPmVj")], 
        [InlineKeyboardButton(text="Шаг 2: Подключиться", url="https://t.me/твоя_ссылка_на_подключение")], 
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")],
        [InlineKeyboardButton(text="↩️ Выбор устройства", callback_data="connect")]
    ]
)
# --- 13. Инструкция для Huawei ---
huawei_setup_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Шаг 1: Скачать приложение", url="https://clck.ru/3TPmod")], 
        [InlineKeyboardButton(text="Шаг 2: Подключиться", url="https://t.me/твоя_ссылка_на_подключение")], 
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")],
        [InlineKeyboardButton(text="↩️ Выбор устройства", callback_data="connect")]
    ]
)
# --- 14. Инструкция для Android TV ---
android_tv_setup_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Скачать приложение", url="https://clck.ru/3TPmod")], 
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")],
        [InlineKeyboardButton(text="↩️ Выбор устройства", callback_data="connect")]
    ]
)
# --- 15. Инструкция для Apple TV ---
apple_tv_setup_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Скачать приложение", url="https://apps.apple.com/us/app/happ-proxy-utility-for-tv/id_твоего_приложения")], 
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")],
        [InlineKeyboardButton(text="↩️ Выбор устройства", callback_data="connect")]
    ]
)