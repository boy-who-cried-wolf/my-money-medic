from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.dashboard import (
    SystemOverviewResponse,
    UserAnalyticsResponse,
    BrokerAnalyticsResponse,
    MatchingAnalyticsResponse,
    QuizAnalyticsResponse,
    PlatformHealthResponse,
    FinancialMetricsResponse,
    UserAnalyticsRequest,
    BrokerAnalyticsRequest,
    MatchingAnalyticsRequest,
    QuizAnalyticsRequest,
    FinancialMetricsRequest,
)
from app.database.models.user import UserType
from app.services.admin_dashboard_service import AdminDashboardService
from app.core.auth import require_admin
from app.database.models.user import User

router = APIRouter()


@router.get("/overview", response_model=SystemOverviewResponse)
def get_system_overview(
    db: Session = Depends(get_db), current_user: User = Depends(require_admin)
):
    """
    Get comprehensive system overview with key platform metrics.

    Admin only endpoint.

    Returns:
    - User statistics (total, by type, new registrations)
    - Broker statistics (active, verified, rates)
    - Match statistics (total, successful, recent activity)
    - Last updated timestamp
    """
    try:
        overview = AdminDashboardService.get_system_overview(db=db)
        return overview
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/analytics/users", response_model=UserAnalyticsResponse)
def get_user_analytics(
    days: int = Query(30, ge=1, le=365, description="Number of days for analysis"),
    user_type: Optional[UserType] = Query(None, description="Filter by user type"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Get detailed user analytics and registration trends.

    Query Parameters:
    - days: Time period for analysis (1-365 days)
    - user_type: Optional filter by user type (client, broker, admin)

    Returns:
    - Daily registration trends by user type
    - User type distribution
    - Verification statistics
    - Most active users
    """
    try:
        analytics = AdminDashboardService.get_user_analytics(
            db=db, days=days, user_type=user_type
        )
        return analytics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/analytics/brokers", response_model=BrokerAnalyticsResponse)
def get_broker_analytics(
    days: int = Query(30, ge=1, le=365, description="Number of days for analysis"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Get comprehensive broker analytics and performance metrics.

    Query Parameters:
    - days: Time period for analysis (1-365 days)

    Returns:
    - License status distribution
    - Experience level distribution
    - Top performing brokers by completion rate
    - Broker verification and activity metrics
    """
    try:
        analytics = AdminDashboardService.get_broker_analytics(db=db, days=days)
        return analytics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/analytics/matching", response_model=MatchingAnalyticsResponse)
def get_matching_analytics(
    days: int = Query(30, ge=1, le=365, description="Number of days for analysis"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Get detailed matching system analytics and performance.

    Query Parameters:
    - days: Time period for analysis (1-365 days)

    Returns:
    - Match status distribution
    - Daily matching trends with acceptance rates
    - Match score distribution by ranges
    - Average response and completion times
    """
    try:
        analytics = AdminDashboardService.get_matching_analytics(db=db, days=days)
        return analytics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/analytics/quiz", response_model=QuizAnalyticsResponse)
def get_quiz_analytics(
    days: int = Query(30, ge=1, le=365, description="Number of days for analysis"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Get quiz system analytics and user engagement metrics.

    Query Parameters:
    - days: Time period for analysis (1-365 days)

    Returns:
    - Quiz completion overview
    - Most popular questions
    - Daily quiz activity trends
    - User completion patterns and distribution
    """
    try:
        analytics = AdminDashboardService.get_quiz_analytics(db=db, days=days)
        return analytics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/health", response_model=PlatformHealthResponse)
def get_platform_health(
    db: Session = Depends(get_db), current_user: User = Depends(require_admin)
):
    """
    Get platform health metrics and system alerts.

    Returns:
    - Recent activity indicators
    - Database health status
    - System alerts and warnings
    - Overall platform status
    """
    try:
        health = AdminDashboardService.get_platform_health(db=db)
        return health
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/analytics/financial", response_model=FinancialMetricsResponse)
def get_financial_metrics(
    days: int = Query(30, ge=1, le=365, description="Number of days for analysis"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Get financial and business metrics for the platform.

    Query Parameters:
    - days: Time period for analysis (1-365 days)

    Returns:
    - Revenue breakdown (subscriptions, commissions)
    - Cost analysis (platform, payouts, operations)
    - Key business metrics (LTV, retention, deal values)

    Note: Currently returns placeholder data. Implement based on payment system.
    """
    try:
        metrics = AdminDashboardService.get_financial_metrics(db=db, days=days)
        return metrics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


# Advanced analytics endpoints
@router.get("/analytics/cohort")
def get_cohort_analysis(
    months: int = Query(
        6, ge=1, le=24, description="Number of months for cohort analysis"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Get user cohort analysis showing retention patterns.

    Query Parameters:
    - months: Number of months to analyze (1-24)

    Returns:
    - Monthly cohort data with retention rates
    - User lifecycle analytics
    """
    # Placeholder for future implementation
    return {
        "message": "Cohort analysis endpoint - implement based on specific business metrics",
        "months": months,
        "note": "This would show user retention patterns by registration month",
    }


@router.get("/analytics/conversion-funnel")
def get_conversion_funnel(
    db: Session = Depends(get_db), current_user: User = Depends(require_admin)
):
    """
    Get conversion funnel analysis from registration to successful match.

    Returns:
    - Step-by-step conversion rates
    - Drop-off points analysis
    - Funnel optimization insights
    """
    # Placeholder for future implementation
    return {
        "message": "Conversion funnel analysis endpoint",
        "stages": [
            "Registration",
            "Profile Completion",
            "Quiz Completion",
            "First Match",
            "Match Acceptance",
            "Successful Completion",
        ],
        "note": "This would show conversion rates between each stage",
    }


@router.get("/users/management")
def get_user_management_data(
    search: Optional[str] = Query(None, description="Search users by name or email"),
    user_type: Optional[UserType] = Query(None, description="Filter by user type"),
    verification_status: Optional[bool] = Query(
        None, description="Filter by verification status"
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Get user management data with search and filtering capabilities.

    Query Parameters:
    - search: Search by name or email
    - user_type: Filter by user type
    - verification_status: Filter by verification status
    - skip: Pagination offset
    - limit: Number of records to return

    Returns:
    - Filtered list of users with management actions
    - Total count and pagination info
    """
    # This would be implemented as a separate user management service
    return {
        "message": "User management endpoint - implement user search and filtering",
        "filters": {
            "search": search,
            "user_type": user_type,
            "verification_status": verification_status,
        },
        "pagination": {"skip": skip, "limit": limit},
    }


@router.get("/brokers/verification-queue")
def get_broker_verification_queue(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Get brokers pending verification for admin review.

    Query Parameters:
    - skip: Pagination offset
    - limit: Number of records to return

    Returns:
    - List of brokers pending verification
    - Required documents and verification details
    - Quick action buttons for approval/rejection
    """
    try:
        from app.database.models.broker import Broker, LicenseStatus

        # Get brokers pending verification
        pending_brokers = (
            db.query(Broker)
            .filter(
                Broker.is_verified == False,
                Broker.license_status == LicenseStatus.PENDING,
                Broker.is_deleted == False,
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

        total = (
            db.query(Broker)
            .filter(
                Broker.is_verified == False,
                Broker.license_status == LicenseStatus.PENDING,
                Broker.is_deleted == False,
            )
            .count()
        )

        broker_data = []
        for broker in pending_brokers:
            user = broker.user
            broker_data.append(
                {
                    "broker_id": str(broker.id),
                    "user_id": str(user.id),
                    "name": user.full_name,
                    "email": user.email,
                    "license_number": broker.license_number,
                    "company_name": broker.company_name,
                    "years_of_experience": broker.years_of_experience,
                    "experience_level": broker.experience_level.value,
                    "created_at": broker.created_at.isoformat(),
                    "documents_submitted": True,  # Placeholder - implement document tracking
                    "verification_status": "pending",
                }
            )

        return {
            "total": total,
            "brokers": broker_data,
            "pagination": {
                "skip": skip,
                "limit": limit,
                "has_more": skip + limit < total,
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("/brokers/{broker_id}/verify")
def verify_broker(
    broker_id: str,
    approved: bool = Query(..., description="True to approve, False to reject"),
    notes: Optional[str] = Query(
        None, description="Admin notes for verification decision"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Approve or reject broker verification.

    Query Parameters:
    - approved: True to approve, False to reject
    - notes: Optional admin notes

    Returns:
    - Updated broker verification status
    - Notification details
    """
    try:
        from app.database.models.broker import Broker, LicenseStatus

        broker = (
            db.query(Broker)
            .filter(Broker.id == broker_id, Broker.is_deleted == False)
            .first()
        )

        if not broker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Broker not found"
            )

        if approved:
            broker.is_verified = True
            broker.license_status = LicenseStatus.ACTIVE
            status_message = "approved"
        else:
            broker.is_verified = False
            broker.license_status = LicenseStatus.REVOKED
            status_message = "rejected"

        db.commit()
        db.refresh(broker)

        # Here you would send notification to broker
        return {
            "broker_id": broker_id,
            "status": status_message,
            "admin_notes": notes,
            "updated_at": broker.updated_at.isoformat(),
            "notification_sent": True,  # Placeholder - implement notification service
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
