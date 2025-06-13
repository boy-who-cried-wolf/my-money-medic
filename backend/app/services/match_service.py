"""
Service module for broker-client matching business logic.
"""

from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from uuid import uuid4
from datetime import datetime

from app.database.models.user import User
from app.database.models.broker import Broker
from app.database.models.response import BrokerClientMatch, MatchStatus
from app.schemas.match import (
    MatchCreate,
    MatchUpdate,
    MatchFilterParams,
    MatchAlgorithmParams,
    BrokerClientMatchCreate,
    BrokerClientMatchUpdate,
)


def create_match(db: Session, match: MatchCreate) -> BrokerClientMatch:
    """
    Create a new broker-client match
    """
    db_match = BrokerClientMatch(
        id=str(uuid4()),
        broker_id=match.broker_id,
        user_id=match.client_id,
        match_score=match.match_score,
        status=match.status,
        matched_by=match.matched_by if hasattr(match, "matched_by") else None,
        notes=match.notes,
    )
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


def get_matches(
    db: Session, filters: MatchFilterParams, skip: int = 0, limit: int = 100
) -> List[BrokerClientMatch]:
    """
    Get matches with filtering and pagination
    """
    query = db.query(BrokerClientMatch).filter(BrokerClientMatch.is_deleted == False)

    # Apply filters
    if filters.broker_id:
        query = query.filter(BrokerClientMatch.broker_id == filters.broker_id)
    if filters.client_id:
        query = query.filter(BrokerClientMatch.user_id == filters.client_id)
    if filters.status:
        query = query.filter(BrokerClientMatch.status == filters.status)
    if filters.min_score:
        query = query.filter(BrokerClientMatch.match_score >= filters.min_score)
    if filters.max_score:
        query = query.filter(BrokerClientMatch.match_score <= filters.max_score)

    # Apply pagination
    return query.offset(skip).limit(limit).all()


def get_match(db: Session, match_id: str) -> Optional[BrokerClientMatch]:
    """
    Get match by ID
    """
    return (
        db.query(BrokerClientMatch)
        .filter(BrokerClientMatch.id == match_id, BrokerClientMatch.is_deleted == False)
        .first()
    )


def update_match(
    db: Session, match_id: str, match: BrokerClientMatchUpdate
) -> Optional[BrokerClientMatch]:
    """
    Update a match
    """
    db_match = get_match(db, match_id)
    if not db_match:
        return None

    # Update attributes
    update_data = match.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_match, key, value)

    db.commit()
    db.refresh(db_match)
    return db_match


def delete_match(db: Session, match_id: str) -> bool:
    """
    Delete a match (soft delete)
    """
    db_match = get_match(db, match_id)
    if not db_match:
        return False

    db_match.is_deleted = True
    db.commit()
    return True


def generate_matches(
    db: Session, params: MatchAlgorithmParams
) -> List[BrokerClientMatch]:
    """
    Generate broker matches for a client based on matching algorithm
    """
    # Import the new matching algorithm
    from app.services.matching_algorithm import generate_broker_matches

    # Get the client
    client = (
        db.query(User)
        .filter(User.id == params.user_id, User.is_deleted == False)
        .first()
    )
    if not client:
        return []

    # Use the sophisticated matching algorithm
    match_results = generate_broker_matches(
        db=db, user_id=params.user_id, save_to_db=False  # We'll handle saving ourselves
    )

    # Create BrokerClientMatch objects from results
    matches = []
    for match_data in match_results:
        if match_data["match_score"] >= params.min_match_score:
            db_match = BrokerClientMatch(
                id=str(uuid4()),
                broker_id=match_data["broker_id"],
                user_id=params.user_id,
                match_score=match_data["match_score"],
                status=MatchStatus.PENDING,
                notes=f"Algorithm match - Score: {match_data['match_score']:.3f}",
            )
            db.add(db_match)
            matches.append(db_match)

    db.commit()
    for match in matches:
        db.refresh(match)

    return matches


def get_user_matches(
    db: Session, user_id: str, limit: int = 10
) -> List[BrokerClientMatch]:
    """
    Get top matches for a client
    """
    return (
        db.query(BrokerClientMatch)
        .filter(
            BrokerClientMatch.user_id == user_id,  # Changed from client_id to user_id
            BrokerClientMatch.is_deleted == False,
        )
        .order_by(BrokerClientMatch.match_score.desc())
        .limit(limit)
        .all()
    )


def get_broker_matches(
    db: Session, broker_id: str, limit: int = 10
) -> List[BrokerClientMatch]:
    """
    Get top matches for a broker
    """
    return (
        db.query(BrokerClientMatch)
        .filter(
            BrokerClientMatch.broker_id == broker_id,
            BrokerClientMatch.is_deleted == False,
        )
        .order_by(BrokerClientMatch.match_score.desc())
        .limit(limit)
        .all()
    )


def accept_match(db: Session, match_id: str) -> BrokerClientMatch:
    """
    Accept a match (by broker)
    """
    db_match = get_match(db, match_id)
    if not db_match:
        return None

    db_match.status = MatchStatus.ACCEPTED
    db_match.responded_at = datetime.utcnow()
    db.commit()
    db.refresh(db_match)
    return db_match


def reject_match(db: Session, match_id: str) -> BrokerClientMatch:
    """
    Reject a match (by broker)
    """
    db_match = get_match(db, match_id)
    if not db_match:
        return None

    db_match.status = MatchStatus.REJECTED
    db_match.responded_at = datetime.utcnow()
    db.commit()
    db.refresh(db_match)
    return db_match


def complete_match(db: Session, match_id: str) -> BrokerClientMatch:
    """
    Mark a match as completed
    """
    db_match = get_match(db, match_id)
    if not db_match:
        return None

    db_match.status = MatchStatus.COMPLETED
    db_match.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(db_match)
    return db_match
