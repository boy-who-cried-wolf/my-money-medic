from sqlalchemy import Column, String, Boolean, Enum, Text, Integer, DateTime, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .base import SoftDeleteModel
from ..connection import Base


class UserType(enum.Enum):
    """Enum for user types"""

    CLIENT = "client"
    BROKER = "broker"
    ADMIN = "admin"


class User(SoftDeleteModel):
    """
    User model for storing user related data
    Inherits id (UUID), created_at, updated_at, and is_deleted from SoftDeleteModel
    """

    __tablename__ = "users"

    # Basic user information
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone_number = Column(String(50))

    # Authentication and status
    password_hash = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=False)
    user_type = Column(Enum(UserType), nullable=False)

    # Relationships
    quiz_responses = relationship(
        "UserQuizResponse", back_populates="user", cascade="all, delete-orphan"
    )

    broker_profile = relationship(
        "Broker", back_populates="user", uselist=False  # one-to-one relationship
    )

    banking_connections = relationship(
        "BankingConnection", back_populates="user", cascade="all, delete-orphan"
    )

    payments = relationship(
        "Payment", back_populates="user", cascade="all, delete-orphan"
    )

    broker_matches = relationship(
        "BrokerClientMatch", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        """String representation of the user"""
        return f"<User {self.id}: {self.email}>"

    @property
    def full_name(self):
        """Return user's full name"""
        return f"{self.first_name} {self.last_name}"
