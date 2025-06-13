from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, JSON, Text
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

from .base import SoftDeleteModel


class UserActivity(SoftDeleteModel):
    """
    Model for tracking user activity on the platform
    """

    __tablename__ = "user_activities"

    user_id = Column(ForeignKey("users.id"), nullable=False)
    activity_type = Column(
        String(100), nullable=False
    )  # e.g., login, profile_update, broker_search
    ip_address = Column(String(50))
    user_agent = Column(String(255))
    activity_metadata = Column(JSON, nullable=True)  # Additional activity data
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        """String representation of the user activity"""
        return f"<UserActivity {self.user_id} - {self.activity_type}>"


class SearchQuery(SoftDeleteModel):
    """
    Model for tracking user search queries
    """

    __tablename__ = "search_queries"

    user_id = Column(
        ForeignKey("users.id"), nullable=True
    )  # Can be null for anonymous users
    query_text = Column(Text, nullable=False)
    filters = Column(JSON, nullable=True)  # Search filters
    result_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        """String representation of the search query"""
        return f"<SearchQuery {self.query_text[:20]}...>"


class MatchMetrics(SoftDeleteModel):
    """
    Model for tracking matching metrics
    """

    __tablename__ = "match_metrics"

    match_id = Column(ForeignKey("broker_client_matches.id"), nullable=False)
    response_time_seconds = Column(Integer, nullable=True)  # Time to respond to match
    time_to_completion_days = Column(Integer, nullable=True)  # Days to complete match
    user_satisfaction = Column(Integer, nullable=True)  # 1-5 rating
    broker_satisfaction = Column(Integer, nullable=True)  # 1-5 rating
    notes = Column(Text)

    def __repr__(self):
        """String representation of the match metrics"""
        return f"<MatchMetrics {self.match_id}>"
