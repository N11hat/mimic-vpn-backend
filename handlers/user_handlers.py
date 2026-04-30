from aiogram import types, Router, F
from aiogram.filters import Command
from keyboards import main_menu_kb, cabinet_kb, connect_kb, sub_balance_kb, tariffs_kb

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("👋 Добро пожаловать в <b>Rumbush VPN</b>!", reply_markup=main_menu_kb, parse_mode="HTML")

# Обработка нажатия на "Личный кабинет"
@router.callback_query(F.data == "cabinet")
async def open_cabinet(callback: types.CallbackQuery):
    await callback.message.edit_text(" <b>Личный кабинет</b>\n\nТут будет твой баланс и статус.", reply_markup=cabinet_kb, parse_mode="HTML")

# Обработка нажатия на "Подключиться"
@router.callback_query(F.data == "connect")
async def open_connect(callback: types.CallbackQuery):
    await callback.message.edit_text(" <b>Выберите ваше устройство:</b>", reply_markup=connect_kb, parse_mode="HTML")

# Кнопка "Назад"
@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(" Главное меню:", reply_markup=main_menu_kb)

# Обработка нажатия на "Подписка и баланс"
@router.callback_query(F.data == "sub_balance")
async def open_sub_balance(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "💳 <b>Управление подпиской и балансом</b>\n\n"
        "Здесь вы можете пополнить внутренний счет или выбрать подходящий тарифный план.",
        reply_markup=sub_balance_kb,
        parse_mode="HTML"
    )

# Обработка нажатия на "Приобрести подписку"
@router.callback_query(F.data == "buy_sub")
async def open_tariffs(callback: types.CallbackQuery):
    # Пока баланс пишем 0₽, позже мы научим бота брать эту цифру из твоей базы данных
    text = (
        "📈 <b>Выберите срок подписки на сервис</b>\n\n"
        "👛 Текущий баланс: <b>0₽</b>\n\n"
        "💥 7 дней — 99₽\n"
        "✨ 1 месяц — 250₽\n"
        "❤️‍🔥 3 месяца — 750₽\n"
        "🔥 6 месяцев — 1250₽\n\n"
        "ℹ️ <i>Оплата будет списана с вашего личного счёта в Личном Кабинете.</i>\n\n"
        "🔒 <i>Выберите подходящий срок подписки и защитите свои данные уже сегодня!</i>"
    )
    
    await callback.message.edit_text(
        text=text,
        reply_markup=tariffs_kb,
        parse_mode="HTML"
    )