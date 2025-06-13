#!/usr/bin/env python
"""
Effi API - Assign Broker to Lead Test

This script tests the assign_broker_to_lead function of the Effi API client.
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
    parser = argparse.ArgumentParser(description="Assign a broker to a lead")
    parser.add_argument("lead_id", help="ID of the lead to update")
    parser.add_argument("broker_id", help="ID of the broker to assign")
    parser.add_argument("--notes", help="Optional notes about the assignment")
    args = parser.parse_args()

    # Check if API key is set
    if not os.getenv("EFFI_API_KEY"):
        print("Error: EFFI_API_KEY environment variable is not set")
        print("Please set it before running this script.")
        return

    # Create client
    client = EffiClient()

    lead_id = args.lead_id
    broker_id = args.broker_id
    notes = args.notes

    print(f"Assigning broker {broker_id} to lead {lead_id}...")

    try:
        # Before assignment - get current lead info
        before_lead = client.get_lead(lead_id)
        print(f"\nLead before assignment:")
        print(f"Lead ID: {before_lead.get('Id')}")
        print(f"Name: {before_lead.get('FirstName')} {before_lead.get('LastName')}")

        current_broker_id = before_lead.get("BrokerId")
        if current_broker_id:
            print(f"Currently assigned to broker: {current_broker_id}")
        else:
            print("Not currently assigned to any broker")

        # Assign broker
        result = client.assign_broker_to_lead(
            lead_id=lead_id, broker_id=broker_id, notes=notes
        )

        # After assignment
        print(f"\nBroker assignment successful!")
        print(f"Lead ID: {result.get('Id')}")
        print(f"Newly assigned broker ID: {result.get('BrokerId')}")

        if result.get("BrokerName"):
            print(f"Broker name: {result.get('BrokerName')}")

        if notes:
            print(f"Notes: {notes}")

        # Print full response as JSON
        print("\nFull response:")
        print(json.dumps(result, indent=2))

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
