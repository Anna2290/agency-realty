"""Тесты бизнес-логики объектов недвижимости."""

import pytest

from app.database.connection import init_db, get_session
from app.database.models import District
from app.logic.property_service import PropertyService


@pytest.fixture(autouse=True)
def setup_db():
    """Создаёт схему БД перед тестами."""
    init_db()
    session = get_session()
    if session.query(District).count() == 0:
        session.add(District(name="Тестовый"))
        session.commit()
    session.close()


def test_create_and_get_property():
    """Проверяет создание и получение объекта."""
    service = PropertyService()
    prop = service.create(
        title="Тестовая квартира",
        property_type="квартира",
        deal_type="продажа",
        area=50.0,
        floors=5,
        floor=2,
        district_id=1,
        address="ул. Тестовая, 1",
        price=3_000_000,
    )
    assert prop.id is not None
    fetched = service.get_by_id(prop.id)
    assert fetched.title == "Тестовая квартира"
    service.delete(prop.id)
    service.close()
