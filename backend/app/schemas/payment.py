from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from uuid import UUID


class PaymentBase(BaseModel):
    """Base schema for payment data"""

    user_id: str
    amount: float
    currency: str
    payment_type: str
    payment_method: str
    description: Optional[str] = None
    reference: Optional[str] = None
    external_id: Optional[str] = None


class PaymentCreate(PaymentBase):
    """Schema for creating a payment"""

    pass


class PaymentUpdate(BaseModel):
    """Schema for updating a payment"""

    status: Optional[str] = None
    description: Optional[str] = None
    reference: Optional[str] = None
    external_id: Optional[str] = None
    processed_at: Optional[datetime] = None
    failure_reason: Optional[str] = None
    refunded_amount: Optional[float] = None


class PaymentFilterParams(BaseModel):
    """Schema for filtering payments"""

    user_id: Optional[str] = None
    status: Optional[str] = None
    payment_type: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None


class PaymentResponse(PaymentBase):
    """Schema for payment response"""

    id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
    processed_at: Optional[datetime] = None
    failure_reason: Optional[str] = None
    refunded_amount: Optional[float] = None
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)


class PaymentStatistics(BaseModel):
    """Schema for payment statistics"""

    total_payments: int
    payment_totals: Dict[str, Dict[str, Any]]
    status_totals: Dict[str, Dict[str, Any]]


class RefundRequest(BaseModel):
    """Schema for requesting a refund"""

    payment_id: str
    amount: Optional[float] = None
    reason: Optional[str] = None


class BankingConnectionBase(BaseModel):
    """Base schema for banking connection data"""

    user_id: UUID
    provider: str
    account_type: str
    account_name: Optional[str] = None
    masked_account_number: Optional[str] = None


class BankingConnectionCreate(BankingConnectionBase):
    """Schema for creating a banking connection"""

    token: str  # Temporary token for initial connection

    @field_validator("token")
    @classmethod
    def validate_token(cls, v):
        if len(v) < 10:  # Basic validation for token length
            raise ValueError("Invalid token")
        return v


class BankingConnectionResponse(BankingConnectionBase):
    """Schema for banking connection response"""

    id: UUID
    is_active: bool
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
