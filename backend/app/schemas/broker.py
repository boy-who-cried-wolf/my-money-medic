from typing import List, Optional, Any, Dict
from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from uuid import UUID


class SpecializationBase(BaseModel):
    """Base schema for specialization data"""

    name: str
    description: Optional[str] = None


class SpecializationCreate(SpecializationBase):
    """Schema for creating a specialization"""

    pass


class SpecializationResponse(SpecializationBase):
    """Schema for specialization response"""

    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BrokerBase(BaseModel):
    """Base schema for broker data"""

    license_number: str
    license_status: str = "pending"
    company_name: Optional[str] = None
    years_of_experience: int
    experience_level: str
    office_address: Optional[str] = None
    service_areas: Optional[List[str]] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    website: Optional[str] = None


class BrokerCreate(BrokerBase):
    """Schema for creating a broker"""

    user_id: UUID
    specialization_ids: Optional[List[UUID]] = None


class BrokerUpdate(BaseModel):
    """Schema for updating broker data"""

    license_status: Optional[str] = None
    company_name: Optional[str] = None
    years_of_experience: Optional[int] = None
    experience_level: Optional[str] = None
    office_address: Optional[str] = None
    service_areas: Optional[List[str]] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    website: Optional[str] = None
    is_verified: Optional[bool] = None

    @field_validator("years_of_experience")
    @classmethod
    def validate_experience(cls, v):
        if v is not None and v < 0:
            raise ValueError("Years of experience cannot be negative")
        return v


class BrokerResponse(BrokerBase):
    """Schema for broker response"""

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    average_rating: float
    success_rate: float
    is_verified: bool
    specializations: List[SpecializationResponse]

    model_config = ConfigDict(from_attributes=True)


class BrokerDetailResponse(BrokerResponse):
    """Schema for detailed broker response with reviews"""

    reviews_count: int
    recent_reviews: List[Dict[str, Any]]


class BrokerSearchParams(BaseModel):
    """Schema for broker search parameters"""

    experience_level: Optional[str] = None
    specializations: Optional[List[str]] = None
    min_rating: Optional[float] = None
    years_of_experience: Optional[int] = None
    location: Optional[str] = None
    service_areas: Optional[List[str]] = None
    is_verified: Optional[bool] = None
    keyword: Optional[str] = None
