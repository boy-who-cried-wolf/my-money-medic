"""
Matching Algorithm for Broker-Client Matching Platform

This module implements a sophisticated matching algorithm that scores brokers
based on client quiz responses, broker attributes, and weighted criteria.
"""

from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import json
from datetime import datetime
from collections import defaultdict

from app.database.models.user import User, UserType
from app.database.models.broker import Broker, Specialization, ExperienceLevel
from app.database.models.quiz import UserQuizResponse, QuizQuestion, QuizCategory
from app.database.models.response import BrokerClientMatch, MatchStatus


class BrokerMatchingAlgorithm:
    """
    Sophisticated matching algorithm that considers multiple factors:
    1. Investment goals alignment
    2. Risk tolerance compatibility
    3. Experience level matching
    4. Service preferences
    5. Communication style
    6. Investment amount range
    7. Sector interests
    8. Certification preferences
    """

    # Weight configuration for different matching criteria
    WEIGHTS = {
        "investment_goals": 0.20,
        "risk_tolerance": 0.15,
        "experience_match": 0.15,
        "service_alignment": 0.15,
        "investment_amount": 0.10,
        "sector_interests": 0.10,
        "communication_style": 0.05,
        "certification_match": 0.05,
        "broker_performance": 0.05,
    }

    # Experience level mapping for compatibility
    EXPERIENCE_COMPATIBILITY = {
        "none": ["junior", "intermediate"],
        "beginner": ["intermediate", "senior"],
        "intermediate": ["intermediate", "senior", "expert"],
        "advanced": ["senior", "expert"],
        "expert": ["expert"],
    }

    # Risk tolerance compatibility matrix
    RISK_COMPATIBILITY = {
        "conservative": ["conservative", "moderate_conservative"],
        "moderate_conservative": ["conservative", "moderate_conservative", "moderate"],
        "moderate": ["moderate_conservative", "moderate", "moderate_aggressive"],
        "moderate_aggressive": ["moderate", "moderate_aggressive", "aggressive"],
        "aggressive": ["moderate_aggressive", "aggressive"],
    }

    def __init__(self, db: Session):
        self.db = db

    def calculate_matches(
        self, user_id: str, top_n: int = 10
    ) -> List[Tuple[Broker, float]]:
        """
        Calculate broker matches for a given client

        Args:
            user_id: The client's user ID
            top_n: Number of top matches to return

        Returns:
            List of tuples containing (Broker, match_score)
        """
        # Get user and their quiz responses
        user = (
            self.db.query(User)
            .filter(User.id == user_id, User.user_type == UserType.CLIENT)
            .first()
        )

        if not user:
            return []

        # Get user's quiz responses
        user_responses = self._get_user_responses(user_id)
        if not user_responses:
            return []

        # Get all active brokers (excluding test/demo brokers)
        brokers = (
            self.db.query(Broker)
            .join(User, Broker.user_id == User.id)
            .filter(
                Broker.is_active == True,
                Broker.is_verified == True,
                Broker.is_deleted == None,
                ~User.email.like("%test%"),  # Exclude test brokers
                ~User.email.like("%demo%"),  # Exclude demo brokers
            )
            .all()
        )

        # Calculate match scores for each broker
        broker_scores = []
        for broker in brokers:
            score = self._calculate_broker_score(broker, user_responses)
            broker_scores.append((broker, score))

        # Sort by score and return top N
        broker_scores.sort(key=lambda x: x[1], reverse=True)
        return broker_scores[:top_n]

    def _get_user_responses(self, user_id: str) -> Dict[str, Any]:
        """Get and organize user's quiz responses"""
        responses = (
            self.db.query(UserQuizResponse)
            .join(QuizQuestion)
            .filter(UserQuizResponse.user_id == user_id)
            .all()
        )

        # Organize responses by question text for easier access
        response_dict = {}
        for response in responses:
            question_text = response.question.text
            response_data = response.response

            # Handle different response formats
            if isinstance(response_data, str):
                try:
                    response_data = json.loads(response_data)
                except:
                    pass

            response_dict[question_text] = {
                "response": response_data,
                "question_type": response.question.question_type.value,
                "weight": response.question.weight,
            }

        return response_dict

    def _calculate_broker_score(
        self, broker: Broker, user_responses: Dict[str, Any]
    ) -> float:
        """Calculate match score for a specific broker"""
        scores = {}

        # 1. Investment Goals Alignment
        scores["investment_goals"] = self._score_investment_goals(
            broker, user_responses
        )

        # 2. Risk Tolerance Compatibility
        scores["risk_tolerance"] = self._score_risk_tolerance(broker, user_responses)

        # 3. Experience Level Matching
        scores["experience_match"] = self._score_experience_match(
            broker, user_responses
        )

        # 4. Service Alignment
        scores["service_alignment"] = self._score_service_alignment(
            broker, user_responses
        )

        # 5. Investment Amount Range
        scores["investment_amount"] = self._score_investment_amount(
            broker, user_responses
        )

        # 6. Sector Interests
        scores["sector_interests"] = self._score_sector_interests(
            broker, user_responses
        )

        # 7. Communication Style
        scores["communication_style"] = self._score_communication_style(
            broker, user_responses
        )

        # 8. Certification Match
        scores["certification_match"] = self._score_certification_match(
            broker, user_responses
        )

        # 9. Broker Performance
        scores["broker_performance"] = self._score_broker_performance(broker)

        # Calculate weighted total score
        total_score = sum(
            score * self.WEIGHTS.get(criteria, 0) for criteria, score in scores.items()
        )

        return min(total_score, 1.0)  # Cap at 1.0

    def _score_investment_goals(
        self, broker: Broker, user_responses: Dict[str, Any]
    ) -> float:
        """Score based on investment goals alignment"""
        goal_response = user_responses.get("What is your primary investment goal?", {})
        if not goal_response:
            return 0.5  # Neutral score if no response

        user_goal = goal_response.get("response")
        if not user_goal:
            return 0.5

        # Handle both list and string formats
        if isinstance(user_goal, list):
            user_goal = user_goal[0] if user_goal else None
        elif isinstance(user_goal, dict):
            user_goal = user_goal.get("answer", str(user_goal))

        if not user_goal:
            return 0.5

        # Map goals to broker specializations
        goal_to_specialization = {
            "retirement": ["retirement_planning", "financial_planning"],
            "wealth_growth": ["investment_management", "wealth_management"],
            "income": ["income_strategies", "dividend_investing"],
            "education": ["education_planning", "529_plans"],
            "home_purchase": ["real_estate_planning", "savings_strategies"],
        }

        # Check if broker has matching specializations
        broker_specializations = [spec.name.lower() for spec in broker.specializations]
        required_specs = goal_to_specialization.get(str(user_goal).lower(), [])

        if not required_specs:
            return 0.7  # Default score if no specific mapping

        # Calculate overlap
        matches = sum(
            1
            for spec in required_specs
            if any(spec in broker_spec for broker_spec in broker_specializations)
        )

        return min(matches / len(required_specs), 1.0) if required_specs else 0.7

    def _score_risk_tolerance(
        self, broker: Broker, user_responses: Dict[str, Any]
    ) -> float:
        """Score based on risk tolerance compatibility"""
        risk_response = user_responses.get("What is your risk tolerance level?", {})
        if not risk_response:
            return 0.5

        user_risk = risk_response.get("response")
        if not user_risk:
            return 0.5

        # Handle both list and string formats
        if isinstance(user_risk, list):
            user_risk = user_risk[0] if user_risk else None
        elif isinstance(user_risk, dict):
            user_risk = user_risk.get("answer", str(user_risk))

        if not user_risk:
            return 0.5

        # Check broker's risk management style (would need to be added to broker model)
        # For now, use a simplified approach based on experience
        broker_risk_styles = {
            ExperienceLevel.JUNIOR: ["conservative", "moderate_conservative"],
            ExperienceLevel.INTERMEDIATE: ["moderate_conservative", "moderate"],
            ExperienceLevel.SENIOR: ["moderate", "moderate_aggressive"],
            ExperienceLevel.EXPERT: ["moderate_aggressive", "aggressive"],
        }

        compatible_risks = self.RISK_COMPATIBILITY.get(
            str(user_risk).lower(), [str(user_risk).lower()]
        )
        broker_styles = broker_risk_styles.get(broker.experience_level, ["moderate"])

        # Check compatibility
        compatibility = any(style in compatible_risks for style in broker_styles)
        return 1.0 if compatibility else 0.3

    def _score_experience_match(
        self, broker: Broker, user_responses: Dict[str, Any]
    ) -> float:
        """Score based on experience level matching"""
        exp_response = user_responses.get(
            "How would you describe your investment experience?", {}
        )
        if not exp_response:
            return 0.5

        user_experience = exp_response.get("response")
        if not user_experience:
            return 0.5

        # Handle both list and string formats
        if isinstance(user_experience, list):
            user_experience = user_experience[0] if user_experience else None
        elif isinstance(user_experience, dict):
            user_experience = user_experience.get("answer", str(user_experience))

        if not user_experience:
            return 0.5

        # Get compatible broker experience levels
        compatible_levels = self.EXPERIENCE_COMPATIBILITY.get(
            str(user_experience).lower(), []
        )

        # Map broker experience enum to string
        broker_exp_map = {
            ExperienceLevel.JUNIOR: "junior",
            ExperienceLevel.INTERMEDIATE: "intermediate",
            ExperienceLevel.SENIOR: "senior",
            ExperienceLevel.EXPERT: "expert",
        }

        broker_exp = broker_exp_map.get(broker.experience_level, "intermediate")

        if broker_exp in compatible_levels:
            # Perfect match gets higher score
            if str(user_experience).lower() == "none" and broker_exp == "junior":
                return 1.0
            elif str(user_experience).lower() == "expert" and broker_exp == "expert":
                return 1.0
            else:
                return 0.8
        else:
            return 0.3

    def _score_service_alignment(
        self, broker: Broker, user_responses: Dict[str, Any]
    ) -> float:
        """Score based on service preferences alignment"""
        service_response = user_responses.get(
            "Which services are most important to you?", {}
        )
        if not service_response:
            return 0.5

        user_services = service_response.get("response", [])
        if not user_services:
            return 0.5

        # Handle both list and string formats
        if isinstance(user_services, str):
            try:
                import json

                user_services = json.loads(user_services)
            except:
                user_services = [user_services]
        elif not isinstance(user_services, list):
            user_services = [str(user_services)]

        # Map services to broker specializations
        service_to_specialization = {
            "financial_planning": "financial_planning",
            "tax_planning": "tax_strategies",
            "estate_planning": "estate_planning",
            "retirement_planning": "retirement_planning",
            "education_planning": "education_planning",
            "insurance": "insurance_planning",
            "investment_management": "investment_management",
            "budgeting": "budgeting",
        }

        broker_specializations = [spec.name.lower() for spec in broker.specializations]

        # Calculate match score
        matches = 0
        for service in user_services:
            service_str = str(service)
            spec_needed = service_to_specialization.get(service_str, service_str)
            if any(
                spec_needed in broker_spec for broker_spec in broker_specializations
            ):
                matches += 1

        return matches / len(user_services) if user_services else 0.5

    def _score_investment_amount(
        self, broker: Broker, user_responses: Dict[str, Any]
    ) -> float:
        """Score based on investment amount compatibility"""
        amount_response = user_responses.get(
            "What is your approximate investment amount?", {}
        )
        if not amount_response:
            return 0.5

        user_amount = amount_response.get("response")
        if not user_amount:
            return 0.5

        # Handle both list and string formats
        if isinstance(user_amount, list):
            user_amount = user_amount[0] if user_amount else None
        elif isinstance(user_amount, dict):
            user_amount = user_amount.get("answer", str(user_amount))

        if not user_amount:
            return 0.5

        # Map amounts to minimum requirements (simplified)
        amount_requirements = {
            "less_10k": 0,
            "10k_50k": 10000,
            "50k_100k": 50000,
            "100k_500k": 100000,
            "500k_plus": 500000,
        }

        # Higher experience brokers typically handle larger accounts
        broker_minimums = {
            ExperienceLevel.JUNIOR: 0,
            ExperienceLevel.INTERMEDIATE: 10000,
            ExperienceLevel.SENIOR: 50000,
            ExperienceLevel.EXPERT: 100000,
        }

        user_min = amount_requirements.get(str(user_amount).lower(), 0)
        broker_min = broker_minimums.get(broker.experience_level, 0)

        # Score based on compatibility
        if user_min >= broker_min:
            return 1.0
        elif user_min >= broker_min * 0.5:
            return 0.7
        else:
            return 0.4

    def _score_sector_interests(
        self, broker: Broker, user_responses: Dict[str, Any]
    ) -> float:
        """Score based on sector interest alignment"""
        sector_response = user_responses.get(
            "Which sectors are you most interested in investing?", {}
        )
        if not sector_response:
            return 0.5

        user_sectors = sector_response.get("response", [])
        if not user_sectors:
            return 0.5

        # Handle both list and string formats
        if isinstance(user_sectors, str):
            try:
                import json

                user_sectors = json.loads(user_sectors)
            except:
                user_sectors = [user_sectors]
        elif not isinstance(user_sectors, list):
            user_sectors = [str(user_sectors)]

        # Check broker specializations for sector expertise
        broker_specializations = [spec.name.lower() for spec in broker.specializations]

        # Count matches
        matches = sum(
            1
            for sector in user_sectors
            if any(str(sector).lower() in spec for spec in broker_specializations)
        )

        return min(matches / len(user_sectors), 1.0) if user_sectors else 0.5

    def _score_communication_style(
        self, broker: Broker, user_responses: Dict[str, Any]
    ) -> float:
        """Score based on communication preferences"""
        comm_response = user_responses.get(
            "How would you prefer to communicate with your broker?", {}
        )
        if not comm_response:
            return 0.8  # Most brokers are flexible with communication

        # For now, return a high score as most brokers accommodate various styles
        return 0.9

    def _score_certification_match(
        self, broker: Broker, user_responses: Dict[str, Any]
    ) -> float:
        """Score based on certification preferences"""
        cert_response = user_responses.get(
            "Do you have any specific broker certification preferences?", {}
        )
        if not cert_response:
            return 0.8

        user_certs = cert_response.get("response", [])
        if not user_certs:
            return 0.8

        # Handle both list and string formats
        if isinstance(user_certs, str):
            try:
                import json

                user_certs = json.loads(user_certs)
            except:
                user_certs = [user_certs]
        elif not isinstance(user_certs, list):
            user_certs = [str(user_certs)]

        if "no_preference" in [str(cert).lower() for cert in user_certs]:
            return 1.0

        # Would need to add certifications to broker model
        # For now, return a moderate score
        return 0.7

    def _score_broker_performance(self, broker: Broker) -> float:
        """Score based on broker's performance metrics"""
        # Use average rating and success rate
        rating_score = broker.average_rating / 5.0 if broker.average_rating else 0.5
        success_score = broker.success_rate if broker.success_rate else 0.5

        # Weight rating more heavily as it's based on client feedback
        return (rating_score * 0.7) + (success_score * 0.3)


def generate_broker_matches(
    db: Session, user_id: str, save_to_db: bool = True
) -> List[Dict[str, Any]]:
    """
    Generate broker matches for a client and optionally save to database

    Args:
        db: Database session
        user_id: Client's user ID
        save_to_db: Whether to save matches to database

    Returns:
        List of match dictionaries with broker info and scores
    """
    algorithm = BrokerMatchingAlgorithm(db)
    matches = algorithm.calculate_matches(user_id, top_n=10)

    results = []
    for broker, score in matches:
        match_data = {
            "broker_id": broker.id,
            "user_id": user_id,
            "match_score": round(score, 3),
            "broker_name": broker.user.full_name,
            "company_name": broker.company_name,
            "experience_level": broker.experience_level.value,
            "average_rating": broker.average_rating,
            "specializations": [spec.name for spec in broker.specializations],
        }
        results.append(match_data)

        if save_to_db:
            # Check if match already exists
            existing_match = (
                db.query(BrokerClientMatch)
                .filter(
                    and_(
                        BrokerClientMatch.user_id == user_id,
                        BrokerClientMatch.broker_id == broker.id,
                        BrokerClientMatch.is_deleted == None,
                    )
                )
                .first()
            )

            if not existing_match:
                new_match = BrokerClientMatch(
                    user_id=user_id,
                    broker_id=broker.id,
                    match_score=round(score, 3),
                    status=MatchStatus.PENDING,
                    notes=f"Generated by matching algorithm on {datetime.utcnow().isoformat()}",
                )
                db.add(new_match)

    if save_to_db:
        db.commit()

    return results
