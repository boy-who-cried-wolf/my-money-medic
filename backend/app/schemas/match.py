from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID


class MatchBase(BaseModel):
    """Base schema for match data"""

    broker_id: str
    client_id: str
    match_score: float
    status: str
    notes: Optional[str] = None


class MatchCreate(MatchBase):
    """Schema for creating a match"""

    matched_by: Optional[str] = None


class MatchUpdate(BaseModel):
    """Schema for updating a match"""

    status: Optional[str] = None
    match_score: Optional[float] = None
    notes: Optional[str] = None


class MatchFilterParams(BaseModel):
    """Schema for filtering matches"""

    broker_id: Optional[str] = None
    client_id: Optional[str] = None
    status: Optional[str] = None
    min_score: Optional[float] = None
    max_score: Optional[float] = None


class MatchAlgorithmParams(BaseModel):
    """Schema for match algorithm parameters"""

    user_id: str
    min_match_score: float = 0.5
    max_matches: int = 10


class BrokerClientMatchCreate(MatchBase):
    """Schema for creating a broker-client match"""

    pass


class BrokerClientMatchUpdate(BaseModel):
    """Schema for updating a broker-client match"""

    status: Optional[str] = None
    match_score: Optional[float] = None
    notes: Optional[str] = None
    responded_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class BrokerClientMatchResponse(MatchBase):
    """Schema for broker-client match response"""

    id: UUID
    created_at: datetime
    matched_at: Optional[datetime] = None
    responded_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
