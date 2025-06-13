from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc, case, extract
from datetime import datetime, timedelta
from uuid import UUID

from app.database.models.user import User, UserType
from app.database.models.broker import Broker, LicenseStatus, ExperienceLevel
from app.database.models.response import BrokerClientMatch, MatchStatus, BrokerReview
from app.database.models.quiz import UserQuizResponse, QuizQuestion, Quiz
from app.database.models.analytics import UserActivity, MatchMetrics, SearchQuery


class AdminDashboardService:
    """Service for admin dashboard functionality and system metrics"""

    @staticmethod
    def get_system_overview(db: Session) -> Dict[str, Any]:
        """Get comprehensive system overview with key metrics"""
        # User statistics
        total_users = db.query(User).filter(User.is_deleted == False).count()
        clients = (
            db.query(User)
            .filter(User.user_type == UserType.CLIENT, User.is_deleted == False)
            .count()
        )
        brokers = (
            db.query(User)
            .filter(User.user_type == UserType.BROKER, User.is_deleted == False)
            .count()
        )
        admins = (
            db.query(User)
            .filter(User.user_type == UserType.ADMIN, User.is_deleted == False)
            .count()
        )

        # Broker statistics
        active_brokers = (
            db.query(Broker)
            .filter(Broker.is_active == True, Broker.is_deleted == False)
            .count()
        )
        verified_brokers = (
            db.query(Broker)
            .filter(Broker.is_verified == True, Broker.is_deleted == False)
            .count()
        )

        # Match statistics
        total_matches = (
            db.query(BrokerClientMatch)
            .filter(BrokerClientMatch.is_deleted == False)
            .count()
        )
        successful_matches = (
            db.query(BrokerClientMatch)
            .filter(
                BrokerClientMatch.status == MatchStatus.COMPLETED,
                BrokerClientMatch.is_deleted == False,
            )
            .count()
        )

        # Recent activity (last 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        new_users_7d = (
            db.query(User)
            .filter(User.created_at >= seven_days_ago, User.is_deleted == False)
            .count()
        )
        new_matches_7d = (
            db.query(BrokerClientMatch)
            .filter(
                BrokerClientMatch.matched_at >= seven_days_ago,
                BrokerClientMatch.is_deleted == False,
            )
            .count()
        )

        # Calculate success rate
        success_rate = 0.0
        if total_matches > 0:
            success_rate = (successful_matches / total_matches) * 100

        return {
            "users": {
                "total": total_users,
                "clients": clients,
                "brokers": brokers,
                "admins": admins,
                "new_users_7d": new_users_7d,
            },
            "brokers": {
                "total": brokers,
                "active": active_brokers,
                "verified": verified_brokers,
                "verification_rate": round(
                    (verified_brokers / brokers * 100) if brokers > 0 else 0, 2
                ),
            },
            "matches": {
                "total": total_matches,
                "successful": successful_matches,
                "success_rate": round(success_rate, 2),
                "new_matches_7d": new_matches_7d,
            },
            "last_updated": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def get_user_analytics(
        db: Session, days: int = 30, user_type: Optional[UserType] = None
    ) -> Dict[str, Any]:
        """Get detailed user analytics and trends"""
        start_date = datetime.utcnow() - timedelta(days=days)

        # Base query
        base_query = db.query(User).filter(
            User.created_at >= start_date, User.is_deleted == False
        )

        if user_type:
            base_query = base_query.filter(User.user_type == user_type)

        # Daily registration trends
        daily_registrations = (
            db.query(
                func.date(User.created_at).label("date"),
                func.count(User.id).label("count"),
                User.user_type,
            )
            .filter(User.created_at >= start_date, User.is_deleted == False)
            .group_by(func.date(User.created_at), User.user_type)
            .all()
        )

        # User type distribution
        user_type_dist = (
            db.query(User.user_type, func.count(User.id).label("count"))
            .filter(User.is_deleted == False)
            .group_by(User.user_type)
            .all()
        )

        # Verification status
        verification_stats = (
            db.query(User.is_verified, func.count(User.id).label("count"))
            .filter(User.is_deleted == False)
            .group_by(User.is_verified)
            .all()
        )

        # Most active users (by activity count)
        active_users = (
            db.query(User, func.count(UserActivity.id).label("activity_count"))
            .join(UserActivity)
            .filter(UserActivity.created_at >= start_date, User.is_deleted == False)
            .group_by(User.id)
            .order_by(desc(func.count(UserActivity.id)))
            .limit(10)
            .all()
        )

        return {
            "period_days": days,
            "daily_trends": [
                {
                    "date": reg.date.isoformat(),
                    "count": reg.count,
                    "user_type": reg.user_type.value,
                }
                for reg in daily_registrations
            ],
            "user_type_distribution": [
                {"user_type": dist.user_type.value, "count": dist.count}
                for dist in user_type_dist
            ],
            "verification_stats": [
                {"verified": dist.is_verified, "count": dist.count}
                for dist in verification_stats
            ],
            "most_active_users": [
                {
                    "user_id": str(user.User.id),
                    "name": user.User.full_name,
                    "email": user.User.email,
                    "user_type": user.User.user_type.value,
                    "activity_count": user.activity_count,
                }
                for user in active_users
            ],
        }

    @staticmethod
    def get_broker_analytics(db: Session, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive broker analytics"""
        start_date = datetime.utcnow() - timedelta(days=days)

        # Broker performance metrics
        broker_performance = (
            db.query(
                Broker,
                func.count(BrokerClientMatch.id).label("total_matches"),
                func.count(
                    case((BrokerClientMatch.status == MatchStatus.COMPLETED, 1))
                ).label("completed_matches"),
                func.avg(BrokerReview.rating).label("avg_rating"),
                func.count(BrokerReview.id).label("review_count"),
            )
            .outerjoin(BrokerClientMatch)
            .outerjoin(BrokerReview)
            .filter(Broker.is_deleted == False)
            .group_by(Broker.id)
            .all()
        )

        # License status distribution
        license_dist = (
            db.query(Broker.license_status, func.count(Broker.id).label("count"))
            .filter(Broker.is_deleted == False)
            .group_by(Broker.license_status)
            .all()
        )

        # Experience level distribution
        experience_dist = (
            db.query(Broker.experience_level, func.count(Broker.id).label("count"))
            .filter(Broker.is_deleted == False)
            .group_by(Broker.experience_level)
            .all()
        )

        # Top performing brokers
        top_brokers = [
            {
                "broker_id": str(perf.Broker.id),
                "license_number": perf.Broker.license_number,
                "company_name": perf.Broker.company_name,
                "total_matches": perf.total_matches or 0,
                "completed_matches": perf.completed_matches or 0,
                "success_rate": round(
                    (
                        (perf.completed_matches / perf.total_matches * 100)
                        if perf.total_matches
                        else 0
                    ),
                    2,
                ),
                "average_rating": round(float(perf.avg_rating or 0), 2),
                "review_count": perf.review_count or 0,
                "is_verified": perf.Broker.is_verified,
                "is_active": perf.Broker.is_active,
            }
            for perf in sorted(
                broker_performance,
                key=lambda x: (x.completed_matches or 0),
                reverse=True,
            )[:10]
        ]

        return {
            "period_days": days,
            "license_distribution": [
                {"status": dist.license_status.value, "count": dist.count}
                for dist in license_dist
            ],
            "experience_distribution": [
                {"level": dist.experience_level.value, "count": dist.count}
                for dist in experience_dist
            ],
            "top_performing_brokers": top_brokers,
        }

    @staticmethod
    def get_matching_analytics(db: Session, days: int = 30) -> Dict[str, Any]:
        """Get detailed matching system analytics"""
        start_date = datetime.utcnow() - timedelta(days=days)

        # Match status distribution
        status_dist = (
            db.query(
                BrokerClientMatch.status,
                func.count(BrokerClientMatch.id).label("count"),
            )
            .filter(
                BrokerClientMatch.matched_at >= start_date,
                BrokerClientMatch.is_deleted == False,
            )
            .group_by(BrokerClientMatch.status)
            .all()
        )

        # Daily matching trends
        daily_matches = (
            db.query(
                func.date(BrokerClientMatch.matched_at).label("date"),
                func.count(BrokerClientMatch.id).label("total_matches"),
                func.count(
                    case((BrokerClientMatch.status == MatchStatus.ACCEPTED, 1))
                ).label("accepted"),
                func.count(
                    case((BrokerClientMatch.status == MatchStatus.COMPLETED, 1))
                ).label("completed"),
            )
            .filter(
                BrokerClientMatch.matched_at >= start_date,
                BrokerClientMatch.is_deleted == False,
            )
            .group_by(func.date(BrokerClientMatch.matched_at))
            .all()
        )

        # Match score distribution
        score_ranges = (
            db.query(
                case(
                    (BrokerClientMatch.match_score >= 90, "90-100"),
                    (BrokerClientMatch.match_score >= 80, "80-89"),
                    (BrokerClientMatch.match_score >= 70, "70-79"),
                    (BrokerClientMatch.match_score >= 60, "60-69"),
                    (BrokerClientMatch.match_score < 60, "Below 60"),
                ).label("score_range"),
                func.count(BrokerClientMatch.id).label("count"),
            )
            .filter(
                BrokerClientMatch.matched_at >= start_date,
                BrokerClientMatch.is_deleted == False,
            )
            .group_by(
                case(
                    (BrokerClientMatch.match_score >= 90, "90-100"),
                    (BrokerClientMatch.match_score >= 80, "80-89"),
                    (BrokerClientMatch.match_score >= 70, "70-79"),
                    (BrokerClientMatch.match_score >= 60, "60-69"),
                    (BrokerClientMatch.match_score < 60, "Below 60"),
                )
            )
            .all()
        )

        # Performance metrics
        avg_response_time = (
            db.query(func.avg(MatchMetrics.response_time_seconds))
            .join(BrokerClientMatch)
            .filter(
                BrokerClientMatch.matched_at >= start_date,
                MatchMetrics.response_time_seconds.isnot(None),
            )
            .scalar()
        )

        avg_completion_time = (
            db.query(func.avg(MatchMetrics.time_to_completion_days))
            .join(BrokerClientMatch)
            .filter(
                BrokerClientMatch.matched_at >= start_date,
                MatchMetrics.time_to_completion_days.isnot(None),
            )
            .scalar()
        )

        return {
            "period_days": days,
            "status_distribution": [
                {"status": dist.status.value, "count": dist.count}
                for dist in status_dist
            ],
            "daily_trends": [
                {
                    "date": trend.date.isoformat(),
                    "total_matches": trend.total_matches,
                    "accepted": trend.accepted,
                    "completed": trend.completed,
                    "acceptance_rate": round(
                        (
                            (trend.accepted / trend.total_matches * 100)
                            if trend.total_matches
                            else 0
                        ),
                        2,
                    ),
                }
                for trend in daily_matches
            ],
            "score_distribution": [
                {"range": range_.score_range, "count": range_.count}
                for range_ in score_ranges
            ],
            "performance_metrics": {
                "average_response_time_seconds": int(avg_response_time or 0),
                "average_completion_time_days": int(avg_completion_time or 0),
            },
        }

    @staticmethod
    def get_quiz_analytics(db: Session, days: int = 30) -> Dict[str, Any]:
        """Get quiz and question analytics"""
        start_date = datetime.utcnow() - timedelta(days=days)

        # Quiz completion stats
        total_responses = (
            db.query(UserQuizResponse)
            .filter(
                UserQuizResponse.created_at >= start_date,
                UserQuizResponse.is_deleted == False,
            )
            .count()
        )

        unique_users = (
            db.query(func.count(func.distinct(UserQuizResponse.user_id)))
            .filter(
                UserQuizResponse.created_at >= start_date,
                UserQuizResponse.is_deleted == False,
            )
            .scalar()
        )

        # Most answered questions (need to join with QuizQuestion to get text)
        popular_questions = (
            db.query(
                QuizQuestion.text,
                func.count(UserQuizResponse.id).label("response_count"),
            )
            .join(UserQuizResponse)
            .filter(
                UserQuizResponse.created_at >= start_date,
                UserQuizResponse.is_deleted == False,
            )
            .group_by(QuizQuestion.text)
            .order_by(desc(func.count(UserQuizResponse.id)))
            .limit(10)
            .all()
        )

        # Daily quiz activity
        daily_activity = (
            db.query(
                func.date(UserQuizResponse.created_at).label("date"),
                func.count(UserQuizResponse.id).label("responses"),
                func.count(func.distinct(UserQuizResponse.user_id)).label(
                    "unique_users"
                ),
            )
            .filter(
                UserQuizResponse.created_at >= start_date,
                UserQuizResponse.is_deleted == False,
            )
            .group_by(func.date(UserQuizResponse.created_at))
            .all()
        )

        # User completion patterns
        user_response_counts = (
            db.query(
                UserQuizResponse.user_id,
                func.count(UserQuizResponse.id).label("response_count"),
            )
            .filter(
                UserQuizResponse.created_at >= start_date,
                UserQuizResponse.is_deleted == False,
            )
            .group_by(UserQuizResponse.user_id)
            .subquery()
        )

        completion_distribution = (
            db.query(
                case(
                    (user_response_counts.c.response_count >= 20, "20+ responses"),
                    (user_response_counts.c.response_count >= 10, "10-19 responses"),
                    (user_response_counts.c.response_count >= 5, "5-9 responses"),
                    (user_response_counts.c.response_count < 5, "1-4 responses"),
                ).label("completion_level"),
                func.count("*").label("user_count"),
            )
            .group_by(
                case(
                    (user_response_counts.c.response_count >= 20, "20+ responses"),
                    (user_response_counts.c.response_count >= 10, "10-19 responses"),
                    (user_response_counts.c.response_count >= 5, "5-9 responses"),
                    (user_response_counts.c.response_count < 5, "1-4 responses"),
                )
            )
            .all()
        )

        return {
            "period_days": days,
            "overview": {
                "total_responses": total_responses,
                "unique_users": unique_users,
                "avg_responses_per_user": round(
                    total_responses / unique_users if unique_users else 0, 2
                ),
            },
            "popular_questions": [
                {
                    "question": q.text[:100] + "..." if len(q.text) > 100 else q.text,
                    "response_count": q.response_count,
                }
                for q in popular_questions
            ],
            "daily_activity": [
                {
                    "date": activity.date.isoformat(),
                    "responses": activity.responses,
                    "unique_users": activity.unique_users,
                }
                for activity in daily_activity
            ],
            "completion_distribution": [
                {"level": dist.completion_level, "user_count": dist.user_count}
                for dist in completion_distribution
            ],
        }

    @staticmethod
    def get_platform_health(db: Session) -> Dict[str, Any]:
        """Get platform health metrics and alerts"""
        now = datetime.utcnow()
        one_hour_ago = now - timedelta(hours=1)
        one_day_ago = now - timedelta(days=1)

        # System activity indicators
        recent_logins = (
            db.query(UserActivity)
            .filter(
                UserActivity.activity_type == "login",
                UserActivity.created_at >= one_hour_ago,
            )
            .count()
        )

        recent_matches = (
            db.query(BrokerClientMatch)
            .filter(
                BrokerClientMatch.matched_at >= one_day_ago,
                BrokerClientMatch.is_deleted == False,
            )
            .count()
        )

        # Error indicators (you might want to add error tracking)
        pending_verifications = (
            db.query(Broker)
            .filter(
                Broker.is_verified == False,
                Broker.license_status == LicenseStatus.PENDING,
                Broker.is_deleted == False,
            )
            .count()
        )

        inactive_brokers = (
            db.query(Broker)
            .filter(Broker.is_active == False, Broker.is_deleted == False)
            .count()
        )

        # Database health (basic checks)
        total_records = {
            "users": db.query(User).filter(User.is_deleted == False).count(),
            "brokers": db.query(Broker).filter(Broker.is_deleted == False).count(),
            "matches": db.query(BrokerClientMatch)
            .filter(BrokerClientMatch.is_deleted == False)
            .count(),
            "reviews": db.query(BrokerReview)
            .filter(BrokerReview.is_deleted == False)
            .count(),
        }

        # Generate alerts
        alerts = []
        if pending_verifications > 10:
            alerts.append(
                {
                    "type": "warning",
                    "message": f"{pending_verifications} brokers pending verification",
                    "action_required": True,
                }
            )

        if inactive_brokers > 5:
            alerts.append(
                {
                    "type": "info",
                    "message": f"{inactive_brokers} inactive brokers",
                    "action_required": False,
                }
            )

        if recent_logins == 0:
            alerts.append(
                {
                    "type": "warning",
                    "message": "No user logins in the past hour",
                    "action_required": False,
                }
            )

        return {
            "timestamp": now.isoformat(),
            "activity_indicators": {
                "recent_logins_1h": recent_logins,
                "recent_matches_24h": recent_matches,
                "pending_verifications": pending_verifications,
                "inactive_brokers": inactive_brokers,
            },
            "database_health": {
                "total_records": total_records,
                "status": (
                    "healthy"
                    if all(count > 0 for count in total_records.values())
                    else "warning"
                ),
            },
            "alerts": alerts,
            "overall_status": (
                "healthy"
                if len([a for a in alerts if a["type"] == "error"]) == 0
                else "warning"
            ),
        }

    @staticmethod
    def get_financial_metrics(db: Session, days: int = 30) -> Dict[str, Any]:
        """Get financial and business metrics (if payment system is integrated)"""

        start_date = datetime.utcnow() - timedelta(days=days)

        # You can expand this based on your payment models
        return {
            "period_days": days,
            "revenue": {
                "total": 0,
                "subscription_revenue": 0,
                "commission_revenue": 0,
                "growth_rate": 0,
            },
            "costs": {
                "platform_costs": 0,
                "broker_payouts": 0,
                "operating_expenses": 0,
            },
            "key_metrics": {
                "average_deal_value": 0,
                "customer_lifetime_value": 0,
                "broker_retention_rate": 0,
            },
        }
