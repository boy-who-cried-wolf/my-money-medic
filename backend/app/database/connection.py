from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get database connection parameters - Railway typically uses DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback to individual environment variables if DATABASE_URL is not set
if not DATABASE_URL:
    DB_USER = os.getenv("DO_DB_USER")
    DB_PASSWORD = os.getenv("DO_DB_PASSWORD")
    DB_HOST = os.getenv("DO_DB_HOST")
    DB_PORT = os.getenv("DO_DB_PORT")
    DB_NAME = os.getenv("DO_DB_NAME")

    if all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
        DATABASE_URL = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        logger.info(
            f"Connecting to database: {DB_NAME} as {DB_USER} on {DB_HOST}:{DB_PORT}"
        )
    else:
        # Default to SQLite for development
        DATABASE_URL = "sqlite:///./test.db"
        logger.warning(
            "Warning: No database configuration found, using SQLite for development"
        )

logger.info(f"Database URL configured: {DATABASE_URL[:50]}...")

# Create engine with appropriate configurations
try:
    if DATABASE_URL.startswith("mysql"):
        # MySQL/MariaDB configuration
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=300,
            pool_timeout=20,
            max_overflow=0,
            echo=False,  # Set to True for SQL debugging
        )
    elif DATABASE_URL.startswith("postgresql"):
        # PostgreSQL configuration (Railway often uses PostgreSQL)
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=300,
            pool_timeout=20,
            max_overflow=0,
            echo=False,
        )
    else:
        # SQLite or other database
        engine = create_engine(DATABASE_URL, echo=False)

    logger.info("Database engine created successfully")

except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}")
    # Use SQLite as absolute fallback
    DATABASE_URL = "sqlite:///./fallback.db"
    engine = create_engine(DATABASE_URL, echo=False)
    logger.warning("Using SQLite fallback database")

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


# Test database connection
def test_connection():
    """Test database connection"""
    try:
        from sqlalchemy import text

        with engine.connect() as connection:
            # Use text() for raw SQL to work with all database types
            connection.execute(text("SELECT 1"))
        logger.info("Database connection test successful")
        return True
    except Exception as e:
        logger.error(f"Database connection test failed: {str(e)}")
        return False


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_database_info():
    """Get information about the current database connection"""
    if DATABASE_URL.startswith("mysql"):
        return f"MySQL Database (DigitalOcean): {DATABASE_URL.split('@')[1].split('/')[0] if '@' in DATABASE_URL else 'Unknown Host'}"
    elif DATABASE_URL.startswith("postgresql"):
        return f"PostgreSQL Database: {DATABASE_URL.split('@')[1].split('/')[0] if '@' in DATABASE_URL else 'Unknown Host'}"
    elif DATABASE_URL.startswith("sqlite"):
        return f"SQLite Database (Local): {DATABASE_URL.replace('sqlite:///', '')}"
    else:
        return f"Database: {DATABASE_URL[:50]}..."
