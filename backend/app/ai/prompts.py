"""
Prompt templates for AI-powered quiz generation.

This module stores and manages the various prompt templates used to instruct
the LLM (e.g., Gemini) for generating different parts of quiz questions.

Using a dedicated module for prompts helps in:
- Keeping the generator logic cleaner.
- Easier management and versioning of prompts.
- Centralizing prompt engineering efforts.
"""

# Example structure for a prompt template
# You can use f-strings or other templating engines as needed.

GENERATE_QUESTION_TEXT_PROMPT_TEMPLATE = (
    "You are an AI assistant designing a quiz for a broker matching platform. "
    "Your task is to generate ONE clear, concise, and relevant quiz question for a client.\n\n"
    "Quiz Category: {category}\n"
    "Specific Topic: {topic}\n\n"
    "The question should help assess a client's needs or preferences to match them with a suitable financial broker.\n"
    "Ensure the question is phrased simply and is easy for a typical client to understand.\n"
    "Avoid overly technical jargon unless the topic inherently requires it (e.g. specific investment products IF that is the topic).\n"
    "Do not ask for personally identifiable information.\n"
    "Do not output any preamble or explanation, only the question text itself.\n"
    "{existing_questions_instructions}"
    "\n\nGenerated Question:"
)

EXISTING_QUESTIONS_INSTRUCTIONS_TEMPLATE = (
    "\n\nAvoid generating questions that are too similar to the following existing questions:"
    "{formatted_existing_questions}"
)

FORMATTED_EXISTING_QUESTION_LINE_TEMPLATE = "\n{index}. {text}"


GENERATE_MCQ_OPTIONS_PROMPT_TEMPLATE = (
    "For the following quiz question for a financial services client:\n"
    'Question: "{question_text}"\n'
    "Topic (for context): {topic}\n\n"
    "Generate exactly {num_options} distinct, plausible multiple-choice options. "
    "One option should be a reasonable or common answer, and the others should be plausible distractors.\n"
    "Keep the option labels concise.\n\n"
    'Return the options as a JSON list of objects, where each object has a "value" string and a "label" string. '
    'The "value" should be a short, unique, machine-readable identifier (e.g., "option_1", "aggressive_growth").'
    'The "label" should be the human-readable text for the option.\n\n'
    "Example JSON format:\n"
    "[\n"
    '  {{"value": "opt_a", "label": "Option A Text"}},\n'
    '  {{"value": "opt_b", "label": "Option B Text"}}\n'
    "]\n\n"
    "JSON Output:"
)

# You can add more prompts here as needed, for example:
# - Prompts for different question types (e.g., scale, boolean if AI assistance is needed there)
# - Prompts for refining or rephrasing questions
# - Prompts for generating entire quizzes based on a theme
