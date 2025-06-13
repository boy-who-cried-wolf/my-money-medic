from sqlalchemy import (
    Column,
    String,
    Float,
    Text,
    ForeignKey,
    Enum,
    Integer,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from .base import SoftDeleteModel


class MatchStatus(enum.Enum):
    """Enum for broker-client match status"""

    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class BrokerClientMatch(SoftDeleteModel):
    """
    Model for storing matches between brokers and clients
    """

    __tablename__ = "broker_client_matches"

    user_id = Column(ForeignKey("users.id"), nullable=False)
    broker_id = Column(ForeignKey("brokers.id"), nullable=False)
    status = Column(Enum(MatchStatus), nullable=False, default=MatchStatus.PENDING)
    match_score = Column(Float, default=0.0)  # Algorithm-determined score
    notes = Column(Text)

    # Match lifecycle dates
    matched_at = Column(DateTime, default=datetime.utcnow)
    responded_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="broker_matches")
    broker = relationship("Broker", back_populates="client_matches")

    def __repr__(self):
        """String representation of the broker-client match"""
        return f"<BrokerClientMatch {self.user_id} - {self.broker_id}>"


class BrokerReview(SoftDeleteModel):
    """
    Model for storing reviews for brokers
    """

    __tablename__ = "broker_reviews"

    broker_id = Column(ForeignKey("brokers.id"), nullable=False)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    review_text = Column(Text)
    is_verified = Column(
        Boolean, default=False
    )  # Verify the user worked with this broker

    # Relationships
    broker = relationship("Broker", back_populates="reviews")

    def __repr__(self):
        """String representation of the broker review"""
        return f"<BrokerReview {self.broker_id} - {self.rating} stars>"
