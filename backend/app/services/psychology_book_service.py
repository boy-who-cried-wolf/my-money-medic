"""
Psychology Book Service for extracting insights from PDF books

This service reads psychology and persuasion books to enhance
the adaptive quiz with psychological insights for better broker matching.
"""

import os
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

# Try to import PyPDF2 for PDF reading
try:
    import PyPDF2

    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logging.warning("PyPDF2 not installed. PDF reading disabled.")

from app.ai.gemini_service import GeminiService

logger = logging.getLogger(__name__)


class PsychologyBookService:
    """Service for extracting and using psychology insights from books"""

    def __init__(self):
        self.gemini_service = GeminiService()

        # Fix path resolution for the backend directory structure
        backend_dir = Path(__file__).parent.parent.parent  # Go up to backend/ directory
        self.books_dir = backend_dir / "data" / "books"
        self.cache_dir = backend_dir / "data" / "cache"

        # Create cache directory with parents if it doesn't exist
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Initialize book metadata
        self.book_metadata = {
            "dark_psychology": {
                "title": "Dark Psychology 7 in 1",
                "focus": "persuasion, influence, NLP, body language analysis",
                "application": "understanding client psychology and decision-making patterns",
            },
            "contagious": {
                "title": "Contagious",
                "focus": "viral psychology, why things catch on",
                "application": "understanding what motivates client behaviors and referrals",
            },
            "buyology": {
                "title": "Buyology",
                "focus": "truth and lies about why we buy",
                "application": "understanding client purchasing psychology and investment decisions",
            },
            "breakthrough_advertising": {
                "title": "Breakthrough Advertising",
                "focus": "advertising psychology that shatters traditions",
                "application": "understanding how to communicate with different client types",
            },
            "cashvertising": {
                "title": "Cashvertising Online",
                "focus": "buyer psychology for online advertising",
                "application": "understanding digital-age client behaviors and preferences",
            },
            "adkar": {
                "title": "ADKAR",
                "focus": "change management psychology",
                "application": "understanding client resistance to financial change and adaptation",
            },
            "10x_easier": {
                "title": "10x Is Easier Than 2x",
                "focus": "growth psychology and mindset",
                "application": "understanding ambitious client psychology and growth mindset",
            },
        }

    def get_psychology_insights_for_quiz(self) -> Dict[str, Any]:
        """Get key psychology insights for enhancing quiz questions"""

        insights = {
            "decision_making_psychology": [
                "People make emotional decisions and justify with logic",
                "Loss aversion: fear of losing is stronger than desire to gain",
                "Social proof influences investment decisions significantly",
                "Authority figures and credentials build immediate trust",
                "Scarcity creates urgency in financial decisions",
                "Anchoring effect influences perception of value and risk",
            ],
            "client_personality_types": [
                "Conservative: values security, stability, and preservation",
                "Aggressive: seeks growth, willing to take calculated risks",
                "Social: influenced by peer opinions and trends",
                "Analytical: requires detailed data and logical explanations",
                "Impulsive: makes quick decisions based on emotions",
                "Skeptical: questions everything, needs proof and evidence",
            ],
            "persuasion_principles": [
                "Reciprocity: people feel obligated to return favors",
                "Commitment: people align actions with stated commitments",
                "Social proof: people follow what others like them do",
                "Authority: people defer to experts and credentials",
                "Liking: people say yes to those they like and trust",
                "Scarcity: people value what's limited or exclusive",
            ],
            "investment_psychology": [
                "Fear and greed drive most investment decisions",
                "Confirmation bias affects information processing",
                "Overconfidence leads to excessive trading",
                "Mental accounting affects money allocation",
                "Herding behavior influences market timing",
                "Present bias affects long-term planning",
            ],
            "communication_styles": [
                "Visual learners prefer charts and graphics",
                "Auditory learners prefer verbal explanations",
                "Kinesthetic learners prefer hands-on examples",
                "Detail-oriented clients want comprehensive analysis",
                "Big-picture clients want summary and outcomes",
                "Relationship-focused clients value personal connection",
            ],
        }

        return insights

    async def generate_psychology_enhanced_question(
        self,
        topic: str,
        category: str,
        question_type: str,
        existing_questions: List[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Generate a question enhanced with psychology insights"""

        psychology_insights = self.get_psychology_insights_for_quiz()

        # Select relevant psychology principles based on topic
        relevant_psychology = self._get_relevant_psychology(topic, psychology_insights)

        prompt = f"""
        You are creating a simple, engaging quiz question for broker-client matching. 
        Use psychology principles but keep it SHORT, SIMPLE, and INTERESTING.

        Topic: {topic}
        Category: {category}
        Question Type: {question_type}

        Psychology Principles (keep these in mind but don't overcomplicate):
        {json.dumps(relevant_psychology, indent=2)}

        REQUIREMENTS:
        - Maximum 2 sentences for the question
        - Use simple, everyday language
        - Make it relatable and engaging
        - Test psychological traits without being obvious
        - Avoid long scenarios or complex explanations
        - Focus on one clear psychological insight
        - Make it feel like a conversation, not an exam

        STYLE GUIDELINES:
        - Start with "When..." or "If..." or "How do you..."
        - Use concrete examples people can relate to
        - Avoid financial jargon
        - Make options short (3-5 words each)
        - Create emotional engagement without being verbose
        """

        if existing_questions:
            prompt += f"\n\nAvoid similarity to these existing questions:\n{existing_questions}"

        if question_type in ["single_choice", "multiple_choice", "multiple_select"]:
            prompt += f"""
            
            Return a JSON object with this structure:
            {{
                "text": "Simple, engaging question (max 2 sentences)",
                "question_type": "{question_type}",
                "options": [
                    {{"value": "option1", "label": "Short option 1"}},
                    {{"value": "option2", "label": "Short option 2"}},
                    {{"value": "option3", "label": "Short option 3"}},
                    {{"value": "option4", "label": "Short option 4"}}
                ],
                "psychology_insight": "Brief explanation of what this reveals",
                "broker_matching_value": "How this helps broker matching"
            }}

            EXAMPLES OF GOOD SHORT OPTIONS:
            - "Research thoroughly first"
            - "Trust my gut feeling"
            - "Ask friends for advice"
            - "Follow expert recommendations"
            """
        elif question_type == "scale":
            prompt += f"""
            
            Return a JSON object with this structure:
            {{
                "text": "Simple, engaging question (max 2 sentences)",
                "question_type": "scale",
                "options": {{
                    "min": 1,
                    "max": 5,
                    "min_label": "Short label (2-3 words)",
                    "max_label": "Short label (2-3 words)"
                }},
                "psychology_insight": "Brief explanation of what this reveals",
                "broker_matching_value": "How this helps broker matching"
            }}

            EXAMPLES OF GOOD SCALE LABELS:
            - "Very uncomfortable" to "Very comfortable"
            - "Never" to "Always"
            - "Strongly disagree" to "Strongly agree"
            """
        else:  # text type
            prompt += f"""
            
            Return a JSON object with this structure:
            {{
                "text": "Simple, engaging open-ended question that invites sharing",
                "question_type": "text",
                "options": null,
                "psychology_insight": "Brief explanation of what this reveals", 
                "broker_matching_value": "How this helps broker matching"
            }}

            EXAMPLES OF GOOD TEXT QUESTIONS:
            - "What's your biggest financial worry?"
            - "Describe your ideal retirement lifestyle."
            - "What financial lesson did you learn the hard way?"
            """

        try:
            result = await self.gemini_service.generate_json(prompt)
            return result
        except Exception as e:
            logger.error(f"Error generating psychology-enhanced question: {str(e)}")
            return None

    def _get_relevant_psychology(
        self, topic: str, insights: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Select psychology principles most relevant to the topic"""

        relevant = {}

        # Always include decision making psychology
        relevant["decision_making_psychology"] = insights["decision_making_psychology"]

        if "risk" in topic.lower() or "tolerance" in topic.lower():
            relevant["investment_psychology"] = insights["investment_psychology"]
            relevant["client_personality_types"] = insights["client_personality_types"]

        elif "goals" in topic.lower() or "planning" in topic.lower():
            relevant["persuasion_principles"] = insights["persuasion_principles"]
            relevant["client_personality_types"] = insights["client_personality_types"]

        elif "communication" in topic.lower() or "service" in topic.lower():
            relevant["communication_styles"] = insights["communication_styles"]
            relevant["persuasion_principles"] = insights["persuasion_principles"]

        elif "experience" in topic.lower() or "knowledge" in topic.lower():
            relevant["investment_psychology"] = insights["investment_psychology"]
            relevant["communication_styles"] = insights["communication_styles"]

        else:
            # Default: include personality types and persuasion
            relevant["client_personality_types"] = insights["client_personality_types"]
            relevant["persuasion_principles"] = insights["persuasion_principles"]

        return relevant

    def get_psychology_based_insights(
        self, quiz_responses: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze quiz responses using psychology principles to generate insights"""

        insights = []

        # Analyze patterns in responses
        for response in quiz_responses:
            answer = response.get("response", {}).get("answer", "")
            question_text = response.get("question_text", "")

            # Psychology-based analysis - keep it simple and friendly
            if isinstance(answer, str):
                # Decision-making style analysis
                if any(
                    word in answer.lower()
                    for word in ["quickly", "immediate", "urgent"]
                ):
                    insights.append(
                        {
                            "type": "decision_style",
                            "insight": "**Quick Decider**: You like to make financial decisions quickly and trust your instincts.",
                            "confidence": 0.85,
                            "psychology_principle": "Present bias",
                        }
                    )
                elif any(
                    word in answer.lower()
                    for word in ["research", "analyze", "study", "careful"]
                ):
                    insights.append(
                        {
                            "type": "decision_style",
                            "insight": "**Thorough Researcher**: You prefer to analyze all the details before making investment decisions.",
                            "confidence": 0.90,
                            "psychology_principle": "Analytical processing",
                        }
                    )

                # Risk psychology analysis
                if any(
                    word in answer.lower()
                    for word in ["safe", "secure", "conservative", "protect"]
                ):
                    insights.append(
                        {
                            "type": "risk_profile",
                            "insight": "**Safety First**: You prioritize protecting your money over chasing high returns.",
                            "confidence": 0.85,
                            "psychology_principle": "Loss aversion",
                        }
                    )
                elif any(
                    word in answer.lower()
                    for word in ["growth", "aggressive", "high return", "opportunity"]
                ):
                    insights.append(
                        {
                            "type": "risk_profile",
                            "insight": "**Growth Focused**: You're comfortable with risk if it means better long-term returns.",
                            "confidence": 0.80,
                            "psychology_principle": "Growth mindset",
                        }
                    )

                # Social influence analysis
                if any(
                    word in answer.lower()
                    for word in ["friends", "family", "others", "popular", "trending"]
                ):
                    insights.append(
                        {
                            "type": "social_style",
                            "insight": "**Social Learner**: You value input from people you trust when making financial decisions.",
                            "confidence": 0.75,
                            "psychology_principle": "Social proof",
                        }
                    )

                # Authority and expertise preference
                if any(
                    word in answer.lower()
                    for word in ["expert", "professional", "certified", "credentials"]
                ):
                    insights.append(
                        {
                            "type": "authority_preference",
                            "insight": "**Expert Guidance**: You prefer working with qualified professionals who have proven expertise.",
                            "confidence": 0.85,
                            "psychology_principle": "Authority trust",
                        }
                    )

        return insights
