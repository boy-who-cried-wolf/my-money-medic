#!/usr/bin/env python
"""
Effi API - Update Lead Test

This script tests the update_lead function of the Effi API client.
"""

import os
import sys
from pathlib import Path
import json
import argparse

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from app.api.effi.client import EffiClient


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Update a lead's information")
    parser.add_argument("lead_id", help="ID of the lead to update")
    parser.add_argument("--first_name", help="First name")
    parser.add_argument("--last_name", help="Last name")
    parser.add_argument("--email", help="Email address")
    parser.add_argument("--phone", help="Phone number")
    parser.add_argument("--postcode", help="Postal code")
    parser.add_argument("--suburb", help="Suburb or city")
    parser.add_argument("--state", help="State or province")
    parser.add_argument("--loan_amount", type=float, help="Loan amount")
    parser.add_argument(
        "--estimated_property_value", type=float, help="Estimated property value"
    )
    parser.add_argument("--notes", help="Additional notes")
    parser.add_argument("--status", help="Lead status")
    args = parser.parse_args()

    # Check if API key is set
    if not os.getenv("EFFI_API_KEY"):
        print("Error: EFFI_API_KEY environment variable is not set")
        print("Please set it before running this script.")
        return

    # Create client
    client = EffiClient()

    lead_id = args.lead_id
    print(f"Updating lead with ID: {lead_id}...")

    # Check if any fields are provided for update
    update_fields = {}
    for field in [
        "first_name",
        "last_name",
        "email",
        "phone",
        "postcode",
        "suburb",
        "state",
        "loan_amount",
        "estimated_property_value",
        "notes",
        "status",
    ]:
        value = getattr(args, field)
        if value is not None:
            update_fields[field] = value

    if not update_fields:
        print("Error: No update fields provided.")
        print("Please specify at least one field to update.")
        return

    try:
        # Before update - get current lead info
        before_lead = client.get_lead(lead_id)
        print(f"\nLead before update:")
        print(f"ID: {before_lead.get('Id')}")
        print(f"Name: {before_lead.get('FirstName')} {before_lead.get('LastName')}")
        print(f"Email: {before_lead.get('Email')}")
        print(f"Phone: {before_lead.get('Phone')}")

        if "LoanAmount" in before_lead:
            print(f"Loan Amount: ${before_lead.get('LoanAmount', 0):,.2f}")

        if "Status" in before_lead:
            print(f"Status: {before_lead.get('Status')}")

        # Print fields being updated
        print("\nUpdating fields:")
        for key, value in update_fields.items():
            print(f"  {key}: {value}")

        # Update lead
        result = client.update_lead(lead_id, **update_fields)

        # After update
        print(f"\nLead update successful!")
        print(f"ID: {result.get('Id')}")
        print(f"Updated Name: {result.get('FirstName')} {result.get('LastName')}")
        print(f"Updated Email: {result.get('Email')}")
        print(f"Updated Phone: {result.get('Phone')}")

        if "LoanAmount" in result:
            print(f"Updated Loan Amount: ${result.get('LoanAmount', 0):,.2f}")

        if "Status" in result:
            print(f"Updated Status: {result.get('Status')}")

        # Print full response as JSON
        print("\nFull response:")
        print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
