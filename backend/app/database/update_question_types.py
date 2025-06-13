"""
Script for updating the question types in the database.
This will add the 'multiple_select' type to the enum in the database.
"""

import sys
import os
from pathlib import Path

# Add the root directory to the Python path
backend_dir = Path(__file__).parent.parent.parent  # backend/
sys.path.insert(0, str(backend_dir))

from app.database.connection import engine
from sqlalchemy import text


def update_question_types():
    """Updates the enum types in the database for quiz questions"""
    with engine.connect() as conn:
        # First, check if the enum type with 'multiple_select' already exists
        try:
            # MySQL/MariaDB access - add enum type
            conn.execute(
                text(
                    """
                ALTER TABLE quiz_questions 
                MODIFY COLUMN question_type ENUM(
                    'multiple_choice', 
                    'multiple_select', 
                    'single_choice', 
                    'text', 
                    'scale', 
                    'boolean'
                ) NOT NULL;
            """
                )
            )
            conn.commit()
            print("Successfully updated the enum type for the question_type column!")
        except Exception as e:
            print(f"Error updating the enum type: {str(e)}")
            conn.rollback()


if __name__ == "__main__":
    print("Updating the question types in the database...")
    update_question_types()
    print("Update completed.")
