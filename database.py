from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import DB_USER, DB_PASS, DB_HOST, DB_NAME, DB_PORT

# Формируем ссылку для подключения к БД
DSN = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@pg_db:{DB_PORT}/{DB_NAME}'

# Создаем асинхронный движок
async_engine = create_async_engine(DSN)
# Создаем асинхронную фабрику сессий
async_session = async_sessionmaker(async_engine, class_=AsyncSession)
