#!/usr/bin/env python
"""
Effi API - Get Specific Lead Test

This script tests the get_lead function of the Effi API client.
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
    parser = argparse.ArgumentParser(description="Get a specific lead by ID")
    parser.add_argument("lead_id", help="ID of the lead to retrieve")
    args = parser.parse_args()

    # Check if API key is set
    if not os.getenv("EFFI_API_KEY"):
        print("Error: EFFI_API_KEY environment variable is not set")
        print("Please set it before running this script.")
        return

    # Create client
    client = EffiClient()

    lead_id = args.lead_id
    print(f"Fetching lead with ID: {lead_id}...")

    try:
        # Get lead details
        lead = client.get_lead(lead_id)

        # Print basic info
        print("\nLead Details:")
        print(f"ID: {lead.get('Id')}")
        print(f"Name: {lead.get('FirstName')} {lead.get('LastName')}")
        print(f"Email: {lead.get('Email')}")
        print(f"Phone: {lead.get('Phone')}")
        print(f"Status: {lead.get('Status')}")
        print(f"Created: {lead.get('CreatedDate')}")

        # Check if we have location data
        if lead.get("Postcode") or lead.get("Suburb") or lead.get("State"):
            print(
                f"\nLocation: {lead.get('Suburb', '')}, {lead.get('State', '')} {lead.get('Postcode', '')}"
            )

        # Check if we have loan info
        if lead.get("LoanAmount") or lead.get("EstimatedPropertyValue"):
            print("\nLoan Information:")
            print(f"Loan Amount: ${lead.get('LoanAmount', 0):,.2f}")
            print(
                f"Estimated Property Value: ${lead.get('EstimatedPropertyValue', 0):,.2f}"
            )

        # Check if we have broker info
        if lead.get("BrokerId"):
            print(f"\nAssigned to Broker ID: {lead.get('BrokerId')}")
            if lead.get("BrokerName"):
                print(f"Broker Name: {lead.get('BrokerName')}")

        # Check for notes
        if lead.get("Notes"):
            print(f"\nNotes: {lead.get('Notes')}")

        # Print the full response as JSON (optional)
        print("\nFull response:")
        print(json.dumps(lead, indent=2))

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
