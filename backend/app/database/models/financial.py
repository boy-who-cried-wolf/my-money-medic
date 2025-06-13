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


class PaymentStatus(enum.Enum):
    """Enum for payment status"""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentType(enum.Enum):
    """Enum for payment type"""

    SUBSCRIPTION = "subscription"
    ONE_TIME = "one_time"
    COMMISSION = "commission"
    REFUND = "refund"


class Payment(SoftDeleteModel):
    """
    Model for storing payment information
    """

    __tablename__ = "payments"

    user_id = Column(ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    payment_type = Column(Enum(PaymentType), nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)

    # Payment metadata
    transaction_id = Column(String(255), unique=True)
    payment_method = Column(String(100))
    description = Column(Text)

    # Payment dates
    payment_date = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="payments")

    def __repr__(self):
        """String representation of the payment"""
        return f"<Payment {self.transaction_id} - {self.amount} {self.currency}>"


class BankingConnectionType(enum.Enum):
    """Enum for banking connection type"""

    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT = "credit"
    INVESTMENT = "investment"


class BankingConnection(SoftDeleteModel):
    """
    Model for storing banking connections
    """

    __tablename__ = "banking_connections"

    user_id = Column(ForeignKey("users.id"), nullable=False)
    provider = Column(String(100), nullable=False)  # eg Stripe
    account_type = Column(Enum(BankingConnectionType), nullable=False)

    # Masked data for security
    account_name = Column(String(255))
    masked_account_number = Column(String(50))  # Last 4 digits

    # Connection status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Integration details - store encrypted
    token_id = Column(String(255))  # Reference to securely stored token

    # Relationships
    user = relationship("User", back_populates="banking_connections")

    def __repr__(self):
        """String representation of the banking connection"""
        return f"<BankingConnection {self.user_id} - {self.provider} - {self.account_type}>"
