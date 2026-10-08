"""Тесты сервиса аутентификации."""

from app.database.connection import init_db
from app.database.models import User
from app.logic.auth_service import AuthService


def test_register_and_login():
    """Регистрация и вход работают."""
    init_db()
    auth = AuthService()
    username = "test_user_01"

    # Удаляем, если уже есть
    existing = auth.session.query(User).filter_by(username=username).first()
    if existing:
        auth.session.delete(existing)
        auth.session.commit()

    user = auth.register(username, "secret123", role="agent")
    assert user is not None
    assert auth.login(username, "secret123") is True
    assert auth.login(username, "wrong") is False
    auth.close()


def test_default_admin_exists():
    """Администратор по умолчанию создаётся."""
    init_db()
    auth = AuthService()
    auth.ensure_default_admin()
    assert auth.login("admin", "admin") is True
    assert auth.is_admin() is True
    auth.close()
