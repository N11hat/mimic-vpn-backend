from datetime import datetime
from sqlalchemy import select, update

from database.models import async_session, User


async def get_or_create_user(tg_id: int, username: str | None = None, referrer_id: int | None = None) -> tuple[User, bool]:
    """
    Возвращает юзера из БД или создаёт нового.
    Второе значение в кортеже — True, если юзер был только что создан.
    referrer_id применяется ТОЛЬКО при создании нового юзера.
    """
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()

        if user:
            # Если username изменился — обновим
            if username and user.username != username:
                user.username = username
                await session.commit()
            return user, False

        # Создаём нового
        # Защита: нельзя пригласить самого себя
        if referrer_id == tg_id:
            referrer_id = None

        # Защита: реферер должен реально существовать в БД
        if referrer_id is not None:
            ref_check = await session.execute(select(User).where(User.tg_id == referrer_id))
            if ref_check.scalar_one_or_none() is None:
                referrer_id = None

        new_user = User(
            tg_id=tg_id,
            username=username,
            referrer_id=referrer_id,
        )
        session.add(new_user)
        await session.commit()
        return new_user, True


async def get_user(tg_id: int) -> User | None:
    """Просто получить юзера, без создания."""
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        return result.scalar_one_or_none()


async def get_balance(tg_id: int) -> int:
    user = await get_user(tg_id)
    return user.balance if user else 0


async def update_balance(tg_id: int, amount: int) -> None:
    """Прибавляет amount к балансу (может быть отрицательным для списания)."""
    async with async_session() as session:
        await session.execute(
            update(User).where(User.tg_id == tg_id).values(balance=User.balance + amount)
        )
        await session.commit()


async def apply_promocode(tg_id: int, code: str) -> int | None:
    """
    Применяет промокод. Возвращает процент скидки или None, если код невалидный/уже использован.
    Пока что хардкод одного промокода NEW = 10%. Потом перенесём в отдельную таблицу.
    """
    PROMOCODES = {"NEW": 10}

    discount = PROMOCODES.get(code.strip().upper())
    if discount is None:
        return None

    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()
        if not user or user.promo_used:
            return None

        user.promo_used = True
        user.discount = discount
        await session.commit()
        return discount


async def get_discount(tg_id: int) -> int:
    user = await get_user(tg_id)
    return user.discount if user else 0


async def count_referrals(tg_id: int) -> int:
    """Сколько юзеров пришло по моей ссылке."""
    async with async_session() as session:
        from sqlalchemy import func
        result = await session.execute(
            select(func.count()).select_from(User).where(User.referrer_id == tg_id)
        )
        return result.scalar() or 0
