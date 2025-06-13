"""
Simplified script to demonstrate password hashing with a user.

This doesn't require database setup, just shows how the password
hashing and verification works with a simple user model.
"""

import os
import sys

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.security import get_password_hash, verify_password


class SimpleUser:
    """Simplified user class for testing password hashing."""

    def __init__(self, email, password):
        self.email = email
        self.password_hash = get_password_hash(password)

    def verify_password(self, password):
        """Verify a password against the stored hash."""
        return verify_password(password, self.password_hash)


def test_user_password():
    """Test password hashing and verification with a simple user."""
    # Create a test user with a password
    user = SimpleUser("test@example.com", "SecurePassword123!")

    print(f"\nCreated user with email: {user.email}")
    print(f"Password hash: {user.password_hash}")

    # Test correct password
    correct_password = "SecurePassword123!"
    print(f"\nVerifying correct password: {correct_password}")
    result = user.verify_password(correct_password)
    print(f"Result: {'✅ Success' if result else '❌ Failed'}")

    # Test incorrect password
    incorrect_password = "WrongPassword456!"
    print(f"\nVerifying incorrect password: {incorrect_password}")
    result = user.verify_password(incorrect_password)
    print(
        f"Result: {'✅ Success' if not result else '❌ Failed (Verification should have failed)'}"
    )

    # Test similar password
    similar_password = "SecurePassword123"  # Missing the exclamation mark
    print(f"\nVerifying similar password: {similar_password}")
    result = user.verify_password(similar_password)
    print(
        f"Result: {'✅ Success' if not result else '❌ Failed (Verification should have failed)'}"
    )

    print("\nThis demonstrates that:")
    print("1. The password is securely hashed when creating a user")
    print("2. The same password can be verified against the hash")
    print("3. Different passwords (even similar ones) are rejected")


if __name__ == "__main__":
    test_user_password()
