"""Валидация пользовательского ввода (соответствует п.4.1.4 ТЗ)."""

from typing import Optional


def is_positive_number(value: str) -> bool:
    """Проверяет, что строка — положительное число."""
    try:
        return float(value) > 0
    except (ValueError, TypeError):
        return False


def is_positive_int(value: str) -> bool:
    """Проверяет, что строка — положительное целое число."""
    try:
        return int(value) > 0
    except (ValueError, TypeError):
        return False


def is_not_empty(value: Optional[str]) -> bool:
    """Проверяет, что строка не пустая."""
    return bool(value and value.strip())


def parse_float(value: str, default: float = 0.0) -> float:
    """Безопасно преобразует строку в float."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def parse_int(value: str, default: int = 0) -> int:
    """Безопасно преобразует строку в int."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default
