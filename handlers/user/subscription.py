from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from keyboards import tariffs_kb
from database.requests import get_discount
from utils.messages import safe_edit
from config import TARIFFS

router = Router()


@router.callback_query(F.data == "buy_sub")
async def open_tariffs(callback: types.CallbackQuery, state: FSMContext):
    discount = await get_discount(callback.from_user.id)

    # Базовые цены из config
    p_7d = TARIFFS["7d"]
    p_1m = TARIFFS["1m"]
    p_3m = TARIFFS["3m"]
    p_6m = TARIFFS["6m"]

    # Если есть скидка — пересчитываем
    if discount > 0:
        p_7d = int(p_7d * (1 - discount / 100))
        p_1m = int(p_1m * (1 - discount / 100))
        p_3m = int(p_3m * (1 - discount / 100))
        p_6m = int(p_6m * (1 - discount / 100))
        discount_text = f"\n🎁 <i>Применена скидка {discount}% по промокоду!</i>\n"
    else:
        discount_text = "\n"

    text = (
        "📋 <b>Выберите срок подписки на сервис</b>\n\n"
        "💳 <b>0₽</b>\n"
        f"{discount_text}\n"
        f"⚡ 7 дней — {p_7d}₽\n"
        f"✨ 1 месяц — {p_1m}₽\n"
        f"🔥 3 месяца — {p_3m}₽\n"
        f"🔥 6 месяцев — {p_6m}₽\n\n"
        "ℹ️ <i>Оплата будет списана с вашего личного счёта в Личном Кабинете.</i>\n\n"
        "🔒 <i>Выберите подходящий срок подписки и защитите свои данные уже сегодня!</i>"
    )

    await safe_edit(
        callback,
        text=text,
        reply_markup=tariffs_kb,
        parse_mode="HTML",
    )
