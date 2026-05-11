from aiogram import Router, types
import asyncio
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from states.user import BroadcastState
from datetime import datetime, timedelta

from filters.admin import IsAdmin
from database.engine import async_session
from database.models import User
from database.requests import (
    create_promocode,
    get_all_promocodes,
    deactivate_promocode,
    get_stats,
    get_user,
    update_balance,
    get_all_user_ids,
)
from sqlalchemy import select

router = Router()
# Все хендлеры этого роутера работают только для админов
router.message.filter(IsAdmin())


@router.message(Command("add_promo"))
async def cmd_add_promo(message: types.Message):
    """
    Создать промокод.
    Использование: /add_promo КОД СКИДКА [ЛИМИТ] [ДНЕЙ]
    Пример: /add_promo SUMMER 15 100 30
    (промокод SUMMER, скидка 15%, лимит 100 использований, действителен 30 дней)
    """
    args = message.text.split()[1:]  # убираем саму команду

    if len(args) < 2:
        await message.answer(
            "❌ <b>Неверный формат</b>\n\n"
            "Используйте: <code>/add_promo КОД СКИДКА [ЛИМИТ] [ДНЕЙ]</code>\n\n"
            "Примеры:\n"
            "• <code>/add_promo NEW 10</code> — без лимитов\n"
            "• <code>/add_promo SUMMER 15 100</code> — лимит 100 активаций\n"
            "• <code>/add_promo BLACKFRIDAY 50 50 7</code> — 50 активаций, 7 дней",
            parse_mode="HTML",
        )
        return

    code = args[0]

    try:
        discount = int(args[1])
        max_uses = int(args[2]) if len(args) > 2 else 0
        days = int(args[3]) if len(args) > 3 else 0
    except ValueError:
        await message.answer("❌ Скидка, лимит и дни должны быть числами.")
        return

    if not (1 <= discount <= 100):
        await message.answer("❌ Скидка должна быть от 1 до 100%.")
        return

    expires_at = datetime.utcnow() + timedelta(days=days) if days > 0 else None

    promo = await create_promocode(
        code=code,
        discount=discount,
        max_uses=max_uses,
        expires_at=expires_at,
        created_by=message.from_user.id,
    )

    if promo is None:
        await message.answer(f"❌ Промокод <code>{code.upper()}</code> уже существует.", parse_mode="HTML")
        return

    text = (
        f"✅ <b>Промокод создан!</b>\n\n"
        f"Код: <code>{promo.code}</code>\n"
        f"Скидка: <b>{promo.discount}%</b>\n"
        f"Лимит активаций: <b>{promo.max_uses if promo.max_uses > 0 else '∞'}</b>\n"
        f"Срок действия: <b>{promo.expires_at.strftime('%d.%m.%Y') if promo.expires_at else 'бессрочно'}</b>"
    )
    await message.answer(text, parse_mode="HTML")


@router.message(Command("list_promo"))
async def cmd_list_promo(message: types.Message):
    """Показывает все активные промокоды."""
    promos = await get_all_promocodes(only_active=True)

    if not promos:
        await message.answer("📋 Активных промокодов нет.")
        return

    lines = ["📋 <b>Активные промокоды:</b>\n"]
    for p in promos:
        usage = f"{p.used_count}/{p.max_uses}" if p.max_uses > 0 else f"{p.used_count}/∞"
        expires = p.expires_at.strftime("%d.%m.%Y") if p.expires_at else "бессрочно"
        lines.append(
            f"• <code>{p.code}</code> — {p.discount}% | использовано {usage} | до {expires}"
        )

    await message.answer("\n".join(lines), parse_mode="HTML")


@router.message(Command("disable_promo"))
async def cmd_disable_promo(message: types.Message):
    """
    Деактивирует промокод.
    Использование: /disable_promo КОД
    """
    args = message.text.split()[1:]

    if not args:
        await message.answer("❌ Укажите код: <code>/disable_promo КОД</code>", parse_mode="HTML")
        return

    code = args[0]
    success = await deactivate_promocode(code)

    if success:
        await message.answer(f"✅ Промокод <code>{code.upper()}</code> деактивирован.", parse_mode="HTML")
    else:
        await message.answer(f"❌ Промокод <code>{code.upper()}</code> не найден.", parse_mode="HTML")



@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    """Показывает статистику бота. Только для админов."""
    stats = await get_stats()

    text = (
        "📊 <b>Статистика Rumbush VPN</b>\n\n"
        "👥 <b>Пользователи:</b>\n"
        f"• Всего: <b>{stats['total_users']}</b>\n"
        f"• Новых сегодня: <b>{stats['new_today']}</b>\n"
        f"• Новых за 7 дней: <b>{stats['new_week']}</b>\n\n"
        "💰 <b>Финансы:</b>\n"
        f"• Сумма на балансах: <b>{stats['total_balance']}₽</b>\n\n"
        "🎟 <b>Промокоды:</b>\n"
        f"• Активных: <b>{stats['active_promos']}</b>\n"
        f"• Всего активаций: <b>{stats['total_promo_uses']}</b>"
    )

    await message.answer(text, parse_mode="HTML")



# ============================================================
# /users — список последних N зарегистрированных пользователей
# ============================================================
@router.message(Command("users"))
async def cmd_users(message: types.Message):
    """
    Показывает последних N зарегистрированных юзеров.
    Использование: /users        — последние 10 (по умолчанию)
                   /users 25     — последние 25
    """
    args = message.text.split()[1:]

    # Сколько пользователей показывать
    limit = 10
    if args:
        try:
            limit = int(args[0])
        except ValueError:
            await message.answer(
                "❌ <b>Неверный формат</b>\n\n"
                "Использование: <code>/users [количество]</code>\n"
                "Пример: <code>/users 25</code>",
                parse_mode="HTML",
            )
            return

    # Защита: разумный диапазон. Telegram не даёт отправить >4096 символов,
    # а каждый юзер — это ~4 строки, поэтому 50 — безопасный потолок.
    if not (1 <= limit <= 50):
        await message.answer(
            "❌ <b>Лимит:</b> от 1 до 50.",
            parse_mode="HTML",
        )
        return

    # Берём последних N юзеров: сортируем по created_at по убыванию
    async with async_session() as session:
        result = await session.execute(
            select(User).order_by(User.created_at.desc()).limit(limit)
        )
        users = list(result.scalars().all())

    if not users:
        await message.answer("📭 В базе пока нет пользователей.")
        return

    lines = [f"👥 <b>Последние {len(users)} пользователей:</b>\n"]
    for u in users:
        username = f"@{u.username}" if u.username else "<i>без username</i>"
        created = u.created_at.strftime("%d.%m.%Y %H:%M")
        lines.append(
            f"• <code>{u.tg_id}</code> — {username}\n"
            f"  📅 {created} | 💰 {u.balance}₽"
        )

    await message.answer("\n".join(lines), parse_mode="HTML")


# ============================================================
# /give — выдать (или списать) деньги на баланс пользователя
# ============================================================
@router.message(Command("give"))
async def cmd_give(message: types.Message):
    """
    Начислить (или списать) рубли на баланс юзера.
    Использование: /give <tg_id> <сумма>
    Примеры:
        /give 1424082929 500      — начислить 500₽
        /give 1424082929 -200     — списать 200₽
    """
    args = message.text.split()[1:]

    if len(args) < 2:
        await message.answer(
            "❌ <b>Неверный формат</b>\n\n"
            "Использование: <code>/give &lt;tg_id&gt; &lt;сумма&gt;</code>\n\n"
            "<b>Примеры:</b>\n"
            "• <code>/give 1424082929 500</code> — начислить 500₽\n"
            "• <code>/give 1424082929 -200</code> — списать 200₽",
            parse_mode="HTML",
        )
        return

    # Парсим аргументы
    try:
        tg_id = int(args[0])
        amount = int(args[1])
    except ValueError:
        await message.answer(
            "❌ tg_id и сумма должны быть целыми числами.",
            parse_mode="HTML",
        )
        return

    if amount == 0:
        await message.answer("❌ Сумма не может быть 0.")
        return

    # Проверяем, что юзер существует
    user = await get_user(tg_id)
    if user is None:
        await message.answer(
            f"❌ Пользователь с tg_id <code>{tg_id}</code> не найден в базе.",
            parse_mode="HTML",
        )
        return

    # Защита от ухода баланса в минус
    new_balance = user.balance + amount
    if new_balance < 0:
        await message.answer(
            f"❌ Недостаточно средств для списания.\n"
            f"Текущий баланс: <b>{user.balance}₽</b>, "
            f"вы пытаетесь списать <b>{abs(amount)}₽</b>.",
            parse_mode="HTML",
        )
        return

    # Применяем изменение
    await update_balance(tg_id, amount)

    # Ответ админу
    username = f"@{user.username}" if user.username else "<i>без username</i>"
    if amount > 0:
        action_text = f"➕ Начислено <b>{amount}₽</b>"
    else:
        action_text = f"➖ Списано <b>{abs(amount)}₽</b>"

    await message.answer(
        f"✅ <b>Готово!</b>\n\n"
        f"Пользователь: {username} (<code>{tg_id}</code>)\n"
        f"{action_text}\n"
        f"Баланс: <b>{user.balance}₽</b> → <b>{new_balance}₽</b>",
        parse_mode="HTML",
    )

    # Уведомление пользователю в личку (если бот не заблокирован)
    try:
        if amount > 0:
            user_text = (
                f"🎁 <b>Вам начислено {amount}₽ на баланс!</b>\n\n"
                f"💰 Текущий баланс: <b>{new_balance}₽</b>"
            )
        else:
            user_text = (
                f"ℹ️ <b>С вашего баланса списано {abs(amount)}₽.</b>\n\n"
                f"💰 Текущий баланс: <b>{new_balance}₽</b>"
            )
        await message.bot.send_message(tg_id, user_text, parse_mode="HTML")
    except Exception as e:
        # Юзер мог заблокировать бота — это не ошибка, просто сообщаем админу
        await message.answer(
            f"⚠️ Не удалось уведомить пользователя в личку: <code>{e}</code>",
            parse_mode="HTML",
        )


# ============================================================
# /broadcast — массовая рассылка всем пользователям
# ============================================================
@router.message(Command("broadcast"))
async def cmd_broadcast(message: types.Message, state: FSMContext):
    """
    Запускает рассылку. Сценарий:
      1. /broadcast <текст>    — сразу с текстом
      2. /broadcast            — бот попросит прислать текст следующим сообщением
    После получения текста — показывает превью и кнопки подтверждения.
    """
    # Сбрасываем возможное предыдущее состояние
    await state.clear()

    # Текст можно передать сразу после команды
    text = message.text.removeprefix("/broadcast").strip()

    if text:
        # Текст уже есть — показываем превью и спрашиваем подтверждение
        await _show_broadcast_preview(message, state, text)
    else:
        # Текста нет — просим прислать его следующим сообщением
        await message.answer(
            "📢 <b>Создание рассылки</b>\n\n"
            "Отправьте текст сообщения следующим сообщением.\n"
            "Поддерживается HTML: <b>жирный</b>, <i>курсив</i>, "
            "<a href='https://example.com'>ссылки</a>.\n\n"
            "Для отмены — /cancel",
            parse_mode="HTML",
        )
        await state.set_state(BroadcastState.waiting_for_text)


@router.message(BroadcastState.waiting_for_text, Command("cancel"))
async def cmd_broadcast_cancel(message: types.Message, state: FSMContext):
    """Отмена ввода текста рассылки."""
    await state.clear()
    await message.answer("❌ Рассылка отменена.")


@router.message(BroadcastState.waiting_for_text)
async def broadcast_get_text(message: types.Message, state: FSMContext):
    """Принимает текст рассылки и показывает превью."""
    text = message.text or message.caption
    if not text:
        await message.answer("❌ Нужен текст. Пришли текстовое сообщение.")
        return
    await _show_broadcast_preview(message, state, text)


async def _show_broadcast_preview(message: types.Message, state: FSMContext, text: str):
    """Внутренняя: показывает превью и кнопки подтверждения."""
    user_ids = await get_all_user_ids()

    confirm_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Отправить", callback_data="broadcast_confirm"),
            InlineKeyboardButton(text="❌ Отмена", callback_data="broadcast_cancel"),
        ]
    ])

    await state.set_state(BroadcastState.waiting_for_confirm)
    await state.update_data(text=text)

    await message.answer(
        f"📢 <b>Превью рассылки</b>\n"
        f"Получателей: <b>{len(user_ids)}</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"{text}\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"Отправить?",
        parse_mode="HTML",
    )
    await message.answer("👇", reply_markup=confirm_kb)


@router.callback_query(BroadcastState.waiting_for_confirm, lambda c: c.data == "broadcast_cancel")
async def broadcast_cancel_callback(callback: types.CallbackQuery, state: FSMContext):
    """Кнопка «Отмена»."""
    await state.clear()
    await callback.message.edit_text("❌ Рассылка отменена.")
    await callback.answer()


@router.callback_query(BroadcastState.waiting_for_confirm, lambda c: c.data == "broadcast_confirm")
async def broadcast_confirm_callback(callback: types.CallbackQuery, state: FSMContext):
    """Кнопка «Отправить» — запускает рассылку."""
    data = await state.get_data()
    text = data.get("text", "")
    await state.clear()

    await callback.answer("Запускаю рассылку…")
    await callback.message.edit_text("⏳ <b>Рассылка запущена…</b>", parse_mode="HTML")

    user_ids = await get_all_user_ids()
    bot = callback.bot

    sent = 0          # доставлено
    blocked = 0       # юзер заблокировал бота
    failed = 0        # прочие ошибки
    total = len(user_ids)

    # Сообщение со статусом, которое будем обновлять каждые ~50 отправок
    status_msg = await callback.message.answer(
        f"📊 Отправлено: 0 / {total}", parse_mode="HTML"
    )

    for i, tg_id in enumerate(user_ids, start=1):
        try:
            await bot.send_message(tg_id, text, parse_mode="HTML")
            sent += 1
        except TelegramForbiddenError:
            # Юзер заблокировал бота — это нормально, идём дальше
            blocked += 1
        except TelegramRetryAfter as e:
            # Telegram попросил подождать — ждём и повторяем для этого юзера
            await asyncio.sleep(e.retry_after)
            try:
                await bot.send_message(tg_id, text, parse_mode="HTML")
                sent += 1
            except Exception:
                failed += 1
        except Exception:
            failed += 1

        # Пауза, чтобы не превысить лимит Telegram (~30 msg/sec).
        # 0.05 = 20 msg/sec — безопасно.
        await asyncio.sleep(0.05)

        # Обновляем прогресс каждые 50 сообщений (чтобы не спамить редактированиями)
        if i % 50 == 0:
            try:
                await status_msg.edit_text(
                    f"📊 Отправлено: {i} / {total}",
                    parse_mode="HTML",
                )
            except Exception:
                pass

    # Итоговый отчёт
    await status_msg.edit_text(
        f"✅ <b>Рассылка завершена</b>\n\n"
        f"📨 Доставлено: <b>{sent}</b>\n"
        f"🚫 Заблокировали бота: <b>{blocked}</b>\n"
        f"⚠️ Ошибок: <b>{failed}</b>\n"
        f"👥 Всего: <b>{total}</b>",
        parse_mode="HTML",
    )
