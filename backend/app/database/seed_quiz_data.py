"""
Script for populating the database with quiz questions for the broker matching platform.
Run this script to add quizzes and questions to the database.
"""

import sys
import os
from pathlib import Path
import uuid
from datetime import datetime

# Add the root directory to the Python path
backend_dir = Path(__file__).parent.parent.parent  # backend/
sys.path.insert(0, str(backend_dir))

from app.database.connection import Sessionlocal, engine
from app.database.models.quiz import Quiz, QuizQuestion
from app.database.models.base import Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Quiz questions with options
BROKER_MATCHING_QUIZ = {
    "title": "Broker Matching Questionnaire",
    "description": "Help us find the perfect broker for your financial needs",
    "category": "broker_matching",
    "questions": [
        {
            "text": "What is your primary investment goal?",
            "question_type": "multiple_choice",
            "options": [
                {"value": "retirement", "label": "Retirement planning"},
                {"value": "wealth_growth", "label": "Wealth growth"},
                {"value": "income", "label": "Regular income"},
                {"value": "education", "label": "Education funding"},
                {"value": "home_purchase", "label": "Saving for home purchase"},
            ],
            "order": 1,
            "weight": 5,
        },
        {
            "text": "How would you describe your investment experience?",
            "question_type": "multiple_choice",
            "options": [
                {"value": "none", "label": "No prior experience"},
                {"value": "beginner", "label": "Beginner (some basic knowledge)"},
                {
                    "value": "intermediate",
                    "label": "Intermediate (familiar with different investment types)",
                },
                {"value": "advanced", "label": "Advanced (active investor)"},
                {"value": "expert", "label": "Expert (professional background)"},
            ],
            "order": 2,
            "weight": 3,
        },
        {
            "text": "What is your risk tolerance level?",
            "question_type": "multiple_choice",
            "options": [
                {"value": "conservative", "label": "Conservative (minimal risk)"},
                {"value": "moderate_conservative", "label": "Moderately Conservative"},
                {"value": "moderate", "label": "Moderate"},
                {"value": "moderate_aggressive", "label": "Moderately Aggressive"},
                {
                    "value": "aggressive",
                    "label": "Aggressive (highest returns potential)",
                },
            ],
            "order": 3,
            "weight": 5,
        },
        {
            "text": "What investment time horizon are you considering?",
            "question_type": "multiple_choice",
            "options": [
                {"value": "short", "label": "Short-term (0-2 years)"},
                {"value": "medium", "label": "Medium-term (3-5 years)"},
                {"value": "long", "label": "Long-term (6-10 years)"},
                {"value": "very_long", "label": "Very long-term (10+ years)"},
            ],
            "order": 4,
            "weight": 4,
        },
        {
            "text": "Which sectors are you most interested in investing?",
            "question_type": "multiple_select",
            "options": [
                {"value": "technology", "label": "Technology"},
                {"value": "healthcare", "label": "Healthcare"},
                {"value": "financial", "label": "Financial Services"},
                {"value": "energy", "label": "Energy"},
                {"value": "real_estate", "label": "Real Estate"},
                {"value": "consumer", "label": "Consumer Goods"},
                {"value": "industrial", "label": "Industrial"},
                {"value": "utility", "label": "Utilities"},
                {"value": "materials", "label": "Materials"},
                {"value": "telecom", "label": "Telecommunications"},
            ],
            "order": 5,
            "weight": 4,
        },
        {
            "text": "How would you prefer to communicate with your broker?",
            "question_type": "multiple_choice",
            "options": [
                {"value": "email", "label": "Email"},
                {"value": "phone", "label": "Phone calls"},
                {"value": "video", "label": "Video meetings"},
                {"value": "in_person", "label": "In-person meetings"},
                {"value": "chat", "label": "Text/chat messages"},
            ],
            "order": 6,
            "weight": 2,
        },
        {
            "text": "How frequently would you like to review your investments?",
            "question_type": "multiple_choice",
            "options": [
                {"value": "weekly", "label": "Weekly"},
                {"value": "monthly", "label": "Monthly"},
                {"value": "quarterly", "label": "Quarterly"},
                {"value": "semiannual", "label": "Semi-annually"},
                {"value": "annual", "label": "Annually"},
            ],
            "order": 7,
            "weight": 2,
        },
        {
            "text": "What is your approximate investment amount?",
            "question_type": "multiple_choice",
            "options": [
                {"value": "less_10k", "label": "Less than $10,000"},
                {"value": "10k_50k", "label": "$10,000 - $50,000"},
                {"value": "50k_100k", "label": "$50,000 - $100,000"},
                {"value": "100k_500k", "label": "$100,000 - $500,000"},
                {"value": "500k_plus", "label": "More than $500,000"},
            ],
            "order": 8,
            "weight": 3,
        },
        {
            "text": "Which services are most important to you?",
            "question_type": "multiple_select",
            "options": [
                {
                    "value": "financial_planning",
                    "label": "Comprehensive financial planning",
                },
                {"value": "tax_planning", "label": "Tax planning"},
                {"value": "estate_planning", "label": "Estate planning"},
                {"value": "retirement_planning", "label": "Retirement planning"},
                {"value": "education_planning", "label": "Education planning"},
                {"value": "insurance", "label": "Insurance analysis"},
                {"value": "investment_management", "label": "Investment management"},
                {"value": "budgeting", "label": "Budgeting and cash flow management"},
            ],
            "order": 9,
            "weight": 4,
        },
        {
            "text": "Do you have any specific broker certification preferences?",
            "question_type": "multiple_select",
            "options": [
                {"value": "cfp", "label": "Certified Financial Planner (CFP)"},
                {"value": "cfa", "label": "Chartered Financial Analyst (CFA)"},
                {"value": "chfc", "label": "Chartered Financial Consultant (ChFC)"},
                {"value": "cpa", "label": "Certified Public Accountant (CPA)"},
                {"value": "no_preference", "label": "No specific preference"},
            ],
            "order": 10,
            "weight": 3,
        },
    ],
}


def seed_quiz_data():
    """Seed the database with quiz data"""
    db = Sessionlocal()
    try:
        # Check if quiz already exists
        existing_quiz = (
            db.query(Quiz).filter_by(title=BROKER_MATCHING_QUIZ["title"]).first()
        )
        if existing_quiz:
            print(f"Quiz '{BROKER_MATCHING_QUIZ['title']}' already exists. Skipping.")
            return

        # Create new quiz
        quiz_id = str(uuid.uuid4())
        now = datetime.utcnow()

        new_quiz = Quiz(
            id=quiz_id,
            title=BROKER_MATCHING_QUIZ["title"],
            description=BROKER_MATCHING_QUIZ["description"],
            category=BROKER_MATCHING_QUIZ["category"],
            created_at=now,
            updated_at=now,
        )
        db.add(new_quiz)
        db.flush()

        # Add quiz questions
        for question_data in BROKER_MATCHING_QUIZ["questions"]:
            question_id = str(uuid.uuid4())
            new_question = QuizQuestion(
                id=question_id,
                quiz_id=quiz_id,
                text=question_data["text"],
                question_type=question_data["question_type"],
                options=question_data["options"],
                order=question_data["order"],
                weight=question_data["weight"],
                created_at=now,
            )
            db.add(new_question)

        db.commit()
        print(
            f"Successfully added quiz '{BROKER_MATCHING_QUIZ['title']}' with {len(BROKER_MATCHING_QUIZ['questions'])} questions."
        )

    except Exception as e:
        db.rollback()
        print(f"Error seeding quiz data: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    print("Starting quiz data seeding...")
    seed_quiz_data()
    print("Finished quiz data seeding.")
