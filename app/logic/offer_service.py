"""Бизнес-логика для формирования коммерческих предложений (КП)."""

from typing import List

from sqlalchemy.orm import Session

from app.database.connection import get_session
from app.database.models import Offer


class OfferService:
    """Сервис формирования и хранения коммерческих предложений."""

    def __init__(self) -> None:
        self.session: Session = get_session()

    def close(self) -> None:
        """Закрывает сессию БД."""
        self.session.close()

    def create(
        self,
        client_id: int,
        property_id: int,
        comment: str = "",
    ) -> Offer:
        """Создаёт коммерческое предложение."""
        offer = Offer(
            client_id=client_id,
            property_id=property_id,
            comment=comment,
        )
        self.session.add(offer)
        self.session.commit()
        self.session.refresh(offer)
        return offer

    def get_by_client(self, client_id: int) -> List[Offer]:
        """Возвращает все КП для клиента."""
        return (
            self.session.query(Offer)
            .filter_by(client_id=client_id)
            .order_by(Offer.created_at.desc())
            .all()
        )

    def get_all(self) -> List[Offer]:
        """Возвращает все КП."""
        return self.session.query(Offer).order_by(Offer.created_at.desc()).all()

    def delete(self, offer_id: int) -> bool:
        """Удаляет КП по id."""
        offer = self.session.query(Offer).filter_by(id=offer_id).first()
        if not offer:
            return False
        self.session.delete(offer)
        self.session.commit()
        return True
