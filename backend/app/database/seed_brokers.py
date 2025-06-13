"""
Script for seeding sample broker data for testing the matching algorithm
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import uuid

# Add the root directory to the Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from app.database.connection import SessionLocal, engine
from app.database.models.base import Base
from app.database.models.user import User, UserType
from app.database.models.broker import (
    Broker,
    Specialization,
    ExperienceLevel,
    LicenseStatus,
)
from app.core.security import get_password_hash

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Sample specializations
SPECIALIZATIONS = [
    {"name": "retirement_planning", "description": "Retirement and pension planning"},
    {"name": "financial_planning", "description": "Comprehensive financial planning"},
    {
        "name": "investment_management",
        "description": "Portfolio and investment management",
    },
    {"name": "wealth_management", "description": "High net worth wealth management"},
    {"name": "tax_strategies", "description": "Tax planning and optimization"},
    {"name": "estate_planning", "description": "Estate and inheritance planning"},
    {"name": "education_planning", "description": "Education savings and 529 plans"},
    {"name": "insurance_planning", "description": "Insurance needs analysis"},
    {"name": "real_estate_planning", "description": "Real estate investment planning"},
    {"name": "income_strategies", "description": "Income generation strategies"},
    {
        "name": "dividend_investing",
        "description": "Dividend-focused investment strategies",
    },
    {"name": "budgeting", "description": "Personal budgeting and cash flow management"},
    {"name": "technology", "description": "Technology sector expertise"},
    {"name": "healthcare", "description": "Healthcare sector expertise"},
    {"name": "financial", "description": "Financial sector expertise"},
    {"name": "energy", "description": "Energy sector expertise"},
    {"name": "real_estate", "description": "Real estate sector expertise"},
]

# Sample brokers
SAMPLE_BROKERS = [
    {
        "user": {
            "first_name": "Sarah",
            "last_name": "Johnson",
            "email": "sarah.johnson@wealthadvisors.com",
            "phone_number": "555-0101",
            "password": "BrokerPass123!",
        },
        "broker": {
            "license_number": "LIC-2024-001",
            "license_status": LicenseStatus.ACTIVE,
            "company_name": "Wealth Advisors Inc.",
            "years_of_experience": 15,
            "experience_level": ExperienceLevel.EXPERT,
            "office_address": "123 Financial District, New York, NY 10004",
            "service_areas": ["New York", "New Jersey", "Connecticut"],
            "bio": "Expert wealth manager with 15 years of experience helping high net worth individuals achieve their financial goals.",
            "average_rating": 4.8,
            "success_rate": 0.92,
            "is_verified": True,
            "is_active": True,
        },
        "specializations": [
            "wealth_management",
            "estate_planning",
            "tax_strategies",
            "financial",
        ],
    },
    {
        "user": {
            "first_name": "Michael",
            "last_name": "Chen",
            "email": "michael.chen@retirementpros.com",
            "phone_number": "555-0102",
            "password": "BrokerPass123!",
        },
        "broker": {
            "license_number": "LIC-2024-002",
            "license_status": LicenseStatus.ACTIVE,
            "company_name": "Retirement Pros LLC",
            "years_of_experience": 10,
            "experience_level": ExperienceLevel.SENIOR,
            "office_address": "456 Retirement Plaza, Chicago, IL 60601",
            "service_areas": ["Illinois", "Wisconsin", "Indiana"],
            "bio": "Specialized in retirement planning with a focus on 401(k) optimization and pension strategies.",
            "average_rating": 4.6,
            "success_rate": 0.88,
            "is_verified": True,
            "is_active": True,
        },
        "specializations": [
            "retirement_planning",
            "financial_planning",
            "insurance_planning",
        ],
    },
    {
        "user": {
            "first_name": "Emily",
            "last_name": "Rodriguez",
            "email": "emily.rodriguez@techfinance.com",
            "phone_number": "555-0103",
            "password": "BrokerPass123!",
        },
        "broker": {
            "license_number": "LIC-2024-003",
            "license_status": LicenseStatus.ACTIVE,
            "company_name": "Tech Finance Advisors",
            "years_of_experience": 7,
            "experience_level": ExperienceLevel.INTERMEDIATE,
            "office_address": "789 Silicon Valley Blvd, San Francisco, CA 94105",
            "service_areas": ["California", "Oregon", "Washington"],
            "bio": "Tech-savvy financial advisor specializing in stock options, RSUs, and tech sector investments.",
            "average_rating": 4.5,
            "success_rate": 0.85,
            "is_verified": True,
            "is_active": True,
        },
        "specializations": [
            "investment_management",
            "technology",
            "wealth_management",
            "tax_strategies",
        ],
    },
    {
        "user": {
            "first_name": "David",
            "last_name": "Thompson",
            "email": "david.thompson@familyfinance.com",
            "phone_number": "555-0104",
            "password": "BrokerPass123!",
        },
        "broker": {
            "license_number": "LIC-2024-004",
            "license_status": LicenseStatus.ACTIVE,
            "company_name": "Family Finance Solutions",
            "years_of_experience": 5,
            "experience_level": ExperienceLevel.INTERMEDIATE,
            "office_address": "321 Main Street, Dallas, TX 75201",
            "service_areas": ["Texas", "Oklahoma", "Arkansas"],
            "bio": "Focused on helping young families with education planning, budgeting, and first-time home purchases.",
            "average_rating": 4.7,
            "success_rate": 0.90,
            "is_verified": True,
            "is_active": True,
        },
        "specializations": [
            "education_planning",
            "budgeting",
            "real_estate_planning",
            "insurance_planning",
        ],
    },
    {
        "user": {
            "first_name": "Jennifer",
            "last_name": "Williams",
            "email": "jennifer.williams@conservativeinvest.com",
            "phone_number": "555-0105",
            "password": "BrokerPass123!",
        },
        "broker": {
            "license_number": "LIC-2024-005",
            "license_status": LicenseStatus.ACTIVE,
            "company_name": "Conservative Investment Group",
            "years_of_experience": 3,
            "experience_level": ExperienceLevel.JUNIOR,
            "office_address": "555 Safety First Ave, Boston, MA 02108",
            "service_areas": ["Massachusetts", "Rhode Island", "New Hampshire"],
            "bio": "Specializing in conservative investment strategies for risk-averse clients and retirees.",
            "average_rating": 4.4,
            "success_rate": 0.82,
            "is_verified": True,
            "is_active": True,
        },
        "specializations": [
            "income_strategies",
            "dividend_investing",
            "retirement_planning",
        ],
    },
    {
        "user": {
            "first_name": "Robert",
            "last_name": "Anderson",
            "email": "robert.anderson@energyinvest.com",
            "phone_number": "555-0106",
            "password": "BrokerPass123!",
        },
        "broker": {
            "license_number": "LIC-2024-006",
            "license_status": LicenseStatus.ACTIVE,
            "company_name": "Energy Investment Partners",
            "years_of_experience": 12,
            "experience_level": ExperienceLevel.SENIOR,
            "office_address": "999 Oil Tower, Houston, TX 77002",
            "service_areas": ["Texas", "Louisiana", "New Mexico"],
            "bio": "Expert in energy sector investments with deep knowledge of oil, gas, and renewable energy markets.",
            "average_rating": 4.5,
            "success_rate": 0.87,
            "is_verified": True,
            "is_active": True,
        },
        "specializations": ["investment_management", "energy", "wealth_management"],
    },
]


def seed_brokers():
    """Seed the database with sample broker data"""
    db = SessionLocal()
    try:
        # First, create specializations
        print("Creating specializations...")
        for spec_data in SPECIALIZATIONS:
            existing_spec = (
                db.query(Specialization).filter_by(name=spec_data["name"]).first()
            )
            if not existing_spec:
                spec = Specialization(
                    id=str(uuid.uuid4()),
                    name=spec_data["name"],
                    description=spec_data["description"],
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                db.add(spec)
        db.commit()

        # Get all specializations for mapping
        all_specs = {spec.name: spec for spec in db.query(Specialization).all()}

        # Create brokers
        print("Creating sample brokers...")
        for broker_data in SAMPLE_BROKERS:
            # Check if user already exists
            existing_user = (
                db.query(User).filter_by(email=broker_data["user"]["email"]).first()
            )
            if existing_user:
                print(f"User {broker_data['user']['email']} already exists. Skipping.")
                continue

            # Create user with UUID
            user = User(
                id=str(uuid.uuid4()),
                first_name=broker_data["user"]["first_name"],
                last_name=broker_data["user"]["last_name"],
                email=broker_data["user"]["email"],
                phone_number=broker_data["user"]["phone_number"],
                password_hash=get_password_hash(broker_data["user"]["password"]),
                user_type=UserType.BROKER,
                is_verified=True,
            )
            db.add(user)
            db.flush()  # Get the user ID

            # Create broker profile
            broker = Broker(
                id=str(uuid.uuid4()),
                user_id=user.id,
                license_number=broker_data["broker"]["license_number"],
                license_status=broker_data["broker"]["license_status"],
                company_name=broker_data["broker"]["company_name"],
                years_of_experience=broker_data["broker"]["years_of_experience"],
                experience_level=broker_data["broker"]["experience_level"],
                office_address=broker_data["broker"]["office_address"],
                service_areas=broker_data["broker"]["service_areas"],
                bio=broker_data["broker"]["bio"],
                average_rating=broker_data["broker"]["average_rating"],
                success_rate=broker_data["broker"]["success_rate"],
                is_verified=broker_data["broker"]["is_verified"],
                is_active=broker_data["broker"]["is_active"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

            # Add specializations
            for spec_name in broker_data["specializations"]:
                if spec_name in all_specs:
                    broker.specializations.append(all_specs[spec_name])

            db.add(broker)
            print(f"Created broker: {user.full_name} ({broker.company_name})")

        db.commit()
        print("Successfully seeded broker data!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding broker data: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Starting broker data seeding...")
    seed_brokers()
    print("Finished broker data seeding.")
