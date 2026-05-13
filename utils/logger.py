"""
Настройка логгера для всего проекта.

Использование в любом файле:
    from utils.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Что-то произошло")
    logger.exception("Ошибка")  # автоматически запишет traceback

Логи пишутся:
  - в консоль (видно при запуске бота),
  - в файл logs/bot.log (с ротацией: 5 файлов по 5 МБ).
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import BASE_DIR, settings


# Папка для логов
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "bot.log"


# Формат записи: время | уровень | имя_модуля | сообщение
_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _setup_root_logger() -> None:
    """
    Настраивает корневой логгер один раз при импорте модуля.
    После этого все вызовы logging.getLogger(name) наследуют эти настройки.
    """
    root = logging.getLogger()

    # Если уже настроено (например, при перезапуске) — не дублируем
    if root.handlers:
        return

    root.setLevel(settings.log_level.upper())

    formatter = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)

    # 1) Вывод в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)

    # 2) Запись в файл с ротацией
    #    maxBytes=5MB — когда файл перерастает 5 МБ, создаётся новый
    #    backupCount=5 — храним последние 5 файлов (bot.log, bot.log.1, ..., bot.log.5)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    # Приглушаем слишком болтливые библиотеки
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)
    logging.getLogger("aiosqlite").setLevel(logging.WARNING)


# Настраиваем при первом импорте
_setup_root_logger()


def get_logger(name: str) -> logging.Logger:
    """
    Получить логгер для конкретного модуля.
    Имя обычно передают как __name__ — так в логах видно,
    из какого файла пришло сообщение.
    """
    return logging.getLogger(name)
