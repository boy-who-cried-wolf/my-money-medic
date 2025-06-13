#!/usr/bin/env python
"""
End-to-End Test for Question Generation.

This script tests the entire flow from PDF processing to question generation
without requiring the API server to be running.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.pdf_service import PDFService
from app.ai.direct_question_generator import DirectQuestionGenerator


async def test_question_generation():
    """Test end-to-end question generation directly."""
    print("Direct Question Generation Test")
    print("==============================\n")

    # Initialize services
    pdf_service = PDFService()
    question_generator = DirectQuestionGenerator()

    # Set up test directories
    test_dir = os.path.join("backend", "data", "books")
    os.makedirs(test_dir, exist_ok=True)

    # Check for PDFs
    pdf_files = [f for f in os.listdir(test_dir) if f.endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found. Creating a sample text to test...")
        sample_content = """
        Psychology is the scientific study of mind and behavior. The field explores cognitive, 
        emotional, and social processes and behaviors by analyzing how people think, feel, 
        learn, interact, perceive, and understand themselves and others. Self-awareness is a 
        fundamental aspect of psychological development, enabling individuals to reflect on 
        their experiences, emotions, and thought patterns. Through introspection and mindfulness, 
        people can gain insight into their own psychological processes, potentially leading to 
        personal growth, improved emotional regulation, and enhanced relationships with others.
        """
        sample_title = "Introduction to Psychology"
        sample_author = "Test Author"

        print("Using sample psychology text for testing")
    else:
        # Use the first PDF file
        pdf_path = os.path.join(test_dir, pdf_files[0])
        print(f"Using PDF file: {pdf_files[0]}")

        text = pdf_service.extract_text_from_pdf(pdf_path)

        # Limit content length for testing
        max_length = 1000
        if len(text) > max_length:
            # Take the first section
            sample_content = text[:max_length]
        else:
            sample_content = text

        sample_title = pdf_files[0].replace(".pdf", "")
        sample_author = "Unknown"

        print(f"Extracted {len(sample_content)} characters from PDF")

    # Generate questions
    print("\nGenerating questions using DirectQuestionGenerator...")

    try:
        questions = await question_generator.generate_questions(
            book_content=sample_content,
            book_title=sample_title,
            book_author=sample_author,
            num_questions=3,
        )

        # Display results
        print("\nGenerated Questions:")
        print("===================\n")

        if not questions:
            print("No questions were generated.")
        else:
            for i, q in enumerate(questions):
                print(f"Question {i+1}: {q['question_text']}")
                print(f"Reasoning: {q['reasoning']}")
                print(f"Tags: {', '.join(q['tags'])}")
                print()

        print("Question generation test completed successfully!")

    except Exception as e:
        print(f"Error generating questions: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_question_generation())
