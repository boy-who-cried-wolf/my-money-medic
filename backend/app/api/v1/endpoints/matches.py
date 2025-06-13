from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.core.auth import get_current_user
from app.database.models.user import User, UserType
from app.schemas.match import (
    BrokerClientMatchCreate,
    BrokerClientMatchResponse,
    BrokerClientMatchUpdate,
    MatchAlgorithmParams,
)
from app.services import match_service
from app.services.matching_algorithm import generate_broker_matches

router = APIRouter()


@router.post(
    "/generate",
    response_model=List[dict],
    status_code=status.HTTP_201_CREATED,
)
def generate_matches_for_current_user(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Generate matches for the current user based on their quiz responses"""
    if current_user.user_type != UserType.CLIENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only clients can generate matches",
        )

    # Generate matches using the sophisticated algorithm
    matches = generate_broker_matches(db=db, user_id=current_user.id, save_to_db=True)

    return matches


@router.get("/my-matches", response_model=List[BrokerClientMatchResponse])
def get_my_matches(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10,
):
    """Get matches for the current user"""
    if current_user.user_type == UserType.CLIENT:
        return match_service.get_user_matches(
            db=db, user_id=current_user.id, limit=limit
        )
    elif current_user.user_type == UserType.BROKER:
        # Get broker profile
        from app.database.models.broker import Broker

        broker = db.query(Broker).filter(Broker.user_id == current_user.id).first()
        if not broker:
            raise HTTPException(status_code=404, detail="Broker profile not found")
        return match_service.get_broker_matches(
            db=db, broker_id=str(broker.id), limit=limit
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin users cannot view matches",
        )


@router.post(
    "/",
    response_model=List[BrokerClientMatchResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_matches(
    params: MatchAlgorithmParams,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate matches for a user based on their quiz responses (admin only)"""
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can generate matches for other users",
        )
    return match_service.generate_matches(db=db, params=params)


@router.get("/user/{user_id}", response_model=List[BrokerClientMatchResponse])
def get_user_matches(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all matches for a client user"""
    # Users can only view their own matches unless they're admin
    if current_user.user_type != UserType.ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own matches",
        )
    return match_service.get_user_matches(db=db, user_id=user_id)


@router.get("/broker/{broker_id}", response_model=List[BrokerClientMatchResponse])
def get_broker_matches(broker_id: str, db: Session = Depends(get_db)):
    """Get all matches for a broker"""
    return match_service.get_broker_matches(db=db, broker_id=broker_id)


@router.get("/{match_id}", response_model=BrokerClientMatchResponse)
def get_match(match_id: str, db: Session = Depends(get_db)):
    """Get a specific match by ID"""
    db_match = match_service.get_match(db=db, match_id=match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_match


@router.put("/{match_id}", response_model=BrokerClientMatchResponse)
def update_match(
    match_id: str, match: BrokerClientMatchUpdate, db: Session = Depends(get_db)
):
    """Update match status and information"""
    db_match = match_service.get_match(db=db, match_id=match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return match_service.update_match(db=db, match_id=match_id, match=match)


@router.post("/{match_id}/accept", response_model=BrokerClientMatchResponse)
def accept_match(match_id: str, db: Session = Depends(get_db)):
    """Accept a match (by broker)"""
    db_match = match_service.get_match(db=db, match_id=match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return match_service.accept_match(db=db, match_id=match_id)


@router.post("/{match_id}/reject", response_model=BrokerClientMatchResponse)
def reject_match(match_id: str, db: Session = Depends(get_db)):
    """Reject a match (by broker)"""
    db_match = match_service.get_match(db=db, match_id=match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return match_service.reject_match(db=db, match_id=match_id)


@router.post("/{match_id}/complete", response_model=BrokerClientMatchResponse)
def complete_match(match_id: str, db: Session = Depends(get_db)):
    """Mark a match as completed"""
    db_match = match_service.get_match(db=db, match_id=match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return match_service.complete_match(db=db, match_id=match_id)
