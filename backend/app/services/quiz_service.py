"""
Service module for quiz-related business logic.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import uuid4, UUID

from app.database.models.quiz import (
    Quiz,
    QuizQuestion,
    UserQuizResponse,
    QuestionType,
    QuizCategory,
)
from app.schemas.quiz import (
    QuizCreate,
    QuizQuestionCreate,
    UserQuizResponseCreate,
)


def create_quiz(db: Session, quiz: QuizCreate) -> Quiz:
    """
    Create a new quiz
    """
    db_quiz = Quiz(
        id=str(uuid4()),
        title=quiz.title,
        description=quiz.description,
        category=quiz.category,
    )
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz


def get_quizzes(db: Session, skip: int = 0, limit: int = 100) -> List[Quiz]:
    """
    Get all quizzes with pagination
    """
    return (
        db.query(Quiz).filter(Quiz.is_deleted.is_(None)).offset(skip).limit(limit).all()
    )


def get_quiz(db: Session, quiz_id: UUID) -> Optional[Quiz]:
    """
    Get quiz by ID
    """
    return (
        db.query(Quiz)
        .filter(Quiz.id == str(quiz_id), Quiz.is_deleted.is_(None))
        .first()
    )


def delete_quiz(db: Session, quiz_id: UUID) -> None:
    """
    Delete a quiz (soft delete)
    """
    db_quiz = get_quiz(db, quiz_id)
    if db_quiz:
        db_quiz.is_deleted = True
        db.commit()


def create_question(
    db: Session, quiz_id: UUID, question: QuizQuestionCreate
) -> QuizQuestion:
    """
    Add a question to a quiz
    """
    db_question = QuizQuestion(
        id=str(uuid4()),
        quiz_id=str(quiz_id),
        text=question.text,
        question_type=question.question_type,
        options=question.options,
        order=question.order,
        weight=question.weight if hasattr(question, "weight") else 1,
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def get_questions(db: Session, quiz_id: UUID) -> List[QuizQuestion]:
    """
    Get all questions for a quiz
    """
    return (
        db.query(QuizQuestion)
        .filter(QuizQuestion.quiz_id == str(quiz_id), QuizQuestion.is_deleted.is_(None))
        .order_by(QuizQuestion.order)
        .all()
    )


def create_user_response(
    db: Session, response: UserQuizResponseCreate
) -> UserQuizResponse:
    """
    Save user's response to a quiz question
    """
    db_response = UserQuizResponse(
        id=str(uuid4()),
        user_id=response.user_id,
        question_id=response.question_id,
        response=response.response,
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


def get_user_responses(db: Session, user_id: str) -> List[UserQuizResponse]:
    """
    Get all responses for a user
    """
    return (
        db.query(UserQuizResponse)
        .filter(
            UserQuizResponse.user_id == user_id, UserQuizResponse.is_deleted.is_(None)
        )
        .all()
    )


def get_matching_quiz(db: Session, user_id: str) -> List[Quiz]:
    """
    Get a quiz for matching a user with brokers
    """
    # For now, just return all quizzes in the BROKER_MATCHING category
    return (
        db.query(Quiz)
        .filter(
            Quiz.category == QuizCategory.BROKER_MATCHING, Quiz.is_deleted.is_(None)
        )
        .all()
    )
