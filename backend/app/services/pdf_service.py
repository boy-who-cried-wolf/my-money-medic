# backend/app/services/pdf_service.py
import os
from pypdf import PdfReader
from tqdm import tqdm


class PDFService:
    """Service for handling PDF operations"""

    def extract_text_from_pdf(self, pdf_path):
        """Extract text content from a PDF file"""
        text = ""
        try:
            with open(pdf_path, "rb") as f:
                pdf = PdfReader(f)
                total_pages = len(pdf.pages)

                # Create a progress bar
                pbar = tqdm(
                    total=total_pages,
                    desc=f"Extracting text from {os.path.basename(pdf_path)}",
                )

                # Process each page with progress
                for page in pdf.pages:
                    text += page.extract_text() + "\n\n"
                    pbar.update(1)

                pbar.close()

        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
        return text

    def process_pdf_directory(self, directory_path):
        """Process all PDFs in a directory and return book data"""
        # Get list of PDF files
        pdf_files = [f for f in os.listdir(directory_path) if f.endswith(".pdf")]
        books = []

        # Process each PDF with a progress bar
        for filename in tqdm(pdf_files, desc="Processing PDF books"):
            pdf_path = os.path.join(directory_path, filename)
            text = self.extract_text_from_pdf(pdf_path)

            # Basic metadata extraction (you might want to improve this)
            title = filename.replace(".pdf", "")
            author = "Unknown"  # Extract from PDF metadata if available

            books.append(
                {
                    "title": title,
                    "author": author,
                    "content": text,
                    "path": pdf_path,
                }
            )
        return books
