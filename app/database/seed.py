"""Наполнение БД тестовыми данными (при первом запуске)."""

from app.database.connection import get_session
from app.database.models import District, Property


def seed_database() -> None:
    """Заполняет БД демо-данными, если таблицы пусты."""
    session = get_session()
    try:
        if session.query(District).count() > 0:
            return

        districts = [
            District(name="Центральный"),
            District(name="Ленинский"),
            District(name="Октябрьский"),
            District(name="Кировский"),
        ]
        session.add_all(districts)
        session.commit()

        properties = [
            Property(
                title="2-комн. квартира, ул. Ленина, 15",
                property_type="квартира",
                deal_type="продажа",
                area=54.5,
                floors=9,
                floor=4,
                district_id=districts[0].id,
                address="ул. Ленина, 15, кв. 42",
                price=6_500_000,
                description="Просторная квартира с ремонтом.",
            ),
            Property(
                title="3-комн. квартира, ул. Мира, 8",
                property_type="квартира",
                deal_type="продажа",
                area=78.0,
                floors=5,
                floor=3,
                district_id=districts[1].id,
                address="ул. Мира, 8, кв. 12",
                price=8_900_000,
                description="Квартира с балконом, рядом парк.",
            ),
            Property(
                title="Офис 60 м², пр. Карла Маркса, 20",
                property_type="помещение",
                deal_type="аренда",
                area=60.0,
                floors=12,
                floor=5,
                district_id=districts[2].id,
                address="пр. Карла Маркса, 20, оф. 501",
                price=45_000,
                description="Офис в бизнес-центре.",
            ),
            Property(
                title="Дом 120 м², ул. Садовая, 3",
                property_type="дом",
                deal_type="продажа",
                area=120.0,
                floors=2,
                district_id=districts[3].id,
                address="ул. Садовая, 3",
                price=12_300_000,
                description="Дом с участком 6 соток.",
            ),
        ]
        session.add_all(properties)
        session.commit()

        # Создаём администратора по умолчанию (admin / admin)
        from app.logic.auth_service import AuthService
        auth = AuthService()
        auth.ensure_default_admin()
        auth.close()
    finally:
        session.close()
