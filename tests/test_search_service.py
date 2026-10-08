"""Тесты сервиса поиска.

ВАЖНО: SearchService.search() возвращает список СЛОВАРЕЙ,
поэтому обращение к полям — через квадратные скобки: prop["price"].
"""

from app.logic.search_service import SearchService


def test_search_returns_list():
    """Поиск всегда возвращает список."""
    service = SearchService()
    result = service.search(deal_type="продажа")
    assert isinstance(result, list)
    service.close()


def test_search_by_price_range():
    """Фильтр по диапазону цен работает."""
    service = SearchService()
    result = service.search(min_price=1_000_000, max_price=20_000_000)
    for prop in result:
        # prop — это словарь, поэтому через ["price"]
        assert 1_000_000 <= prop["price"] <= 20_000_000
    service.close()