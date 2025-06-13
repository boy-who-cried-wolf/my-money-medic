"""
Utility script to create a test user in the database.

This script creates a test user with known credentials that can be used
for testing the authentication system.

Usage:
    python create_test_user.py
    python create_test_user.py --email test@example.com --password TestPassword123!
"""

import os
import sys
import argparse
from uuid import UUID

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.models import User, UserType
from app.database import init_db, Sessionlocal
from app.core.security import get_password_hash


def create_test_user(email, password, first_name="Test", last_name="User"):
    """Create a test user in the database."""
    print(f"\nCreating test user with email: {email}")

    # Initialize the database if not already done
    init_db()

    # Create database session
    db = Sessionlocal()

    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"User with email {email} already exists with ID: {existing_user.id}")
            # Update password
            existing_user.password_hash = get_password_hash(password)
            db.commit()
            print(f"Updated password for user: {email}")
            return existing_user.id

        # Hash the password
        hashed_password = get_password_hash(password)
        print(f"Password hash: {hashed_password}")

        # Create user
        user = User(
            email=email,
            password_hash=hashed_password,
            first_name=first_name,
            last_name=last_name,
            phone_number="1234567890",
            user_type=UserType.CLIENT,
            is_verified=True,
        )

        # Add user to database
        db.add(user)
        db.commit()
        db.refresh(user)

        print(f"Created test user with ID: {user.id}")
        return user.id

    except Exception as e:
        print(f"Error creating test user: {e}")
        return None

    finally:
        db.close()


def main():
    """Parse arguments and create test user."""
    parser = argparse.ArgumentParser(description="Create a test user in the database")
    parser.add_argument(
        "--email", default="test@example.com", help="Email address for test user"
    )
    parser.add_argument(
        "--password", default="TestPassword123!", help="Password for test user"
    )
    parser.add_argument("--first-name", default="Test", help="First name for test user")
    parser.add_argument("--last-name", default="User", help="Last name for test user")

    args = parser.parse_args()

    user_id = create_test_user(
        args.email, args.password, args.first_name, args.last_name
    )

    if user_id:
        print("\nTest user created successfully.")
        print("You can now use these credentials for testing:")
        print(f"Email: {args.email}")
        print(f"Password: {args.password}")
        print(f"User ID: {user_id}\n")


if __name__ == "__main__":
    main()
