"""Бизнес-логика для работы с клиентами."""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.database.connection import get_session
from app.database.models import Client


class ClientService:
    """Сервис управления клиентами агентства."""

    def __init__(self) -> None:
        self.session: Session = get_session()

    def close(self) -> None:
        """Закрывает сессию БД."""
        self.session.close()

    def get_all(self) -> List[Client]:
        """Возвращает всех клиентов."""
        return self.session.query(Client).order_by(Client.full_name).all()

    def get_by_id(self, client_id: int) -> Optional[Client]:
        """Возвращает клиента по id."""
        return self.session.query(Client).filter_by(id=client_id).first()

    def create(self, full_name: str, phone: str, email: str = "", request: str = "") -> Client:
        """Создаёт нового клиента."""
        client = Client(
            full_name=full_name,
            phone=phone,
            email=email,
            request=request,
        )
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client

    def update(self, client_id: int, **fields) -> Optional[Client]:
        """Обновляет данные клиента."""
        client = self.get_by_id(client_id)
        if not client:
            return None
        for key, value in fields.items():
            if hasattr(client, key):
                setattr(client, key, value)
        self.session.commit()
        self.session.refresh(client)
        return client

    def delete(self, client_id: int) -> bool:
        """Удаляет клиента по id."""
        client = self.get_by_id(client_id)
        if not client:
            return False
        self.session.delete(client)
        self.session.commit()
        return True
