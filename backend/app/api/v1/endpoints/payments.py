from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
    BankingConnectionCreate,
    BankingConnectionResponse,
)
from app.services import payment_service

router = APIRouter()


# Payment endpoints
@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    """Create a new payment record"""
    return payment_service.create_payment(db=db, payment=payment)


@router.get("/", response_model=List[PaymentResponse])
def read_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all payments with pagination"""
    return payment_service.get_payments(db=db, skip=skip, limit=limit)


@router.get("/{payment_id}", response_model=PaymentResponse)
def read_payment(payment_id: str, db: Session = Depends(get_db)):
    """Get payment by ID"""
    db_payment = payment_service.get_payment(db=db, payment_id=payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment


@router.get("/user/{user_id}", response_model=List[PaymentResponse])
def read_user_payments(user_id: str, db: Session = Depends(get_db)):
    """Get all payments for a user"""
    return payment_service.get_user_payments(db=db, user_id=user_id)


# Banking connection endpoints
@router.post(
    "/banking",
    response_model=BankingConnectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_banking_connection(
    connection: BankingConnectionCreate, db: Session = Depends(get_db)
):
    """Create a new banking connection"""
    return payment_service.create_banking_connection(db=db, connection=connection)


@router.get("/banking/user/{user_id}", response_model=List[BankingConnectionResponse])
def read_user_banking_connections(user_id: str, db: Session = Depends(get_db)):
    """Get all banking connections for a user"""
    return payment_service.get_user_banking_connections(db=db, user_id=user_id)


@router.delete("/banking/{connection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_banking_connection(connection_id: str, db: Session = Depends(get_db)):
    """Delete a banking connection"""
    db_connection = payment_service.get_banking_connection(
        db=db, connection_id=connection_id
    )
    if db_connection is None:
        raise HTTPException(status_code=404, detail="Banking connection not found")
    payment_service.delete_banking_connection(db=db, connection_id=connection_id)
    return None


# Payment processing endpoints
@router.post("/process", response_model=PaymentResponse)
def process_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    """Process a payment through payment gateway"""
    return payment_service.process_payment(db=db, payment=payment)


@router.post("/{payment_id}/refund", response_model=PaymentResponse)
def refund_payment(payment_id: str, db: Session = Depends(get_db)):
    """Refund a payment"""
    db_payment = payment_service.get_payment(db=db, payment_id=payment_id)
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment_service.refund_payment(db=db, payment_id=payment_id)
