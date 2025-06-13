#!/usr/bin/env python3
"""
Startup diagnostic script for Railway deployment
This script helps diagnose common deployment issues
"""

import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def check_environment():
    """Check environment variables"""
    logger.info("=== Environment Check ===")

    # Check Python version
    logger.info(f"Python version: {sys.version}")

    # Check working directory
    logger.info(f"Working directory: {os.getcwd()}")

    # Check important environment variables
    env_vars = [
        "PORT",
        "DATABASE_URL",
        "SECRET_KEY",
        "DO_DB_USER",
        "DO_DB_PASSWORD",
        "DO_DB_HOST",
        "RAILWAY_ENVIRONMENT",
        "RAILWAY_SERVICE_NAME",
    ]

    for var in env_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if "password" in var.lower() or "key" in var.lower():
                masked_value = (
                    f"{value[:4]}***{value[-4:]}" if len(value) > 8 else "***"
                )
                logger.info(f"{var}: {masked_value}")
            else:
                logger.info(f"{var}: {value}")
        else:
            logger.warning(f"{var}: NOT SET")


def check_files():
    """Check required files"""
    logger.info("=== File Check ===")

    required_files = [
        "server.py",
        "requirements.txt",
        "app/__init__.py",
        "app/database/__init__.py",
    ]

    for file_path in required_files:
        if Path(file_path).exists():
            logger.info(f"✓ {file_path} exists")
        else:
            logger.error(f"✗ {file_path} missing")


def test_imports():
    """Test critical imports"""
    logger.info("=== Import Check ===")

    try:
        import fastapi

        logger.info(f"✓ FastAPI {fastapi.__version__}")
    except ImportError as e:
        logger.error(f"✗ FastAPI import failed: {e}")

    try:
        import uvicorn

        logger.info(f"✓ Uvicorn {uvicorn.__version__}")
    except ImportError as e:
        logger.error(f"✗ Uvicorn import failed: {e}")

    try:
        import sqlalchemy

        logger.info(f"✓ SQLAlchemy {sqlalchemy.__version__}")
    except ImportError as e:
        logger.error(f"✗ SQLAlchemy import failed: {e}")


def test_app_import():
    """Test importing the FastAPI app"""
    logger.info("=== App Import Check ===")

    try:
        from server import app

        logger.info("✓ FastAPI app imported successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to import FastAPI app: {e}")
        return False


def main():
    """Run all diagnostic checks"""
    logger.info("Starting Railway deployment diagnostics...")

    check_environment()
    check_files()
    test_imports()
    app_imported = test_app_import()

    if app_imported:
        logger.info("🎉 All checks passed! App should start successfully.")
    else:
        logger.error("❌ Some checks failed. Review the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
