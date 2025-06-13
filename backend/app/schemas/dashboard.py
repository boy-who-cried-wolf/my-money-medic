from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

from app.database.models.response import MatchStatus
from app.database.models.user import UserType
from app.database.models.broker import LicenseStatus, ExperienceLevel


# Enums for request parameters
class TimePeriod(str, Enum):
    WEEK = "7"
    MONTH = "30"
    QUARTER = "90"
    YEAR = "365"


class AlertType(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


# Base models
class PaginationParams(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)


class DateRangeParams(BaseModel):
    days: int = Field(default=30, ge=1, le=365)


# Broker Dashboard Schemas
class BrokerProfileInfo(BaseModel):
    license_number: str
    license_status: str
    company_name: Optional[str]
    years_of_experience: int
    experience_level: str
    is_verified: bool
    is_active: bool


class BrokerStatistics(BaseModel):
    total_matches: int
    pending_matches: int
    accepted_matches: int
    completed_matches: int
    success_rate: float
    recent_matches_30d: int


class BrokerReviewStats(BaseModel):
    total_reviews: int
    average_rating: float
    positive_reviews: int


class BrokerOverviewResponse(BaseModel):
    broker_id: str
    profile: BrokerProfileInfo
    statistics: BrokerStatistics
    reviews: BrokerReviewStats


class ClientInfo(BaseModel):
    id: str
    name: str
    email: str
    phone_number: Optional[str]


class MatchInfo(BaseModel):
    match_id: str
    client: ClientInfo
    status: str
    match_score: float
    matched_at: datetime
    responded_at: Optional[datetime]
    completed_at: Optional[datetime]
    notes: Optional[str]


class BrokerMatchesResponse(BaseModel):
    total: int
    matches: List[MatchInfo]
    pagination: Dict[str, Any]


class ResponseTimeMetrics(BaseModel):
    average_seconds: int
    minimum_seconds: int
    maximum_seconds: int


class CompletionTimeMetrics(BaseModel):
    average_days: int
    minimum_days: int
    maximum_days: int


class DailyTrend(BaseModel):
    date: str
    matches: int


class StatusDistribution(BaseModel):
    status: str
    count: int


class BrokerPerformanceResponse(BaseModel):
    period_days: int
    response_times: ResponseTimeMetrics
    completion_times: CompletionTimeMetrics
    daily_trends: List[DailyTrend]
    status_distribution: List[StatusDistribution]


class UpdateMatchStatusRequest(BaseModel):
    status: MatchStatus
    notes: Optional[str] = None


class UpdateMatchStatusResponse(BaseModel):
    match_id: str
    old_status: str
    new_status: str
    updated_at: datetime


class RatingDistribution(BaseModel):
    rating: int
    count: int


class ReviewInfo(BaseModel):
    review_id: str
    client_name: str
    rating: int
    review_text: Optional[str]
    is_verified: bool
    created_at: datetime


class BrokerReviewsResponse(BaseModel):
    total: int
    reviews: List[ReviewInfo]
    rating_distribution: List[RatingDistribution]
    pagination: Dict[str, Any]


class QuizInsight(BaseModel):
    question_text: str
    response_value: str
    created_at: datetime


class ActivityInfo(BaseModel):
    activity_type: str
    created_at: datetime
    metadata: Optional[Dict[str, Any]]


class ClientInsightsResponse(BaseModel):
    client: ClientInfo
    match_details: Dict[str, Any]
    quiz_insights: Dict[str, Any]
    recent_activity: List[ActivityInfo]


# Admin Dashboard Schemas
class UserStats(BaseModel):
    total: int
    clients: int
    brokers: int
    admins: int
    new_users_7d: int


class BrokerStats(BaseModel):
    total: int
    active: int
    verified: int
    verification_rate: float


class MatchStats(BaseModel):
    total: int
    successful: int
    success_rate: float
    new_matches_7d: int


class SystemOverviewResponse(BaseModel):
    users: UserStats
    brokers: BrokerStats
    matches: MatchStats
    last_updated: datetime


class UserTrend(BaseModel):
    date: str
    count: int
    user_type: str


class UserTypeDistribution(BaseModel):
    user_type: str
    count: int


class VerificationStat(BaseModel):
    verified: bool
    count: int


class ActiveUser(BaseModel):
    user_id: str
    name: str
    email: str
    user_type: str
    activity_count: int


class UserAnalyticsResponse(BaseModel):
    period_days: int
    daily_trends: List[UserTrend]
    user_type_distribution: List[UserTypeDistribution]
    verification_stats: List[VerificationStat]
    most_active_users: List[ActiveUser]


class LicenseDistribution(BaseModel):
    status: str
    count: int


class ExperienceDistribution(BaseModel):
    level: str
    count: int


class TopBroker(BaseModel):
    broker_id: str
    license_number: str
    company_name: Optional[str]
    total_matches: int
    completed_matches: int
    success_rate: float
    average_rating: float
    review_count: int
    is_verified: bool
    is_active: bool


class BrokerAnalyticsResponse(BaseModel):
    period_days: int
    license_distribution: List[LicenseDistribution]
    experience_distribution: List[ExperienceDistribution]
    top_performing_brokers: List[TopBroker]


class MatchingDailyTrend(BaseModel):
    date: str
    total_matches: int
    accepted: int
    completed: int
    acceptance_rate: float


class ScoreDistribution(BaseModel):
    range: str
    count: int


class PerformanceMetrics(BaseModel):
    average_response_time_seconds: int
    average_completion_time_days: int


class MatchingAnalyticsResponse(BaseModel):
    period_days: int
    status_distribution: List[StatusDistribution]
    daily_trends: List[MatchingDailyTrend]
    score_distribution: List[ScoreDistribution]
    performance_metrics: PerformanceMetrics


class QuizOverview(BaseModel):
    total_responses: int
    unique_users: int
    avg_responses_per_user: float


class PopularQuestion(BaseModel):
    question: str
    response_count: int


class QuizDailyActivity(BaseModel):
    date: str
    responses: int
    unique_users: int


class CompletionDistribution(BaseModel):
    level: str
    user_count: int


class QuizAnalyticsResponse(BaseModel):
    period_days: int
    overview: QuizOverview
    popular_questions: List[PopularQuestion]
    daily_activity: List[QuizDailyActivity]
    completion_distribution: List[CompletionDistribution]


class ActivityIndicators(BaseModel):
    recent_logins_1h: int
    recent_matches_24h: int
    pending_verifications: int
    inactive_brokers: int


class DatabaseHealth(BaseModel):
    total_records: Dict[str, int]
    status: str


class Alert(BaseModel):
    type: AlertType
    message: str
    action_required: bool


class PlatformHealthResponse(BaseModel):
    timestamp: datetime
    activity_indicators: ActivityIndicators
    database_health: DatabaseHealth
    alerts: List[Alert]
    overall_status: str


class RevenueMetrics(BaseModel):
    total: float
    subscription_revenue: float
    commission_revenue: float
    growth_rate: float


class CostMetrics(BaseModel):
    platform_costs: float
    broker_payouts: float
    operating_expenses: float


class KeyMetrics(BaseModel):
    average_deal_value: float
    customer_lifetime_value: float
    broker_retention_rate: float


class FinancialMetricsResponse(BaseModel):
    period_days: int
    revenue: RevenueMetrics
    costs: CostMetrics
    key_metrics: KeyMetrics


# Request models for filters
class BrokerMatchesRequest(BaseModel):
    status: Optional[MatchStatus] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)


class UserAnalyticsRequest(BaseModel):
    days: int = Field(default=30, ge=1, le=365)
    user_type: Optional[UserType] = None


class BrokerAnalyticsRequest(BaseModel):
    days: int = Field(default=30, ge=1, le=365)


class MatchingAnalyticsRequest(BaseModel):
    days: int = Field(default=30, ge=1, le=365)


class QuizAnalyticsRequest(BaseModel):
    days: int = Field(default=30, ge=1, le=365)


class FinancialMetricsRequest(BaseModel):
    days: int = Field(default=30, ge=1, le=365)
