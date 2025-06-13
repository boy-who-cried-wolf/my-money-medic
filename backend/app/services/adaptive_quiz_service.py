"""
Adaptive Quiz Service for dynamic question generation and personalized quiz flows.

This service creates personalized quiz experiences by:
1. Analyzing user responses in real-time
2. Generating follow-up questions based on previous answers
3. Adapting question difficulty and focus areas
4. Providing AI-powered insights enhanced with psychology principles
"""

from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from datetime import datetime
import json
import uuid
import logging
from fastapi import HTTPException

from app.database.models.user import User, UserType
from app.database.models.quiz import (
    Quiz,
    QuizQuestion,
    UserQuizResponse,
    QuestionType,
    QuizCategory,
)
from app.database.models.broker import Broker
from app.ai.quiz_generator import QuizQuestionGenerator
from app.ai.gemini_service import GeminiService
from app.services.matching_algorithm import BrokerMatchingAlgorithm
from app.services.psychology_book_service import PsychologyBookService

logger = logging.getLogger(__name__)


class AdaptiveQuizService:
    """
    Service for creating adaptive, personalized quiz experiences enhanced with psychology.
    """

    def __init__(self, db: Session):
        self.db = db
        self.quiz_generator = QuizQuestionGenerator()
        self.gemini_service = GeminiService()
        self.psychology_service = PsychologyBookService()
        self.matching_algorithm = BrokerMatchingAlgorithm(db)

        # Simple in-memory session storage (in production, use Redis)
        self.session_storage = {}

        # Define quiz structure: exactly 10 questions
        self.total_questions = 10
        self.text_questions_limit = 2  # Only 2 text questions
        self.selection_questions_limit = 8  # 8 selection-based questions

    async def start_adaptive_quiz(self, user_id: str) -> Dict[str, Any]:
        """
        Start an adaptive quiz session for a user.

        Args:
            user_id: The user's ID

        Returns:
            Dict containing quiz session info and first question
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        # Create a new adaptive quiz session with structured plan
        quiz_session = {
            "session_id": str(uuid.uuid4()),
            "user_id": user_id,
            "started_at": datetime.utcnow().isoformat(),
            "current_question": 1,
            "total_questions": self.total_questions,
            "responses": [],
            "insights": [],
            "focus_areas": self._determine_initial_focus_areas(user),
            "question_plan": self._create_question_plan(),
            "text_questions_used": 0,
            "selection_questions_used": 0,
        }

        # Generate the first question using psychology enhancement
        first_question = await self._generate_psychology_enhanced_question(
            quiz_session, user
        )

        # Store first question text in session for repetition prevention
        quiz_session["current_question_text"] = first_question.get("text", "")

        return {
            "session": quiz_session,
            "question": first_question,
            "progress": {
                "current": 1,
                "total": self.total_questions,
                "completion_percentage": 10.0,  # 1/10 * 100
            },
        }

    def _create_question_plan(self) -> List[Dict[str, Any]]:
        """Create a structured plan for the 10 questions with optimal type distribution"""

        plan = [
            # Core foundation questions (selection-based)
            {
                "order": 1,
                "topic": "Investment goals and timeline",
                "category": "FINANCIAL_GOALS",
                "type": "single_choice",
            },
            {
                "order": 2,
                "topic": "Risk tolerance and emotional response",
                "category": "RISK_TOLERANCE",
                "type": "scale",
            },
            {
                "order": 3,
                "topic": "Investment experience and knowledge",
                "category": "EXPERIENCE",
                "type": "multiple_choice",
            },
            {
                "order": 4,
                "topic": "Decision-making psychology and style",
                "category": "PSYCHOLOGY",
                "type": "single_choice",
            },
            # Psychology-driven questions (selection-based)
            {
                "order": 5,
                "topic": "Social influence and peer behavior",
                "category": "PSYCHOLOGY",
                "type": "multiple_choice",
            },
            {
                "order": 6,
                "topic": "Communication preferences and learning style",
                "category": "PREFERENCES",
                "type": "single_choice",
            },
            {
                "order": 7,
                "topic": "Authority and expertise preferences",
                "category": "PSYCHOLOGY",
                "type": "scale",
            },
            {
                "order": 8,
                "topic": "Financial anxiety and loss aversion",
                "category": "PSYCHOLOGY",
                "type": "single_choice",
            },
            # Deep insight questions (text-based for detailed analysis)
            {
                "order": 9,
                "topic": "Past financial experiences and lessons",
                "category": "EXPERIENCE",
                "type": "text",
            },
            {
                "order": 10,
                "topic": "Future financial vision and aspirations",
                "category": "FINANCIAL_GOALS",
                "type": "text",
            },
        ]

        return plan

    async def submit_response_and_get_next(
        self, session_data: Dict[str, Any], response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Submit a response and get the next adaptive question.

        Args:
            session_data: Current quiz session data
            response: User's response to current question

        Returns:
            Dict containing next question and updated session
        """
        logger.info(f"Processing response in submit_response_and_get_next: {json.dumps(response)}")
        
        # Store the response with question text for repetition prevention
        current_question_text = session_data.get("current_question_text", "")
        response_data = {
            "question_number": session_data["current_question"],
            "response": response.get("answer"),
            "question_text": current_question_text,
            "timestamp": datetime.utcnow().isoformat(),
        }
        logger.info(f"Formatted response data for storage: {json.dumps(response_data)}")
        
        session_data["responses"].append(response_data)

        # Analyze the response for psychology-enhanced insights
        try:
            insights = await self._analyze_response_with_psychology(session_data, response)
            session_data["insights"].extend(insights)
            logger.info(f"Generated insights: {json.dumps(insights)}")
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}", exc_info=True)
            insights = []

        # Update focus areas based on response
        try:
            session_data["focus_areas"] = await self._update_focus_areas(
                session_data, response
            )
            logger.info(f"Updated focus areas: {json.dumps(session_data['focus_areas'])}")
        except Exception as e:
            logger.error(f"Error updating focus areas: {str(e)}", exc_info=True)

        # Check if we've reached 10 questions
        if session_data["current_question"] >= self.total_questions:
            # Complete the quiz
            return await self._complete_quiz(session_data, "total_questions_completed")

        # Generate next question
        session_data["current_question"] += 1
        next_question = await self._generate_psychology_enhanced_question(
            session_data,
            self.db.query(User).filter(User.id == session_data["user_id"]).first(),
        )

        # Store current question text in session for next iteration
        session_data["current_question_text"] = next_question.get("text", "")

        # Update progress
        progress = {
            "current": session_data["current_question"],
            "total": self.total_questions,
            "completion_percentage": (
                session_data["current_question"] / self.total_questions
            )
            * 100,
        }

        logger.info(f"Generated next question: {json.dumps(next_question)}")
        logger.info(f"Updated progress: {json.dumps(progress)}")

        return {
            "session": session_data,
            "question": next_question,
            "progress": progress,
            "insights": insights[-2:] if insights else [],  # Last 2 insights
        }

    async def _generate_psychology_enhanced_question(
        self, session_data: Dict[str, Any], user: User
    ) -> Dict[str, Any]:
        """Generate the next question using psychology enhancement"""

        current_question_num = session_data["current_question"]
        question_plan = session_data.get("question_plan", [])

        # Get the planned question details
        if current_question_num <= len(question_plan):
            planned_question = question_plan[current_question_num - 1]
            topic = planned_question["topic"]
            category = planned_question["category"]
            question_type = planned_question["type"]
        else:
            # Fallback if plan is missing
            topic, category = await self._determine_next_topic(session_data)
            question_type = self._choose_question_type_controlled(session_data)

        # Get existing questions for repetition prevention
        existing_questions = self._get_previous_questions(session_data)

        # Try psychology-enhanced generation first
        question_data = (
            await self.psychology_service.generate_psychology_enhanced_question(
                topic=topic,
                category=category,
                question_type=question_type,
                existing_questions=existing_questions,
            )
        )

        if not question_data:
            # Fallback to standard AI generation
            question_data = await self.quiz_generator.create_ai_question_data(
                topic=topic,
                category=category,
                question_type_str=question_type,
                order=current_question_num,
                existing_question_texts=existing_questions,
            )

        if not question_data:
            # Final fallback to predefined question
            question_data = self._get_fallback_question(
                topic, category, current_question_num
            )

        # Track question type usage
        if question_type == "text":
            session_data["text_questions_used"] = (
                session_data.get("text_questions_used", 0) + 1
            )
        else:
            session_data["selection_questions_used"] = (
                session_data.get("selection_questions_used", 0) + 1
            )

        # Add enhanced adaptive context with psychology insights
        question_data["adaptive_context"] = {
            "focus_area": topic,
            "reasoning": f"Question {current_question_num}/10: {topic}",
            "importance": self._calculate_question_importance(topic, session_data),
            "psychology_principle": question_data.get(
                "psychology_insight", "Behavioral analysis"
            ),
            "broker_matching_value": question_data.get(
                "broker_matching_value", "Helps determine optimal broker match"
            ),
        }

        # Add question metadata
        question_data.update(
            {
                "id": str(uuid.uuid4()),
                "order": current_question_num,
                "weight": 1,
                "is_ai_generated": True,
                "psychology_enhanced": True,
            }
        )

        return question_data

    def _choose_question_type_controlled(self, session_data: Dict[str, Any]) -> str:
        """Choose question type based on controlled distribution (8 selection, 2 text)"""

        text_used = session_data.get("text_questions_used", 0)
        selection_used = session_data.get("selection_questions_used", 0)
        current_question = session_data.get("current_question", 1)

        # Force text questions in positions 9 and 10 for deep insights
        if current_question >= 9 and text_used < self.text_questions_limit:
            return "text"

        # If we've used up text questions, use selection
        if text_used >= self.text_questions_limit:
            return self._get_selection_question_type(session_data)

        # If we've used up selection questions, use text
        if selection_used >= self.selection_questions_limit:
            return "text"

        # Early questions should be selection-based for engagement
        if current_question <= 8:
            return self._get_selection_question_type(session_data)

        # Default to selection if unsure
        return self._get_selection_question_type(session_data)

    def _get_selection_question_type(self, session_data: Dict[str, Any]) -> str:
        """Get appropriate selection-based question type for variety"""

        responses = session_data.get("responses", [])
        question_types_used = [
            r.get("question_type") for r in responses if r.get("question_type")
        ]

        # Ensure variety in selection types
        if question_types_used.count("single_choice") < 4:
            return "single_choice"
        elif question_types_used.count("multiple_choice") < 3:
            return "multiple_choice"
        elif question_types_used.count("scale") < 2:
            return "scale"
        else:
            return "single_choice"  # Default

    async def _analyze_response_with_psychology(
        self, session_data: Dict[str, Any], response: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Analyze user response using psychology principles"""
        logger.info("Starting _analyze_response_with_psychology")
        logger.info(f"Session data type: {type(session_data)}")
        logger.info(f"Session data: {json.dumps(session_data)}")
        logger.info(f"Response type: {type(response)}")
        logger.info(f"Response data: {json.dumps(response)}")

        # Get both basic insights and psychology-enhanced insights
        try:
            logger.info("Calling _analyze_response for basic insights")
            basic_insights = await self._analyze_response(session_data, response)
            logger.info(f"Basic insights generated: {json.dumps(basic_insights)}")
        except Exception as e:
            logger.error(f"Error in _analyze_response: {str(e)}", exc_info=True)
            basic_insights = []

        # Get psychology-based insights from the psychology service
        try:
            logger.info("Getting responses from session data")
            responses = session_data.get("responses", [])
            logger.info(f"Responses type: {type(responses)}")
            logger.info(f"Responses data: {json.dumps(responses)}")

            # Log each response in detail
            for i, resp in enumerate(responses):
                logger.info(f"Response {i} type: {type(resp)}")
                logger.info(f"Response {i} data: {json.dumps(resp)}")
                if isinstance(resp, dict):
                    logger.info(f"Response {i} keys: {resp.keys()}")
                    if "response" in resp:
                        logger.info(f"Response {i} response type: {type(resp['response'])}")
                        logger.info(f"Response {i} response data: {resp['response']}")

            logger.info("Calling psychology service for insights")
            psychology_insights = self.psychology_service.get_psychology_based_insights(responses)
            logger.info(f"Psychology insights generated: {json.dumps(psychology_insights)}")
        except Exception as e:
            logger.error(f"Error in psychology service: {str(e)}", exc_info=True)
            logger.error(f"Error occurred with responses: {json.dumps(responses)}")
            psychology_insights = []

        logger.info("Combining insights")
        all_insights = basic_insights + psychology_insights
        logger.info(f"Total insights generated: {len(all_insights)}")
        logger.info(f"Final insights: {json.dumps(all_insights)}")

        return all_insights

    async def _should_continue_quiz(
        self, session_data: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """Determine if quiz should continue - always complete all 10 questions"""

        responses = session_data.get("responses", [])

        # Always complete all 10 questions
        if len(responses) < self.total_questions:
            return True, "questions_remaining"

        return False, "all_questions_completed"

    async def _generate_final_insights(
        self, session_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate comprehensive final insights enhanced with psychology principles"""

        responses = session_data.get("responses", [])
        existing_insights = session_data.get("insights", [])

        # Enhanced prompt for much more personalized insights
        prompt = f"""
        Create 4 HIGHLY PERSONALIZED insights for a client based on their quiz responses. 
        Make each insight feel like it came from a financial advisor who really knows them.

        Quiz Responses:
        {json.dumps(responses[-10:], indent=2)}

        RULES:
        - Write in second person ("You" statements)
        - Be specific about their personality and preferences
        - Include actionable broker matching advice
        - Make each insight unique and personal
        - Keep each insight under 100 characters total

        Format EXACTLY like this:
        **[Insight Title]**: [Personalized insight about their style/needs]

        Examples of GOOD insights:
        **Your Decision Style**: You research thoroughly before investing - find detail-oriented brokers.
        **Risk Comfort Zone**: You prefer steady growth over quick wins - seek conservative specialists.
        **Communication Match**: You value clear explanations - choose brokers who teach as they advise.
        **Investment Mindset**: You're building long-term wealth - find brokers with retirement expertise.

        Generate exactly 4 personalized insights:
        """

        try:
            ai_insights = await self.gemini_service.generate_text(prompt)

            # Parse AI insights
            final_insights = []
            if ai_insights:
                lines = ai_insights.split("\n")
                for line in lines:
                    if line.strip().startswith("**") and ":" in line:
                        insight_text = line.strip()
                        if insight_text and len(insight_text) < 200:
                            final_insights.append(
                                {
                                    "type": "personalized_insight",
                                    "insight": insight_text,
                                    "confidence": 0.90,
                                    "source": "ai_enhanced_analysis",
                                    "is_actionable": True,
                                }
                            )

            # If we don't have 4 good insights, add personalized fallbacks based on responses
            if len(final_insights) < 4:
                personalized_fallbacks = self._create_personalized_fallbacks(responses)

                for fallback in personalized_fallbacks:
                    if len(final_insights) < 4:
                        final_insights.append(fallback)

            return final_insights[:4]

        except Exception as e:
            print(f"Error generating personalized insights: {e}")
            # Return personalized fallback insights
            return self._create_personalized_fallbacks(responses)

    def _create_personalized_fallbacks(
        self, responses: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create personalized fallback insights based on response analysis"""

        fallbacks = []

        # Analyze responses for personalization
        response_analysis = self._analyze_response_patterns(responses)

        # Decision-making style insights
        if response_analysis.get("decision_style") == "analytical":
            fallbacks.append(
                {
                    "type": "personalized_insight",
                    "insight": "**Data Driven**: You love details and research - seek brokers with comprehensive reports.",
                    "confidence": 0.85,
                    "source": "pattern_analysis",
                    "is_actionable": True,
                }
            )
        elif response_analysis.get("decision_style") == "social":
            fallbacks.append(
                {
                    "type": "personalized_insight",
                    "insight": "**Trust Builder**: You value referrals and testimonials - find well-reviewed brokers.",
                    "confidence": 0.85,
                    "source": "pattern_analysis",
                    "is_actionable": True,
                }
            )
        else:
            fallbacks.append(
                {
                    "type": "personalized_insight",
                    "insight": "**Balanced Approach**: You consider multiple factors - seek experienced, well-rounded brokers.",
                    "confidence": 0.80,
                    "source": "pattern_analysis",
                    "is_actionable": True,
                }
            )

        # Risk tolerance insights
        if response_analysis.get("risk_level") == "conservative":
            fallbacks.append(
                {
                    "type": "personalized_insight",
                    "insight": "**Safety First**: You prioritize security - choose brokers specializing in stable investments.",
                    "confidence": 0.85,
                    "source": "pattern_analysis",
                    "is_actionable": True,
                }
            )
        elif response_analysis.get("risk_level") == "aggressive":
            fallbacks.append(
                {
                    "type": "personalized_insight",
                    "insight": "**Growth Focused**: You're comfortable with risk - find brokers with strong growth strategies.",
                    "confidence": 0.85,
                    "source": "pattern_analysis",
                    "is_actionable": True,
                }
            )
        else:
            fallbacks.append(
                {
                    "type": "personalized_insight",
                    "insight": "**Balanced Investor**: You want growth with protection - seek diversification experts.",
                    "confidence": 0.80,
                    "source": "pattern_analysis",
                    "is_actionable": True,
                }
            )

        # Communication style insights
        if response_analysis.get("communication") == "visual":
            fallbacks.append(
                {
                    "type": "personalized_insight",
                    "insight": "**Visual Learner**: You prefer charts and graphs - find brokers with great presentations.",
                    "confidence": 0.80,
                    "source": "pattern_analysis",
                    "is_actionable": True,
                }
            )
        else:
            fallbacks.append(
                {
                    "type": "personalized_insight",
                    "insight": "**Clear Communication**: You value straightforward advice - choose transparent brokers.",
                    "confidence": 0.80,
                    "source": "pattern_analysis",
                    "is_actionable": True,
                }
            )

        # Investment approach insight
        fallbacks.append(
            {
                "type": "personalized_insight",
                "insight": "**Long-term Thinker**: You're building wealth over time - find brokers who share your vision.",
                "confidence": 0.80,
                "source": "pattern_analysis",
                "is_actionable": True,
            }
        )

        return fallbacks

    async def _analyze_response(
        self, session_data: Dict[str, Any], response: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Analyze user response to generate insights."""

        insights = []

        # Basic response analysis
        if response.get("answer"):
            answer = response["answer"]

            # Risk tolerance insights
            if isinstance(answer, str):
                if any(
                    word in answer.lower()
                    for word in ["conservative", "safe", "low risk"]
                ):
                    insights.append(
                        {
                            "type": "risk_profile",
                            "insight": "User shows preference for conservative investment approaches",
                            "confidence": 0.8,
                        }
                    )
                elif any(
                    word in answer.lower()
                    for word in ["aggressive", "high risk", "growth"]
                ):
                    insights.append(
                        {
                            "type": "risk_profile",
                            "insight": "User appears comfortable with higher-risk investments",
                            "confidence": 0.8,
                        }
                    )

            # Investment amount insights
            if isinstance(answer, str) and any(
                amount in answer for amount in ["100k", "500k", "million"]
            ):
                insights.append(
                    {
                        "type": "investment_capacity",
                        "insight": "User indicates significant investment capacity",
                        "confidence": 0.9,
                    }
                )

        return insights

    async def _update_focus_areas(
        self, session_data: Dict[str, Any], response: Dict[str, Any]
    ) -> List[str]:
        """Update focus areas based on response analysis."""

        current_areas = session_data.get("focus_areas", [])

        # Add new focus areas based on response
        answer = response.get("answer", "")

        if isinstance(answer, str):
            if "retirement" in answer.lower():
                if "retirement_planning" not in current_areas:
                    current_areas.append("retirement_planning")
            elif "tax" in answer.lower():
                if "tax_optimization" not in current_areas:
                    current_areas.append("tax_optimization")
            elif "estate" in answer.lower():
                if "estate_planning" not in current_areas:
                    current_areas.append("estate_planning")

        return current_areas

    async def _complete_quiz(
        self, session_data: Dict[str, Any], reason: str
    ) -> Dict[str, Any]:
        """Complete the quiz and generate final insights and matches."""

        user_id = session_data["user_id"]

        # Save responses to database
        await self._save_responses_to_db(session_data)

        # Generate comprehensive insights
        final_insights = await self._generate_final_insights(session_data)

        # Generate broker matches
        matches = await self._generate_matches(user_id)

        # Generate personalized recommendations
        recommendations = await self._generate_recommendations(session_data, matches)

        return {
            "completed": True,
            "reason": reason,
            "session": session_data,
            "insights": final_insights,
            "matches": matches[:5],  # Top 5 matches
            "recommendations": recommendations,
            "completion_time": datetime.utcnow().isoformat(),
        }

    async def _save_responses_to_db(self, session_data: Dict[str, Any]) -> None:
        """Save quiz responses to database."""

        user_id = session_data["user_id"]
        responses = session_data.get("responses", [])

        # Create or get adaptive quiz record
        quiz = (
            self.db.query(Quiz)
            .filter(Quiz.title == "Adaptive Broker Matching Quiz")
            .first()
        )

        if not quiz:
            quiz = Quiz(
                id=str(uuid.uuid4()),
                title="Adaptive Broker Matching Quiz",
                description="AI-powered adaptive quiz for personalized broker matching",
                category=QuizCategory.BROKER_MATCHING,
            )
            self.db.add(quiz)
            self.db.flush()

        # Save each response
        for response_data in responses:
            # Create a question record for this adaptive question
            question = QuizQuestion(
                id=str(uuid.uuid4()),
                quiz_id=quiz.id,
                text=response_data.get(
                    "question_text",
                    f"Adaptive Question {response_data['question_number']}",
                ),
                question_type=QuestionType.TEXT,  # Simplified for adaptive questions
                order=response_data["question_number"],
                weight=1,
            )
            self.db.add(question)
            self.db.flush()

            # Save user response
            user_response = UserQuizResponse(
                id=str(uuid.uuid4()),
                user_id=user_id,
                question_id=question.id,
                response=json.dumps(response_data["response"]),
            )
            self.db.add(user_response)

        self.db.commit()

    async def _generate_matches(self, user_id: str) -> List[Dict[str, Any]]:
        """Generate broker matches using the matching algorithm."""

        try:
            from app.services.matching_algorithm import generate_broker_matches

            matches = generate_broker_matches(self.db, user_id, save_to_db=True)
            return matches
        except Exception as e:
            print(f"Error generating matches: {e}")
            return []

    async def _generate_recommendations(
        self, session_data: Dict[str, Any], matches: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate personalized recommendations based on quiz results and matches."""

        recommendations = []
        responses = session_data.get("responses", [])
        insights = session_data.get("insights", [])

        # Analyze response patterns to create specific recommendations
        response_analysis = self._analyze_response_patterns(responses)

        # Decision-making style recommendations - make them punchy
        if response_analysis.get("decision_style") == "social":
            recommendations.append("✓ Find brokers with excellent client testimonials")
        elif response_analysis.get("decision_style") == "analytical":
            recommendations.append("✓ Choose data-driven brokers with detailed reports")
        elif response_analysis.get("decision_style") == "intuitive":
            recommendations.append(
                "✓ Look for brokers who explain the big picture clearly"
            )
        else:
            recommendations.append(
                "✓ Pick brokers who adapt to your communication style"
            )

        # Risk tolerance recommendations - short and specific
        if response_analysis.get("risk_level") == "conservative":
            recommendations.append("✓ Focus on income-generating, stable investments")
        elif response_analysis.get("risk_level") == "aggressive":
            recommendations.append("✓ Seek growth-focused, high-return strategies")
        else:
            recommendations.append("✓ Target balanced portfolios with moderate risk")

        # Communication preference recommendations - actionable
        if response_analysis.get("communication") == "visual":
            recommendations.append(
                "✓ Prioritize brokers with excellent charts and visuals"
            )
        elif response_analysis.get("communication") == "personal":
            recommendations.append(
                "✓ Choose brokers who offer regular personal meetings"
            )
        else:
            recommendations.append(
                "✓ Find brokers who use your preferred communication methods"
            )

        # Match-based recommendations - personalized
        if matches and len(matches) > 0:
            top_match = matches[0]
            broker_name = top_match.get("broker_name", "your top match")
            match_score = top_match.get("match_score", 0) * 100
            recommendations.append(
                f"✓ Best match: {broker_name} ({match_score:.0f}% compatible)"
            )
        else:
            recommendations.append("✓ We'll find brokers perfect for your profile")

        return recommendations[:4]  # Keep it to 4 recommendations max

    def _analyze_response_patterns(
        self, responses: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """Analyze response patterns to determine client preferences"""

        patterns = {
            "decision_style": "balanced",
            "risk_level": "moderate",
            "communication": "mixed",
        }

        # Simple pattern analysis
        for response in responses:
            try:
                # Handle both string and dictionary responses
                if isinstance(response, str):
                    answer = response.lower()
                elif isinstance(response, dict):
                    resp_data = response.get("response", {})
                    if isinstance(resp_data, str):
                        answer = resp_data.lower()
                    elif isinstance(resp_data, dict):
                        answer = str(resp_data.get("answer", "")).lower()
                    else:
                        answer = str(resp_data).lower()
                else:
                    answer = str(response).lower()

                logger.info(f"Processing answer: {answer}")

                # Decision-making style patterns
                if any(word in answer for word in ["friends", "family", "others", "social"]):
                    patterns["decision_style"] = "social"
                elif any(word in answer for word in ["research", "analyze", "data", "study"]):
                    patterns["decision_style"] = "analytical"
                elif any(word in answer for word in ["gut", "feeling", "intuition", "instinct"]):
                    patterns["decision_style"] = "intuitive"

                # Risk level patterns
                if any(word in answer for word in ["safe", "secure", "conservative", "protect", "worried"]):
                    patterns["risk_level"] = "conservative"
                elif any(word in answer for word in ["aggressive", "growth", "risk", "opportunity", "high"]):
                    patterns["risk_level"] = "aggressive"

                # Communication patterns
                if any(word in answer for word in ["charts", "graphs", "visual", "reports"]):
                    patterns["communication"] = "visual"
                elif any(word in answer for word in ["meeting", "discussion", "talk", "conversation"]):
                    patterns["communication"] = "personal"

            except Exception as e:
                logger.error(f"Error processing response pattern: {str(e)}")
                logger.error(f"Problematic response: {json.dumps(response)}")
                continue

        logger.info(f"Final patterns: {json.dumps(patterns)}")
        return patterns

    def _get_previous_questions(self, session_data: Dict[str, Any]) -> List[str]:
        """Get list of previous question texts to avoid repetition."""

        responses = session_data.get("responses", [])
        question_texts = []

        # Extract question texts from responses
        for response in responses:
            question_text = response.get("question_text", "")
            if question_text and question_text not in question_texts:
                question_texts.append(question_text)

        # Also include current question text if available
        current_question_text = session_data.get("current_question_text", "")
        if current_question_text and current_question_text not in question_texts:
            question_texts.append(current_question_text)

        return question_texts

    def _get_fallback_question(
        self, topic: str, category: str, order: int
    ) -> Dict[str, Any]:
        """Get a fallback question if AI generation fails."""

        fallback_questions = {
            "Investment goals and timeline": {
                "text": "What's your main financial goal for the next 10 years?",
                "question_type": "single_choice",
                "options": [
                    {"value": "retirement", "label": "Build retirement fund"},
                    {"value": "wealth_growth", "label": "Grow my wealth"},
                    {"value": "income", "label": "Generate income"},
                    {"value": "education", "label": "Save for education"},
                ],
            },
            "Risk tolerance and emotional response": {
                "text": "How do you feel about investment ups and downs?",
                "question_type": "scale",
                "options": {
                    "min": 1,
                    "max": 5,
                    "min_label": "Very worried",
                    "max_label": "Totally fine",
                },
            },
            "Investment experience and knowledge": {
                "text": "How would you describe your investment experience?",
                "question_type": "multiple_choice",
                "options": [
                    {"value": "beginner", "label": "Just starting out"},
                    {"value": "intermediate", "label": "Some experience"},
                    {"value": "advanced", "label": "Pretty experienced"},
                    {"value": "expert", "label": "Very experienced"},
                ],
            },
            "Decision-making psychology and style": {
                "text": "When making big financial decisions, you usually:",
                "question_type": "single_choice",
                "options": [
                    {"value": "research", "label": "Research everything first"},
                    {"value": "intuition", "label": "Trust your gut"},
                    {"value": "advice", "label": "Ask for advice"},
                    {"value": "quick", "label": "Decide quickly"},
                ],
            },
            "Social influence and peer behavior": {
                "text": "Who influences your financial decisions most?",
                "question_type": "multiple_choice",
                "options": [
                    {"value": "family", "label": "Family members"},
                    {"value": "friends", "label": "Close friends"},
                    {"value": "experts", "label": "Financial experts"},
                    {"value": "myself", "label": "Just myself"},
                ],
            },
            "Communication preferences and learning style": {
                "text": "How do you prefer to learn about investments?",
                "question_type": "single_choice",
                "options": [
                    {"value": "charts", "label": "Charts and graphs"},
                    {"value": "conversation", "label": "Personal discussion"},
                    {"value": "reports", "label": "Detailed reports"},
                    {"value": "videos", "label": "Videos and demos"},
                ],
            },
            "Authority and expertise preferences": {
                "text": "How important are professional credentials to you?",
                "question_type": "scale",
                "options": {
                    "min": 1,
                    "max": 5,
                    "min_label": "Not important",
                    "max_label": "Very important",
                },
            },
            "Financial anxiety and loss aversion": {
                "text": "What worries you most about investing?",
                "question_type": "single_choice",
                "options": [
                    {"value": "losing_money", "label": "Losing money"},
                    {"value": "bad_timing", "label": "Bad timing"},
                    {"value": "wrong_choice", "label": "Wrong investments"},
                    {"value": "market_crash", "label": "Market crashes"},
                ],
            },
            "Past financial experiences and lessons": {
                "text": "What's one financial lesson you learned the hard way?",
                "question_type": "text",
                "options": None,
            },
            "Future financial vision and aspirations": {
                "text": "Describe your ideal financial future in one sentence.",
                "question_type": "text",
                "options": None,
            },
        }

        fallback = fallback_questions.get(
            topic,
            {
                "text": f"How do you feel about {topic.lower()}?",
                "question_type": "text",
                "options": None,
            },
        )

        return {
            "id": str(uuid.uuid4()),
            "text": fallback["text"],
            "question_type": fallback["question_type"],
            "options": fallback.get("options"),
            "order": order,
            "weight": 1,
        }

    def _summarize_responses(self, responses: List[Dict[str, Any]]) -> str:
        """Create a summary of user responses for AI analysis."""

        if not responses:
            return "No responses yet"

        summary_parts = []
        for i, response in enumerate(responses[-3:], 1):  # Last 3 responses
            answer = response.get("response", {}).get("answer", "")
            summary_parts.append(f"Q{i}: {str(answer)[:100]}")

        return "; ".join(summary_parts)

    def _calculate_question_importance(
        self, topic: str, session_data: Dict[str, Any]
    ) -> float:
        """Calculate the importance of a question topic for this user."""

        # Base importance
        importance = 0.5

        # Increase importance for focus areas
        focus_areas = session_data.get("focus_areas", [])
        if any(area in topic.lower() for area in focus_areas):
            importance += 0.3

        # Increase importance for under-explored areas
        responses = session_data.get("responses", [])
        topic_mentions = sum(1 for r in responses if topic.lower() in str(r).lower())
        if topic_mentions == 0:
            importance += 0.2

        return min(importance, 1.0)

    async def _determine_next_topic(
        self, session_data: Dict[str, Any]
    ) -> Tuple[str, str]:
        """Determine the next question topic based on session context."""

        focus_areas = session_data.get("focus_areas", [])
        responses = session_data.get("responses", [])
        current_question = session_data.get("current_question", 1)

        # Core topics that should always be covered
        core_topics = [
            ("Investment goals and timeline", "FINANCIAL_GOALS"),
            ("Risk tolerance and comfort level", "RISK_TOLERANCE"),
            ("Investment experience and knowledge", "EXPERIENCE"),
            ("Service preferences and communication style", "PREFERENCES"),
        ]

        # Advanced topics based on responses
        advanced_topics = [
            ("Specific investment sectors of interest", "PREFERENCES"),
            ("Tax planning considerations", "FINANCIAL_GOALS"),
            ("Estate planning needs", "FINANCIAL_GOALS"),
            ("International investment exposure", "PREFERENCES"),
            ("Alternative investment interest", "EXPERIENCE"),
            ("Retirement planning specifics", "FINANCIAL_GOALS"),
        ]

        # For first few questions, stick to core topics
        if current_question <= 4:
            topic_index = (current_question - 1) % len(core_topics)
            return core_topics[topic_index]

        # For later questions, use focus areas and response analysis
        if focus_areas:
            # Use AI to determine most relevant next topic
            prompt = f"""
            Based on the user's quiz responses and focus areas, determine the most relevant next topic to explore.
            
            Focus areas: {', '.join(focus_areas)}
            Previous responses summary: {self._summarize_responses(responses)}
            Question number: {current_question}
            
            Choose from these topics:
            {[topic[0] for topic in advanced_topics]}
            
            Return only the topic name that would provide the most valuable insights for broker matching.
            """

            try:
                ai_topic = await self.gemini_service.generate_text(prompt)
                # Find matching topic
                for topic, category in advanced_topics:
                    if ai_topic and topic.lower() in ai_topic.lower():
                        return (topic, category)
            except:
                pass

        # Fallback to advanced topics in order
        topic_index = (current_question - 5) % len(advanced_topics)
        return advanced_topics[topic_index]

    def _determine_initial_focus_areas(self, user: User) -> List[str]:
        """Determine initial focus areas based on user profile."""

        focus_areas = ["investment_goals", "risk_assessment", "psychology_analysis"]

        # Add focus areas based on user type
        if user.user_type == UserType.CLIENT:
            focus_areas.extend(["broker_preferences", "service_needs"])

        return focus_areas

    async def generate_insights(self, session_id: str) -> Dict[str, Any]:
        """Generate insights based on quiz responses."""

        try:
            session = self.session_storage.get(session_id)
            if not session:
                return {
                    "session_id": session_id,
                    "insights": [],
                    "recommendations": [],
                    "investment_profile": {
                        "investment_horizon": "Not assessed",
                        "risk_tolerance": "Not assessed",
                        "preferred_focus": "Not assessed",
                    },
                    "matches": [],
                    "total_responses": 0,
                    "completion_status": "no_data",
                    "confidence_score": 0.0,
                }

            responses = session.get("responses", [])

            # Generate investment profile summary first (simpler)
            investment_profile = self._generate_investment_profile(responses)

            # Generate final insights with psychology enhancement
            try:
                final_insights = await self._generate_final_insights(session)
            except Exception as e:
                final_insights = []

            # Get broker matches
            try:
                matches = await self._get_broker_matches(session_id)
            except Exception as e:
                matches = []

            # Generate recommendations
            try:
                recommendations = await self._generate_recommendations(session, matches)
            except Exception as e:
                recommendations = []

            return {
                "session_id": session_id,
                "insights": final_insights,
                "recommendations": recommendations,
                "investment_profile": investment_profile,
                "matches": matches,
                "total_responses": len(responses),
                "completion_status": (
                    "completed" if len(responses) >= 5 else "in_progress"
                ),
                "confidence_score": 0.90,
            }

        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            return {
                "session_id": session_id,
                "insights": [],
                "recommendations": [],
                "investment_profile": {
                    "investment_horizon": "Error",
                    "risk_tolerance": "Error",
                    "preferred_focus": "Error",
                },
                "matches": [],
                "total_responses": 0,
                "completion_status": "error",
                "confidence_score": 0.0,
                "error": str(e),
            }

    def _set_session(self, session_id: str, session_data: Dict[str, Any]):
        """Store session data"""
        self.session_storage[session_id] = session_data

    def _get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data"""
        return self.session_storage.get(session_id)

    async def _get_broker_matches(self, session_id: str) -> List[Dict[str, Any]]:
        """Get broker matches for the session"""
        try:
            session = self.session_storage.get(session_id)
            if not session:
                return []

            user_id = session.get("user_id")
            if not user_id:
                return []

            # Generate matches using the matching algorithm
            matches = await self._generate_matches(user_id)

            # If no matches from algorithm, create some sample matches for demo
            if not matches or len(matches) == 0:
                from app.database.models.broker import Broker
                from app.database.models.user import User

                # Get some actual brokers from database
                brokers = self.db.query(Broker).limit(3).all()

                if brokers:
                    demo_matches = []
                    for i, broker in enumerate(brokers):
                        user = (
                            self.db.query(User)
                            .filter(User.id == broker.user_id)
                            .first()
                        )
                        if user:
                            demo_matches.append(
                                {
                                    "broker_id": broker.id,
                                    "broker_name": f"{user.first_name} {user.last_name}",
                                    "match_score": 0.85 - (i * 0.05),  # 85%, 80%, 75%
                                    "specializations": [
                                        spec.name for spec in broker.specializations
                                    ],
                                    "experience_level": (
                                        broker.experience_level.value
                                        if broker.experience_level
                                        else "Intermediate"
                                    ),
                                    "rating": 4.5 - (i * 0.1),
                                    "location": (
                                        f"{broker.address_city}, {broker.address_state}"
                                        if broker.address_city
                                        else "Available"
                                    ),
                                }
                            )
                    if demo_matches:
                        return demo_matches

                # Fallback to hardcoded demo brokers
                return [
                    {
                        "broker_id": "demo_1",
                        "broker_name": "Sarah Johnson",
                        "match_score": 0.92,
                        "specializations": [
                            "Retirement Planning",
                            "Investment Management",
                        ],
                        "experience_level": "Senior",
                        "rating": 4.8,
                        "location": "Melbourne, VIC",
                    },
                    {
                        "broker_id": "demo_2",
                        "broker_name": "Michael Chen",
                        "match_score": 0.88,
                        "specializations": ["Real Estate Investment", "Tax Planning"],
                        "experience_level": "Expert",
                        "rating": 4.7,
                        "location": "Sydney, NSW",
                    },
                    {
                        "broker_id": "demo_3",
                        "broker_name": "Emma Thompson",
                        "match_score": 0.84,
                        "specializations": ["Financial Planning", "Risk Management"],
                        "experience_level": "Senior",
                        "rating": 4.6,
                        "location": "Brisbane, QLD",
                    },
                ]

            return matches
        except Exception as e:
            logger.error(f"Error getting broker matches: {e}")
            # Return demo matches as fallback
            return [
                {
                    "broker_id": "demo_1",
                    "broker_name": "Sarah Johnson",
                    "match_score": 0.92,
                    "specializations": ["Retirement Planning", "Investment Management"],
                    "experience_level": "Senior",
                    "rating": 4.8,
                    "location": "Melbourne, VIC",
                },
                {
                    "broker_id": "demo_2",
                    "broker_name": "Michael Chen",
                    "match_score": 0.88,
                    "specializations": ["Real Estate Investment", "Tax Planning"],
                    "experience_level": "Expert",
                    "rating": 4.7,
                    "location": "Sydney, NSW",
                },
                {
                    "broker_id": "demo_3",
                    "broker_name": "Emma Thompson",
                    "match_score": 0.84,
                    "specializations": ["Financial Planning", "Risk Management"],
                    "experience_level": "Senior",
                    "rating": 4.6,
                    "location": "Brisbane, QLD",
                },
            ]

    def _generate_investment_profile(
        self, responses: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """Generate a clean investment profile summary from responses"""

        profile = {
            "investment_horizon": "Medium-term (3-7 years)",
            "risk_tolerance": "Moderate",
            "preferred_focus": "Balanced Growth",
        }

        # Analyze responses to determine profile
        response_texts = []
        for response in responses:
            if response.get("response"):
                answer = response["response"].get("answer", "")
                if answer:
                    # Convert to string and then to lowercase
                    answer_str = str(answer).lower()
                    response_texts.append(answer_str)

        # Determine investment horizon
        all_text = " ".join(response_texts)
        if any(word in all_text for word in ["retirement", "long", "future", "years"]):
            profile["investment_horizon"] = "Long-term (7+ years)"
        elif any(word in all_text for word in ["short", "soon", "immediate", "quick"]):
            profile["investment_horizon"] = "Short-term (1-3 years)"

        # Determine risk tolerance
        if any(
            word in all_text for word in ["safe", "conservative", "stable", "secure"]
        ):
            profile["risk_tolerance"] = "Conservative"
        elif any(
            word in all_text for word in ["aggressive", "risky", "growth", "high"]
        ):
            profile["risk_tolerance"] = "Aggressive"

        # Determine preferred focus
        if any(word in all_text for word in ["income", "dividends", "steady"]):
            profile["preferred_focus"] = "Income Generation"
        elif any(word in all_text for word in ["growth", "capital", "appreciate"]):
            profile["preferred_focus"] = "Capital Growth"
        elif any(word in all_text for word in ["research", "analysis", "study"]):
            profile["preferred_focus"] = "Research-Based"

        return profile

    async def restore_quiz_session(
        self, 
        user_id: str, 
        session_id: str,
        existing_responses: List[UserQuizResponse]
    ) -> Dict[str, Any]:
        """
        Restore an incomplete quiz session.

        Args:
            user_id: The user's ID
            session_id: The session ID to restore
            existing_responses: List of existing responses for this session

        Returns:
            Dict containing restored session info and next question
        """
        logger.info(f"Restoring quiz session for user {user_id} with {len(existing_responses)} responses")
        
        # Create session data from existing responses
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "started_at": existing_responses[0].created_at.isoformat(),
            "current_question": len(existing_responses) + 1,  # Next question number
            "total_questions": self.total_questions,
            "responses": [],
            "insights": [],
            "focus_areas": [],
            "question_plan": self._create_question_plan(),
            "text_questions_used": 0,
            "selection_questions_used": 0,
        }

        # Process existing responses
        for resp in existing_responses:
            logger.info(f"Processing response: {resp.id}")
            logger.info(f"Response type: {type(resp.response)}")
            logger.info(f"Response data: {resp.response}")
            
            response_data = resp.response
            if isinstance(response_data, str):
                try:
                    response_data = json.loads(response_data)
                    logger.info("Successfully parsed response data from string")
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse response data: {e}")
                    response_data = {"answer": response_data}

            if not isinstance(response_data, dict):
                logger.error(f"Response data is not a dictionary: {type(response_data)}")
                response_data = {"answer": str(response_data)}

            session_data["responses"].append({
                "question_number": response_data.get("question_order", 0),
                "response": response_data.get("answer"),
                "question_text": response_data.get("question_text", ""),
                "timestamp": resp.created_at.isoformat(),
            })

        logger.info(f"Processed {len(session_data['responses'])} responses")

        # Update focus areas based on existing responses
        if session_data["responses"]:
            last_response = session_data["responses"][-1]
            logger.info(f"Updating focus areas based on last response: {last_response}")
            session_data["focus_areas"] = await self._update_focus_areas(
                session_data,
                {"answer": last_response["response"]}
            )
        else:
            logger.warning("No responses found to update focus areas")

        # Generate next question
        logger.info("Generating next question")
        next_question = await self._generate_psychology_enhanced_question(
            session_data,
            self.db.query(User).filter(User.id == user_id).first(),
        )

        # Store current question text in session
        session_data["current_question_text"] = next_question.get("text", "")

        # Calculate progress
        progress = {
            "current": session_data["current_question"],
            "total": self.total_questions,
            "completion_percentage": (
                session_data["current_question"] / self.total_questions
            ) * 100,
        }

        logger.info(f"Session restored successfully. Progress: {progress}")

        return {
            "session": session_data,
            "question": next_question,
            "progress": progress,
        }
