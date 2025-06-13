"""
Direct question generator module using Google Gen AI SDK without LangChain.
"""

import json
from typing import List, Dict, Any
from app.core.config import settings
import google.generativeai as genai
from tqdm import tqdm


class DirectQuestionGenerator:
    """
    Question generator that directly uses Google's Gen AI SDK.

    This class bypasses LangChain entirely and uses the official Google SDK,
    which is more robust to API changes.
    """

    def __init__(self, model_name=None, temperature=0.7):
        """Initialize the direct question generator."""
        self.model_name = model_name or settings.LLM_MODEL_NAME
        self.temperature = temperature

        # Configure the API
        genai.configure(api_key=settings.GEMINI_API_KEY)

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

        # Create the prompt with JSON output instructions
        prompt = f"""
        Based on the following excerpt from a psychological book, generate {num_questions} thought-provoking
        questions that would help someone gain deeper insights into themselves.
        
        Book title: {book_title}
        Book author: {book_author}
        Excerpt: {book_content}
        
        For each question, provide:
        1. The question text
        2. The psychological reasoning behind asking this question
        3. Relevant psychological concepts or themes (as tags)
        
        Return your response in the following JSON format:
        {{
            "questions": [
                {{
                    "question_text": "Question 1?",
                    "reasoning": "Reasoning for question 1",
                    "tags": ["tag1", "tag2", "tag3"]
                }},
                ...
            ]
        }}
        """

        try:
            # Show loading spinner
            with tqdm(
                total=1,
                desc="Generating AI questions",
                bar_format="{desc}: {percentage:3.0f}%|{bar}| {elapsed} elapsed",
            ) as pbar:
                # Initialize the model
                model = genai.GenerativeModel(
                    model_name=self.model_name,
                    generation_config={"temperature": self.temperature},
                )

                # Call the Gemini API
                response = model.generate_content(prompt)

                # Update progress
                pbar.update(1)

            # Parse the JSON response
            try:
                # Try to parse the JSON directly
                result = json.loads(response.text)
                return result.get("questions", [])
            except json.JSONDecodeError:
                # If direct JSON parsing fails, extract JSON from the text
                return self._extract_json_from_text(response.text)

        except Exception as e:
            # Fallback to simpler approach if needed
            print(f"Error generating questions: {str(e)}")
            return self._generate_fallback_questions(
                book_title, book_author, num_questions
            )

    def _extract_json_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract JSON from text that might contain markdown or other content."""
        # Look for JSON block in markdown
        if "```json" in text and "```" in text.split("```json", 1)[1]:
            json_text = text.split("```json", 1)[1].split("```", 1)[0].strip()
            try:
                data = json.loads(json_text)
                return data.get("questions", [])
            except:
                pass

        # Try to find anything that looks like JSON
        import re

        json_pattern = r"(\{.*?\})"
        match = re.search(json_pattern, text, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(0))
                if "questions" in data:
                    return data.get("questions", [])
            except:
                pass

        # Manual parsing as last resort
        return self._parse_text_as_questions(text)

    def _parse_text_as_questions(self, text: str) -> List[Dict[str, Any]]:
        """Parse plain text into question structures."""
        questions = []
        lines = text.strip().split("\n")
        current_question = None

        for line in lines:
            if "Question" in line or line.strip().startswith("1."):
                if current_question:
                    questions.append(current_question)
                current_question = {
                    "question_text": line.strip(),
                    "reasoning": "",
                    "tags": [],
                }
            elif current_question and ("Reasoning" in line or "reasoning" in line):
                parts = line.split(":", 1)
                if len(parts) > 1:
                    current_question["reasoning"] = parts[1].strip()
            elif current_question and ("Tags" in line or "tags" in line):
                parts = line.split(":", 1)
                if len(parts) > 1:
                    current_question["tags"] = [
                        tag.strip() for tag in parts[1].split(",")
                    ]

        if current_question:
            questions.append(current_question)

        return questions

    def _generate_fallback_questions(
        self, title: str, author: str, num_questions: int
    ) -> List[Dict[str, Any]]:
        """Generate fallback questions if everything else fails."""
        return [
            {
                "question_text": f"How do the ideas in '{title}' by {author} relate to your personal experiences?",
                "reasoning": "This question helps connect psychological concepts to personal life events",
                "tags": ["self-reflection", "personal experience", "application"],
            },
            {
                "question_text": "What emotions arise when you consider implementing these psychological concepts in your daily life?",
                "reasoning": "Emotional awareness is key to psychological growth and self-understanding",
                "tags": ["emotional awareness", "implementation", "daily practice"],
            },
            {
                "question_text": "Which concept from this reading challenges your current beliefs most strongly?",
                "reasoning": "Confronting challenging ideas facilitates cognitive restructuring and growth",
                "tags": ["cognitive dissonance", "belief systems", "growth mindset"],
            },
        ][:num_questions]
