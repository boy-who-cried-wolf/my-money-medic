from .connection import engine, get_db, Base, test_connection
from .models import *
import logging

logger = logging.getLogger(__name__)


def init_db():
    """
    Initialize the database and create all tables.

    This function creates all tables defined in the models.
    It should be called when the application starts.
    """
    try:
        # Test database connection first
        if not test_connection():
            logger.error("Database connection test failed - skipping table creation")
            return False

        # Create all tables
        Base.metadata.create_all(bind=engine)

        # Log successful initialization
        logger.info("Database initialized successfully.")
        return True

    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        logger.warning("Application will continue without database initialization")
        return False


# Export dependencies
__all__ = ["init_db", "get_db", "engine", "Base"]
