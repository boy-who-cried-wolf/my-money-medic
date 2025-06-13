from sqlalchemy import Column, String, Text, ForeignKey, Integer, Enum, JSON, Boolean
from sqlalchemy.orm import relationship
import enum
from uuid import UUID

from .base import SoftDeleteModel, EnumAsStr


class QuestionType(enum.Enum):
    """Enum for quiz question types"""

    MULTIPLE_CHOICE = "multiple_choice"
    MULTIPLE_SELECT = "multiple_select"
    SINGLE_CHOICE = "single_choice"
    TEXT = "text"
    SCALE = "scale"
    BOOLEAN = "boolean"


class QuizCategory(enum.Enum):
    """Enum for quiz categories"""

    FINANCIAL_GOALS = "FINANCIAL_GOALS"
    EXPERIENCE = "EXPERIENCE"
    RISK_TOLERANCE = "RISK_TOLERANCE"
    PREFERENCES = "PREFERENCES"
    BROKER_MATCHING = "BROKER_MATCHING"


class Quiz(SoftDeleteModel):
    """
    Quiz model for storing quizzes
    """

    __tablename__ = "quizzes"

    title = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(EnumAsStr(QuizCategory, length=50), nullable=False)

    # Relationships
    questions = relationship(
        "QuizQuestion", back_populates="quiz", cascade="all, delete-orphan"
    )

    def __repr__(self):
        """String representation of the quiz"""
        return f"<Quiz {self.title}>"


class QuizQuestion(SoftDeleteModel):
    """
    Quiz Question model for storing quiz questions
    """

    __tablename__ = "quiz_questions"

    quiz_id = Column(ForeignKey("quizzes.id"), nullable=False)
    text = Column(Text, nullable=False)
    question_type = Column(EnumAsStr(QuestionType, length=50), nullable=False)
    options = Column(JSON, nullable=True)  # For multiple/single choice questions
    order = Column(Integer, nullable=False)
    weight = Column(Integer, default=1)  # For weighted scoring

    # Relationships
    quiz = relationship("Quiz", back_populates="questions")
    responses = relationship(
        "UserQuizResponse", back_populates="question", cascade="all, delete-orphan"
    )

    def __repr__(self):
        """String representation of the quiz question"""
        return f"<QuizQuestion {self.text[:20]}...>"


class UserQuizResponse(SoftDeleteModel):
    """
    User Quiz Response model for storing user's answers to quiz questions
    """

    __tablename__ = "user_quiz_responses"

    user_id = Column(ForeignKey("users.id"), nullable=False)
    question_id = Column(ForeignKey("quiz_questions.id"), nullable=False)
    response = Column(JSON, nullable=False)  # Store any type of response

    # Relationships
    user = relationship("User", back_populates="quiz_responses")
    question = relationship("QuizQuestion", back_populates="responses")

    def __repr__(self):
        """String representation of the user quiz response"""
        return f"<UserQuizResponse {self.user_id} - {self.question_id}>"
