from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.schemas.broker import (
    BrokerCreate,
    BrokerResponse,
    BrokerUpdate,
    BrokerSearchParams,
)
from app.services import broker_service

router = APIRouter()


@router.post("/", response_model=BrokerResponse, status_code=status.HTTP_201_CREATED)
def create_broker(broker: BrokerCreate, db: Session = Depends(get_db)):
    """Create a new broker profile"""
    return broker_service.create_broker(db=db, broker=broker)


@router.get("/", response_model=List[BrokerResponse])
def read_brokers(
    skip: int = 0,
    limit: int = 20,
    experience_level: Optional[str] = None,
    specialization: Optional[str] = None,
    rating: Optional[float] = None,
    db: Session = Depends(get_db),
):
    """Get all brokers with optional filtering"""
    return broker_service.get_brokers(
        db=db,
        skip=skip,
        limit=limit,
        experience_level=experience_level,
        specialization=specialization,
        rating=rating,
    )


@router.get("/{broker_id}", response_model=BrokerResponse)
def read_broker(broker_id: str, db: Session = Depends(get_db)):
    """Get broker by ID"""
    db_broker = broker_service.get_broker(db=db, broker_id=broker_id)
    if db_broker is None:
        raise HTTPException(status_code=404, detail="Broker not found")
    return db_broker


@router.put("/{broker_id}", response_model=BrokerResponse)
def update_broker(broker_id: str, broker: BrokerUpdate, db: Session = Depends(get_db)):
    """Update broker information"""
    db_broker = broker_service.get_broker(db=db, broker_id=broker_id)
    if db_broker is None:
        raise HTTPException(status_code=404, detail="Broker not found")
    return broker_service.update_broker(db=db, broker_id=broker_id, broker=broker)


@router.delete("/{broker_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_broker(broker_id: str, db: Session = Depends(get_db)):
    """Delete a broker profile (soft delete)"""
    db_broker = broker_service.get_broker(db=db, broker_id=broker_id)
    if db_broker is None:
        raise HTTPException(status_code=404, detail="Broker not found")
    broker_service.delete_broker(db=db, broker_id=broker_id)
    return None


@router.post("/search", response_model=List[BrokerResponse])
def search_brokers(search_params: BrokerSearchParams, db: Session = Depends(get_db)):
    """Search for brokers based on various criteria"""
    return broker_service.search_brokers(db=db, search_params=search_params)


@router.get("/{broker_id}/reviews", response_model=List[BrokerResponse])
def get_broker_reviews(broker_id: str, db: Session = Depends(get_db)):
    """Get reviews for a specific broker"""
    db_broker = broker_service.get_broker(db=db, broker_id=broker_id)
    if db_broker is None:
        raise HTTPException(status_code=404, detail="Broker not found")
    return broker_service.get_broker_reviews(db=db, broker_id=broker_id)


@router.post("/{broker_id}/specializations/{specialization_id}")
def add_broker_specialization(
    broker_id: str, specialization_id: str, db: Session = Depends(get_db)
):
    """Add a specialization to a broker's profile"""
    result = broker_service.add_specialization(
        db=db, broker_id=broker_id, specialization_id=specialization_id
    )
    if not result:
        raise HTTPException(
            status_code=404, detail="Broker or specialization not found"
        )
    return {"message": "Specialization added successfully"}
