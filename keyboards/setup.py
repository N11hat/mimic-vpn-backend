from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- 8. Инструкция для Android ---
android_setup_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Шаг 1: Скачать приложение", url="https://play.google.com/store/apps/details?id=com.happproxy")],
        [InlineKeyboardButton(text="Шаг 2: Подключиться", url="https://t.me/твоя_ссылка_на_подключение")],
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")],
        [InlineKeyboardButton(text="🔙 Выбор устройства", callback_data="connect")]
    ]
)

# --- 9. Инструкция для iOS ---
ios_setup_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Шаг 1: Скачать приложение", url="https://apps.apple.com/ru/app/happ-proxy-utility-plus/id6746188897")],
        [InlineKeyboardButton(text="Шаг 2: Подключиться", url="https://t.me/твоя_ссылка_на_подключение")],
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")],
        [InlineKeyboardButton(text="🔙 Выбор устройства", callback_data="connect")]
    ]
)

# --- 10. Инструкция для Windows 10+ ---
win10_setup_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Шаг 1: Скачать приложение", url="https://clck.ru/3TP7C5")],
        [InlineKeyboardButton(text="Шаг 2: Подключиться", url="https://t.me/твоя_ссылка_на_подключение")],
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")],
        [InlineKeyboardButton(text="🔙 Выбор устройства", callback_data="connect")]
    ]
)

# --- 11. Инструкция для MacOS ---
macos_setup_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Шаг 1: Скачать приложение", url="https://apps.apple.com/ru/app/happ-proxy-utility-plus/id6746188897")],
        [InlineKeyboardButton(text="Шаг 2: Подключиться", url="https://t.me/твоя_ссылка_на_подключение")],
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")],
        [InlineKeyboardButton(text="🔙 Выбор устройства", callback_data="connect")]
    ]
)

# --- 12. Инструкция для Windows 7 ---
win7_setup_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Шаг 1: Скачать приложение", url="https://clck.ru/3TPmJV")],
        [InlineKeyboardButton(text="Шаг 2: Подключиться", url="https://t.me/твоя_ссылка_на_подключение")],
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")],
        [InlineKeyboardButton(text="🔙 Выбор устройства", callback_data="connect")]
    ]
)

# --- 13. Инструкция для Linux ---
linux_setup_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Шаг 1: Скачать приложение", url="https://clck.ru/3TPmVj")],
        [InlineKeyboardButton(text="Шаг 2: Подключиться", url="https://t.me/твоя_ссылка_на_подключение")],
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")],
        [InlineKeyboardButton(text="🔙 Выбор устройства", callback_data="connect")]
    ]
)

# --- 14. Инструкция для Huawei ---
huawei_setup_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Шаг 1: Скачать приложение", url="https://clck.ru/3TPmod")],
        [InlineKeyboardButton(text="Шаг 2: Подключиться", url="https://t.me/твоя_ссылка_на_подключение")],
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")],
        [InlineKeyboardButton(text="🔙 Выбор устройства", callback_data="connect")]
    ]
)

# --- 15. Инструкция для Android TV ---
android_tv_setup_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Скачать приложение", url="https://clck.ru/3TPmod")],
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")],
        [InlineKeyboardButton(text="🔙 Выбор устройства", callback_data="connect")]
    ]
)

# --- 16. Инструкция для Apple TV ---
apple_tv_setup_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Скачать приложение", url="https://apps.apple.com/us/app/happ-proxy-utility-for-tv/id_твоего_приложения")],
        [InlineKeyboardButton(text="🆘 Поддержка", url="https://t.me/RumbushVPN")],
        [InlineKeyboardButton(text="🔙 Выбор устройства", callback_data="connect")]
    ]
)
