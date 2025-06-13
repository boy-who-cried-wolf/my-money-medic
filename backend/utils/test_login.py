"""
Utility script to test the login flow.

This script tests the login process by attempting to authenticate
with provided credentials and generating a JWT token if successful.

Usage:
    python test_login.py
    python test_login.py --email test@example.com --password TestPassword123!
"""

import os
import sys
import argparse
from datetime import timedelta

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Sessionlocal
from app.services.user_service import authenticate_user
from app.core.security import create_access_token


def test_login(email, password):
    """Test login with provided credentials."""
    print(f"\nAttempting login with:")
    print(f"Email: {email}")
    print(f"Password: {password}")

    # Create database session
    db = Sessionlocal()

    try:
        # Authenticate user
        user = authenticate_user(db, email, password)

        if not user:
            print("\nAuthentication failed: Invalid credentials")
            return False

        print(f"\nAuthentication successful for user:")
        print(f"User ID: {user.id}")
        print(f"Name: {user.first_name} {user.last_name}")
        print(f"Email: {user.email}")
        print(f"User Type: {user.user_type}")

        # Create access token
        token = create_access_token(
            subject=str(user.id), expires_delta=timedelta(minutes=30)
        )

        print(f"\nGenerated access token:")
        print(f"Token: {token}")
        print("\nThis token can be used to access protected endpoints for 30 minutes.")

        return True

    except Exception as e:
        print(f"Error during login: {e}")
        return False

    finally:
        db.close()


def main():
    """Parse arguments and test login."""
    parser = argparse.ArgumentParser(description="Test login process")
    parser.add_argument("--email", default="test@example.com", help="Email address")
    parser.add_argument("--password", default="TestPassword123!", help="Password")

    args = parser.parse_args()

    test_login(args.email, args.password)


if __name__ == "__main__":
    main()
