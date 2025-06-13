"""
Question generator module for creating psychological questions from book content.
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from app.core.config import settings
from app.ai.base import BaseAIService


class Question(BaseModel):
    """Model for a psychological question."""

    question_text: str = Field(description="The text of the psychological question")
    reasoning: str = Field(
        description="The psychological reasoning behind the question"
    )
    tags: List[str] = Field(
        description="Psychological concepts or themes related to this question"
    )


class QuestionList(BaseModel):
    """Model for a list of psychological questions."""

    questions: List[Question] = Field(description="List of psychological questions")


class QuestionGenerator(BaseAIService):
    """
    Specialized service for generating psychological questions from book content.

    This class extends the BaseAIService to provide specific functionality
    for generating insightful psychological questions based on book excerpts.
    """

    def __init__(self, model_name=None, temperature=0.7):
        """Initialize the question generator service."""
        super().__init__(model_name, temperature)

        # Set up the output parser
        self.parser = PydanticOutputParser(pydantic_object=QuestionList)

        # Create the prompt template
        self.prompt_template = PromptTemplate(
            template="""
            Based on the following excerpt from a psychological book, generate {num_questions} thought-provoking
            questions that would help someone gain deeper insights into themselves.
            
            Book title: {title}
            Book author: {author}
            Excerpt: {content}
            
            For each question, provide:
            1. The question text
            2. The psychological reasoning behind asking this question
            3. Relevant psychological concepts or themes (as tags)
            
            {format_instructions}
            """,
            input_variables=["title", "author", "content", "num_questions"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        # Create the generation chain
        self.chain = self.create_chain(self.prompt_template)

    async def generate_questions(
        self,
        book_content: str,
        book_title: str,
        book_author: str,
        num_questions: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Generate psychological questions based on book content.

        Args:
            book_content: The excerpt from the psychological book
            book_title: The title of the book
            book_author: The author of the book
            num_questions: Number of questions to generate (default: 3)

        Returns:
            List of generated questions with reasoning and tags
        """
        # Validate and constrain input
        if num_questions < 1:
            num_questions = 1
        elif num_questions > settings.MAX_QUESTIONS_PER_REQUEST:
            num_questions = settings.MAX_QUESTIONS_PER_REQUEST

        # Generate the response
        result = await self.generate(
            self.chain,
            title=book_title,
            author=book_author,
            content=book_content,
            num_questions=num_questions,
        )

        # Parse the result
        try:
            parsed_output = self.parser.parse(result.content)
            return parsed_output.questions
        except Exception as e:
            # Fallback to simple parsing if the LLM output doesn't match expected format
            return self._fallback_parse(
                result.content if hasattr(result, "content") else str(result),
                num_questions,
            )

    def _fallback_parse(self, text: str, num_questions: int) -> List[Dict[str, Any]]:
        """
        Fallback parsing method for when structured parsing fails.

        Args:
            text: The raw text from the LLM
            num_questions: Maximum number of questions to return

        Returns:
            List of question dictionaries
        """
        questions = []
        # Try to extract questions manually from the text
        lines = text.strip().split("\n")
        current_question = None

        for line in lines:
            if line.strip().startswith("Question ") or line.strip().startswith("1."):
                if current_question:
                    questions.append(current_question)
                current_question = {
                    "question_text": line.strip(),
                    "reasoning": "",
                    "tags": [],
                }
            elif current_question and line.strip().startswith("Reasoning:"):
                current_question["reasoning"] = line.replace("Reasoning:", "").strip()
            elif current_question and line.strip().startswith("Tags:"):
                tags_text = line.replace("Tags:", "").strip()
                current_question["tags"] = [tag.strip() for tag in tags_text.split(",")]

        if current_question:
            questions.append(current_question)

        return questions[:num_questions]
