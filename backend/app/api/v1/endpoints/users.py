from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services import user_service
from app.core.security import verify_token

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    return user_service.create_user(db=db, user=user)


@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users with pagination"""
    return user_service.get_users(db=db, skip=skip, limit=limit)


@router.get("/me", response_model=UserResponse)
def read_current_user(
    db: Session = Depends(get_db), user_id: str = Depends(verify_token)
):
    """Get the current authenticated user"""
    db_user = user_service.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: str, db: Session = Depends(get_db)):
    """Get user by ID"""
    db_user = user_service.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user: UserUpdate, db: Session = Depends(get_db)):
    """Update user information"""
    db_user = user_service.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_service.update_user(db=db, user_id=user_id, user=user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    """Delete a user (soft delete)"""
    db_user = user_service.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_service.delete_user(db=db, user_id=user_id)
    return None


@router.get("/{user_id}/profile", response_model=UserResponse)
def read_user_profile(user_id: str, db: Session = Depends(get_db)):
    """Get user profile by ID"""
    db_user = user_service.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
