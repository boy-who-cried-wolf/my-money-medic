#!/usr/bin/env python3
"""
Quick script to check database configuration and test connection
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=== Database Configuration Check ===")
print(f"DATABASE_URL exists: {bool(os.getenv('DATABASE_URL'))}")
print(f"DO_DB_HOST: {os.getenv('DO_DB_HOST', 'Not set')}")
print(f"DO_DB_USER: {os.getenv('DO_DB_USER', 'Not set')}")
print(f"DO_DB_NAME: {os.getenv('DO_DB_NAME', 'Not set')}")
print(f"DO_DB_PORT: {os.getenv('DO_DB_PORT', 'Not set')}")

# Test database connection
print("\n=== Testing Database Connection ===")
try:
    from app.database.connection import test_connection

    if test_connection():
        print("✅ Database connection successful!")
    else:
        print("❌ Database connection failed!")
except Exception as e:
    print(f"❌ Database connection error: {str(e)}")

print("\n=== Alternative: Use SQLite for testing ===")
print("To use SQLite instead of DigitalOcean:")
print("1. Create a .env file with:")
print("   DATABASE_URL=sqlite:///./test.db")
print("   SECRET_KEY=your-secret-key-here")
print("2. Run database initialization scripts")
