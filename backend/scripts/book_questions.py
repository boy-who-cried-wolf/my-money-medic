#!/usr/bin/env python
"""
Book Questions Generator

This script reads PDF books from the data folder, allows selecting one,
and generates psychological questions based on its content.
"""

import os
import sys
import json
import random
import requests
from pathlib import Path
from tqdm import tqdm

# Add the parent directory to sys.path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from app.services.pdf_service import PDFService
from app.core.config import settings

# Load environment variables
load_dotenv()

# Constants
API_URL = "http://127.0.0.1:8000/api/v1/questions/generate/public"
MAX_CONTENT_LENGTH = 1000  # Characters to use from the book


def main():
    """Run the book questions generator."""
    print("Book Questions Generator")
    print("========================\n")

    # Initialize PDF service
    pdf_service = PDFService()

    # Get book directory path
    book_dir = settings.BOOK_DIRECTORY
    if not os.path.exists(book_dir):
        print(f"Book directory not found: {book_dir}")
        print("Creating directory...")
        os.makedirs(book_dir, exist_ok=True)
        print(f"Please place PDF books in: {os.path.abspath(book_dir)}")
        return

    # Process all books in the directory - now with tqdm progress in pdf_service
    print(f"Reading books from: {os.path.abspath(book_dir)}")
    books = pdf_service.process_pdf_directory(book_dir)

    if not books:
        print("No PDF books found! Please add some PDFs to the data/books directory.")
        return

    # Display available books
    print(f"\nFound {len(books)} books:")
    for i, book in enumerate(books):
        print(f"{i+1}. {book['title']} by {book['author']}")

    # Select a book
    while True:
        try:
            choice = int(input("\nSelect a book number (or 0 to exit): "))
            if choice == 0:
                return
            if 1 <= choice <= len(books):
                selected_book = books[choice - 1]
                break
            print(f"Please enter a number between 1 and {len(books)}")
        except ValueError:
            print("Please enter a valid number")

    # Generate questions from the selected book
    print(f"\nGenerating questions for: {selected_book['title']}")

    # Get a section of the book content
    content = selected_book["content"]
    if len(content) > MAX_CONTENT_LENGTH:
        # Take a random section for variety
        start = random.randint(0, len(content) - MAX_CONTENT_LENGTH)
        content = content[start : start + MAX_CONTENT_LENGTH]

    # Prepare request data
    request_data = {
        "title": selected_book["title"],
        "author": selected_book["author"],
        "content": content,
        "num_questions": 3,
    }

    # Make API request with progress bar
    try:
        with tqdm(
            total=100,
            desc="API Request",
            bar_format="{desc}: {percentage:3.0f}%|{bar}| {elapsed}",
        ) as pbar:
            # Update to 30% - Sending request
            pbar.update(30)

            # Make the actual API request
            response = requests.post(API_URL, json=request_data)

            # Update to 90% - Processing response
            pbar.update(60)

            # Check response status
            response.raise_for_status()

            # Complete progress bar
            pbar.update(10)

        # Display questions
        result = response.json()
        print("\nGenerated Questions:")
        print("===================\n")

        for i, q in enumerate(result["questions"]):
            print(f"Question {i+1}: {q['question_text']}")
            print(f"Reasoning: {q['reasoning']}")
            print(f"Tags: {', '.join(q['tags'])}")
            print()

    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        if hasattr(e, "response") and e.response:
            print(f"Response: {e.response.text}")


if __name__ == "__main__":
    main()
