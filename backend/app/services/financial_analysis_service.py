"""
Financial Analysis Service

This service integrates Effi API data with AI-powered financial insights
to enhance broker matching and provide comprehensive financial analysis.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import asyncio
from statistics import mean, median
import json

from app.api.effi.client import EffiClient
from app.ai.gemini_service import GeminiService
from app.database.models.user import User
from app.database.models.broker import Broker

logger = logging.getLogger(__name__)


class FinancialAnalysisService:
    """
    Service for analyzing financial data from Effi API and generating AI-powered insights
    """

    def __init__(self):
        """Initialize the financial analysis service"""
        self.effi_client = EffiClient()
        self.gemini_service = GeminiService()

    async def analyze_lead_financial_profile(
        self, lead_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze a single lead's financial profile and generate insights

        Args:
            lead_data: Lead data from Effi API

        Returns:
            Dictionary containing financial analysis and insights
        """
        try:
            # Extract financial indicators
            financial_indicators = self._extract_financial_indicators(lead_data)

            # Generate AI insights
            ai_insights = await self._generate_financial_insights(
                financial_indicators, lead_data
            )

            # Calculate risk profile
            risk_profile = self._calculate_risk_profile(financial_indicators)

            # Generate recommendations
            recommendations = await self._generate_recommendations(
                financial_indicators, risk_profile
            )

            return {
                "lead_id": lead_data.get("Id") or lead_data.get("id"),
                "financial_indicators": financial_indicators,
                "risk_profile": risk_profile,
                "ai_insights": ai_insights,
                "recommendations": recommendations,
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "confidence_score": self._calculate_confidence_score(
                    financial_indicators
                ),
            }

        except Exception as e:
            logger.error(f"Error analyzing lead financial profile: {str(e)}")
            return {
                "error": str(e),
                "analysis_timestamp": datetime.utcnow().isoformat(),
            }

    def _extract_financial_indicators(
        self, lead_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract key financial indicators from lead data

        Args:
            lead_data: Raw lead data from Effi API

        Returns:
            Dictionary of financial indicators
        """
        # Handle different case formats from API
        loan_amount = (
            lead_data.get("LoanAmount")
            or lead_data.get("loanAmount")
            or lead_data.get("loan_amount")
            or 0
        )

        property_value = (
            lead_data.get("EstimatedPropertyValue")
            or lead_data.get("estimatedPropertyValue")
            or lead_data.get("estimated_property_value")
            or 0
        )

        # Calculate derived indicators
        loan_to_value_ratio = 0
        if property_value > 0:
            loan_to_value_ratio = (loan_amount / property_value) * 100

        # Estimate income based on loan amount (rough calculation)
        estimated_annual_income = loan_amount * 0.2 if loan_amount > 0 else 0

        return {
            "loan_amount": float(loan_amount),
            "property_value": float(property_value),
            "loan_to_value_ratio": round(loan_to_value_ratio, 2),
            "estimated_annual_income": round(estimated_annual_income, 2),
            "location": {
                "suburb": lead_data.get("Suburb") or lead_data.get("suburb") or "",
                "state": lead_data.get("State") or lead_data.get("state") or "",
                "postcode": lead_data.get("Postcode")
                or lead_data.get("postcode")
                or "",
            },
            "contact_info": {
                "email": lead_data.get("Email") or lead_data.get("email") or "",
                "phone": lead_data.get("Phone") or lead_data.get("phone") or "",
            },
        }

    def _calculate_risk_profile(
        self, financial_indicators: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate risk profile based on financial indicators

        Args:
            financial_indicators: Extracted financial indicators

        Returns:
            Risk profile assessment
        """
        risk_factors = []
        risk_score = 50  # Start with neutral score

        # Loan-to-Value Ratio Analysis
        ltv = financial_indicators.get("loan_to_value_ratio", 0)
        if ltv > 90:
            risk_factors.append("High LTV ratio (>90%)")
            risk_score += 20
        elif ltv > 80:
            risk_factors.append("Moderate LTV ratio (80-90%)")
            risk_score += 10
        elif ltv < 60:
            risk_factors.append("Conservative LTV ratio (<60%)")
            risk_score -= 10

        # Loan Amount Analysis
        loan_amount = financial_indicators.get("loan_amount", 0)
        if loan_amount > 1000000:
            risk_factors.append("High loan amount (>$1M)")
            risk_score += 15
        elif loan_amount < 200000:
            risk_factors.append("Low loan amount (<$200K)")
            risk_score -= 5

        # Income to Loan Ratio
        estimated_income = financial_indicators.get("estimated_annual_income", 0)
        if estimated_income > 0:
            income_to_loan_ratio = loan_amount / estimated_income
            if income_to_loan_ratio > 6:
                risk_factors.append("High debt-to-income ratio")
                risk_score += 15
            elif income_to_loan_ratio < 3:
                risk_factors.append("Conservative debt-to-income ratio")
                risk_score -= 10

        # Normalize risk score (0-100)
        risk_score = max(0, min(100, risk_score))

        # Determine risk category
        if risk_score >= 70:
            risk_category = "HIGH"
        elif risk_score >= 40:
            risk_category = "MEDIUM"
        else:
            risk_category = "LOW"

        return {
            "risk_score": risk_score,
            "risk_category": risk_category,
            "risk_factors": risk_factors,
            "ltv_ratio": ltv,
            "debt_to_income_estimate": round(loan_amount / max(estimated_income, 1), 2),
        }

    async def _generate_financial_insights(
        self, financial_indicators: Dict[str, Any], lead_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate AI-powered financial insights using Gemini

        Args:
            financial_indicators: Extracted financial indicators
            lead_data: Original lead data

        Returns:
            AI-generated insights
        """
        try:
            prompt = f"""
            As a financial advisor AI, analyze this client's financial profile and provide insights:

            Financial Profile:
            - Loan Amount: ${financial_indicators.get('loan_amount', 0):,.2f}
            - Property Value: ${financial_indicators.get('property_value', 0):,.2f}
            - Loan-to-Value Ratio: {financial_indicators.get('loan_to_value_ratio', 0):.1f}%
            - Estimated Annual Income: ${financial_indicators.get('estimated_annual_income', 0):,.2f}
            - Location: {financial_indicators.get('location', {}).get('suburb', '')}, {financial_indicators.get('location', {}).get('state', '')}

            Please provide a JSON response with the following structure:
            {{
                "financial_health_score": <number 1-100>,
                "key_strengths": ["strength1", "strength2", "strength3"],
                "areas_of_concern": ["concern1", "concern2"],
                "market_insights": "Brief analysis of their market position",
                "investment_readiness": "Assessment of their readiness for investment",
                "broker_requirements": ["requirement1", "requirement2", "requirement3"]
            }}

            Focus on practical insights that would help match them with the right broker.
            """

            insights = await self.gemini_service.generate_json(prompt, strict=False)

            if insights:
                return insights
            else:
                # Fallback insights if AI generation fails
                return self._generate_fallback_insights(financial_indicators)

        except Exception as e:
            logger.error(f"Error generating AI insights: {str(e)}")
            return self._generate_fallback_insights(financial_indicators)

    def _generate_fallback_insights(
        self, financial_indicators: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate fallback insights when AI generation fails

        Args:
            financial_indicators: Financial indicators

        Returns:
            Basic insights based on rules
        """
        ltv = financial_indicators.get("loan_to_value_ratio", 0)
        loan_amount = financial_indicators.get("loan_amount", 0)

        strengths = []
        concerns = []

        if ltv < 80:
            strengths.append("Conservative loan-to-value ratio")
        if loan_amount > 500000:
            strengths.append("Substantial investment capacity")
        if ltv > 90:
            concerns.append("High loan-to-value ratio may limit options")
        if loan_amount < 100000:
            concerns.append("Limited loan amount may restrict property choices")

        return {
            "financial_health_score": max(20, min(80, 100 - ltv)),
            "key_strengths": strengths or ["Seeking professional financial guidance"],
            "areas_of_concern": concerns or ["Standard risk assessment needed"],
            "market_insights": "Market analysis based on location and loan amount",
            "investment_readiness": (
                "Moderate" if ltv < 85 else "Requires careful assessment"
            ),
            "broker_requirements": [
                "Experienced with similar loan amounts",
                "Local market knowledge",
                "Risk assessment expertise",
            ],
        }

    async def _generate_recommendations(
        self, financial_indicators: Dict[str, Any], risk_profile: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Generate personalized recommendations

        Args:
            financial_indicators: Financial indicators
            risk_profile: Risk profile assessment

        Returns:
            List of recommendations
        """
        try:
            prompt = f"""
            Based on this financial profile, generate 3-5 specific recommendations:

            Financial Indicators:
            - Loan Amount: ${financial_indicators.get('loan_amount', 0):,.2f}
            - LTV Ratio: {financial_indicators.get('loan_to_value_ratio', 0):.1f}%
            - Risk Category: {risk_profile.get('risk_category', 'MEDIUM')}
            - Risk Score: {risk_profile.get('risk_score', 50)}

            Provide recommendations as JSON array:
            [
                {{
                    "title": "Recommendation Title",
                    "description": "Detailed description",
                    "priority": "high|medium|low",
                    "category": "financing|investment|risk_management|market_strategy",
                    "potential_impact": "Description of potential impact"
                }}
            ]
            """

            recommendations = await self.gemini_service.generate_json(
                prompt, strict=False
            )

            if isinstance(recommendations, list):
                return recommendations
            else:
                return self._generate_fallback_recommendations(
                    financial_indicators, risk_profile
                )

        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return self._generate_fallback_recommendations(
                financial_indicators, risk_profile
            )

    def _generate_fallback_recommendations(
        self, financial_indicators: Dict[str, Any], risk_profile: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate fallback recommendations"""
        recommendations = []

        ltv = financial_indicators.get("loan_to_value_ratio", 0)
        risk_category = risk_profile.get("risk_category", "MEDIUM")

        if ltv > 85:
            recommendations.append(
                {
                    "title": "Consider Larger Down Payment",
                    "description": "Reducing loan-to-value ratio could improve loan terms and reduce risk",
                    "priority": "high",
                    "category": "financing",
                    "potential_impact": "Better interest rates and loan approval odds",
                }
            )

        if risk_category == "HIGH":
            recommendations.append(
                {
                    "title": "Risk Assessment Review",
                    "description": "Comprehensive risk assessment recommended before proceeding",
                    "priority": "high",
                    "category": "risk_management",
                    "potential_impact": "Identify and mitigate potential financial risks",
                }
            )

        recommendations.append(
            {
                "title": "Market Analysis",
                "description": "Detailed local market analysis for optimal investment timing",
                "priority": "medium",
                "category": "market_strategy",
                "potential_impact": "Maximize investment returns through market timing",
            }
        )

        return recommendations

    def _calculate_confidence_score(
        self, financial_indicators: Dict[str, Any]
    ) -> float:
        """
        Calculate confidence score for the analysis

        Args:
            financial_indicators: Financial indicators

        Returns:
            Confidence score (0-100)
        """
        score = 50  # Base score

        # Increase confidence based on available data
        if financial_indicators.get("loan_amount", 0) > 0:
            score += 20
        if financial_indicators.get("property_value", 0) > 0:
            score += 20
        if financial_indicators.get("location", {}).get("suburb"):
            score += 10

        return min(100, score)

    async def analyze_market_trends(
        self, location: str = None, days_back: int = 30
    ) -> Dict[str, Any]:
        """
        Analyze market trends from recent leads

        Args:
            location: Optional location filter
            days_back: Number of days to look back

        Returns:
            Market trend analysis
        """
        try:
            # Get recent leads from Effi
            from_date = (datetime.now() - timedelta(days=days_back)).strftime(
                "%Y-%m-%d"
            )
            to_date = datetime.now().strftime("%Y-%m-%d")

            leads_response = self.effi_client.get_leads(
                from_date=from_date, to_date=to_date, top=100
            )

            leads = leads_response.get("Items", [])

            if not leads:
                return {"error": "No recent leads found for analysis"}

            # Filter by location if specified
            if location:
                leads = [
                    lead
                    for lead in leads
                    if location.lower()
                    in (
                        (lead.get("Suburb") or "").lower()
                        + (lead.get("State") or "").lower()
                        + (lead.get("Postcode") or "").lower()
                    )
                ]

            # Analyze trends
            loan_amounts = []
            property_values = []
            ltv_ratios = []

            for lead in leads:
                loan_amount = lead.get("LoanAmount") or lead.get("loanAmount") or 0
                property_value = (
                    lead.get("EstimatedPropertyValue")
                    or lead.get("estimatedPropertyValue")
                    or 0
                )

                if loan_amount > 0:
                    loan_amounts.append(float(loan_amount))
                if property_value > 0:
                    property_values.append(float(property_value))
                if loan_amount > 0 and property_value > 0:
                    ltv_ratios.append((loan_amount / property_value) * 100)

            # Generate AI insights about trends
            trend_insights = await self._generate_market_trend_insights(
                loan_amounts, property_values, ltv_ratios, location
            )

            return {
                "analysis_period": f"{from_date} to {to_date}",
                "total_leads": len(leads),
                "location_filter": location,
                "loan_amount_trends": {
                    "average": round(mean(loan_amounts), 2) if loan_amounts else 0,
                    "median": round(median(loan_amounts), 2) if loan_amounts else 0,
                    "min": round(min(loan_amounts), 2) if loan_amounts else 0,
                    "max": round(max(loan_amounts), 2) if loan_amounts else 0,
                    "count": len(loan_amounts),
                },
                "property_value_trends": {
                    "average": (
                        round(mean(property_values), 2) if property_values else 0
                    ),
                    "median": (
                        round(median(property_values), 2) if property_values else 0
                    ),
                    "min": round(min(property_values), 2) if property_values else 0,
                    "max": round(max(property_values), 2) if property_values else 0,
                    "count": len(property_values),
                },
                "ltv_trends": {
                    "average": round(mean(ltv_ratios), 2) if ltv_ratios else 0,
                    "median": round(median(ltv_ratios), 2) if ltv_ratios else 0,
                    "count": len(ltv_ratios),
                },
                "ai_insights": trend_insights,
                "analysis_timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(f"Error analyzing market trends: {str(e)}")
            return {"error": str(e)}

    async def _generate_market_trend_insights(
        self,
        loan_amounts: List[float],
        property_values: List[float],
        ltv_ratios: List[float],
        location: str = None,
    ) -> Dict[str, Any]:
        """Generate AI insights about market trends"""
        try:
            avg_loan = mean(loan_amounts) if loan_amounts else 0
            avg_property = mean(property_values) if property_values else 0
            avg_ltv = mean(ltv_ratios) if ltv_ratios else 0

            prompt = f"""
            Analyze these market trends and provide insights:

            Market Data:
            - Average Loan Amount: ${avg_loan:,.2f}
            - Average Property Value: ${avg_property:,.2f}
            - Average LTV Ratio: {avg_ltv:.1f}%
            - Location: {location or "All locations"}
            - Sample Size: {len(loan_amounts)} loans

            Provide JSON response:
            {{
                "market_sentiment": "bullish|bearish|neutral",
                "key_trends": ["trend1", "trend2", "trend3"],
                "risk_assessment": "Market risk level and factors",
                "opportunities": ["opportunity1", "opportunity2"],
                "broker_implications": "What this means for brokers"
            }}
            """

            insights = await self.gemini_service.generate_json(prompt, strict=False)
            return insights or {
                "market_sentiment": "neutral",
                "key_trends": ["Insufficient data for detailed analysis"],
            }

        except Exception as e:
            logger.error(f"Error generating market trend insights: {str(e)}")
            return {"error": str(e)}

    async def enhance_broker_matching(
        self, user_id: str, db: Session
    ) -> Dict[str, Any]:
        """
        Enhance broker matching using Effi financial data analysis

        Args:
            user_id: User ID to match
            db: Database session

        Returns:
            Enhanced matching results
        """
        try:
            # Get user data
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return {"error": "User not found"}

            # Search for similar leads in Effi (by email or other criteria)
            similar_leads = []
            if user.email:
                try:
                    search_results = self.effi_client.search_leads(
                        email=user.email, page_size=5
                    )
                    similar_leads = search_results.get("Items", [])
                except:
                    pass  # Continue without Effi data if search fails

            # Analyze financial patterns from similar leads
            financial_analysis = None
            if similar_leads:
                # Use the most recent lead for analysis
                latest_lead = similar_leads[0]
                financial_analysis = await self.analyze_lead_financial_profile(
                    latest_lead
                )

            # Get standard broker matches using the existing service
            from app.services.matching_algorithm import generate_broker_matches

            standard_matches = generate_broker_matches(db, user_id, save_to_db=False)

            # Enhance matches with financial insights
            enhanced_matches = []
            for match in standard_matches:
                enhanced_match = match.copy()

                if financial_analysis:
                    # Add financial compatibility score
                    financial_score = self._calculate_financial_compatibility(
                        financial_analysis, match
                    )
                    enhanced_match["financial_compatibility"] = financial_score
                    enhanced_match["financial_insights"] = financial_analysis.get(
                        "ai_insights", {}
                    )

                    # Adjust overall score
                    original_score = enhanced_match.get("match_score", 0)
                    enhanced_score = (original_score * 0.7) + (financial_score * 0.3)
                    enhanced_match["enhanced_compatibility_score"] = round(
                        enhanced_score, 2
                    )

                enhanced_matches.append(enhanced_match)

            # Sort by enhanced score if available
            enhanced_matches.sort(
                key=lambda x: x.get(
                    "enhanced_compatibility_score", x.get("match_score", 0)
                ),
                reverse=True,
            )

            return {
                "user_id": user_id,
                "enhanced_matches": enhanced_matches,
                "financial_analysis": financial_analysis,
                "effi_leads_found": len(similar_leads),
                "enhancement_timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(f"Error enhancing broker matching: {str(e)}")
            return {"error": str(e)}

    def _calculate_financial_compatibility(
        self, financial_analysis: Dict[str, Any], broker_match: Dict[str, Any]
    ) -> float:
        """
        Calculate financial compatibility between client analysis and broker

        Args:
            financial_analysis: Client financial analysis
            broker_match: Broker match information

        Returns:
            Compatibility score (0-100)
        """
        score = 50  # Base score

        risk_category = financial_analysis.get("risk_profile", {}).get(
            "risk_category", "MEDIUM"
        )
        loan_amount = financial_analysis.get("financial_indicators", {}).get(
            "loan_amount", 0
        )

        # Broker specialization matching
        broker_specializations = broker_match.get("specializations", [])

        # Risk category matching
        if risk_category == "HIGH" and any(
            "risk" in spec.lower() for spec in broker_specializations
        ):
            score += 20
        elif risk_category == "LOW" and any(
            "first" in spec.lower() or "residential" in spec.lower()
            for spec in broker_specializations
        ):
            score += 15

        # Loan amount matching
        if loan_amount > 1000000 and any(
            "commercial" in spec.lower() or "investment" in spec.lower()
            for spec in broker_specializations
        ):
            score += 15
        elif loan_amount < 500000 and any(
            "residential" in spec.lower() or "first" in spec.lower()
            for spec in broker_specializations
        ):
            score += 10

        return min(100, max(0, score))


# Convenience function for easy import
async def analyze_lead_financial_profile(lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function to analyze a single lead's financial profile"""
    service = FinancialAnalysisService()
    return await service.analyze_lead_financial_profile(lead_data)


async def analyze_market_trends(
    location: str = None, days_back: int = 30
) -> Dict[str, Any]:
    """Convenience function to analyze market trends"""
    service = FinancialAnalysisService()
    return await service.analyze_market_trends(location, days_back)
