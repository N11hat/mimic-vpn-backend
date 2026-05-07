from aiogram import types, Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from keyboards import top_up_kb, top_up_presets_kb
from database.requests import get_balance
from utils.messages import safe_edit
from states import TopUpState
from config import MIN_TOP_UP, MAX_TOP_UP

router = Router()


# --- Открытие главного меню пополнения ---
@router.callback_query(F.data == "top_up_balance")
async def open_top_up_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(None)

    balance = await get_balance(callback.from_user.id)

    text = (
        "💵 <b>Пополнение личного счёта</b>\n\n"
        f"💳 Текущий баланс: <b>{balance}₽</b>\n\n"
        "ℹ️ Пополнение баланса — разовая операция, не подписка. "
        "Ваши платёжные данные остаются в безопасности.\n\n"
        "🎯 <b>Вы можете:</b>\n"
        f"• Выбрать готовую сумму из списка ниже\n"
        f"• Ввести любую сумму от <b>{MIN_TOP_UP}₽</b>"
        f" до <b>{MAX_TOP_UP}₽</b>\n\n"
        "👇 <i>Выберите сумму для пополнения баланса</i>"
    )

    await safe_edit(callback, text, reply_markup=top_up_kb, parse_mode="HTML")


# --- Нажатие на "Ввести сумму" ---
@router.callback_query(F.data == "custom_amount")
async def enter_custom_amount(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    balance = await get_balance(callback.from_user.id)

    text = (
        f"⭐ Текущий баланс: <b>{balance}₽</b>\n\n"
        f"💰 <b>Введите сумму для пополнения Вашего баланса</b>\n\n"
        f"ℹ️ <b>Доступный диапазон:</b>"
        f" <b>от {MIN_TOP_UP}₽ до {MAX_TOP_UP}₽</b>."
        f" <i>Просто отправьте число в чат (например: 500)</i>"
    )

    await safe_edit(callback, text,
                    reply_markup=top_up_presets_kb, parse_mode="HTML")
    await state.set_state(TopUpState.waiting_for_amount)


# --- Ловим введённый текст ---
@router.message(TopUpState.waiting_for_amount)
async def process_custom_amount(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text.strip())
    except ValueError:
        await message.answer(
            "❌ <b>Ошибка:</b> Пожалуйста, отправьте только число (например: 500).",
            parse_mode="HTML"
        )
        return

    if amount < MIN_TOP_UP or amount > MAX_TOP_UP:
        await message.answer(
            f"❌ <b>Ошибка:</b> Сумма должна быть"
            f" от {MIN_TOP_UP}₽ до {MAX_TOP_UP}₽. Попробуйте еще раз.",
            parse_mode="HTML"
        )
        return

    await state.set_state(None)
    await message.answer(
        f"✅ <b>Отлично!</b> Вы выбрали пополнение на <b>{amount}₽</b>.\n\n"
        "<i>(Дальше здесь появится ссылка на платёжную систему)</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Вернуться в кабинет",
                                  callback_data="cabinet")]
        ]),
        parse_mode="HTML"
    )


# --- Обработка готовых кнопок (100, 200, 500...) ---
@router.callback_query(F.data.startswith("pay_"))
async def process_preset_amount(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(None)

    amount = int(callback.data.split("_")[1])

    await safe_edit(
        callback,
        f"✅ <b>Отлично!</b> Вы выбрали пополнение на <b>{amount}₽</b>.\n\n"
        "<i>(Дальше здесь появится ссылка на платёжную систему)</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Вернуться в кабинет",
                                  callback_data="cabinet")]
        ]),
    )
