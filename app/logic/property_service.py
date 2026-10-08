"""Бизнес-логика для работы с объектами недвижимости (CRUD).

Учитывает owner_id — объект принадлежит конкретному менеджеру.
"""

from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from app.database.connection import get_session
from app.database.models import Property, District


class PropertyService:
    """Сервис управления объектами недвижимости."""

    def __init__(self) -> None:
        self.session: Session = get_session()

    def close(self) -> None:
        """Закрывает сессию БД."""
        self.session.close()

    # ---------- Чтение ----------

    def get_all(self) -> List[Property]:
        """Все объекты (для поиска и админа)."""
        return (
            self.session.query(Property)
            .options(joinedload(Property.district))
            .order_by(Property.created_at.desc())
            .all()
        )

    def get_by_owner(self, owner_id: int) -> List[Property]:
        """Объекты конкретного менеджера (по owner_id)."""
        return (
            self.session.query(Property)
            .options(joinedload(Property.district))
            .filter(Property.owner_id == owner_id)
            .order_by(Property.created_at.desc())
            .all()
        )

    def get_by_id(self, property_id: int) -> Optional[Property]:
        """Возвращает объект по id."""
        return self.session.query(Property).filter_by(id=property_id).first()

    # ---------- Создание ----------

    def create(
        self,
        title: str,
        property_type: str,
        deal_type: str,
        area: float,
        floors: int,
        floor: Optional[int],
        district_id: int,
        address: str,
        price: float,
        description: str = "",
        rooms: Optional[int] = None,
        status: str = "активен",
        owner_id: Optional[int] = None,
    ) -> Property:
        """Создаёт новый объект недвижимости."""
        prop = Property(
            owner_id=owner_id,
            title=title,
            property_type=property_type,
            deal_type=deal_type,
            area=area,
            floors=floors,
            floor=floor,
            rooms=rooms,
            district_id=district_id,
            address=address,
            price=price,
            status=status,
            description=description,
        )
        self.session.add(prop)
        self.session.commit()
        self.session.refresh(prop)
        return prop

    # ---------- Обновление ----------

    def update(self, property_id: int, **fields) -> Optional[Property]:
        """Обновляет поля объекта недвижимости."""
        prop = self.get_by_id(property_id)
        if not prop:
            return None
        for key, value in fields.items():
            if hasattr(prop, key):
                setattr(prop, key, value)
        self.session.commit()
        self.session.refresh(prop)
        return prop

    # ---------- Удаление ----------

    def delete(self, property_id: int) -> bool:
        """Удаляет объект по id."""
        prop = self.get_by_id(property_id)
        if not prop:
            return False
        self.session.delete(prop)
        self.session.commit()
        return True

    # ---------- Справочники ----------

    def get_districts(self) -> List[District]:
        """Список всех районов."""
        return self.session.query(District).order_by(District.name).all()

    def get_district_by_name(self, name: str) -> Optional[District]:
        """Район по имени."""
        return self.session.query(District).filter_by(name=name).first()
