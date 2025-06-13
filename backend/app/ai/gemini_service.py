"""
Service for interacting with the Google Gemini API.

This module provides a wrapper around the Google Generative AI SDK
to facilitate making calls to Gemini models, particularly Gemini Flash.

Setup:
1. Install the Google Generative AI SDK:
   pip install google-generativeai

2. Obtain an API key from Google AI Studio (https://makersuite.google.com/)
   and set it as an environment variable or in your application's configuration.
   For example, as `GEMINI_API_KEY`.
"""

import google.generativeai as genai
import os
from typing import Optional, List, Dict, Any

# --- Configuration ---
# It's recommended to load the API key from environment variables or a secure config.
# For example, from your app.core.config.settings
# from app.core.config import settings
# API_KEY = settings.GEMINI_API_KEY

# As a placeholder, trying to get from environment variable:
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print(
        "WARNING: GEMINI_API_KEY environment variable not set. GeminiService will not function."
    )
    # You might want to raise an exception here or handle it based on your app's startup procedures.
else:
    try:
        genai.configure(api_key=API_KEY)
    except Exception as e:
        print(f"Error configuring Google Generative AI: {e}")
        API_KEY = None  # Prevent further use if configuration fails


# --- Model Configuration ---
# Upgraded to Gemini 2.5 Flash Preview - the latest and most advanced model
# with enhanced performance, price-performance optimization, and improved capabilities
DEFAULT_MODEL_NAME = (
    "gemini-2.5-flash-preview-05-20"  # Latest Gemini 2.5 Flash Preview model
)

# Safety settings can be adjusted to control content generation.
# See: https://ai.google.dev/docs/safety_setting_gemini
DEFAULT_SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

# Generation configuration optimized for Gemini 2.5 Flash Preview
# See: https://ai.google.dev/api/python/google/generativeai/GenerationConfig
DEFAULT_GENERATION_CONFIG = genai.types.GenerationConfig(
    # candidate_count=1, # Number of generated responses to return
    # stop_sequences=['x'], # Sequences to stop generation at
    max_output_tokens=4096,  # Increased for more detailed responses
    temperature=0.8,  # Optimized for creative but consistent question generation
    top_p=0.95,  # Nucleus sampling for better quality outputs
    # top_k=40,         # Top-k sampling for focused but diverse responses
)


class GeminiService:
    """
    A service class to interact with the Google Gemini API.
    """

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL_NAME,
        generation_config: Optional[genai.types.GenerationConfig] = None,
        safety_settings: Optional[List[Dict[str, Any]]] = None,
    ):
        """
        Initializes the GeminiService.

        Args:
            model_name (str): The name of the Gemini model to use.
            generation_config (Optional[genai.types.GenerationConfig]): Model generation configuration.
            safety_settings (Optional[List[Dict[str, Any]]]): Safety settings for content generation.
        """
        if not API_KEY:
            raise ValueError(
                "Gemini API key is not configured. Cannot initialize GeminiService."
            )

        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config or DEFAULT_GENERATION_CONFIG,
            safety_settings=safety_settings or DEFAULT_SAFETY_SETTINGS,
        )
        print(f"GeminiService initialized with model: {model_name}")

    async def generate_text(self, prompt: str) -> Optional[str]:
        """
        Generates text content based on a given prompt.

        Args:
            prompt (str): The prompt to send to the Gemini model.

        Returns:
            Optional[str]: The generated text, or None if an error occurs or content is blocked.
        """
        try:
            response = await self.model.generate_content_async(prompt)
            # Accessing the text directly. You might need to inspect `response.candidates`
            # for more complex scenarios or if `candidate_count > 1`.
            if response.candidates and response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text
            else:
                # This can happen if the content is blocked by safety settings
                # or if the response is empty for other reasons.
                print(
                    f'Gemini Warning: No content parts in response. Prompt: "{prompt[:100]}..."'
                )
                if response.prompt_feedback:
                    print(f"Prompt Feedback: {response.prompt_feedback}")
                return None
        except Exception as e:
            print(f"Error during Gemini text generation: {e}")
            # Consider logging the full exception traceback here
            return None

    async def generate_json(self, prompt: str, strict: bool = True) -> Optional[Any]:
        """
        Attempts to generate text that can be parsed as JSON.
        Note: Gemini models (especially Flash) may not always strictly adhere to JSON format
        in their raw output unless specifically fine-tuned or prompted very carefully with
        few-shot examples or by using newer model versions with explicit JSON mode.

        This is a simplified version. For robust JSON, you might need more complex prompting
        or to use models/features specifically designed for JSON output if available.

        Args:
            prompt (str): The prompt designed to elicit a JSON response.
            strict (bool): If True, raises an error if parsing fails. If False, returns None.

        Returns:
            Optional[Any]: The parsed JSON data, or None if generation/parsing fails.
        """
        import json

        text_response = await self.generate_text(prompt)
        if not text_response:
            return None

        try:
            # Attempt to clean up the response a bit if it includes markdown code fences
            if text_response.strip().startswith("```json"):
                text_response = text_response.strip()[7:]
                if text_response.strip().endswith("```"):
                    text_response = text_response.strip()[:-3]

            json_data = json.loads(text_response)
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from Gemini response: {e}")
            print(f"Raw Gemini response for JSON prompt: {text_response}")
            if strict:
                raise
            return None


# Example Usage (can be removed or moved to a test/script file):
async def main():
    if not API_KEY:
        print("Cannot run GeminiService example without API_KEY.")
        return

    service = GeminiService()

    # Text generation example
    text_prompt = "Explain the concept of a Large Language Model in one sentence."
    print(f"\nSending text prompt: {text_prompt}")
    generated_text = await service.generate_text(text_prompt)
    if generated_text:
        print(f"Gemini Response (Text):\n{generated_text}")
    else:
        print("Failed to generate text or content was blocked.")

    # JSON generation example (experimental)
    json_prompt = """
    Generate a JSON object representing a simple quiz question with a "text" field 
    and an "options" field which is a list of strings.
    Example: {"text": "What is 2+2?", "options": ["3", "4", "5"]}
    """
    print(f"\nSending JSON prompt: {json_prompt}")
    generated_json = await service.generate_json(json_prompt, strict=False)
    if generated_json:
        print(f"Gemini Response (JSON Parsed):\n{generated_json}")
    else:
        print("Failed to generate or parse JSON.")


if __name__ == "__main__":
    import asyncio

    # To run this example from the command line (e.g., for testing this file):
    # Ensure GEMINI_API_KEY is set in your environment.
    # python -m backend.app.ai.gemini_service (if run from project root)
    # or python backend/app/ai/gemini_service.py (if run from project root)
    # asyncio.run(main())
    pass
