from datetime import datetime, timedelta
from sqlalchemy import select, update

from database.engine import async_session
from database.models import User, Promocode, UserPromocode

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
    Применяет промокод. Возвращает процент скидки или None при ошибке.
    Проверки: код существует, активен, не истёк, не превышен лимит,
    юзер ещё не применял этот код.
    """
    code = code.strip().upper()

    async with async_session() as session:
        # Ищем промокод
        promo_result = await session.execute(
            select(Promocode).where(Promocode.code == code)
        )
        promo = promo_result.scalar_one_or_none()

        if not promo or not promo.is_active:
            return None

        # Проверка срока действия
        if promo.expires_at and promo.expires_at < datetime.utcnow():
            return None

        # Проверка лимита
        if promo.max_uses > 0 and promo.used_count >= promo.max_uses:
            return None

        # Проверка: этот юзер уже применял этот промокод?
        history_result = await session.execute(
            select(UserPromocode).where(
                UserPromocode.user_tg_id == tg_id,
                UserPromocode.promocode_id == promo.id,
            )
        )
        if history_result.scalar_one_or_none():
            return None

        # Получаем юзера и применяем скидку
        user_result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = user_result.scalar_one_or_none()
        if not user:
            return None

        user.promo_used = True
        user.discount = promo.discount

        # Записываем в историю и увеличиваем счётчик
        session.add(UserPromocode(user_tg_id=tg_id, promocode_id=promo.id))
        promo.used_count += 1

        await session.commit()
        return promo.discount

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




async def create_promocode(
    code: str,
    discount: int,
    max_uses: int = 0,
    expires_at: datetime | None = None,
    created_by: int | None = None,
) -> Promocode | None:
    """
    Создаёт новый промокод. Возвращает объект Promocode или None,
    если код с таким именем уже существует.
    """
    code = code.strip().upper()

    async with async_session() as session:
        # Проверка уникальности
        existing = await session.execute(select(Promocode).where(Promocode.code == code))
        if existing.scalar_one_or_none():
            return None

        promo = Promocode(
            code=code,
            discount=discount,
            max_uses=max_uses,
            expires_at=expires_at,
            created_by=created_by,
        )
        session.add(promo)
        await session.commit()
        await session.refresh(promo)
        return promo


async def get_all_promocodes(only_active: bool = True) -> list[Promocode]:
    """Возвращает список всех промокодов."""
    async with async_session() as session:
        query = select(Promocode).order_by(Promocode.created_at.desc())
        if only_active:
            query = query.where(Promocode.is_active == True)
        result = await session.execute(query)
        return list(result.scalars().all())


async def deactivate_promocode(code: str) -> bool:
    """Деактивирует промокод. Возвращает True, если успех, False — если код не найден."""
    code = code.strip().upper()

    async with async_session() as session:
        result = await session.execute(select(Promocode).where(Promocode.code == code))
        promo = result.scalar_one_or_none()

        if not promo:
            return False

        promo.is_active = False
        await session.commit()
        return True


async def get_stats() -> dict:
    """Собирает статистику для команды /stats."""
    from sqlalchemy import func
    from datetime import timezone

    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = now - timedelta(days=7)

    async with async_session() as session:
        # Всего пользователей
        total_users = await session.scalar(
            select(func.count()).select_from(User)
        )

        # Новых сегодня
        new_today = await session.scalar(
            select(func.count()).select_from(User)
            .where(User.created_at >= today_start)
        )

        # Новых за 7 дней
        new_week = await session.scalar(
            select(func.count()).select_from(User)
            .where(User.created_at >= week_start)
        )

        # Сумма всех балансов
        total_balance = await session.scalar(
            select(func.sum(User.balance))
        ) or 0

        # Активных промокодов
        active_promos = await session.scalar(
            select(func.count()).select_from(Promocode)
            .where(Promocode.is_active == True)
        )

        # Всего активаций промокодов
        total_promo_uses = await session.scalar(
            select(func.sum(Promocode.used_count))
        ) or 0

    return {
        "total_users": total_users,
        "new_today": new_today,
        "new_week": new_week,
        "total_balance": total_balance,
        "active_promos": active_promos,
        "total_promo_uses": total_promo_uses,
    }
