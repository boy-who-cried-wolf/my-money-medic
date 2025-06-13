from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc, case
from datetime import datetime, timedelta
from uuid import UUID

from app.database.models.user import User, UserType
from app.database.models.broker import Broker, LicenseStatus
from app.database.models.response import BrokerClientMatch, MatchStatus, BrokerReview
from app.database.models.quiz import UserQuizResponse
from app.database.models.analytics import UserActivity, MatchMetrics


class BrokerDashboardService:
    """Service for broker dashboard functionality and metrics"""

    @staticmethod
    def get_broker_overview(db: Session, broker_id: str) -> Dict[str, Any]:
        """Get comprehensive broker overview statistics"""
        broker = db.query(Broker).filter(Broker.id == broker_id).first()
        if not broker:
            raise ValueError("Broker not found")

        # Basic stats
        total_matches = (
            db.query(BrokerClientMatch)
            .filter(
                BrokerClientMatch.broker_id == broker_id,
                BrokerClientMatch.is_deleted == False,
            )
            .count()
        )

        pending_matches = (
            db.query(BrokerClientMatch)
            .filter(
                BrokerClientMatch.broker_id == broker_id,
                BrokerClientMatch.status == MatchStatus.PENDING,
                BrokerClientMatch.is_deleted == False,
            )
            .count()
        )

        accepted_matches = (
            db.query(BrokerClientMatch)
            .filter(
                BrokerClientMatch.broker_id == broker_id,
                BrokerClientMatch.status == MatchStatus.ACCEPTED,
                BrokerClientMatch.is_deleted == False,
            )
            .count()
        )

        completed_matches = (
            db.query(BrokerClientMatch)
            .filter(
                BrokerClientMatch.broker_id == broker_id,
                BrokerClientMatch.status == MatchStatus.COMPLETED,
                BrokerClientMatch.is_deleted == False,
            )
            .count()
        )

        # Reviews stats
        reviews_data = (
            db.query(
                func.count(BrokerReview.id).label("total_reviews"),
                func.avg(BrokerReview.rating).label("avg_rating"),
                func.count(case([(BrokerReview.rating >= 4, 1)])).label(
                    "positive_reviews"
                ),
            )
            .filter(
                BrokerReview.broker_id == broker_id, BrokerReview.is_deleted == False
            )
            .first()
        )

        # Calculate success rate
        success_rate = 0.0
        if total_matches > 0:
            success_rate = (completed_matches / total_matches) * 100

        # Recent activity (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_matches = (
            db.query(BrokerClientMatch)
            .filter(
                BrokerClientMatch.broker_id == broker_id,
                BrokerClientMatch.matched_at >= thirty_days_ago,
                BrokerClientMatch.is_deleted == False,
            )
            .count()
        )

        return {
            "broker_id": broker_id,
            "profile": {
                "license_number": broker.license_number,
                "license_status": broker.license_status.value,
                "company_name": broker.company_name,
                "years_of_experience": broker.years_of_experience,
                "experience_level": broker.experience_level.value,
                "is_verified": broker.is_verified,
                "is_active": broker.is_active,
            },
            "statistics": {
                "total_matches": total_matches,
                "pending_matches": pending_matches,
                "accepted_matches": accepted_matches,
                "completed_matches": completed_matches,
                "success_rate": round(success_rate, 2),
                "recent_matches_30d": recent_matches,
            },
            "reviews": {
                "total_reviews": reviews_data.total_reviews or 0,
                "average_rating": round(float(reviews_data.avg_rating or 0), 2),
                "positive_reviews": reviews_data.positive_reviews or 0,
            },
        }

    @staticmethod
    def get_broker_matches(
        db: Session,
        broker_id: str,
        status: Optional[MatchStatus] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Dict[str, Any]:
        """Get broker's matches with filtering and pagination"""
        query = (
            db.query(BrokerClientMatch)
            .join(User)
            .filter(
                BrokerClientMatch.broker_id == broker_id,
                BrokerClientMatch.is_deleted == False,
            )
        )

        if status:
            query = query.filter(BrokerClientMatch.status == status)

        total = query.count()
        matches = (
            query.order_by(desc(BrokerClientMatch.matched_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

        matches_data = []
        for match in matches:
            user = match.user
            matches_data.append(
                {
                    "match_id": str(match.id),
                    "client": {
                        "id": str(user.id),
                        "name": user.full_name,
                        "email": user.email,
                        "phone_number": user.phone_number,
                    },
                    "status": match.status.value,
                    "match_score": match.match_score,
                    "matched_at": match.matched_at.isoformat(),
                    "responded_at": (
                        match.responded_at.isoformat() if match.responded_at else None
                    ),
                    "completed_at": (
                        match.completed_at.isoformat() if match.completed_at else None
                    ),
                    "notes": match.notes,
                }
            )

        return {
            "total": total,
            "matches": matches_data,
            "pagination": {
                "skip": skip,
                "limit": limit,
                "has_more": skip + limit < total,
            },
        }

    @staticmethod
    def get_broker_performance_metrics(
        db: Session, broker_id: str, days: int = 30
    ) -> Dict[str, Any]:
        """Get detailed performance metrics for broker"""
        start_date = datetime.utcnow() - timedelta(days=days)

        # Response time metrics
        response_metrics = (
            db.query(
                func.avg(MatchMetrics.response_time_seconds).label("avg_response_time"),
                func.min(MatchMetrics.response_time_seconds).label("min_response_time"),
                func.max(MatchMetrics.response_time_seconds).label("max_response_time"),
            )
            .join(BrokerClientMatch)
            .filter(
                BrokerClientMatch.broker_id == broker_id,
                BrokerClientMatch.matched_at >= start_date,
                MatchMetrics.response_time_seconds.isnot(None),
            )
            .first()
        )

        # Completion time metrics
        completion_metrics = (
            db.query(
                func.avg(MatchMetrics.time_to_completion_days).label(
                    "avg_completion_time"
                ),
                func.min(MatchMetrics.time_to_completion_days).label(
                    "min_completion_time"
                ),
                func.max(MatchMetrics.time_to_completion_days).label(
                    "max_completion_time"
                ),
            )
            .join(BrokerClientMatch)
            .filter(
                BrokerClientMatch.broker_id == broker_id,
                BrokerClientMatch.matched_at >= start_date,
                MatchMetrics.time_to_completion_days.isnot(None),
            )
            .first()
        )

        # Daily match trends
        daily_matches = (
            db.query(
                func.date(BrokerClientMatch.matched_at).label("date"),
                func.count(BrokerClientMatch.id).label("count"),
            )
            .filter(
                BrokerClientMatch.broker_id == broker_id,
                BrokerClientMatch.matched_at >= start_date,
                BrokerClientMatch.is_deleted == False,
            )
            .group_by(func.date(BrokerClientMatch.matched_at))
            .all()
        )

        # Status distribution
        status_distribution = (
            db.query(
                BrokerClientMatch.status,
                func.count(BrokerClientMatch.id).label("count"),
            )
            .filter(
                BrokerClientMatch.broker_id == broker_id,
                BrokerClientMatch.matched_at >= start_date,
                BrokerClientMatch.is_deleted == False,
            )
            .group_by(BrokerClientMatch.status)
            .all()
        )

        return {
            "period_days": days,
            "response_times": {
                "average_seconds": int(response_metrics.avg_response_time or 0),
                "minimum_seconds": int(response_metrics.min_response_time or 0),
                "maximum_seconds": int(response_metrics.max_response_time or 0),
            },
            "completion_times": {
                "average_days": int(completion_metrics.avg_completion_time or 0),
                "minimum_days": int(completion_metrics.min_completion_time or 0),
                "maximum_days": int(completion_metrics.max_completion_time or 0),
            },
            "daily_trends": [
                {"date": trend.date.isoformat(), "matches": trend.count}
                for trend in daily_matches
            ],
            "status_distribution": [
                {"status": status.status.value, "count": status.count}
                for status in status_distribution
            ],
        }

    @staticmethod
    def update_match_status(
        db: Session,
        broker_id: str,
        match_id: str,
        status: MatchStatus,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update match status with timestamp tracking"""
        match = (
            db.query(BrokerClientMatch)
            .filter(
                BrokerClientMatch.id == match_id,
                BrokerClientMatch.broker_id == broker_id,
                BrokerClientMatch.is_deleted == False,
            )
            .first()
        )

        if not match:
            raise ValueError("Match not found or unauthorized")

        old_status = match.status
        match.status = status

        # Update timestamps based on status
        now = datetime.utcnow()
        if (
            status in [MatchStatus.ACCEPTED, MatchStatus.REJECTED]
            and not match.responded_at
        ):
            match.responded_at = now
        elif status == MatchStatus.COMPLETED and not match.completed_at:
            match.completed_at = now

        if notes:
            match.notes = notes

        match.updated_at = now
        db.commit()
        db.refresh(match)

        return {
            "match_id": str(match.id),
            "old_status": old_status.value,
            "new_status": status.value,
            "updated_at": now.isoformat(),
        }

    @staticmethod
    def get_broker_reviews(
        db: Session, broker_id: str, skip: int = 0, limit: int = 20
    ) -> Dict[str, Any]:
        """Get broker reviews with pagination"""
        query = (
            db.query(BrokerReview)
            .join(User)
            .filter(
                BrokerReview.broker_id == broker_id, BrokerReview.is_deleted == False
            )
        )

        total = query.count()
        reviews = (
            query.order_by(desc(BrokerReview.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

        reviews_data = []
        for review in reviews:
            user = db.query(User).filter(User.id == review.user_id).first()
            reviews_data.append(
                {
                    "review_id": str(review.id),
                    "client_name": user.full_name if user else "Anonymous",
                    "rating": review.rating,
                    "review_text": review.review_text,
                    "is_verified": review.is_verified,
                    "created_at": review.created_at.isoformat(),
                }
            )

        # Rating distribution
        rating_distribution = (
            db.query(BrokerReview.rating, func.count(BrokerReview.id).label("count"))
            .filter(
                BrokerReview.broker_id == broker_id, BrokerReview.is_deleted == False
            )
            .group_by(BrokerReview.rating)
            .all()
        )

        return {
            "total": total,
            "reviews": reviews_data,
            "rating_distribution": [
                {"rating": dist.rating, "count": dist.count}
                for dist in rating_distribution
            ],
            "pagination": {
                "skip": skip,
                "limit": limit,
                "has_more": skip + limit < total,
            },
        }

    @staticmethod
    def get_client_insights(
        db: Session, broker_id: str, client_id: str
    ) -> Dict[str, Any]:
        """Get detailed insights about a specific client for the broker"""
        # Verify the broker-client relationship
        match = (
            db.query(BrokerClientMatch)
            .filter(
                BrokerClientMatch.broker_id == broker_id,
                BrokerClientMatch.user_id == client_id,
                BrokerClientMatch.is_deleted == False,
            )
            .first()
        )

        if not match:
            raise ValueError("No active match between broker and client")

        client = db.query(User).filter(User.id == client_id).first()
        if not client:
            raise ValueError("Client not found")

        # Get client's quiz responses for insights
        quiz_responses = (
            db.query(UserQuizResponse)
            .filter(
                UserQuizResponse.user_id == client_id,
                UserQuizResponse.is_deleted == False,
            )
            .all()
        )

        # Get client activity
        activities = (
            db.query(UserActivity)
            .filter(UserActivity.user_id == client_id)
            .order_by(desc(UserActivity.created_at))
            .limit(10)
            .all()
        )

        return {
            "client": {
                "id": str(client.id),
                "name": client.full_name,
                "email": client.email,
                "phone_number": client.phone_number,
                "is_verified": client.is_verified,
            },
            "match_details": {
                "match_score": match.match_score,
                "status": match.status.value,
                "matched_at": match.matched_at.isoformat(),
                "responded_at": (
                    match.responded_at.isoformat() if match.responded_at else None
                ),
                "notes": match.notes,
            },
            "quiz_insights": {
                "total_responses": len(quiz_responses),
                "recent_responses": [
                    {
                        "question_text": (
                            resp.question.text
                            if resp.question
                            else "Question not found"
                        ),
                        "response_value": str(resp.response),
                        "created_at": resp.created_at.isoformat(),
                    }
                    for resp in quiz_responses[-5:]  # Last 5 responses
                ],
            },
            "recent_activity": [
                {
                    "activity_type": activity.activity_type,
                    "created_at": activity.created_at.isoformat(),
                    "metadata": activity.activity_metadata,
                }
                for activity in activities
            ],
        }
