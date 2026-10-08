"""Подключение к базе данных и инициализация схемы."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import DATABASE_URL
from app.database.models import Base

# Движок SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False, future=True)

# Фабрика сессий
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


def init_db() -> None:
    """Создаёт все таблицы в базе данных, если они ещё не созданы."""
    Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    """Возвращает новую сессию для работы с БД.

    Returns:
        Session: объект сессии SQLAlchemy.
    """
    return SessionLocal()
