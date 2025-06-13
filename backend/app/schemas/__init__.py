"""Schema module for Pydantic models used in API."""

# Import all schemas for easier imports elsewhere
from .user import UserCreate, UserResponse, UserUpdate, UserLogin, UserRegister
from .broker import (
    BrokerCreate,
    BrokerResponse,
    BrokerUpdate,
    BrokerSearchParams,
    SpecializationCreate,
    SpecializationResponse,
)
from .quiz import (
    QuizCreate,
    QuizResponse,
    QuizQuestionCreate,
    QuizQuestionResponse,
    UserQuizResponseCreate,
    UserQuizResponseResponse,
)
from .match import (
    BrokerClientMatchCreate,
    BrokerClientMatchResponse,
    BrokerClientMatchUpdate,
    MatchAlgorithmParams,
)
from .payment import (
    PaymentCreate,
    PaymentResponse,
    BankingConnectionCreate,
    BankingConnectionResponse,
)
from .dashboard import (
    BrokerOverviewResponse,
    BrokerMatchesResponse,
    BrokerPerformanceResponse,
    UpdateMatchStatusRequest,
    UpdateMatchStatusResponse,
    BrokerReviewsResponse,
    ClientInsightsResponse,
    SystemOverviewResponse,
    UserAnalyticsResponse,
    BrokerAnalyticsResponse,
    MatchingAnalyticsResponse,
    QuizAnalyticsResponse,
    PlatformHealthResponse,
    FinancialMetricsResponse,
)
