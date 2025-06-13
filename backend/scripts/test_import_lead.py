#!/usr/bin/env python
"""
Effi API - Import Lead Test

This script tests the import_lead function of the Effi API client.
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime, timedelta
import uuid

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

    # Generate a unique email to avoid duplicates
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"test.lead.{unique_id}@example.com"

    # Sample lead data
    lead_data = {
        "first_name": "Test",
        "last_name": "Lead",
        "email": test_email,
        "phone": "0412345678",
        "postcode": "2000",
        "suburb": "Sydney",
        "state": "NSW",
        "loan_amount": 500000,
        "estimated_property_value": 750000,
        "source_url": "https://yourwebsite.com/mortgage-calculator",
        "notes": "This is a test lead created via the API.",
        "reference": f"TEST-{unique_id}",
    }

    print(f"Importing test lead with email: {test_email}...")

    try:
        # Import lead
        result = client.import_lead(**lead_data)

        # Print result
        print("\nLead successfully imported:")

        # Handle different response formats
        if isinstance(result, str):
            # If the API just returned an ID
            print(f"Lead ID: {result}")
            print(f"Name: {lead_data['first_name']} {lead_data['last_name']}")
            print(f"Email: {lead_data['email']}")
            print("Status: New (assumed)")
            print("No broker assigned yet")
        else:
            # Handle dictionary response with potential different casing
            lead_id = result.get("Id") or result.get("id")
            first_name = (
                result.get("FirstName")
                or result.get("firstName")
                or lead_data["first_name"]
            )
            last_name = (
                result.get("LastName")
                or result.get("lastName")
                or lead_data["last_name"]
            )
            email = result.get("Email") or result.get("email") or lead_data["email"]
            status = result.get("Status") or result.get("status") or "New"
            broker_id = result.get("BrokerId") or result.get("brokerId")

            print(f"Lead ID: {lead_id}")
            print(f"Name: {first_name} {last_name}")
            print(f"Email: {email}")
            print(f"Status: {status}")

            if broker_id:
                broker_name = result.get("BrokerName") or result.get("brokerName") or ""
                print(f"Assigned to Broker ID: {broker_id}")
                if broker_name:
                    print(f"Broker Name: {broker_name}")
            else:
                print("No broker assigned yet")

        # Print full response as JSON
        print("\nFull response:")
        print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
