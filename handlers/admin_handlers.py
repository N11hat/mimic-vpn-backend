from aiogram import Router, types
from aiogram.filters import Command
from datetime import datetime, timedelta

from filters.admin import IsAdmin
from database.requests import (
    create_promocode,
    get_all_promocodes,
    deactivate_promocode,
)


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
