"""Сервис фильтрации объектов под запросы покупателей.

ВАЖНО: возвращает список словарей, а не ORM-объектов Property.
Это сделано, чтобы:
1) избежать ошибки DetachedInstanceError после закрытия сессии;
2) UI мог обращаться к row["id"], row["price"] и т.д.
"""

from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app.database.connection import get_session
from app.database.models import Property


class SearchService:
    """Фильтрация объектов недвижимости по параметрам."""

    def __init__(self) -> None:
        self.session: Session = get_session()

    def close(self) -> None:
        """Закрывает сессию БД."""
        self.session.close()

    def search(
        self,
        deal_type: Optional[str] = None,
        property_type: Optional[str] = None,
        district_id: Optional[int] = None,
        min_area: Optional[float] = None,
        max_area: Optional[float] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_floors: Optional[int] = None,
        max_floors: Optional[int] = None,
    ) -> List[dict]:
        """Ищет объекты по фильтрам, возвращает СПИСОК СЛОВАРЕЙ.

        Каждый элемент:
            {
                "id": int,
                "title": str,
                "property_type": str,
                "deal_type": str,
                "area": float,
                "floors": int,
                "floor": int | None,
                "rooms": int | None,
                "price": float,
                "address": str,
                "district": str,
                "status": str,
            }
        """
        query = self.session.query(Property).options(joinedload(Property.district))

        if deal_type:
            query = query.filter(Property.deal_type == deal_type)
        if property_type:
            query = query.filter(Property.property_type == property_type)
        if district_id:
            query = query.filter(Property.district_id == district_id)
        if min_area is not None:
            query = query.filter(Property.area >= min_area)
        if max_area is not None:
            query = query.filter(Property.area <= max_area)
        if min_price is not None:
            query = query.filter(Property.price >= min_price)
        if max_price is not None:
            query = query.filter(Property.price <= max_price)
        if min_floors is not None:
            query = query.filter(Property.floors >= min_floors)
        if max_floors is not None:
            query = query.filter(Property.floors <= max_floors)

        props = query.order_by(Property.price.asc()).all()

        return [
            {
                "id": p.id,
                "title": p.title,
                "property_type": p.property_type,
                "deal_type": p.deal_type,
                "area": p.area,
                "floors": p.floors,
                "floor": p.floor,
                "rooms": p.rooms,
                "price": p.price,
                "address": p.address,
                "district": p.district.name if p.district else "—",
                "status": p.status or "активен",
            }
            for p in props
        ]
