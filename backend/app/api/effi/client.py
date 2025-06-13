"""
Effi API Client

This module provides a client for interacting with the Effi API.
"""

import requests
import logging
from typing import Dict, Any, Optional, List, Union
from datetime import datetime, timedelta
import os

from app.core.config import settings

logger = logging.getLogger(__name__)


class EffiClient:
    """Client for the Effi API."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """Initialize the Effi API client.

        Args:
            api_key: API key for authentication. If not provided, uses the one from settings.
            base_url: Base URL for the API. If not provided, uses the one from settings.
        """
        self.api_key = api_key or os.getenv("EFFI_API_KEY")
        self.base_url = base_url or os.getenv(
            "EFFI_BASE_URL", "https://broker-service-m2m.lf.effi.com.au"
        )
        self.token = None
        self.token_expiry = None

        # Validate required settings
        if not self.api_key:
            raise ValueError("Effi API key is required")

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests.

        Returns:
            Headers dictionary with authentication.
        """
        # TODO: Implement proper authentication based on Effi documentation
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "x-api-key": self.api_key,
        }

    def search_leads(
        self,
        status: Optional[str] = None,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        postal_code: Optional[str] = None,
        broker_id: Optional[str] = None,
        min_loan_amount: Optional[float] = None,
        max_loan_amount: Optional[float] = None,
        created_from: Optional[str] = None,
        created_to: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Dict[str, Any]:
        """Search for leads with various filters.

        Args:
            status: Filter by lead status (e.g., "New", "InProgress")
            name: Search by lead name
            email: Filter by email address
            phone: Filter by phone number
            postal_code: Filter by postal code
            broker_id: Filter by assigned broker ID
            min_loan_amount: Minimum loan amount
            max_loan_amount: Maximum loan amount
            created_from: Created from date (format: YYYY-MM-DD)
            created_to: Created to date (format: YYYY-MM-DD)
            page: Page number (default: 1)
            page_size: Number of records per page (default: 20)

        Returns:
            Dictionary containing leads matching the filters and pagination information
        """
        url = f"{self.base_url}/api/Leads/Search"

        # Calculate skip value for pagination
        skip = (page - 1) * page_size

        # Build query parameters
        params = {"top": page_size, "skip": skip}

        if status:
            params["status"] = status
        if name:
            params["search"] = name
        if email:
            params["email"] = email
        if phone:
            params["phone"] = phone
        if postal_code:
            params["postalCode"] = postal_code
        if broker_id:
            params["brokerId"] = broker_id
        if min_loan_amount is not None:
            params["minAmount"] = min_loan_amount
        if max_loan_amount is not None:
            params["maxAmount"] = max_loan_amount
        if created_from:
            params["from"] = created_from
        if created_to:
            params["to"] = created_to

        # Make the request
        try:
            response = requests.get(url, params=params, headers=self._get_headers())
            response.raise_for_status()  # Raise exception for 4XX/5XX status codes

            # Get the JSON response
            data = response.json()

            # If the response is a list, convert it to the expected dictionary format
            if isinstance(data, list):
                return {
                    "Items": data,
                    "TotalCount": len(data),
                    "CurrentPage": page,
                    "PageSize": page_size,
                    "TotalPages": (len(data) + page_size - 1) // page_size,
                }

            # Return the JSON response as is if it's already in the expected format
            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching leads: {str(e)}")
            raise Exception(f"Error searching leads: {str(e)}")

    def get_leads(
        self,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        top: int = 50,
        skip: int = 0,
    ) -> Dict[str, Any]:
        """Get all leads.

        Args:
            from_date: Created from date (format: YYYY-MM-DD)
            to_date: Created to date (format: YYYY-MM-DD)
            top: Number of records to be fetched (default: 50)
            skip: Number of records to be skipped (default: 0)

        Returns:
            Dictionary containing lead data with pagination information
        """
        url = f"{self.base_url}/api/v2/Leads"

        # Build query parameters
        params = {"top": top, "skip": skip}

        if from_date:
            params["from"] = from_date

        if to_date:
            params["to"] = to_date

        # Make the request
        try:
            response = requests.get(url, params=params, headers=self._get_headers())
            response.raise_for_status()  # Raise exception for 4XX/5XX status codes

            # Get the JSON response
            data = response.json()

            # If the response is a list, convert it to the expected dictionary format
            if isinstance(data, list):
                page = (skip // top) + 1
                return {
                    "Items": data,
                    "TotalCount": len(data),
                    "CurrentPage": page,
                    "PageSize": top,
                    "TotalPages": (len(data) + top - 1) // top,
                }

            # Return the JSON response as is if it's already in the expected format
            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching leads: {str(e)}")
            raise

    def get_lead(self, lead_id: str) -> Dict[str, Any]:
        """Get a specific lead by ID.

        Args:
            lead_id: ID of the lead to retrieve

        Returns:
            Lead object with details
        """
        url = f"{self.base_url}/api/Leads/{lead_id}"

        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()  # Raise exception for 4XX/5XX status codes

            # Return the JSON response
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching lead {lead_id}: {str(e)}")
            raise

    def update_lead(self, lead_id: str, **kwargs) -> Dict[str, Any]:
        """Update a lead in the platform.

        Args:
            lead_id: ID of the lead to update
            **kwargs: Fields to update, which can include:
                - first_name: First name of the lead
                - last_name: Last name of the lead
                - email: Email address of the lead
                - phone: Phone number of the lead
                - postcode: Postal code
                - suburb: Suburb or city
                - state: State or province
                - broker_id: Broker ID to assign the lead to
                - estimated_property_value: Estimated property value
                - loan_amount: Loan amount requested
                - reference: Reference code
                - source_url: Source URL where the lead was generated
                - best_time_to_contact: Best time to contact (ISO date format)
                - notes: Additional notes about the lead
                - status: Status of the lead

        Returns:
            The updated lead object
        """
        url = f"{self.base_url}/api/Leads/{lead_id}"

        # Build request payload - convert from snake_case to PascalCase
        field_mapping = {
            "first_name": "FirstName",
            "last_name": "LastName",
            "email": "Email",
            "phone": "Phone",
            "postcode": "Postcode",
            "suburb": "Suburb",
            "state": "State",
            "broker_id": "BrokerId",
            "estimated_property_value": "EstimatedPropertyValue",
            "loan_amount": "LoanAmount",
            "reference": "Reference",
            "source_url": "SourceUrl",
            "best_time_to_contact": "BestTimeToContact",
            "notes": "Notes",
            "status": "Status",
        }

        # First get current lead data to update only the changed fields
        try:
            current_lead = self.get_lead(lead_id)
        except:
            # If we can't get the current lead data, proceed with just the provided fields
            current_lead = {}

        # Start with current lead data
        payload = current_lead

        # Update with new data
        for key, value in kwargs.items():
            if key in field_mapping and value is not None:
                payload[field_mapping[key]] = value

        # Make the request
        try:
            response = requests.put(url, json=payload, headers=self._get_headers())
            response.raise_for_status()  # Raise exception for 4XX/5XX status codes

            # Return the JSON response
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error updating lead {lead_id}: {str(e)}")
            raise

    def assign_broker_to_lead(
        self, lead_id: str, broker_id: str, notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Assign a broker to a lead.

        Args:
            lead_id: ID of the lead to update
            broker_id: ID of the broker to assign
            notes: Optional notes about the assignment

        Returns:
            Updated lead object
        """
        url = f"{self.base_url}/api/v2/Leads/{lead_id}/AssignBroker"

        # Build payload
        payload = {"BrokerId": broker_id}

        if notes:
            payload["Notes"] = notes

        try:
            response = requests.put(url, json=payload, headers=self._get_headers())
            response.raise_for_status()  # Raise exception for 4XX/5XX status codes

            # Return the JSON response
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(
                f"Error assigning broker {broker_id} to lead {lead_id}: {str(e)}"
            )
            raise

    def import_lead(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        postcode: Optional[str] = None,
        suburb: Optional[str] = None,
        state: Optional[str] = None,
        broker_id: Optional[str] = None,
        estimated_property_value: Optional[float] = None,
        loan_amount: Optional[float] = None,
        reference: Optional[str] = None,
        source_url: Optional[str] = None,
        best_time_to_contact: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Import a lead into the platform.

        Args:
            first_name: First name of the lead
            last_name: Last name of the lead
            email: Email address of the lead
            phone: Phone number of the lead
            postcode: Postal code
            suburb: Suburb or city
            state: State or province
            broker_id: Optional broker ID to assign the lead to
            estimated_property_value: Estimated property value
            loan_amount: Loan amount requested
            reference: Reference code
            source_url: Source URL where the lead was generated
            best_time_to_contact: Best time to contact (ISO date format)
            notes: Additional notes about the lead

        Returns:
            The created lead object
        """
        url = f"{self.base_url}/api/Leads/Import"

        # Build request payload
        payload = {
            "FirstName": first_name,
            "LastName": last_name,
            "Email": email,
            "Phone": phone,
        }

        # Add optional fields if provided
        if postcode:
            payload["Postcode"] = postcode
        if suburb:
            payload["Suburb"] = suburb
        if state:
            payload["State"] = state
        if broker_id:
            payload["BrokerId"] = broker_id
        if estimated_property_value is not None:
            payload["EstimatedPropertyValue"] = estimated_property_value
        if loan_amount is not None:
            payload["LoanAmount"] = loan_amount
        if reference:
            payload["Reference"] = reference
        if source_url:
            payload["SourceUrl"] = source_url
        if best_time_to_contact:
            payload["BestTimeToContact"] = best_time_to_contact
        if notes:
            payload["Notes"] = notes

        # Make the request
        try:
            response = requests.post(url, json=payload, headers=self._get_headers())
            response.raise_for_status()  # Raise exception for 4XX/5XX status codes

            # Get the JSON response
            result = response.json()

            # If the result is a string (just an ID), wrap it in a dictionary
            if isinstance(result, str):
                return {
                    "id": result,
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": email,
                    "phone": phone,
                }

            # Return the JSON response
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"Error importing lead: {str(e)}")
            raise
