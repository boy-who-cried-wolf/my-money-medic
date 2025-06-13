"""
Test script for the Adaptive Quiz System
"""

import sys
import os
from pathlib import Path
import asyncio
import json
import uuid

# Add the root directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.database.connection import SessionLocal
from app.database.models.user import User, UserType
from app.services.adaptive_quiz_service import AdaptiveQuizService
from app.core.security import get_password_hash


async def create_test_client():
    """Create a test client for adaptive quiz testing"""
    db = SessionLocal()
    try:
        test_email = "adaptive.test@example.com"
        existing_user = db.query(User).filter_by(email=test_email).first()

        if existing_user:
            print(f"Test client already exists with ID: {existing_user.id}")
            return existing_user.id

        # Create test client
        user = User(
            id=str(uuid.uuid4()),
            first_name="Adaptive",
            last_name="TestClient",
            email=test_email,
            phone_number="555-8888",
            password_hash=get_password_hash("TestPass123!"),
            user_type=UserType.CLIENT,
            is_verified=True,
        )
        db.add(user)
        db.commit()

        print(f"Created test client with ID: {user.id}")
        return user.id

    except Exception as e:
        db.rollback()
        print(f"Error creating test client: {str(e)}")
        return None
    finally:
        db.close()


async def test_adaptive_quiz_flow():
    """Test the complete adaptive quiz flow"""
    db = SessionLocal()
    try:
        # Create or get test client
        client_id = await create_test_client()
        if not client_id:
            return

        print("\n" + "=" * 60)
        print("TESTING ADAPTIVE QUIZ SYSTEM")
        print("=" * 60)

        # Initialize adaptive quiz service
        adaptive_service = AdaptiveQuizService(db)

        # Start adaptive quiz
        print("\n1. Starting adaptive quiz...")
        start_result = await adaptive_service.start_adaptive_quiz(client_id)

        print(f"✓ Quiz started successfully")
        print(f"  Session ID: {start_result['session']['session_id']}")
        print(f"  First question: {start_result['question']['text']}")
        print(f"  Question type: {start_result['question']['question_type']}")
        print(f"  Progress: {start_result['progress']['completion_percentage']:.1f}%")

        # Simulate user responses
        test_responses = [
            {"answer": "retirement"},  # Investment goal
            {"answer": "intermediate"},  # Experience level
            {"answer": "moderate"},  # Risk tolerance
            {"answer": "video"},  # Communication preference
            {"answer": ["retirement_planning", "tax_planning"]},  # Services
            {"answer": "100k_500k"},  # Investment amount
            {"answer": ["technology", "healthcare"]},  # Sectors
            {
                "answer": "I'm particularly interested in sustainable investing and ESG funds"
            },  # Text response
        ]

        session_data = start_result["session"]
        question_count = 1

        print(f"\n2. Processing {len(test_responses)} test responses...")

        for i, response in enumerate(test_responses):
            print(f"\n   Response {i+1}: {response}")

            try:
                result = await adaptive_service.submit_response_and_get_next(
                    session_data, response
                )

                # Update session data
                session_data = result.get("session", session_data)
                question_count += 1

                if result.get("completed"):
                    print(f"   ✓ Quiz completed after {question_count} questions!")
                    print(f"   Completion reason: {result.get('reason')}")

                    # Display final results
                    print(f"\n3. Final Results:")
                    print(
                        f"   Total insights generated: {len(result.get('insights', []))}"
                    )
                    print(f"   Broker matches found: {len(result.get('matches', []))}")
                    print(
                        f"   Recommendations: {len(result.get('recommendations', []))}"
                    )

                    # Show top insights
                    insights = result.get("insights", [])
                    if insights:
                        print(f"\n   Top Insights:")
                        for j, insight in enumerate(insights[:3], 1):
                            print(f"   {j}. {insight.get('insight', 'N/A')}")

                    # Show top matches
                    matches = result.get("matches", [])
                    if matches:
                        print(f"\n   Top Broker Matches:")
                        for j, match in enumerate(matches[:3], 1):
                            print(
                                f"   {j}. {match.get('broker_name', 'Unknown')} - {match.get('match_score', 0)*100:.1f}% match"
                            )

                    # Show recommendations
                    recommendations = result.get("recommendations", [])
                    if recommendations:
                        print(f"\n   Personalized Recommendations:")
                        for j, rec in enumerate(recommendations, 1):
                            print(f"   {j}. {rec}")

                    break
                else:
                    next_question = result.get("question", {})
                    progress = result.get("progress", {})
                    insights = result.get("insights", [])

                    print(
                        f"   ✓ Response processed. Next question: {next_question.get('text', 'N/A')}"
                    )
                    print(
                        f"   Progress: {progress.get('completion_percentage', 0):.1f}%"
                    )

                    if insights:
                        print(f"   New insights: {len(insights)}")
                        for insight in insights:
                            print(f"     - {insight.get('insight', 'N/A')}")

            except Exception as e:
                print(f"   ✗ Error processing response {i+1}: {str(e)}")
                break

        print(f"\n4. Quiz session completed!")
        print(f"   Total questions answered: {len(session_data.get('responses', []))}")
        print(
            f"   Focus areas identified: {', '.join(session_data.get('focus_areas', []))}"
        )

    except Exception as e:
        print(f"Error testing adaptive quiz: {str(e)}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()


async def test_question_generation():
    """Test dynamic question generation"""
    db = SessionLocal()
    try:
        print("\n" + "=" * 60)
        print("TESTING DYNAMIC QUESTION GENERATION")
        print("=" * 60)

        adaptive_service = AdaptiveQuizService(db)

        # Test different question types
        test_cases = [
            {
                "topic": "Investment timeline and goals",
                "category": "FINANCIAL_GOALS",
                "question_type": "single_choice",
            },
            {
                "topic": "Risk tolerance for market volatility",
                "category": "RISK_TOLERANCE",
                "question_type": "scale",
            },
            {
                "topic": "Previous investment experience",
                "category": "EXPERIENCE",
                "question_type": "multiple_choice",
            },
            {
                "topic": "Specific financial planning needs",
                "category": "PREFERENCES",
                "question_type": "text",
            },
        ]

        for i, test_case in enumerate(test_cases, 1):
            print(
                f"\n{i}. Generating {test_case['question_type']} question about {test_case['topic']}..."
            )

            try:
                question_data = (
                    await adaptive_service.quiz_generator.create_ai_question_data(
                        topic=test_case["topic"],
                        category=test_case["category"],
                        question_type_str=test_case["question_type"],
                        order=i,
                    )
                )

                if question_data:
                    print(f"   ✓ Generated successfully!")
                    print(f"   Question: {question_data.get('text', 'N/A')}")
                    print(f"   Type: {question_data.get('question_type', 'N/A')}")

                    options = question_data.get("options")
                    if options:
                        if isinstance(options, list):
                            print(f"   Options: {len(options)} choices")
                            for j, option in enumerate(options[:3], 1):
                                print(f"     {j}. {option.get('label', 'N/A')}")
                        elif isinstance(options, dict):
                            print(
                                f"   Scale: {options.get('min', 'N/A')} to {options.get('max', 'N/A')}"
                            )
                else:
                    print(f"   ✗ Failed to generate question")

            except Exception as e:
                print(f"   ✗ Error generating question: {str(e)}")

    except Exception as e:
        print(f"Error testing question generation: {str(e)}")
    finally:
        db.close()


async def test_insights_generation():
    """Test AI insights generation"""
    db = SessionLocal()
    try:
        print("\n" + "=" * 60)
        print("TESTING AI INSIGHTS GENERATION")
        print("=" * 60)

        adaptive_service = AdaptiveQuizService(db)

        # Mock session data with responses
        mock_session = {
            "user_id": "test-user",
            "responses": [
                {
                    "question_number": 1,
                    "response": {"answer": "retirement"},
                    "question_text": "What is your primary investment goal?",
                },
                {
                    "question_number": 2,
                    "response": {"answer": "conservative"},
                    "question_text": "What is your risk tolerance?",
                },
                {
                    "question_number": 3,
                    "response": {"answer": "beginner"},
                    "question_text": "What is your investment experience?",
                },
                {
                    "question_number": 4,
                    "response": {"answer": "50k_100k"},
                    "question_text": "What is your investment amount?",
                },
            ],
            "insights": [
                {
                    "type": "risk_profile",
                    "insight": "User shows preference for conservative investment approaches",
                    "confidence": 0.8,
                }
            ],
        }

        print("Generating comprehensive insights from mock responses...")

        try:
            insights = await adaptive_service._generate_final_insights(mock_session)

            print(f"✓ Generated {len(insights)} insights:")
            for i, insight in enumerate(insights, 1):
                print(
                    f"   {i}. [{insight.get('type', 'unknown')}] {insight.get('insight', 'N/A')}"
                )
                print(f"      Confidence: {insight.get('confidence', 0):.1f}")

        except Exception as e:
            print(f"✗ Error generating insights: {str(e)}")

    except Exception as e:
        print(f"Error testing insights: {str(e)}")
    finally:
        db.close()


async def main():
    """Run all adaptive quiz tests"""
    print("Starting Adaptive Quiz System Tests...")

    # Test question generation
    await test_question_generation()

    # Test insights generation
    await test_insights_generation()

    # Test full adaptive quiz flow
    await test_adaptive_quiz_flow()

    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
