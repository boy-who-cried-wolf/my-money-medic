from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel, Field
from app.ai.direct_question_generator import DirectQuestionGenerator
from app.core.config import settings
from app.core.auth import get_current_user
from app.schemas.user import User

router = APIRouter()
question_generator = DirectQuestionGenerator()


class BookExcerpt(BaseModel):
    """Schema for book excerpt input."""

    title: str = Field(
        ..., min_length=1, description="The title of the psychological book"
    )
    author: str = Field(
        ..., min_length=1, description="The author of the psychological book"
    )
    content: str = Field(
        ...,
        min_length=settings.MIN_BOOK_EXCERPT_LENGTH,
        description="Excerpt from the psychological book",
    )
    num_questions: int = Field(
        3,
        ge=1,
        le=settings.MAX_QUESTIONS_PER_REQUEST,
        description="Number of questions to generate",
    )


class QuestionResponse(BaseModel):
    """Schema for a generated psychological question."""

    question_text: str = Field(
        ..., description="The text of the psychological question"
    )
    reasoning: str = Field(
        ..., description="The psychological reasoning behind the question"
    )
    tags: List[str] = Field(
        ..., description="Psychological concepts or themes related to this question"
    )


class QuestionsResponse(BaseModel):
    """Schema for the response containing generated questions."""

    questions: List[QuestionResponse] = Field(
        ..., description="Generated psychological questions"
    )


# Optional dependency for current user that allows None in development mode
async def get_optional_current_user(
    current_user: User = Depends(get_current_user),
) -> Optional[User]:
    """
    Get the current user or return None in development mode.

    This allows endpoints to work without authentication in development.
    """
    return current_user


@router.post(
    "/generate", response_model=QuestionsResponse, status_code=status.HTTP_200_OK
)
async def generate_questions(
    book_excerpt: BookExcerpt,
    current_user: Optional[User] = Depends(get_optional_current_user),
):
    """
    Generate psychological questions based on a book excerpt.

    This endpoint requires authentication in production, but can work without
    authentication in development mode.
    """
    try:
        questions = await question_generator.generate_questions(
            book_content=book_excerpt.content,
            book_title=book_excerpt.title,
            book_author=book_excerpt.author,
            num_questions=book_excerpt.num_questions,
        )

        return {"questions": questions}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate questions: {str(e)}",
        )


@router.post(
    "/generate/public", response_model=QuestionsResponse, status_code=status.HTTP_200_OK
)
async def generate_questions_public(book_excerpt: BookExcerpt):
    """
    Generate psychological questions based on a book excerpt (public endpoint).

    This public endpoint does not require authentication and will generate
    thought-provoking psychological questions based on the provided book excerpt.
    """
    # For public endpoint, limit the number of questions to 3
    book_excerpt.num_questions = min(book_excerpt.num_questions, 3)

    try:
        questions = await question_generator.generate_questions(
            book_content=book_excerpt.content,
            book_title=book_excerpt.title,
            book_author=book_excerpt.author,
            num_questions=book_excerpt.num_questions,
        )

        return {"questions": questions}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate questions: {str(e)}",
        )
