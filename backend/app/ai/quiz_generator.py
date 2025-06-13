"""
Quiz Question Generator using Gemini AI.

This module uses the GeminiService to generate quiz questions, including text
and multiple-choice options, tailored for a broker matching platform.
"""

from typing import List, Optional, Dict, Any
from uuid import uuid4

from app.ai.gemini_service import (
    GeminiService,
)  # Assuming GeminiService is in the same directory

# from app.database.models.quiz import QuestionType # If you need to reference the enum directly


class QuizQuestionGenerator:
    """
    Generates quiz questions and their components using an AI service (Gemini).
    """

    def __init__(self, gemini_service: Optional[GeminiService] = None):
        """
        Initializes the QuizQuestionGenerator.

        Args:
            gemini_service (Optional[GeminiService]):
                An instance of GeminiService. If None, a default one will be created.
        """
        self.ai_service = gemini_service or GeminiService()
        # In a real app, you might pass the GeminiService instance via dependency injection.

    async def generate_question_text(
        self,
        topic: str,
        category: str,  # e.g., "FINANCIAL_GOALS", "RISK_TOLERANCE"
        existing_questions_texts: Optional[List[str]] = None,
    ) -> Optional[str]:
        """
        Generates the text for a single quiz question based on a topic and category.

        Args:
            topic (str): The specific topic for the question (e.g., "Retirement Planning Horizon").
            category (str): The broader category of the quiz (e.g., "Financial Goals").
            existing_questions_texts (Optional[List[str]]):
                A list of existing question texts to encourage novelty.

        Returns:
            Optional[str]: The generated question text, or None on failure.
        """
        prompt = f"""
        You are an AI assistant designing a quiz for a broker matching platform. 
        Your task is to generate ONE clear, concise, and relevant quiz question for a client.

        Quiz Category: {category}
        Specific Topic: {topic}

        The question should help assess a client's needs or preferences to match them with a suitable financial broker.
        Ensure the question is phrased simply and is easy for a typical client to understand.
        Avoid overly technical jargon unless the topic inherently requires it (e.g. specific investment products IF that is the topic).
        Do not ask for personally identifiable information.
        Do not output any preamble or explanation, only the question text itself.
        
        IMPORTANT: Make sure your question is unique and different from any previously asked questions.
        """

        if existing_questions_texts and len(existing_questions_texts) > 0:
            prompt += f"\n\nYou MUST avoid generating questions that are similar to these existing questions:"
            for i, q_text in enumerate(existing_questions_texts, 1):
                prompt += f"\n{i}. {q_text}"

            prompt += f"\n\nGenerate a completely different question about {topic} that covers a different aspect or uses different wording."
        else:
            prompt += f"\n\nThis is the first question about {topic}."

        prompt += "\n\nGenerated Question:"

        question_text = await self.ai_service.generate_text(prompt)
        return question_text.strip() if question_text else None

    async def generate_multiple_choice_options(
        self,
        question_text: str,
        num_options: int = 4,
        topic: Optional[str] = None,  # context for options
    ) -> Optional[List[Dict[str, str]]]:
        """
        Generates plausible multiple-choice options for a given question text.

        Args:
            question_text (str): The text of the question.
            num_options (int): The desired number of options.
            topic (Optional[str]): The topic of the question for context.

        Returns:
            Optional[List[Dict[str, str]]]:
                A list of option dictionaries (e.g., [{"value": "a", "label": "Option A"}]),
                or None on failure.
        """
        # Gemini is better at generating JSON if explicitly asked in the prompt
        # and the output is structured as a JSON string.
        prompt = f"""
        For the following quiz question for a financial services client:
        Question: "{question_text}"
        Topic (for context): {topic or 'General Financial Knowledge'}

        Generate exactly {num_options} distinct, plausible multiple-choice options. 
        One option should be a reasonable or common answer, and the others should be plausible distractors.
        Keep the option labels concise.

        Return the options as a JSON list of objects, where each object has a "value" string and a "label" string. 
        The "value" should be a short, unique, machine-readable identifier (e.g., "option_1", "aggressive_growth").
        The "label" should be the human-readable text for the option.

        Example JSON format:
        [
            {{"value": "opt_a", "label": "Option A Text"}},
            {{"value": "opt_b", "label": "Option B Text"}}
        ]

        JSON Output:
        """

        # Using the generate_json method from GeminiService
        generated_data = await self.ai_service.generate_json(prompt)

        if isinstance(generated_data, list) and all(
            isinstance(item, dict) for item in generated_data
        ):
            # Basic validation for structure
            valid_options = []
            for i, opt in enumerate(generated_data):
                if "value" in opt and "label" in opt:
                    valid_options.append(
                        {"value": str(opt["value"]), "label": str(opt["label"])}
                    )
                else:
                    # Handle malformed item, or decide to skip it
                    print(f"Warning: Malformed option received: {opt}")
            return (
                valid_options if len(valid_options) == num_options else None
            )  # Ensure correct number of valid options

        print(
            f"Warning: Could not generate valid JSON list of options for question: {question_text}"
        )
        return None

    async def create_ai_question_data(
        self,
        topic: str,
        category: str,  # Corresponds to QuizCategory enum values
        question_type_str: str,  # Corresponds to QuestionType enum values (e.g., "SINGLE_CHOICE", "TEXT")
        order: int,
        existing_question_texts: Optional[List[str]] = None,
        quiz_id_for_logging: Optional[str] = None,  # Optional: for logging/context
    ) -> Optional[Dict[str, Any]]:
        """
        Generates a complete data structure for a new AI-generated quiz question.

        Args:
            topic (str): The specific topic for the question.
            category (str): The category of the quiz.
            question_type_str (str): The desired question type (e.g., "SINGLE_CHOICE", "TEXT").
            order (int): The order of this question in the quiz.
            existing_question_texts (Optional[List[str]]): For novelty.
            quiz_id_for_logging (Optional[str]): ID of the parent quiz for logging/context.

        Returns:
            Optional[Dict[str, Any]]: A dictionary suitable for creating a QuizQuestion model instance,
                                     or None if generation fails at any critical step.
        """
        print(
            f"Generating AI question for quiz '{quiz_id_for_logging or 'N/A'}' - Topic: {topic}, Type: {question_type_str}"
        )

        question_text = await self.generate_question_text(
            topic, category, existing_question_texts
        )
        if not question_text:
            print(f"Failed to generate question text for topic: {topic}")
            return None

        options_data: Optional[List[Dict[str, str]]] = None
        actual_question_type = question_type_str  # Assume it matches initially

        # QuestionType enum string values for comparison
        # These should match your actual enum string values in models/quiz.py
        # e.g., QuestionType.SINGLE_CHOICE.value which is "single_choice"
        choice_based_types = ["single_choice", "multiple_choice", "multiple_select"]
        # Note: MULTIPLE_SELECT and MULTIPLE_CHOICE are often treated similarly for option generation.

        if question_type_str.lower() in choice_based_types:
            num_options = 4  # Default, can be made configurable
            options_data = await self.generate_multiple_choice_options(
                question_text, num_options, topic
            )
            if not options_data or len(options_data) != num_options:
                print(
                    f"Failed to generate sufficient/valid options for: {question_text}. Defaulting to TEXT type."
                )
                # Fallback strategy: if options can't be generated, convert to a TEXT question
                actual_question_type = "text"  # QuestionType.TEXT.value
                options_data = None  # Ensure options are None for TEXT type
        elif question_type_str.lower() == "scale":
            # For SCALE, options might define the scale range, e.g., {"min":1, "max":5, "min_label":"Low", "max_label":"High"}
            # This is more structured and might not need AI generation for the options themselves,
            # but AI could help define appropriate labels for a given scale question.
            # For now, we assume scale options are manually defined or not AI-generated with this method.
            options_data = {
                "min": 1,
                "max": 5,
                "min_label": "Strongly Disagree",
                "max_label": "Strongly Agree",
            }  # Example default
            # pass # Or handle scale option generation if desired
        elif question_type_str.lower() in ["text", "boolean"]:
            options_data = None  # No options needed for these types
        else:
            print(
                f"Warning: Unsupported question type for AI option generation: {question_type_str}. No options will be generated."
            )
            options_data = None
            actual_question_type = (
                "text"  # Fallback to text if type is unknown for AI generation
            )

        question_id = uuid4()
        return {
            "id": question_id,
            # "quiz_id": quiz_id, # This should be set when associating with an actual quiz object
            "text": question_text,
            "question_type": actual_question_type,  # Use the actual type (could be fallback)
            "options": options_data,
            "order": order,
            "weight": 1,  # Default weight for AI-generated questions, can be adjusted
            "is_ai_generated": True,  # Flag this question
            # created_at, updated_at will be handled by the ORM/database
        }


# Example Usage (can be removed or moved to a test/script file):
async def demo_quiz_generation():
    if not GeminiService().model:  # Basic check if API_KEY was likely loaded
        print("Gemini API Key not configured. Cannot run AI Quiz Generation Demo.")
        return

    generator = QuizQuestionGenerator()

    print("\n--- Demo: Generating Financial Goals Question (Single Choice) ---")
    q_data_1 = await generator.create_ai_question_data(
        topic="Client's primary long-term financial objective",
        category="FINANCIAL_GOALS",
        question_type_str="single_choice",  # Ensure this matches QuestionType.SINGLE_CHOICE.value
        order=1,
        quiz_id_for_logging="demo_quiz_fg",
    )
    if q_data_1:
        print(f"Generated Question Data 1:\n{q_data_1}\n")

    print("\n--- Demo: Generating Risk Tolerance Question (Scale) ---")
    # For SCALE, options are typically predefined, but text can be AI-generated.
    q_data_2 = await generator.create_ai_question_data(
        topic="Client's comfort level with seeing investment values fluctuate significantly for higher potential returns",
        category="RISK_TOLERANCE",
        question_type_str="scale",  # Ensure this matches QuestionType.SCALE.value
        order=2,
        quiz_id_for_logging="demo_quiz_rt",
    )
    if q_data_2:
        print(f"Generated Question Data 2:\n{q_data_2}\n")

    print("\n--- Demo: Generating Investment Experience Question (Text) ---")
    q_data_3 = await generator.create_ai_question_data(
        topic="Client's past experiences with specific investment products like derivatives or private equity",
        category="EXPERIENCE",
        question_type_str="text",  # Ensure this matches QuestionType.TEXT.value
        order=3,
        quiz_id_for_logging="demo_quiz_exp",
    )
    if q_data_3:
        print(f"Generated Question Data 3:\n{q_data_3}\n")

    print("\n--- Demo: Generating Question with attempt for novelty ---")
    existing = ["What is your main financial goal for the next 5 years?"]
    q_data_4 = await generator.create_ai_question_data(
        topic="Client's short-term saving goals",
        category="FINANCIAL_GOALS",
        question_type_str="multiple_choice",
        order=4,
        existing_question_texts=existing,
        quiz_id_for_logging="demo_quiz_fg_novel",
    )
    if q_data_4:
        print(f"Generated Question Data 4 (novelty attempt):\n{q_data_4}\n")


if __name__ == "__main__":
    import asyncio

    # To run this example from the command line:
    # Ensure GEMINI_API_KEY is set in your environment.
    # Make sure you run from the project root: python -m backend.app.ai.quiz_generator
    # asyncio.run(demo_quiz_generation())
    pass
