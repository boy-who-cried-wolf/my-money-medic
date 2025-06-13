from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import UUID

from app.database.models import User, UserType
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


def get_user(db: Session, user_id: UUID) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id, User.is_deleted.is_(None)).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email, User.is_deleted.is_(None)).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get all users with pagination"""
    return (
        db.query(User).filter(User.is_deleted.is_(None)).offset(skip).limit(limit).all()
    )


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user"""
    # Check if user already exists
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise ValueError("Email already registered")

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create user instance
    db_user = User(
        email=user.email,
        password_hash=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone,
        user_type=UserType(user.user_type),
    )

    # Save to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(db: Session, user_id: UUID, user: UserUpdate) -> User:
    """Update user information"""
    db_user = get_user(db, user_id)

    # Update user fields
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        if value is not None:
            setattr(db_user, key, value)

    # Save changes
    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: UUID) -> None:
    """Soft delete a user"""
    db_user = get_user(db, user_id)
    db_user.soft_delete()
    db.commit()


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
