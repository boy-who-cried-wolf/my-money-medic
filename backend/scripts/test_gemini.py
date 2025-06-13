#!/usr/bin/env python
"""
Test script for Gemini integration.

Run this script to verify that your Gemini API is configured correctly.
"""

import sys
import os
from pathlib import Path
import asyncio

# Add the parent directory to sys.path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

from app.core.config import settings
from app.ai.base import BaseAIService


async def test_gemini_connection():
    """Test connection to Gemini API"""

    print(f"Testing connection to Gemini API using model: {settings.LLM_MODEL_NAME}")
    print(
        f"API Key: {settings.GEMINI_API_KEY[:5]}...{settings.GEMINI_API_KEY[-4:] if settings.GEMINI_API_KEY else 'None'}"
    )

    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_api_key_here":
        print("ERROR: Please set your Gemini API key in the .env file")
        print("Go to https://makersuite.google.com/ to get your API key")
        return

    try:
        # Create AI service with default LLM (should be Gemini)
        ai_service = BaseAIService()

        # Test with a simple prompt
        from langchain_core.prompts import PromptTemplate

        prompt = PromptTemplate.from_template(
            "What is your name and what LLM are you? Answer in one sentence."
        )

        # Create a chain for the test prompt
        chain = ai_service.create_chain(prompt)

        # Run the chain
        print("Sending test prompt to Gemini API...")
        result = await ai_service.generate(chain)

        print("\nGemini response:")
        print("-" * 40)
        if hasattr(result, "content"):
            print(result.content)
        else:
            print(str(result))
        print("-" * 40)
        print("\nGemini API connection successful!")

    except Exception as e:
        print(f"ERROR: Failed to connect to Gemini API: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_gemini_connection())
