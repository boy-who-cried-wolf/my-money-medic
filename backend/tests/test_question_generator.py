"""
Tests for the question generator functionality.
"""

import os
import pytest
import sys
from pathlib import Path

# Add the parent directory to the path
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

from app.ai.direct_question_generator import DirectQuestionGenerator


@pytest.mark.asyncio
async def test_direct_question_generator():
    """Test that the DirectQuestionGenerator can generate questions."""
    # Sample content
    sample_content = """
    Psychology is the scientific study of mind and behavior. The field explores cognitive, 
    emotional, and social processes and behaviors by analyzing how people think, feel, 
    learn, interact, perceive, and understand themselves and others. Self-awareness is a 
    fundamental aspect of psychological development, enabling individuals to reflect on 
    their experiences, emotions, and thought patterns.
    """
    sample_title = "Introduction to Psychology"
    sample_author = "Test Author"

    # Initialize the generator
    generator = DirectQuestionGenerator()

    # Generate questions
    questions = await generator.generate_questions(
        book_content=sample_content,
        book_title=sample_title,
        book_author=sample_author,
        num_questions=2,
    )

    # Verify results
    assert questions is not None, "Questions should not be None"
    assert len(questions) > 0, "Should generate at least one question"

    # Check question structure
    if questions:
        question = questions[0]
        assert "question_text" in question, "Question should have 'question_text'"
        assert "reasoning" in question, "Question should have 'reasoning'"
        assert "tags" in question, "Question should have 'tags'"
        assert isinstance(question["tags"], list), "Tags should be a list"


@pytest.mark.asyncio
async def test_question_generation_limits():
    """Test that the question generator respects the limits."""
    # Sample content
    sample_content = "This is a test content."
    sample_title = "Test Book"
    sample_author = "Test Author"

    # Initialize the generator
    generator = DirectQuestionGenerator()

    # Test with different limits
    for num in [1, 3, 5]:
        questions = await generator.generate_questions(
            book_content=sample_content,
            book_title=sample_title,
            book_author=sample_author,
            num_questions=num,
        )

        # There might be fewer questions than requested if the content is short
        assert len(questions) <= num, f"Should generate at most {num} questions"


if __name__ == "__main__":
    # This allows running the tests directly with pytest
    pytest.main(["-xvs", __file__])
