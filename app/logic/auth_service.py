"""Бизнес-логика аутентификации и разграничения прав доступа."""

import hashlib
import hmac
import os
from typing import Optional

from sqlalchemy.orm import Session

from app.database.connection import get_session
from app.database.models import User

_ITERATIONS = 100_000
_SALT_SIZE = 16


def _hash_password(password: str, salt: Optional[bytes] = None) -> str:
    """Хэширует пароль через PBKDF2-HMAC-SHA256."""
    if salt is None:
        salt = os.urandom(_SALT_SIZE)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, _ITERATIONS
    )
    return f"{salt.hex()}${digest.hex()}"


def _verify_password(password: str, stored: str) -> bool:
    """Проверяет пароль против сохранённого хэша."""
    try:
        salt_hex, hash_hex = stored.split("$")
        salt = bytes.fromhex(salt_hex)
    except (ValueError, AttributeError):
        return False
    candidate = _hash_password(password, salt)
    return hmac.compare_digest(candidate, stored)


class AuthService:
    """Сервис аутентификации и управления пользователями."""

    def __init__(self) -> None:
        self.session: Session = get_session()
        self.current_user: Optional[User] = None

    def close(self) -> None:
        """Закрывает сессию БД."""
        self.session.close()

    def register(
        self,
        username: str,
        password: str,
        role: str = "agent",
    ) -> Optional[User]:
        """Регистрирует нового пользователя."""
        if self.session.query(User).filter_by(username=username).first():
            return None
        user = User(
            username=username,
            password_hash=_hash_password(password),
            role=role,
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def login(self, username: str, password: str) -> bool:
        """Выполняет вход пользователя."""
        user = self.session.query(User).filter_by(username=username).first()
        if not user:
            return False
        if not _verify_password(password, user.password_hash):
            return False
        self.current_user = user
        return True

    def logout(self) -> None:
        """Выполняет выход текущего пользователя."""
        self.current_user = None

    def is_authenticated(self) -> bool:
        """Проверяет, вошёл ли пользователь."""
        return self.current_user is not None

    def is_admin(self) -> bool:
        """Проверяет, является ли текущий пользователь администратором."""
        return bool(self.current_user and self.current_user.role == "admin")

    def ensure_default_admin(self) -> None:
        """Создаёт администратора по умолчанию (admin/admin), если его нет."""
        existing = self.session.query(User).filter_by(username="admin").first()
        if existing is None:
            self.register("admin", "admin", role="admin")