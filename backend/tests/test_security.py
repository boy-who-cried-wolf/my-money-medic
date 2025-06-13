"""Test file for security module functionality."""

import unittest
import os
import sys

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta
from jose import jwt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get security settings from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


class TestSecurity(unittest.TestCase):
    """Tests for security module."""

    def test_password_hashing(self):
        """Test that password hashing and verification works."""
        # Test simple password
        original_password = "TestPassword123!"
        hashed_password = get_password_hash(original_password)

        # Verify that the hash is not the same as the original password
        self.assertNotEqual(original_password, hashed_password)

        # Verify that the password verification function works
        self.assertTrue(verify_password(original_password, hashed_password))

        # Verify that an incorrect password fails verification
        self.assertFalse(verify_password("WrongPassword", hashed_password))

        # Test that even similar passwords get different hashes
        similar_password = "TestPassword123!!"
        similar_hashed = get_password_hash(similar_password)
        self.assertNotEqual(hashed_password, similar_hashed)

    def test_jwt_token(self):
        """Test JWT token creation and verification."""
        if not SECRET_KEY:
            self.skipTest("SECRET_KEY not set in environment variables")

        # Create a token
        user_id = "test-user-123"
        token = create_access_token(user_id, expires_delta=timedelta(minutes=30))

        # Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Verify payload contains user_id
        self.assertEqual(payload["sub"], user_id)

        # Verify token has expiration
        self.assertIn("exp", payload)


if __name__ == "__main__":
    unittest.main()
