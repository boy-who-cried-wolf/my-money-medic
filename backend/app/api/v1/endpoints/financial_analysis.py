"""
Financial Analysis API Endpoints

Provides endpoints for analyzing financial data from Effi API,
generating AI insights, and enhancing broker matching.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import asyncio

from app.database import get_db
from app.core.auth import get_current_user
from app.database.models.user import User, UserType
from app.api.effi.client import EffiClient

router = APIRouter()


def require_admin_or_broker(current_user: User = Depends(get_current_user)):
    """Require admin or broker role"""
    if current_user.user_type not in [UserType.ADMIN, UserType.BROKER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or broker access required",
        )
    return current_user


def require_admin(current_user: User = Depends(get_current_user)):
    """Require admin role"""
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return current_user


@router.post("/analyze-lead")
async def analyze_lead_financial_profile(
    lead_data: Dict[str, Any], current_user: User = Depends(require_admin_or_broker)
):
    """
    Analyze a lead's financial profile and generate AI insights

    Requires: Admin or Broker role
    """
    try:
        from app.services.financial_analysis_service import FinancialAnalysisService

        service = FinancialAnalysisService()
        analysis = await service.analyze_lead_financial_profile(lead_data)

        return {"success": True, "analysis": analysis, "analyzed_by": current_user.id}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing lead: {str(e)}",
        )


@router.get("/market-trends")
async def get_market_trends(
    location: Optional[str] = Query(
        None, description="Location filter (suburb, state, or postcode)"
    ),
    days_back: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    current_user: User = Depends(require_admin_or_broker),
):
    """
    Analyze market trends from recent Effi leads

    Requires: Admin or Broker role
    """
    try:
        from app.services.financial_analysis_service import FinancialAnalysisService

        service = FinancialAnalysisService()
        trends = await service.analyze_market_trends(
            location=location, days_back=days_back
        )

        return {"success": True, "trends": trends, "requested_by": current_user.id}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing market trends: {str(e)}",
        )


@router.post("/enhance-matching/{user_id}")
async def enhance_broker_matching(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin_or_broker),
):
    """
    Enhance broker matching using Effi financial data analysis

    Requires: Admin or Broker role
    """
    try:
        from app.services.financial_analysis_service import FinancialAnalysisService

        service = FinancialAnalysisService()
        enhanced_matches = await service.enhance_broker_matching(user_id, db)

        return {
            "success": True,
            "enhanced_matches": enhanced_matches,
            "enhanced_by": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error enhancing broker matching: {str(e)}",
        )


@router.get("/effi-leads")
async def search_effi_leads(
    status: Optional[str] = Query(None, description="Lead status filter"),
    name: Optional[str] = Query(None, description="Name search"),
    email: Optional[str] = Query(None, description="Email filter"),
    phone: Optional[str] = Query(None, description="Phone filter"),
    postal_code: Optional[str] = Query(None, description="Postal code filter"),
    broker_id: Optional[str] = Query(None, description="Broker ID filter"),
    min_loan_amount: Optional[float] = Query(None, description="Minimum loan amount"),
    max_loan_amount: Optional[float] = Query(None, description="Maximum loan amount"),
    created_from: Optional[str] = Query(
        None, description="Created from date (YYYY-MM-DD)"
    ),
    created_to: Optional[str] = Query(None, description="Created to date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Results per page"),
    current_user: User = Depends(require_admin_or_broker),
):
    """
    Search Effi leads with various filters

    Requires: Admin or Broker role
    """
    try:
        effi_client = EffiClient()

        leads = effi_client.search_leads(
            status=status,
            name=name,
            email=email,
            phone=phone,
            postal_code=postal_code,
            broker_id=broker_id,
            min_loan_amount=min_loan_amount,
            max_loan_amount=max_loan_amount,
            created_from=created_from,
            created_to=created_to,
            page=page,
            page_size=page_size,
        )

        return {"success": True, "leads": leads, "searched_by": current_user.id}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching Effi leads: {str(e)}",
        )


@router.get("/effi-leads/{lead_id}")
async def get_effi_lead(
    lead_id: str, current_user: User = Depends(require_admin_or_broker)
):
    """
    Get a specific Effi lead by ID

    Requires: Admin or Broker role
    """
    try:
        effi_client = EffiClient()
        lead = effi_client.get_lead(lead_id)

        return {"success": True, "lead": lead, "retrieved_by": current_user.id}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving Effi lead: {str(e)}",
        )


@router.post("/effi-leads/{lead_id}/analyze")
async def analyze_effi_lead(
    lead_id: str, current_user: User = Depends(require_admin_or_broker)
):
    """
    Analyze a specific Effi lead's financial profile

    Requires: Admin or Broker role
    """
    try:
        # Get the lead from Effi
        effi_client = EffiClient()
        lead_data = effi_client.get_lead(lead_id)

        # Analyze the lead
        from app.services.financial_analysis_service import FinancialAnalysisService

        service = FinancialAnalysisService()
        analysis = await service.analyze_lead_financial_profile(lead_data)

        return {
            "success": True,
            "lead_data": lead_data,
            "analysis": analysis,
            "analyzed_by": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing Effi lead: {str(e)}",
        )


@router.post("/batch-analyze")
async def batch_analyze_leads(
    lead_ids: List[str], current_user: User = Depends(require_admin)
):
    """
    Batch analyze multiple leads from Effi

    Requires: Admin role
    """
    try:
        if len(lead_ids) > 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum 50 leads can be analyzed in a batch",
            )

        effi_client = EffiClient()
        from app.services.financial_analysis_service import FinancialAnalysisService

        service = FinancialAnalysisService()

        results = []

        for lead_id in lead_ids:
            try:
                # Get lead data
                lead_data = effi_client.get_lead(lead_id)

                # Analyze lead
                analysis = await service.analyze_lead_financial_profile(lead_data)

                results.append(
                    {"lead_id": lead_id, "success": True, "analysis": analysis}
                )

            except Exception as e:
                results.append({"lead_id": lead_id, "success": False, "error": str(e)})

        return {
            "success": True,
            "batch_results": results,
            "total_processed": len(results),
            "successful": len([r for r in results if r["success"]]),
            "failed": len([r for r in results if not r["success"]]),
            "analyzed_by": current_user.id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in batch analysis: {str(e)}",
        )


@router.get("/my-financial-analysis")
async def get_my_financial_analysis(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Get financial analysis for the current user (if available from Effi)

    Available to all authenticated users
    """
    try:
        from app.services.financial_analysis_service import FinancialAnalysisService

        service = FinancialAnalysisService()
        enhanced_matches = await service.enhance_broker_matching(current_user.id, db)

        # Extract just the financial analysis part for the user
        financial_analysis = enhanced_matches.get("financial_analysis")

        if not financial_analysis:
            return {
                "success": True,
                "message": "No financial data found in Effi system",
                "has_analysis": False,
            }

        return {
            "success": True,
            "has_analysis": True,
            "financial_analysis": financial_analysis,
            "effi_leads_found": enhanced_matches.get("effi_leads_found", 0),
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving financial analysis: {str(e)}",
        )


@router.post("/test-effi-connection")
async def test_effi_connection(current_user: User = Depends(require_admin)):
    """
    Test Effi API connection and retrieve sample data

    Requires: Admin role
    """
    try:
        effi_client = EffiClient()

        # Test basic connection by getting recent leads
        test_response = effi_client.get_leads(top=5, skip=0)

        return {
            "success": True,
            "connection_status": "Connected",
            "sample_data": test_response,
            "tested_by": current_user.id,
        }

    except Exception as e:
        return {
            "success": False,
            "connection_status": "Failed",
            "error": str(e),
            "tested_by": current_user.id,
        }
