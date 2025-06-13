#!/usr/bin/env python3
"""
Initialize local SQLite database with test data
This script bypasses DigitalOcean connection issues for local development
"""

import os
import sys
from pathlib import Path

# Override DATABASE_URL for local SQLite
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "Z-TyucmOGwPVE0LpuJFfFEExtOThOCUTUBjFPBEMcZg"

print("🚀 Initializing local SQLite database...")
print(f"DATABASE_URL: {os.environ['DATABASE_URL']}")

# Now import and initialize
from app.database import init_db
from app.database.connection import test_connection

print("\n📊 Step 1: Testing database connection...")
if test_connection():
    print("✅ Database connection successful!")
else:
    print("❌ Database connection failed!")
    sys.exit(1)

print("\n🏗️  Step 2: Initializing database tables...")
if init_db():
    print("✅ Database tables created successfully!")
else:
    print("❌ Database initialization failed!")
    sys.exit(1)

print("\n📝 Step 3: Seeding quiz data...")
try:
    from app.database.seed_quiz_data import seed_quiz_data

    seed_quiz_data()
    print("✅ Quiz data seeded successfully!")
except Exception as e:
    print(f"❌ Quiz seeding failed: {str(e)}")

print("\n👥 Step 4: Seeding broker data...")
try:
    from app.database.seed_brokers import seed_brokers

    seed_brokers()
    print("✅ Broker data seeded successfully!")
except Exception as e:
    print(f"❌ Broker seeding failed: {str(e)}")

print("\n🧪 Step 5: Creating test user...")
try:
    from app.database.connection import SessionLocal
    from app.database.models.user import User, UserType
    from app.core.security import get_password_hash
    import uuid

    db = SessionLocal()

    # Check if test user exists
    test_email = "test@example.com"
    existing_user = db.query(User).filter_by(email=test_email).first()

    if not existing_user:
        test_user = User(
            id=str(uuid.uuid4()),
            first_name="Test",
            last_name="User",
            email=test_email,
            phone_number="555-1234",
            password_hash=get_password_hash("TestPass123!"),
            user_type=UserType.CLIENT,
            is_verified=True,
        )
        db.add(test_user)
        db.commit()
        print(f"✅ Test user created: {test_email} / TestPass123!")
    else:
        print(f"✅ Test user already exists: {test_email}")

    db.close()

except Exception as e:
    print(f"❌ Test user creation failed: {str(e)}")

print("\n🎉 Database initialization complete!")
print("\n📋 Login credentials:")
print("   Email: test@example.com")
print("   Password: TestPass123!")
print("\n🚀 Start your server with: uvicorn server:app --reload")
print("🔗 Test login at: http://localhost:8000/api/docs")
