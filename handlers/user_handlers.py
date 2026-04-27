from aiogram import types, Router, F
from aiogram.filters import Command
from keyboards import main_menu_kb, cabinet_kb, connect_kb

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("👋 Добро пожаловать в <b>Rumbush VPN</b>!", reply_markup=main_menu_kb, parse_mode="HTML")

# Обработка нажатия на "Личный кабинет"
@router.callback_query(F.data == "cabinet")
async def open_cabinet(callback: types.CallbackQuery):
    await callback.message.edit_text("👤 <b>Личный кабинет</b>\n\nТут будет твой баланс и статус.", reply_markup=cabinet_kb, parse_mode="HTML")

# Обработка нажатия на "Подключиться"
@router.callback_query(F.data == "connect")
async def open_connect(callback: types.CallbackQuery):
    await callback.message.edit_text("🚀 <b>Выберите ваше устройство:</b>", reply_markup=connect_kb, parse_mode="HTML")

# Кнопка "Назад"
@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text("Главное меню:", reply_markup=main_menu_kb)