from typing import List, Optional, Any, Dict, Union
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID


class QuizBase(BaseModel):
    """Base schema for quiz data"""

    title: str
    description: Optional[str] = None
    category: str


class QuizCreate(QuizBase):
    """Schema for creating a quiz"""

    pass


class QuizQuestionBase(BaseModel):
    """Base schema for quiz question data"""

    text: str
    question_type: Any
    options: Optional[Any] = None
    order: int
    weight: Optional[int] = 1
    is_ai_generated: Optional[bool] = False


class QuizQuestionCreate(QuizQuestionBase):
    """Schema for creating a quiz question"""

    pass


class QuizQuestionUpdate(QuizQuestionBase):
    text: Optional[str] = None
    question_type: Optional[Any] = None
    order: Optional[int] = None


class UserQuizResponseBase(BaseModel):
    """Base schema for user quiz response data"""

    user_id: UUID
    question_id: UUID
    response: Union[str, int, bool, List[str], Dict[str, Any]]


class UserQuizResponseCreate(UserQuizResponseBase):
    """Schema for creating a user quiz response"""

    pass


class QuizQuestionResponse(QuizQuestionBase):
    """Schema for quiz question response"""

    id: UUID
    quiz_id: UUID

    model_config = ConfigDict(from_attributes=True)


class QuizResponse(QuizBase):
    """Schema for quiz response"""

    id: UUID
    created_at: datetime
    questions: List[QuizQuestionResponse]

    model_config = ConfigDict(from_attributes=True)


class UserQuizResponseResponse(UserQuizResponseBase):
    """Schema for user quiz response"""

    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuizAnalyticsResponse(BaseModel):
    """Schema for quiz analytics data"""

    quiz_id: UUID
    title: str
    total_responses: int
    average_completion_time: Optional[float] = None
    completion_rate: float
    question_analytics: List[Dict[str, Any]]
