from aiogram import types, Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from keyboards import cabinet_kb
from database.requests import get_balance, count_referrals, apply_promocode
from utils.messages import safe_edit
from states import PromoState

router = Router()


@router.callback_query(F.data == "sub_balance")
async def open_sub_balance(callback: types.CallbackQuery):
    from keyboards import sub_balance_kb
    await safe_edit(
        callback,
        "💳 <b>Управление подпиской и балансом</b>\n\n"
        "Здесь вы можете пополнить внутренний счёт или выбрать подходящий тарифный план.",
        reply_markup=sub_balance_kb,
        parse_mode="HTML",
    )


@router.callback_query(F.data == "partner")
async def open_partner_program(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    bot_info = await callback.bot.get_me()
    bot_username = bot_info.username
    ref_link = f"https://t.me/{bot_username}?start=ref_{user_id}"

    partner_balance = await get_balance(user_id)
    referrals_count = await count_referrals(user_id)

    text = (
        "🤝 <b>Партнёрская программа</b>\n\n"
        "Приглашайте друзей и зарабатывайте <b>20%</b> с каждой их покупки на свой баланс!\n\n"
        f"💰 Ваш текущий баланс: <b>{partner_balance}₽</b>\n\n"
        f"👥 Приглашено друзей: <b>{referrals_count}</b>\n\n"
        "🔗 <b>Ваша персональная ссылка:</b>\n"
        f"<code>{ref_link}</code>\n\n"
        "<i>(Нажмите на ссылку, чтобы скопировать)</i>"
    )

    await safe_edit(
        callback,
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Вернуться в кабинет",
                                  callback_data="cabinet")]
        ]),
    )


# --- 1. Нажатие на кнопку "Промокоды" ---
@router.callback_query(F.data == "promo")
async def enter_promo_code(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await safe_edit(
        callback,
        "🎟 <b>Активация промокода</b>\n\n"
        "Отправьте ваш промокод ответным сообщением:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Отмена", callback_data="cabinet")]
        ]),
    )
    await state.set_state(PromoState.waiting_for_promo)


# --- 2. Ловим текст промокода ---
@router.message(PromoState.waiting_for_promo)
async def process_promo_code(message: types.Message, state: FSMContext):
    code = message.text.strip().upper()
    discount = await apply_promocode(message.from_user.id, code)

    if discount is not None:
        await message.answer(
            f"✅ <b>Промокод успешно активирован!</b>\n\n"
            f"Вы получили скидку <b>{discount}%</b> на все тарифы."
            " Перейдите к покупке подписки.",
            reply_markup=cabinet_kb,
            parse_mode="HTML",
        )
    else:
        await message.answer(
            "❌ <b>Промокод не найден, истёк или уже использован.</b>\n\n"
            "Проверьте правильность ввода или вернитесь в кабинет.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Вернуться в кабинет",
                                      callback_data="cabinet")]
            ]),
            parse_mode="HTML",
        )

    await state.set_state(None)
