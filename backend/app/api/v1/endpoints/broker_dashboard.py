from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.dashboard import (
    BrokerOverviewResponse,
    BrokerMatchesResponse,
    BrokerPerformanceResponse,
    UpdateMatchStatusRequest,
    UpdateMatchStatusResponse,
    BrokerReviewsResponse,
    ClientInsightsResponse,
    BrokerMatchesRequest,
)
from app.database.models.response import MatchStatus
from app.services.broker_dashboard_service import BrokerDashboardService
from app.core.auth import get_current_user, require_broker_or_admin
from app.database.models.user import User

router = APIRouter()


@router.get("/overview/{broker_id}", response_model=BrokerOverviewResponse)
def get_broker_overview(
    broker_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_broker_or_admin),
):
    """
    Get comprehensive broker overview with statistics, profile info, and reviews.

    Accessible by:
    - The broker themselves
    - Admin users

    Returns:
    - Broker profile information
    - Match statistics and success rate
    - Review metrics and ratings
    """
    try:
        # Check if user is the broker or an admin
        if current_user.user_type.value != "admin":
            # Check if this is the broker's own profile
            if (
                not current_user.broker_profile
                or str(current_user.broker_profile.id) != broker_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied. You can only view your own dashboard.",
                )

        overview = BrokerDashboardService.get_broker_overview(
            db=db, broker_id=broker_id
        )
        return overview
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/matches/{broker_id}", response_model=BrokerMatchesResponse)
def get_broker_matches(
    broker_id: str,
    status_filter: Optional[MatchStatus] = Query(None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_broker_or_admin),
):
    """
    Get broker's client matches with filtering and pagination.

    Query Parameters:
    - status: Filter by match status (pending, accepted, rejected, completed, cancelled)
    - skip: Number of records to skip for pagination
    - limit: Maximum number of records to return

    Returns:
    - List of matches with client information
    - Total count and pagination info
    """
    try:
        # Check authorization
        if current_user.user_type.value != "admin":
            if (
                not current_user.broker_profile
                or str(current_user.broker_profile.id) != broker_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied. You can only view your own matches.",
                )

        matches = BrokerDashboardService.get_broker_matches(
            db=db, broker_id=broker_id, status=status_filter, skip=skip, limit=limit
        )
        return matches
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/performance/{broker_id}", response_model=BrokerPerformanceResponse)
def get_broker_performance(
    broker_id: str,
    days: int = Query(
        30, ge=1, le=365, description="Number of days for performance analysis"
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_broker_or_admin),
):
    """
    Get detailed performance metrics for broker including response times,
    completion rates, and trends over specified time period.

    Query Parameters:
    - days: Time period for analysis (1-365 days)

    Returns:
    - Response time metrics
    - Completion time metrics
    - Daily match trends
    - Status distribution
    """
    try:
        # Check authorization
        if current_user.user_type.value != "admin":
            if (
                not current_user.broker_profile
                or str(current_user.broker_profile.id) != broker_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied. You can only view your own performance.",
                )

        performance = BrokerDashboardService.get_broker_performance_metrics(
            db=db, broker_id=broker_id, days=days
        )
        return performance
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.put(
    "/matches/{broker_id}/{match_id}/status", response_model=UpdateMatchStatusResponse
)
def update_match_status(
    broker_id: str,
    match_id: str,
    request: UpdateMatchStatusRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_broker_or_admin),
):
    """
    Update the status of a broker-client match.

    Allowed status transitions:
    - PENDING -> ACCEPTED, REJECTED
    - ACCEPTED -> COMPLETED, CANCELLED
    - Any status -> CANCELLED (by admin)

    Body Parameters:
    - status: New match status
    - notes: Optional notes about the status change
    """
    try:
        # Check authorization
        if current_user.user_type.value != "admin":
            if (
                not current_user.broker_profile
                or str(current_user.broker_profile.id) != broker_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied. You can only update your own matches.",
                )

        result = BrokerDashboardService.update_match_status(
            db=db,
            broker_id=broker_id,
            match_id=match_id,
            status=request.status,
            notes=request.notes,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/reviews/{broker_id}", response_model=BrokerReviewsResponse)
def get_broker_reviews(
    broker_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_broker_or_admin),
):
    """
    Get broker reviews with rating distribution and pagination.

    Query Parameters:
    - skip: Number of records to skip for pagination
    - limit: Maximum number of records to return

    Returns:
    - List of reviews with client information
    - Rating distribution (1-5 stars)
    - Total count and pagination info
    """
    try:
        # Check authorization
        if current_user.user_type.value != "admin":
            if (
                not current_user.broker_profile
                or str(current_user.broker_profile.id) != broker_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied. You can only view your own reviews.",
                )

        reviews = BrokerDashboardService.get_broker_reviews(
            db=db, broker_id=broker_id, skip=skip, limit=limit
        )
        return reviews
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get(
    "/client-insights/{broker_id}/{client_id}", response_model=ClientInsightsResponse
)
def get_client_insights(
    broker_id: str,
    client_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_broker_or_admin),
):
    """
    Get detailed insights about a specific client including:
    - Client profile information
    - Match details and score
    - Quiz responses and insights
    - Recent activity history

    Note: Only accessible for clients who have an active match with the broker.
    """
    try:
        # Check authorization
        if current_user.user_type.value != "admin":
            if (
                not current_user.broker_profile
                or str(current_user.broker_profile.id) != broker_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied. You can only view insights for your own clients.",
                )

        insights = BrokerDashboardService.get_client_insights(
            db=db, broker_id=broker_id, client_id=client_id
        )
        return insights
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


# Additional utility endpoints
@router.get("/stats/summary/{broker_id}")
def get_broker_stats_summary(
    broker_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_broker_or_admin),
):
    """
    Get a quick summary of key broker statistics for dashboard widgets.

    Returns:
    - Current pending matches count
    - Success rate percentage
    - Average rating
    - Recent activity indicators
    """
    try:
        # Check authorization
        if current_user.user_type.value != "admin":
            if (
                not current_user.broker_profile
                or str(current_user.broker_profile.id) != broker_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
                )

        overview = BrokerDashboardService.get_broker_overview(
            db=db, broker_id=broker_id
        )

        # Extract key metrics for quick display
        summary = {
            "pending_matches": overview["statistics"]["pending_matches"],
            "success_rate": overview["statistics"]["success_rate"],
            "average_rating": overview["reviews"]["average_rating"],
            "total_reviews": overview["reviews"]["total_reviews"],
            "recent_activity": overview["statistics"]["recent_matches_30d"],
            "verification_status": overview["profile"]["is_verified"],
            "active_status": overview["profile"]["is_active"],
        }

        return summary
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
