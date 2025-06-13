"""User related schemas."""

from typing import Annotated, Optional
from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
    StringConstraints,
    ConfigDict,
    Field,
)
import re
from datetime import datetime
from uuid import UUID


class UserRegister(BaseModel):
    # User email, automatically validated by EmailStr
    email: EmailStr
    # Password with minimum 8 characters
    password: Annotated[str, StringConstraints(min_length=8)]
    # First name between 2-50 characters
    first_name: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    # Last name between 2-50 characters
    last_name: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    # Phone number in international or local format
    phone: str

    @field_validator("password")
    @classmethod
    def password_validation(cls, v):
        """
        Validate password complexity:
        - At least 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        - At least one special character (@$!%*?&)
        """
        if not re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", v
        ):
            raise ValueError(
                "Password must contain at least 8 characters, "
                "one uppercase letter, one lowercase letter, "
                "one number and one special character"
            )
        return v

    @field_validator("phone")
    @classmethod
    def phone_validation(cls, v):
        """
        Validate phone number format:
        - International format: +1234567890
        - Local format: 1234567890
        - Formatted: 123-456-7890
        Returns: Cleaned number (digits only)
        """
        # Pattern to match international or local formats
        phone_pattern = re.compile(r"^\+?\d{10,12}$|^\d{3}-\d{3}-\d{4}$")
        if not phone_pattern.match(v):
            raise ValueError(
                "Phone number must be in format: +1234567890, 1234567890, or 123-456-7890"
            )
        # Remove any non-digit characters
        return re.sub(r"\D", "", v)

    @field_validator("first_name", "last_name")
    @classmethod
    def name_validation(cls, v):
        """
        Validate name format:
        - Must start with a letter
        - Can contain letters, spaces, hyphens, and apostrophes
        - Auto-capitalizes first letter of each word
        """
        if not re.match(r"^[A-Za-z][A-Za-z\s\-\']+$", v):
            raise ValueError(
                "Name must start with a letter and contain only letters, "
                "spaces, hyphens, and apostrophes"
            )
        return " ".join(word.capitalize() for word in v.split())


class UserLogin(BaseModel):
    # User email for login
    email: EmailStr
    # User password for login
    password: str


class UserBase(BaseModel):
    """Base schema for user data."""

    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    """Schema for creating a new user."""

    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8)]
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = None
    user_type: str = Field(..., description="Type of user (e.g., 'client', 'broker')")

    @field_validator("password")
    @classmethod
    def password_validation(cls, v):
        """
        Validate password complexity:
        - At least 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        - At least one special character (@$!%*?&)
        """
        if not re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", v
        ):
            raise ValueError(
                "Password must contain at least 8 characters, "
                "one uppercase letter, one lowercase letter, "
                "one number and one special character"
            )
        return v


class UserUpdate(UserBase):
    """Schema for updating an existing user."""

    password: Optional[str] = None
    phone: Optional[str] = None
    profile_image: Optional[str] = None

    @field_validator("first_name", "last_name")
    def name_must_be_valid(cls, v):
        if v and len(v.strip()) == 0:
            raise ValueError("Empty string is not a valid name")
        return v


class UserResponse(UserBase):
    """Schema for user response"""

    id: UUID
    created_at: datetime
    updated_at: datetime
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    """Schema for user data returned from API."""

    id: str
    phone: Optional[str] = None
    profile_image: Optional[str] = None
    user_type: str = Field(..., description="Type of user (e.g., 'client', 'broker')")

    # Configuration for Pydantic v2
    model_config = ConfigDict(from_attributes=True)


class UserInDB(User):
    """Schema for user data stored in the database."""

    hashed_password: str
