from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from uuid import UUID

from app.database.models import Broker, Specialization, BrokerReview
from app.schemas.broker import BrokerCreate, BrokerUpdate, BrokerSearchParams


def get_broker(db: Session, broker_id: UUID) -> Optional[Broker]:
    """Get broker by ID"""
    return (
        db.query(Broker)
        .filter(Broker.id == broker_id, Broker.is_deleted.is_(None))
        .first()
    )


def get_broker_by_user_id(db: Session, user_id: UUID) -> Optional[Broker]:
    """Get broker by user ID"""
    return (
        db.query(Broker)
        .filter(Broker.user_id == user_id, Broker.is_deleted.is_(None))
        .first()
    )


def get_broker_by_license(db: Session, license_number: str) -> Optional[Broker]:
    """Get broker by license number"""
    return (
        db.query(Broker)
        .filter(Broker.license_number == license_number, Broker.is_deleted.is_(None))
        .first()
    )


def get_brokers(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    experience_level: Optional[str] = None,
    specialization: Optional[str] = None,
    rating: Optional[float] = None,
) -> List[Broker]:
    """Get all brokers with optional filtering"""
    query = db.query(Broker).filter(Broker.is_deleted.is_(None))

    # Apply filters if provided
    if experience_level:
        query = query.filter(Broker.experience_level == experience_level)

    if rating is not None:
        query = query.filter(Broker.average_rating >= rating)

    if specialization:
        query = query.join(Broker.specializations).filter(
            Specialization.name == specialization
        )

    return query.offset(skip).limit(limit).all()


def create_broker(db: Session, broker: BrokerCreate) -> Broker:
    """Create a new broker profile"""
    # Check if license number already exists
    existing_broker = get_broker_by_license(db, broker.license_number)
    if existing_broker:
        raise ValueError("License number already registered")

    # Check if user already has a broker profile
    existing_user_broker = get_broker_by_user_id(db, broker.user_id)
    if existing_user_broker:
        raise ValueError("User already has a broker profile")

    # Create broker instance
    db_broker = Broker(
        user_id=broker.user_id,
        license_number=broker.license_number,
        license_status=broker.license_status,
        company_name=broker.company_name,
        years_of_experience=broker.years_of_experience,
        experience_level=broker.experience_level,
        office_address=broker.office_address,
        service_areas=broker.service_areas,
        bio=broker.bio,
        profile_image=broker.profile_image,
        website=broker.website,
    )

    # Add specializations if provided
    if broker.specialization_ids:
        specializations = (
            db.query(Specialization)
            .filter(
                Specialization.id.in_(broker.specialization_ids),
                Specialization.is_deleted.is_(None),
            )
            .all()
        )
        db_broker.specializations = specializations

    # Save to database
    db.add(db_broker)
    db.commit()
    db.refresh(db_broker)

    return db_broker


def update_broker(db: Session, broker_id: UUID, broker: BrokerUpdate) -> Broker:
    """Update broker information"""
    db_broker = get_broker(db, broker_id)

    # Update broker fields
    broker_data = broker.model_dump(exclude_unset=True)
    for key, value in broker_data.items():
        # Skip service_areas as it needs special handling
        if key != "service_areas" and value is not None:
            setattr(db_broker, key, value)

    # Handle service_areas separately as it's a JSON field
    if broker.service_areas is not None:
        db_broker.service_areas = broker.service_areas

    # Save changes
    db.commit()
    db.refresh(db_broker)

    return db_broker


def delete_broker(db: Session, broker_id: UUID) -> None:
    """Soft delete a broker profile"""
    db_broker = get_broker(db, broker_id)
    db_broker.soft_delete()
    db.commit()


def search_brokers(db: Session, search_params: BrokerSearchParams) -> List[Broker]:
    """Search for brokers based on various criteria"""
    query = db.query(Broker).filter(Broker.is_deleted.is_(None))

    filters = []

    # Apply experience level filter
    if search_params.experience_level:
        filters.append(Broker.experience_level == search_params.experience_level)

    # Apply years of experience filter
    if search_params.years_of_experience:
        filters.append(Broker.years_of_experience >= search_params.years_of_experience)

    # Apply minimum rating filter
    if search_params.min_rating:
        filters.append(Broker.average_rating >= search_params.min_rating)

    # Apply verification filter
    if search_params.is_verified is not None:
        filters.append(Broker.is_verified == search_params.is_verified)

    # Apply service area filter
    if search_params.service_areas:
        # This would depend on how service_areas is stored in the database
        # For JSON fields, use contains operator or similar based on DB
        pass

    # Apply keyword search
    if search_params.keyword:
        keyword = f"%{search_params.keyword}%"
        filters.append(
            or_(Broker.bio.ilike(keyword), Broker.company_name.ilike(keyword))
        )

    # Apply specialization filter
    if search_params.specializations:
        query = query.join(Broker.specializations).filter(
            Specialization.name.in_(search_params.specializations)
        )

    # Apply all filters
    if filters:
        query = query.filter(and_(*filters))

    return query.all()


def get_broker_reviews(db: Session, broker_id: UUID) -> List[BrokerReview]:
    """Get reviews for a specific broker"""
    return (
        db.query(BrokerReview)
        .filter(BrokerReview.broker_id == broker_id, BrokerReview.is_deleted.is_(None))
        .all()
    )


def add_specialization(db: Session, broker_id: UUID, specialization_id: UUID) -> bool:
    """Add a specialization to a broker's profile"""
    db_broker = get_broker(db, broker_id)
    if not db_broker:
        return False

    specialization = (
        db.query(Specialization)
        .filter(
            Specialization.id == specialization_id, Specialization.is_deleted.is_(None)
        )
        .first()
    )

    if not specialization:
        return False

    # Check if broker already has this specialization
    if specialization in db_broker.specializations:
        return True

    # Add specialization
    db_broker.specializations.append(specialization)
    db.commit()

    return True
