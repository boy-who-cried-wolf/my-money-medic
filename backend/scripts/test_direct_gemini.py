#!/usr/bin/env python
"""
Test direct Gemini API integration using the latest Google Gen AI SDK.

This script bypasses LangChain and directly uses the google-generativeai package.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to sys.path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

# Import config settings
from app.core.config import settings

# Import the new Google Gen AI SDK
import google.generativeai as genai


def test_direct_gemini():
    """Test direct connection to Gemini API with the new SDK"""

    print(
        f"Testing direct connection to Gemini API using model: {settings.LLM_MODEL_NAME}"
    )
    print(
        f"API Key: {settings.GEMINI_API_KEY[:5]}...{settings.GEMINI_API_KEY[-4:] if settings.GEMINI_API_KEY else 'None'}"
    )

    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_api_key_here":
        print("ERROR: Please set your Gemini API key in the .env file")
        print("Go to https://makersuite.google.com/ to get your API key")
        return

    try:
        # Configure the Gemini API
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # List available models to verify connection
        print("\nAvailable models:")
        try:
            models = genai.list_models()
            for m in models:
                print(f" - {m.name}")
        except Exception as e:
            print(f"Failed to list models: {str(e)}")

        # Send a simple prompt to the model
        print("\nSending test prompt to Gemini API...")

        model = genai.GenerativeModel(settings.LLM_MODEL_NAME)
        response = model.generate_content(
            "What is your name and what LLM are you? Answer in one sentence."
        )

        print("\nGemini response:")
        print("-" * 40)
        print(response.text)
        print("-" * 40)
        print("\nDirect Gemini API connection successful!")

    except Exception as e:
        print(f"ERROR: Failed to connect to Gemini API: {str(e)}")
        import traceback

        traceback.print_exc()

        print("\nTry using one of these models instead:")
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            for m in genai.list_models():
                print(f" - {m.name}")
        except:
            print("Could not list models")


if __name__ == "__main__":
    test_direct_gemini()
