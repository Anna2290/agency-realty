"""ORM-модели базы данных."""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class District(Base):
    """Справочник районов города."""

    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    properties = relationship("Property", back_populates="district")

    def __repr__(self) -> str:
        return f"<District(id={self.id}, name='{self.name}')>"


class Property(Base):
    """Объект недвижимости (принадлежит конкретному менеджеру)."""

    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # менеджер
    title = Column(String(200), nullable=False)
    property_type = Column(String(50), nullable=False)
    deal_type = Column(String(20), nullable=False)
    area = Column(Float, nullable=False)
    floors = Column(Integer, nullable=False)
    floor = Column(Integer, nullable=True)
    rooms = Column(Integer, nullable=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False)
    address = Column(String(300), nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String(30), default="активен")
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    district = relationship("District", back_populates="properties")
    owner = relationship("User", back_populates="properties")
    offers = relationship("Offer", back_populates="property")

    def __repr__(self) -> str:
        return f"<Property(id={self.id}, title='{self.title}', price={self.price})>"


class Client(Base):
    """Клиент агентства."""

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(200), nullable=False)
    phone = Column(String(30), nullable=False)
    email = Column(String(100), nullable=True)
    request = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    offers = relationship("Offer", back_populates="client")

    def __repr__(self) -> str:
        return f"<Client(id={self.id}, name='{self.full_name}')>"


class Offer(Base):
    """Коммерческое предложение клиенту."""

    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="offers")
    property = relationship("Property", back_populates="offers")

    def __repr__(self) -> str:
        return f"<Offer(id={self.id}, client_id={self.client_id}, property_id={self.property_id})>"


class User(Base):
    """Пользователь системы (агент / администратор)."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(200), nullable=False)
    role = Column(String(20), default="agent")

    properties = relationship("Property", back_populates="owner")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
