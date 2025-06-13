#!/usr/bin/env python
"""
Test script for the search_leads function in the Effi API client.
This script performs an advanced search for leads with various filter options.
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.api.effi.client import EffiClient


def main():
    """Execute the lead search test."""
    parser = argparse.ArgumentParser(
        description="Search for leads with advanced filters"
    )

    # Add search filter options
    parser.add_argument("--status", help="Filter by lead status")
    parser.add_argument("--name", help="Search by lead name (partial match)")
    parser.add_argument("--email", help="Search by lead email (partial match)")
    parser.add_argument("--phone", help="Search by lead phone (partial match)")
    parser.add_argument(
        "--postal-code", dest="postal_code", help="Filter by postal code"
    )
    parser.add_argument(
        "--broker-id", dest="broker_id", help="Filter by assigned broker ID"
    )
    parser.add_argument(
        "--min-loan", dest="min_loan_amount", type=float, help="Minimum loan amount"
    )
    parser.add_argument(
        "--max-loan", dest="max_loan_amount", type=float, help="Maximum loan amount"
    )
    parser.add_argument(
        "--created-from", dest="created_from", help="Created from date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--created-to", dest="created_to", help="Created to date (YYYY-MM-DD)"
    )
    parser.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
    parser.add_argument(
        "--page-size",
        dest="page_size",
        type=int,
        default=20,
        help="Results per page (default: 20)",
    )

    args = parser.parse_args()

    # Check for API key
    if not os.environ.get("EFFI_API_KEY"):
        print("Error: EFFI_API_KEY environment variable is not set")
        print(
            "Please set the environment variable with: export EFFI_API_KEY=your_api_key"
        )
        sys.exit(1)

    # Create the client
    client = EffiClient()

    # Determine if any search filters were provided
    filter_args = {
        "status": args.status,
        "name": args.name,
        "email": args.email,
        "phone": args.phone,
        "postal_code": args.postal_code,
        "broker_id": args.broker_id,
        "min_loan_amount": args.min_loan_amount,
        "max_loan_amount": args.max_loan_amount,
        "created_from": args.created_from,
        "created_to": args.created_to,
        "page": args.page,
        "page_size": args.page_size,
    }

    # Remove None values to only use provided filters
    filter_args = {k: v for k, v in filter_args.items() if v is not None}

    print("\n=== Searching for leads with the following filters ===")
    if filter_args:
        for key, value in filter_args.items():
            if key not in [
                "page",
                "page_size",
            ]:  # Skip pagination parameters in the display
                print(f"  {key}: {value}")
    else:
        print("  No filters applied - retrieving all leads")

    print(f"\nPage {args.page}, {args.page_size} results per page")

    try:
        # Search for leads with the specified filters
        result = client.search_leads(**filter_args)

        # Print total count
        print(f"\nFound {result.get('TotalCount', 0)} leads in total")

        # Print lead details
        if "Items" in result and result["Items"]:
            print("\n=== Leads ===")
            for i, lead in enumerate(result["Items"], 1):
                print(f"\nLead {i} of {len(result['Items'])}:")
                print(f"  ID: {lead.get('Id')}")
                print(f"  Name: {lead.get('FirstName', '')} {lead.get('LastName', '')}")
                print(f"  Email: {lead.get('Email')}")
                print(f"  Phone: {lead.get('Phone')}")
                print(f"  Status: {lead.get('Status')}")

                if lead.get("BrokerId"):
                    print(
                        f"  Assigned Broker: {lead.get('BrokerName', '')} ({lead.get('BrokerId')})"
                    )
                else:
                    print("  Assigned Broker: None")

                if lead.get("LoanAmount"):
                    print(f"  Loan Amount: ${lead.get('LoanAmount', 0):,.2f}")

                if lead.get("DateCreated"):
                    print(f"  Created: {lead.get('DateCreated')}")
        else:
            print("\nNo leads found matching the search criteria")

        # Print full response
        print("\n=== Full Response ===")
        print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
