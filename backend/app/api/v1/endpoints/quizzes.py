from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.database import get_db
from app.schemas.quiz import (
    QuizCreate,
    QuizResponse,
    QuizQuestionCreate,
    QuizQuestionResponse,
    UserQuizResponseCreate,
    UserQuizResponseResponse,
    QuizAnalyticsResponse,
)
from app.services import quiz_service
from app.core.security import verify_token
from app.database.models.quiz import Quiz, QuizQuestion
from uuid import UUID

router = APIRouter()


# Quiz management endpoints
@router.post("/", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db)):
    """Create a new quiz"""
    return quiz_service.create_quiz(db=db, quiz=quiz)


@router.get("/", response_model=List[Dict[str, Any]])
def get_quizzes(
    db: Session = Depends(get_db),
    user_id: str = Depends(verify_token),
    skip: int = 0,
    limit: int = 10,
):
    """Get all available quizzes"""
    try:
        quizzes = db.query(Quiz).offset(skip).limit(limit).all()
        return [
            {
                "id": str(quiz.id),
                "title": quiz.title,
                "description": quiz.description,
                "category": quiz.category,
                "created_at": quiz.created_at,
                "question_count": db.query(QuizQuestion)
                .filter(QuizQuestion.quiz_id == quiz.id)
                .count(),
            }
            for quiz in quizzes
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{quiz_id}", response_model=Dict[str, Any])
def get_quiz(
    quiz_id: UUID, db: Session = Depends(get_db), user_id: str = Depends(verify_token)
):
    """Get a specific quiz with questions"""
    try:
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Quiz with ID {quiz_id} not found",
            )

        questions = (
            db.query(QuizQuestion)
            .filter(QuizQuestion.quiz_id == quiz_id)
            .order_by(QuizQuestion.order)
            .all()
        )

        return {
            "id": str(quiz.id),
            "title": quiz.title,
            "description": quiz.description,
            "category": quiz.category,
            "created_at": quiz.created_at,
            "questions": [
                {
                    "id": str(q.id),
                    "text": q.text,
                    "question_type": q.question_type,
                    "options": q.options,
                    "order": q.order,
                    "weight": q.weight,
                }
                for q in questions
            ],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(quiz_id: str, db: Session = Depends(get_db)):
    """Delete a quiz (soft delete)"""
    db_quiz = quiz_service.get_quiz(db=db, quiz_id=quiz_id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    quiz_service.delete_quiz(db=db, quiz_id=quiz_id)
    return None


# Quiz question endpoints
@router.post(
    "/{quiz_id}/questions",
    response_model=QuizQuestionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_question(
    quiz_id: str, question: QuizQuestionCreate, db: Session = Depends(get_db)
):
    """Add a question to a quiz"""
    db_quiz = quiz_service.get_quiz(db=db, quiz_id=quiz_id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz_service.create_question(db=db, quiz_id=quiz_id, question=question)


@router.get("/{quiz_id}/questions", response_model=List[QuizQuestionResponse])
def read_questions(quiz_id: UUID, db: Session = Depends(get_db)):
    """Get all questions for a quiz"""
    db_quiz = quiz_service.get_quiz(db=db, quiz_id=quiz_id)
    if db_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz_service.get_questions(db=db, quiz_id=quiz_id)


# User quiz response endpoints
@router.post(
    "/responses",
    response_model=UserQuizResponseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user_response(
    response: UserQuizResponseCreate, db: Session = Depends(get_db)
):
    """Save user's response to a quiz question"""
    return quiz_service.create_user_response(db=db, response=response)


@router.get("/user/{user_id}/responses", response_model=List[UserQuizResponseResponse])
def read_user_responses(user_id: str, db: Session = Depends(get_db)):
    """Get all responses for a user"""
    return quiz_service.get_user_responses(db=db, user_id=user_id)


@router.get("/match/{user_id}", response_model=List[QuizResponse])
def get_matching_quiz(user_id: str, db: Session = Depends(get_db)):
    """Get a quiz for matching a user with brokers"""
    return quiz_service.get_matching_quiz(db=db, user_id=user_id)


@router.post("/{quiz_id}/submit", status_code=status.HTTP_200_OK)
def submit_quiz(
    quiz_id: str,
    responses: List[Dict[str, Any]],
    db: Session = Depends(get_db),
    user_id: str = Depends(verify_token),
):
    """Submit a complete quiz with all user responses and generate matches"""
    try:
        from app.database.models.quiz import UserQuizResponse, QuizQuestion
        from app.services.matching_algorithm import generate_broker_matches
        import json

        # Verify quiz exists
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Quiz with ID {quiz_id} not found",
            )

        # Delete any existing responses for this user and quiz
        existing_responses = (
            db.query(UserQuizResponse)
            .join(QuizQuestion)
            .filter(
                UserQuizResponse.user_id == user_id, QuizQuestion.quiz_id == quiz_id
            )
            .all()
        )

        for response in existing_responses:
            db.delete(response)

        # Save new responses
        saved_responses = []
        for response_data in responses:
            question_id = response_data.get("question_id")
            answer = response_data.get("answer")

            if not question_id or answer is None:
                continue

            # Verify question belongs to this quiz
            question = (
                db.query(QuizQuestion)
                .filter(QuizQuestion.id == question_id, QuizQuestion.quiz_id == quiz_id)
                .first()
            )

            if not question:
                continue

            # Create response
            user_response = UserQuizResponse(
                user_id=user_id,
                question_id=question_id,
                response=json.dumps(answer) if isinstance(answer, list) else answer,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(user_response)
            saved_responses.append(user_response)

        # Commit responses
        db.commit()

        # Generate matches if this is the broker matching quiz
        matches = []
        if (
            quiz.category.value == "BROKER_MATCHING"
            or quiz.category.value == "broker_matching"
        ):
            match_results = generate_broker_matches(
                db=db, user_id=user_id, save_to_db=True
            )
            matches = match_results[:5]  # Return top 5 matches

        return {
            "message": "Quiz submitted successfully",
            "user_id": user_id,
            "quiz_id": quiz_id,
            "responses_saved": len(saved_responses),
            "matches_generated": len(matches),
            "top_matches": matches,
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error submitting quiz: {str(e)}",
        )


@router.get("/analytics/{quiz_id}", response_model=QuizAnalyticsResponse)
def get_quiz_analytics(quiz_id: str, db: Session = Depends(get_db)):
    """Get analytics for a quiz"""
    return quiz_service.get_quiz_analytics(db=db, quiz_id=quiz_id)


@router.get("/public", response_model=List[Dict[str, Any]])
def get_public_quizzes(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    """Get all available quizzes - public endpoint for testing, no auth required"""
    try:
        quizzes = db.query(Quiz).offset(skip).limit(limit).all()
        return [
            {
                "id": str(quiz.id),
                "title": quiz.title,
                "description": quiz.description,
                "category": quiz.category,
                "created_at": quiz.created_at,
                "question_count": db.query(QuizQuestion)
                .filter(QuizQuestion.quiz_id == quiz.id)
                .count(),
            }
            for quiz in quizzes
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
