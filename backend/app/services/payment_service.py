"""
Service module for payment-related business logic
"""

from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from uuid import uuid4
from datetime import datetime

from app.database.models.financial import Payment, PaymentStatus, PaymentType
from app.schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
    PaymentFilterParams,
)


def create_payment(db: Session, payment: PaymentCreate) -> Payment:
    """
    Create a new payment
    """
    db_payment = Payment(
        id=str(uuid4()),
        user_id=payment.user_id,
        amount=payment.amount,
        currency=payment.currency,
        payment_type=payment.payment_type,
        payment_method=payment.payment_method,
        status=PaymentStatus.PENDING,
        description=payment.description,
        reference=payment.reference,
        external_id=payment.external_id,
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def get_payments(
    db: Session, filters: PaymentFilterParams, skip: int = 0, limit: int = 100
) -> List[Payment]:
    """
    Get payments with filtering and pagination
    """
    query = db.query(Payment).filter(Payment.is_deleted == False)

    # Apply filters
    if filters.user_id:
        query = query.filter(Payment.user_id == filters.user_id)
    if filters.status:
        query = query.filter(Payment.status == filters.status)
    if filters.payment_type:
        query = query.filter(Payment.payment_type == filters.payment_type)
    if filters.min_amount:
        query = query.filter(Payment.amount >= filters.min_amount)
    if filters.max_amount:
        query = query.filter(Payment.amount <= filters.max_amount)
    if filters.from_date:
        query = query.filter(Payment.created_at >= filters.from_date)
    if filters.to_date:
        query = query.filter(Payment.created_at <= filters.to_date)

    # Apply pagination
    return query.order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()


def get_payment(db: Session, payment_id: str) -> Optional[Payment]:
    """
    Get payment by ID
    """
    return (
        db.query(Payment)
        .filter(Payment.id == payment_id, Payment.is_deleted == False)
        .first()
    )


def update_payment(
    db: Session, payment_id: str, payment: PaymentUpdate
) -> Optional[Payment]:
    """
    Update a payment
    """
    db_payment = get_payment(db, payment_id)
    if not db_payment:
        return None

    # Update attributes
    update_data = payment.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_payment, key, value)

    db.commit()
    db.refresh(db_payment)
    return db_payment


def delete_payment(db: Session, payment_id: str) -> bool:
    """
    Delete a payment (soft delete)
    """
    db_payment = get_payment(db, payment_id)
    if not db_payment:
        return False

    db_payment.is_deleted = True
    db.commit()
    return True


def process_payment(db: Session, payment_id: str) -> Optional[Payment]:
    """
    Process a pending payment
    In a real application, this would interact with a payment gateway
    """
    db_payment = get_payment(db, payment_id)
    if not db_payment or db_payment.status != PaymentStatus.PENDING:
        return None

    # Simulate payment processing
    # In a real application, this would call the payment gateway API
    import random

    if random.random() < 0.9:  # 90% success rate for testing
        db_payment.status = PaymentStatus.COMPLETED
        db_payment.processed_at = datetime.utcnow()
    else:
        db_payment.status = PaymentStatus.FAILED
        db_payment.failure_reason = "Payment gateway error"

    db.commit()
    db.refresh(db_payment)
    return db_payment


def refund_payment(
    db: Session, payment_id: str, amount: Optional[float] = None
) -> Optional[Payment]:
    """
    Refund a completed payment
    """
    db_payment = get_payment(db, payment_id)
    if not db_payment or db_payment.status != PaymentStatus.COMPLETED:
        return None

    # Default to full refund if amount not specified
    refund_amount = amount if amount is not None else db_payment.amount

    # Create refund payment record
    refund_payment = Payment(
        id=str(uuid4()),
        user_id=db_payment.user_id,
        amount=refund_amount,
        currency=db_payment.currency,
        payment_type=PaymentType.REFUND,
        payment_method=db_payment.payment_method,
        status=PaymentStatus.COMPLETED,
        description=f"Refund for payment {db_payment.id}",
        reference=db_payment.id,
        external_id=None,
        processed_at=datetime.utcnow(),
    )

    # Update original payment
    db_payment.refunded_amount = refund_amount
    if refund_amount >= db_payment.amount:
        db_payment.status = PaymentStatus.REFUNDED
    else:
        db_payment.status = PaymentStatus.PARTIALLY_REFUNDED

    db.add(refund_payment)
    db.commit()
    db.refresh(db_payment)
    db.refresh(refund_payment)

    return refund_payment


def get_user_transactions(db: Session, user_id: str, limit: int = 20) -> List[Payment]:
    """
    Get a user's payment history
    """
    return (
        db.query(Payment)
        .filter(Payment.user_id == user_id, Payment.is_deleted == False)
        .order_by(Payment.created_at.desc())
        .limit(limit)
        .all()
    )


def get_payment_statistics(
    db: Session, user_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get payment statistics, optionally filtered by user
    """
    query = db.query(Payment).filter(Payment.is_deleted == False)

    if user_id:
        query = query.filter(Payment.user_id == user_id)

    # Get total payments and amounts
    total_payments = query.count()

    # Get totals by payment type
    payment_totals = {}
    for payment_type in PaymentType:
        type_query = query.filter(Payment.payment_type == payment_type)
        payment_totals[payment_type.value] = {
            "count": type_query.count(),
            "amount": sum(payment.amount for payment in type_query.all()),
        }

    # Get totals by status
    status_totals = {}
    for status in PaymentStatus:
        status_query = query.filter(Payment.status == status)
        status_totals[status.value] = {
            "count": status_query.count(),
            "amount": sum(payment.amount for payment in status_query.all()),
        }

    return {
        "total_payments": total_payments,
        "payment_totals": payment_totals,
        "status_totals": status_totals,
    }
