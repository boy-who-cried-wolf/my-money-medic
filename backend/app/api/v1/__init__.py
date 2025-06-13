"""API v1 router module."""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    users,
    auth,
    brokers,
    quizzes,
    matches,
    payments,
    questions,
    adaptive_quiz,
    financial_analysis,
    monitoring,
    broker_dashboard,
    admin_dashboard,
)

# Create API router for v1
api_router = APIRouter()

# Include endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(brokers.router, prefix="/brokers", tags=["Brokers"])
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["Quizzes"])
api_router.include_router(
    adaptive_quiz.router, prefix="/adaptive-quiz", tags=["Adaptive Quiz"]
)
api_router.include_router(matches.router, prefix="/matches", tags=["Matching"])
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])
api_router.include_router(questions.router, prefix="/questions", tags=["Questions"])
api_router.include_router(
    financial_analysis.router, prefix="/financial-analysis", tags=["Financial Analysis"]
)
api_router.include_router(
    monitoring.router, prefix="/monitoring", tags=["Monitoring & Analytics"]
)
api_router.include_router(
    broker_dashboard.router, prefix="/broker-dashboard", tags=["Broker Dashboard"]
)
api_router.include_router(
    admin_dashboard.router, prefix="/admin-dashboard", tags=["Admin Dashboard"]
)
