"""
Конфигурация бота. Все настройки — здесь.
Читаются из .env через pydantic-settings: типы валидируются,
обязательные поля проверяются при старте.
"""
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Корень проекта (папка, где лежит этот файл)
BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """Настройки бота. Загружаются из .env при старте."""

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # игнорировать лишние переменные в .env
    )

    # === Telegram-бот ===
    bot_token: str = Field(..., description="Токен бота из BotFather")
    admins: list[int] = Field(
        default=[1424082929, 818638190],
        description="Telegram ID админов",
    )

    # === База данных ===
    db_path: Path = Field(
        default=BASE_DIR / "data" / "vpn.db",
        description="Путь к файлу SQLite",
    )

    # === Тарифы (цены в рублях) ===
    tariff_7d: int = 99
    tariff_1m: int = 250
    tariff_3m: int = 750
    tariff_6m: int = 1250

    # === Лимиты пополнения баланса (рубли) ===
    min_top_up: int = 50
    max_top_up: int = 15000

    # === Партнёрская программа ===
    referral_percent: int = 20

    # === Ссылки и контакты ===
    support_url: str = "https://t.me/RumbushVPN"

    # === VPN (временные значения, потом возьмём из Marzban API) ===
    demo_vpn_key: str = (
        "https://sub.g-link.cc/subkey/p2DzuS-QE99aLH9HWyHSeoTj4"
    )

    # === Логирование ===
    log_level: str = "INFO"  # DEBUG / INFO / WARNING / ERROR

    @property
    def db_url(self) -> str:
        """URL для SQLAlchemy. Формируется из db_path."""
        return f"sqlite+aiosqlite:///{self.db_path}"

    @property
    def tariffs(self) -> dict[str, int]:
        """Удобный доступ к тарифам как к dict (для совместимости со старым кодом)."""
        return {
            "7d": self.tariff_7d,
            "1m": self.tariff_1m,
            "3m": self.tariff_3m,
            "6m": self.tariff_6m,
        }


# Единственный экземпляр настроек, импортируется по всему проекту
settings = Settings()


# === Обратная совместимость со старым кодом ===
# Чтобы не переписывать сразу все 10 файлов, оставляем старые имена-алиасы.
# Постепенно уберём их в следующих шагах.
BOT_TOKEN = settings.bot_token
ADMINS = settings.admins
TARIFFS = settings.tariffs
MIN_TOP_UP = settings.min_top_up
MAX_TOP_UP = settings.max_top_up
REFERRAL_PERCENT = settings.referral_percent
SUPPORT_URL = settings.support_url
DEMO_VPN_KEY = settings.demo_vpn_key
