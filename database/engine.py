from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Подключение к базе данных SQLite
# echo=False — не выводить все SQL-запросы в консоль (полезно включить echo=True
# когда отлаживаешь — тогда увидишь все запросы к БД в терминале)
engine = create_async_engine(
    'sqlite+aiosqlite:///vpn_database.db',
    echo=False,
)

# Фабрика сессий. Каждый раз когда пишешь "async with async_session() as session:"
# — создаётся новое соединение с БД, которое автоматически закрывается в конце блока.
# expire_on_commit=False — объекты не "протухают" после commit(), можно читать их дальше.
async_session = async_sessionmaker(engine, expire_on_commit=False)
