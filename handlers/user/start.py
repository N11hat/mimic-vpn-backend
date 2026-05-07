from aiogram import types, Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import FSInputFile

from keyboards import main_menu_kb, cabinet_kb, connect_kb
from database.requests import get_or_create_user
from utils.messages import safe_edit

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message, command: CommandObject):
    # Парсим реферера из ссылки ?start=ref_12345
    referrer_id = None
    args = command.args
    if args and args.startswith("ref_"):
        try:
            referrer_id = int(args.split("_")[1])
        except (ValueError, IndexError):
            pass

    # Регистрируем (или находим) юзера в БД
    user, is_new = await get_or_create_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
        referrer_id=referrer_id,
    )

    # Приветствие
    text = (
        "👋 Добро пожаловать в <b>Rumbush VPN</b>!\n\n"
        "Безопасный и быстрый интернет без границ."
    )

    # Бонус приветствия по реферальной ссылке (только новым юзерам)
    if is_new and user.referrer_id:
        text += "\n\n🎁 <i>Вы приглашены пользователем нашей сети!</i>"

    await message.answer(text, reply_markup=main_menu_kb, parse_mode="HTML")


@router.callback_query(F.data == "cabinet")
async def open_cabinet(callback: types.CallbackQuery):
    photo = FSInputFile("images/cabinet_banner.jpg")

    text = (
        "<b>Личный кабинет</b>\n\n"
        "Тут будет твой баланс и статус."
    )

    await callback.message.delete()
    await callback.message.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=cabinet_kb,
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "connect")
async def open_connect(callback: types.CallbackQuery):
    await safe_edit(callback, " <b>Выберите ваше устройство:</b>",
                    reply_markup=connect_kb, parse_mode="HTML")


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await safe_edit(callback, " Главное меню:", reply_markup=main_menu_kb)
