import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMINS = [1424082929, 818638190]  # tg_id админов



# === ТАРИФЫ (цены в рублях) ===
TARIFFS = {
    "7d":  99,    # 7 дней
    "1m":  250,   # 1 месяц
    "3m":  750,   # 3 месяца
    "6m":  1250,  # 6 месяцев
}


# === VPN ===
# Временный ключ для всех юзеров (пока нет Marzban)
DEFAULT_VPN_KEY = "https://sub.g-link.cc/subkey/p2DzuS-QE99aLH9HWyHSeoTj4"


# === Ссылки на скачивание HAPP ===
HAPP_LINKS = {
    "android":     "https://clck.ru/3TP3Xe",
    "ios":         "https://apps.apple.com/",
    "win10":       "https://clck.ru/3TP7C5",
    "win7":        "https://clck.ru/3TPmJV",
    "macos":       "https://clck.ru/3TP7i2",
    "linux":       "https://clck.ru/3TPmVj",
    "huawei":      "https://clck.ru/3TPmod",
    "android_tv":  "https://clck.ru/3TPmod",  # та же что Huawei
    "apple_tv":    "https://apps.apple.com/",
}


# === Лимиты пополнения баланса ===
BALANCE_MIN = 50
BALANCE_MAX = 15000
