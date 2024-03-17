from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()


# Зоздаём модель таблицы в декларативном стиле
class RequestInfo(Base):
    __tablename__ = 'request_info'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    telegram_id: Mapped[int] = mapped_column(nullable=False)
    date_time: Mapped[str] = mapped_column(nullable=False)
    article: Mapped[int] = mapped_column(nullable=False)

