from typing import List, Dict, Any, Optional
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from app.core.config import settings
from langchain.chains import LLMChain

# Import the appropriate LLM based on configuration
if settings.LLM_PROVIDER.lower() == "anthropic":
    from langchain_anthropic import ChatAnthropic as LLM
else:
    from langchain_openai import ChatOpenAI as LLM


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


class QuestionService:
    """Service for generating psychological questions based on book content."""

    def __init__(self):
        """Initialize the question service with the appropriate LLM."""
        self.llm = LLM(
            model=settings.LLM_MODEL_NAME,
            temperature=0.7,
        )
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

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

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
        if num_questions < 1:
            num_questions = 1
        elif num_questions > 5:
            num_questions = 5

        # Run the chain
        result = await self.chain.arun(
            title=book_title,
            author=book_author,
            content=book_content,
            num_questions=num_questions,
        )

        # Parse the result
        try:
            parsed_output = self.parser.parse(result)
            return parsed_output.questions
        except Exception as e:
            # Fallback to simple parsing if the LLM output doesn't match expected format
            questions = []
            # Try to extract questions manually from the text
            lines = result.strip().split("\n")
            current_question = None

            for line in lines:
                if line.strip().startswith("Question ") or line.strip().startswith(
                    "1."
                ):
                    if current_question:
                        questions.append(current_question)
                    current_question = {
                        "question_text": line.strip(),
                        "reasoning": "",
                        "tags": [],
                    }
                elif current_question and line.strip().startswith("Reasoning:"):
                    current_question["reasoning"] = line.replace(
                        "Reasoning:", ""
                    ).strip()
                elif current_question and line.strip().startswith("Tags:"):
                    tags_text = line.replace("Tags:", "").strip()
                    current_question["tags"] = [
                        tag.strip() for tag in tags_text.split(",")
                    ]

            if current_question:
                questions.append(current_question)

            return questions[:num_questions]
