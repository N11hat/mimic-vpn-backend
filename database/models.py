from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine('sqlite+aiosqlite:///vpn_database.db', echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String, nullable=True)

    # Подписка
    trial_used: Mapped[bool] = mapped_column(Boolean, default=False)
    subscription_end: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    vpn_key: Mapped[str] = mapped_column(String, nullable=True)

    # Баланс и финансы
    balance: Mapped[int] = mapped_column(Integer, default=0)  # в рублях

    # Реферальная система (храним tg_id пригласившего)
    referrer_id: Mapped[int] = mapped_column(BigInteger, nullable=True)

    # Промокоды
    promo_used: Mapped[bool] = mapped_column(Boolean, default=False)
    discount: Mapped[int] = mapped_column(Integer, default=0)  # процент скидки

    # Метаданные
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Promocode(Base):
    __tablename__ = 'promocodes'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String, unique=True)
    discount: Mapped[int] = mapped_column(Integer)  # процент скидки

    # Лимиты
    max_uses: Mapped[int] = mapped_column(Integer, default=0)  # 0 = без лимита
    used_count: Mapped[int] = mapped_column(Integer, default=0)

    # Срок действия (None = бессрочный)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Активность
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Метаданные
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_by: Mapped[int] = mapped_column(BigInteger, nullable=True)  # tg_id админа


class UserPromocode(Base):
    """История применения промокодов: какой юзер какой промокод применил."""
    __tablename__ = 'user_promocodes'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_tg_id: Mapped[int] = mapped_column(BigInteger)
    promocode_id: Mapped[int] = mapped_column(ForeignKey('promocodes.id'))
    used_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)





async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
