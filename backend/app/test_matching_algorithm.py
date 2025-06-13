"""
Test script for the matching algorithm
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import uuid

# Add the root directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.database.connection import SessionLocal
from app.database.models.user import User, UserType
from app.database.models.quiz import Quiz, QuizQuestion, UserQuizResponse
from app.services.matching_algorithm import (
    BrokerMatchingAlgorithm,
    generate_broker_matches,
)
from app.core.security import get_password_hash


def create_test_client():
    """Create a test client with quiz responses"""
    db = SessionLocal()
    try:
        # Check if test client exists
        test_email = "test.client@example.com"
        existing_user = db.query(User).filter_by(email=test_email).first()

        if existing_user:
            print(f"Test client already exists with ID: {existing_user.id}")
            return existing_user.id

        # Create test client with UUID
        user = User(
            id=str(uuid.uuid4()),
            first_name="Test",
            last_name="Client",
            email=test_email,
            phone_number="555-9999",
            password_hash=get_password_hash("TestPass123!"),
            user_type=UserType.CLIENT,
            is_verified=True,
        )
        db.add(user)
        db.flush()

        # Get the broker matching quiz
        quiz = db.query(Quiz).filter_by(title="Broker Matching Questionnaire").first()
        if not quiz:
            print(
                "Error: Broker Matching Questionnaire not found. Please run seed_quiz_data.py first."
            )
            return None

        # Create test responses
        test_responses = {
            "What is your primary investment goal?": "retirement",
            "How would you describe your investment experience?": "intermediate",
            "What is your risk tolerance level?": "moderate",
            "What investment time horizon are you considering?": "long",
            "Which sectors are you most interested in investing?": [
                "technology",
                "healthcare",
                "financial",
            ],
            "How would you prefer to communicate with your broker?": "video",
            "How frequently would you like to review your investments?": "quarterly",
            "What is your approximate investment amount?": "100k_500k",
            "Which services are most important to you?": [
                "retirement_planning",
                "tax_planning",
                "investment_management",
            ],
            "Do you have any specific broker certification preferences?": [
                "cfp",
                "cfa",
            ],
        }

        # Add quiz responses
        questions = db.query(QuizQuestion).filter_by(quiz_id=quiz.id).all()
        for question in questions:
            if question.text in test_responses:
                response = UserQuizResponse(
                    id=str(uuid.uuid4()),
                    user_id=user.id,
                    question_id=question.id,
                    response=(
                        json.dumps(test_responses[question.text])
                        if isinstance(test_responses[question.text], list)
                        else test_responses[question.text]
                    ),
                )
                db.add(response)

        db.commit()
        print(f"Created test client with ID: {user.id}")
        return user.id

    except Exception as e:
        db.rollback()
        print(f"Error creating test client: {str(e)}")
        return None
    finally:
        db.close()


def test_matching_algorithm():
    """Test the matching algorithm with a test client"""
    db = SessionLocal()
    try:
        # Create or get test client
        client_id = create_test_client()
        if not client_id:
            return

        print("\n" + "=" * 60)
        print("TESTING MATCHING ALGORITHM")
        print("=" * 60)

        # Initialize algorithm
        algorithm = BrokerMatchingAlgorithm(db)

        # Get user responses
        user_responses = algorithm._get_user_responses(client_id)
        print(f"\nUser has {len(user_responses)} quiz responses")

        # Calculate matches
        print("\nCalculating broker matches...")
        matches = algorithm.calculate_matches(client_id, top_n=5)

        if not matches:
            print("No matches found! Make sure you have run seed_brokers.py")
            return

        print(f"\nFound {len(matches)} matches:")
        print("-" * 60)

        for i, (broker, score) in enumerate(matches, 1):
            print(f"\n{i}. {broker.user.full_name} - {broker.company_name}")
            print(f"   Match Score: {score:.3f} ({score*100:.1f}%)")
            print(
                f"   Experience: {broker.experience_level.value} ({broker.years_of_experience} years)"
            )
            print(f"   Rating: {broker.average_rating}/5.0")
            print(
                f"   Specializations: {', '.join([s.name for s in broker.specializations])}"
            )

        # Test the generate_broker_matches function
        print("\n" + "=" * 60)
        print("TESTING GENERATE_BROKER_MATCHES FUNCTION")
        print("=" * 60)

        match_results = generate_broker_matches(db, client_id, save_to_db=True)

        print(f"\nGenerated {len(match_results)} matches and saved to database")
        for match in match_results[:3]:  # Show top 3
            print(f"\n- {match['broker_name']} ({match['company_name']})")
            print(f"  Score: {match['match_score']}")
            print(f"  Experience: {match['experience_level']}")
            print(f"  Specializations: {', '.join(match['specializations'])}")

    except Exception as e:
        print(f"Error testing algorithm: {str(e)}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_matching_algorithm()
