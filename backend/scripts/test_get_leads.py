#!/usr/bin/env python
"""
Effi API - Get Leads Test

This script tests the get_leads function of the Effi API client.
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime, timedelta

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from app.api.effi.client import EffiClient


def main():
    # Check if API key is set
    if not os.getenv("EFFI_API_KEY"):
        print("Error: EFFI_API_KEY environment variable is not set")
        print("Please set it before running this script.")
        return

    # Create client
    client = EffiClient()

    # Calculate date range (last 30 days)
    to_date = datetime.now().strftime("%Y-%m-%d")
    from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    print(f"Fetching leads from {from_date} to {to_date}...")

    try:
        # Get leads
        response = client.get_leads(
            from_date=from_date,
            to_date=to_date,
            top=10,  # Limit to 10 leads for testing
            skip=0,
        )

        # Extract leads from the response
        leads = response.get("Items", [])

        # Print results
        print(f"Found {len(leads)} leads:")

        for i, lead in enumerate(leads, 1):
            print(f"\nLead #{i}:")
            print(f"ID: {lead.get('id')}")
            # Account for different case formats in API responses
            first_name = lead.get("FirstName") or lead.get("firstName") or ""
            last_name = lead.get("LastName") or lead.get("lastName") or ""
            print(f"Name: {first_name} {last_name}")
            print(f"Email: {lead.get('Email') or lead.get('email')}")
            print(f"Phone: {lead.get('Phone') or lead.get('phone')}")

            suburb = lead.get("Suburb") or lead.get("suburb") or ""
            state = lead.get("State") or lead.get("state") or ""
            postcode = lead.get("Postcode") or lead.get("postcode") or ""
            print(f"Location: {suburb}, {state} {postcode}")

            loan_amount = lead.get("LoanAmount") or lead.get("loanAmount") or 0
            print(f"Loan Amount: ${float(loan_amount):,.2f}")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
