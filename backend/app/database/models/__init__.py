from .base import Base, TimestampedModel, SoftDeleteModel
from .user import User, UserType
from .broker import Broker, Specialization, LicenseStatus, ExperienceLevel
from .quiz import Quiz, QuizQuestion, UserQuizResponse, QuestionType, QuizCategory
from .response import BrokerClientMatch, BrokerReview, MatchStatus
from .financial import (
    Payment,
    BankingConnection,
    PaymentStatus,
    PaymentType,
    BankingConnectionType,
)
from .analytics import UserActivity, SearchQuery, MatchMetrics

# This allows importing all models from: from app.database.models import User, Broker, etc.
__all__ = [
    "Base",
    "TimestampedModel",
    "SoftDeleteModel",
    "User",
    "UserType",
    "Broker",
    "Specialization",
    "LicenseStatus",
    "ExperienceLevel",
    "Quiz",
    "QuizQuestion",
    "UserQuizResponse",
    "QuestionType",
    "QuizCategory",
    "BrokerClientMatch",
    "BrokerReview",
    "MatchStatus",
    "Payment",
    "BankingConnection",
    "PaymentStatus",
    "PaymentType",
    "BankingConnectionType",
    "UserActivity",
    "SearchQuery",
    "MatchMetrics",
]
