"""Token related schemas."""

from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """Schema for access token."""
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema for token payload."""
    sub: Optional[str] = None 