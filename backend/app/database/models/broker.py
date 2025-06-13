from sqlalchemy import (
    Column,
    String,
    Float,
    Text,
    ForeignKey,
    Enum,
    Integer,
    Boolean,
    Table,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.mysql import JSON
import enum
from uuid import UUID

from .base import SoftDeleteModel


class LicenseStatus(enum.Enum):
    """Enum for broker license status"""

    ACTIVE = "active"
    PENDING = "pending"
    REVOKED = "revoked"
    EXPIRED = "expired"


class ExperienceLevel(enum.Enum):
    """Enum for broker experience level"""

    JUNIOR = "junior"
    INTERMEDIATE = "intermediate"
    SENIOR = "senior"
    EXPERT = "expert"


# Association table for broker specializations
broker_specialization = Table(
    "broker_specialization",
    SoftDeleteModel.metadata,
    Column("broker_id", ForeignKey("brokers.id"), primary_key=True),
    Column("specialization_id", ForeignKey("specializations.id"), primary_key=True),
)


class Broker(SoftDeleteModel):
    """
    Broker model for storing broker profile information
    Inherits id, created_at, updated_at, and is_deleted from SoftDeleteModel
    """

    __tablename__ = "brokers"

    # User relationship (one-to-one)
    user_id = Column(ForeignKey("users.id"), nullable=False, unique=True)
    user = relationship("User", back_populates="broker_profile")

    # Professional information
    license_number = Column(String(100), nullable=False, unique=True)
    license_status = Column(
        Enum(LicenseStatus), nullable=False, default=LicenseStatus.PENDING
    )
    company_name = Column(String(255))
    years_of_experience = Column(Integer, nullable=False)
    experience_level = Column(Enum(ExperienceLevel), nullable=False)

    # Contact and location
    office_address = Column(Text)
    service_areas = Column(JSON)  # List of areas/regions served

    # Bio and professional details
    bio = Column(Text)
    profile_image = Column(String(255))
    website = Column(String(255))

    # Ratings and performance
    average_rating = Column(Float, default=0.0)
    success_rate = Column(Float, default=0.0)

    # Verification status
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    specializations = relationship(
        "Specialization", secondary=broker_specialization, back_populates="brokers"
    )

    client_matches = relationship(
        "BrokerClientMatch", back_populates="broker", cascade="all, delete-orphan"
    )

    reviews = relationship(
        "BrokerReview", back_populates="broker", cascade="all, delete-orphan"
    )

    def __repr__(self):
        """String representation of the broker"""
        return f"<Broker {self.license_number}>"


class Specialization(SoftDeleteModel):
    """Model for broker specializations"""

    __tablename__ = "specializations"

    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)

    # Relationships
    brokers = relationship(
        "Broker", secondary=broker_specialization, back_populates="specializations"
    )

    def __repr__(self):
        """String representation of the specialization"""
        return f"<Specialization {self.name}>"
