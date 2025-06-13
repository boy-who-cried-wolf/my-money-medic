"""Authentication utilities for the API."""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.connection import get_db
from app.schemas.token import TokenPayload
from app.schemas.user import User
from app.database.models.user import User as UserModel, UserType

# OAuth2 password bearer token setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new JWT access token for a user.

    Args:
        subject: Subject of the token (typically user ID)
        expires_delta: Optional token expiration time delta

    Returns:
        JWT access token as string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> UserModel:
    """
    Get the current authenticated user from JWT token.

    Args:
        token: JWT token from Authorization header
        db: Database session

    Returns:
        User model object for the authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT token
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        token_data = TokenPayload(sub=user_id)
    except JWTError:
        raise credentials_exception

    # Get user from database
    user = db.query(UserModel).filter(UserModel.id == token_data.sub).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


async def require_admin(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    """
    Require the current user to be an admin.

    Args:
        current_user: Currently authenticated user

    Returns:
        User model if user is admin

    Raises:
        HTTPException: If user is not an admin
    """
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return current_user


async def require_broker_or_admin(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    """
    Require the current user to be a broker or admin.

    Args:
        current_user: Currently authenticated user

    Returns:
        User model if user is broker or admin

    Raises:
        HTTPException: If user is not a broker or admin
    """
    if current_user.user_type not in [UserType.BROKER, UserType.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Broker or admin access required",
        )
    return current_user


async def require_client_or_admin(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    """
    Require the current user to be a client or admin.

    Args:
        current_user: Currently authenticated user

    Returns:
        User model if user is client or admin

    Raises:
        HTTPException: If user is not a client or admin
    """
    if current_user.user_type not in [UserType.CLIENT, UserType.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client or admin access required",
        )
    return current_user
