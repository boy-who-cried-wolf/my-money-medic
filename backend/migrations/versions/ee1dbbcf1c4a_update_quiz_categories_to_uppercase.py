"""Update quiz categories to uppercase

Revision ID: ee1dbbcf1c4a
Revises: f1a9044368c8
Create Date: 2024-03-27 19:18:56.330021

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ee1dbbcf1c4a'
down_revision = 'f1a9044368c8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # First, drop the foreign key constraint from messages to conversations
    op.drop_constraint('messages_ibfk_1', 'messages', type_='foreignkey')
    
    # Update quiz categories to uppercase
    op.execute("""
        UPDATE quizzes 
        SET category = UPPER(category)
        WHERE category IN ('financial_goals', 'experience', 'risk_tolerance', 'preferences', 'broker_matching')
    """)
    
    # Recreate the foreign key constraint
    op.create_foreign_key(
        'messages_ibfk_1',
        'messages', 'conversations',
        ['conversation_id'], ['id']
    )


def downgrade() -> None:
    # First, drop the foreign key constraint
    op.drop_constraint('messages_ibfk_1', 'messages', type_='foreignkey')
    
    # Convert categories back to lowercase
    op.execute("""
        UPDATE quizzes 
        SET category = LOWER(category)
        WHERE category IN ('FINANCIAL_GOALS', 'EXPERIENCE', 'RISK_TOLERANCE', 'PREFERENCES', 'BROKER_MATCHING')
    """)
    
    # Recreate the foreign key constraint
    op.create_foreign_key(
        'messages_ibfk_1',
        'messages', 'conversations',
        ['conversation_id'], ['id']
    ) 