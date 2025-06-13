"""
Test script for Adaptive Quiz API endpoints
"""

import sys
import os
from pathlib import Path
import asyncio
import json
import uuid
import requests
from datetime import datetime

# Add the root directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.database.connection import SessionLocal
from app.database.models.user import User, UserType
from app.core.security import get_password_hash, create_access_token


BASE_URL = "http://localhost:8000/api/v1"


async def create_test_users():
    """Create test users for API testing"""
    db = SessionLocal()
    try:
        users = {}

        # Create test client
        client_email = "api.client@example.com"
        existing_client = db.query(User).filter_by(email=client_email).first()

        if not existing_client:
            client = User(
                id=str(uuid.uuid4()),
                first_name="API",
                last_name="TestClient",
                email=client_email,
                phone_number="555-9999",
                password_hash=get_password_hash("TestPass123!"),
                user_type=UserType.CLIENT,
                is_verified=True,
            )
            db.add(client)
            users["client"] = client
        else:
            users["client"] = existing_client

        # Create test admin
        admin_email = "api.admin@example.com"
        existing_admin = db.query(User).filter_by(email=admin_email).first()

        if not existing_admin:
            admin = User(
                id=str(uuid.uuid4()),
                first_name="API",
                last_name="TestAdmin",
                email=admin_email,
                phone_number="555-0000",
                password_hash=get_password_hash("AdminPass123!"),
                user_type=UserType.ADMIN,
                is_verified=True,
            )
            db.add(admin)
            users["admin"] = admin
        else:
            users["admin"] = existing_admin

        db.commit()

        # Generate tokens using correct function signature
        tokens = {}
        for role, user in users.items():
            # Use user.id as the subject (not email)
            tokens[role] = create_access_token(subject=str(user.id))

        return users, tokens

    except Exception as e:
        db.rollback()
        print(f"Error creating test users: {str(e)}")
        return {}, {}
    finally:
        db.close()


def test_start_adaptive_quiz(client_token):
    """Test starting an adaptive quiz"""
    print("\n1. Testing: Start Adaptive Quiz")

    headers = {"Authorization": f"Bearer {client_token}"}

    try:
        response = requests.post(f"{BASE_URL}/adaptive-quiz/start", headers=headers)

        if response.status_code == 200:
            data = response.json()
            print("   ✓ Quiz started successfully")
            print(f"   Session ID: {data['data']['session']['session_id']}")
            print(f"   First question: {data['data']['question']['text'][:80]}...")
            print(f"   Question type: {data['data']['question']['question_type']}")
            return data["data"]
        else:
            print(f"   ✗ Failed with status {response.status_code}: {response.text}")
            return None

    except requests.exceptions.ConnectionError:
        print("   ⚠ Server not running. Please start the FastAPI server first.")
        return None
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return None


def test_submit_response(client_token, session_data):
    """Test submitting a response"""
    print("\n2. Testing: Submit Response")

    headers = {"Authorization": f"Bearer {client_token}"}

    test_response = {"answer": "retirement"}

    payload = {"session_data": session_data["session"], "response": test_response}

    try:
        response = requests.post(
            f"{BASE_URL}/adaptive-quiz/respond", headers=headers, json=payload
        )

        if response.status_code == 200:
            data = response.json()
            print("   ✓ Response submitted successfully")

            if data["data"].get("completed"):
                print("   ✓ Quiz completed!")
                print(f"   Insights: {len(data['data'].get('insights', []))}")
                print(f"   Matches: {len(data['data'].get('matches', []))}")
            else:
                print(f"   Next question: {data['data']['question']['text'][:80]}...")
                print(
                    f"   Progress: {data['data']['progress']['completion_percentage']:.1f}%"
                )

            return data["data"]
        else:
            print(f"   ✗ Failed with status {response.status_code}: {response.text}")
            return None

    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return None


def test_generate_question(admin_token):
    """Test dynamic question generation"""
    print("\n3. Testing: Generate Dynamic Question")

    headers = {"Authorization": f"Bearer {admin_token}"}

    params = {
        "topic": "Investment risk tolerance",
        "category": "RISK_TOLERANCE",
        "question_type": "scale",
    }

    try:
        response = requests.post(
            f"{BASE_URL}/adaptive-quiz/generate-question",
            headers=headers,
            params=params,
        )

        if response.status_code == 200:
            data = response.json()
            print("   ✓ Question generated successfully")
            question = data["data"]["question"]
            print(f"   Question: {question['text']}")
            print(f"   Type: {question['question_type']}")

            if question.get("options"):
                if isinstance(question["options"], dict):
                    print(
                        f"   Scale: {question['options'].get('min')} to {question['options'].get('max')}"
                    )
                elif isinstance(question["options"], list):
                    print(f"   Options: {len(question['options'])} choices")

            return data["data"]
        else:
            print(f"   ✗ Failed with status {response.status_code}: {response.text}")
            return None

    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return None


def test_get_insights(admin_token, user_id):
    """Test getting user insights"""
    print("\n4. Testing: Get User Insights")

    headers = {"Authorization": f"Bearer {admin_token}"}

    try:
        response = requests.get(
            f"{BASE_URL}/adaptive-quiz/insights/{user_id}", headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            print("   ✓ Insights retrieved successfully")
            insights = data["data"]["insights"]
            print(f"   Total insights: {len(insights)}")

            if insights:
                print("   Sample insights:")
                for i, insight in enumerate(insights[:2], 1):
                    print(
                        f"   {i}. [{insight.get('type', 'unknown')}] {insight.get('insight', 'N/A')[:80]}..."
                    )

            return data["data"]
        else:
            print(f"   ✗ Failed with status {response.status_code}: {response.text}")
            return None

    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return None


def test_adaptive_flow(admin_token):
    """Test the complete adaptive flow"""
    print("\n5. Testing: Complete Adaptive Flow")

    headers = {"Authorization": f"Bearer {admin_token}"}

    test_responses = [
        {"answer": "retirement"},
        {"answer": "conservative"},
        {"answer": "beginner"},
        {"answer": "monthly"},
        {"answer": "50k_100k"},
    ]

    try:
        response = requests.post(
            f"{BASE_URL}/adaptive-quiz/test-flow",
            headers=headers,
            json={
                "test_responses": test_responses
            },  # Wrap in object with named parameter
        )

        if response.status_code == 200:
            data = response.json()
            print("   ✓ Test flow completed successfully")

            flow_results = data["data"]["test_flow_results"]
            print(f"   Flow steps: {len(flow_results)}")

            # Check if quiz was completed
            for step in flow_results:
                if step.get("result", {}).get("completed"):
                    print("   ✓ Quiz completed in test flow")
                    break
            else:
                print("   ⚠ Quiz did not complete in test flow")

            return data["data"]
        else:
            print(f"   ✗ Failed with status {response.status_code}: {response.text}")
            return None

    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return None


async def main():
    """Run all API tests"""
    print("Starting Adaptive Quiz API Tests...")
    print("=" * 60)

    # Create test users and get tokens
    print("Setting up test users...")
    users, tokens = await create_test_users()

    if not tokens:
        print("Failed to create test users. Exiting.")
        return

    client_token = tokens.get("client")
    admin_token = tokens.get("admin")
    client_id = users.get("client").id

    print(f"✓ Test users created")
    print(f"  Client ID: {client_id}")

    # Test 1: Start adaptive quiz
    quiz_data = test_start_adaptive_quiz(client_token)

    if quiz_data:
        # Test 2: Submit response
        response_data = test_submit_response(client_token, quiz_data)

    # Test 3: Generate question (admin only)
    test_generate_question(admin_token)

    # Test 4: Get insights (admin only)
    test_get_insights(admin_token, client_id)

    # Test 5: Test complete flow (admin only)
    test_adaptive_flow(admin_token)

    print("\n" + "=" * 60)
    print("API TESTS COMPLETED")
    print("=" * 60)
    print("\nNote: Some tests may fail if the FastAPI server is not running.")
    print("To start the server, run: uvicorn app.main:app --reload")


if __name__ == "__main__":
    asyncio.run(main())
