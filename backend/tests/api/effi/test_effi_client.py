import pytest
import requests
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from app.api.effi.client import EffiClient

# Test data
TEST_API_KEY = "test_api_key"
TEST_LEAD = {
    "Id": "123",
    "FirstName": "John",
    "LastName": "Doe",
    "Email": "john.doe@example.com",
    "Phone": "1234567890",
    "Status": "New",
}


class TestEffiClient:
    """Tests for the Effi API client."""

    def test_init(self):
        """Test initialization with API key."""
        client = EffiClient(api_key=TEST_API_KEY)
        assert client.api_key == TEST_API_KEY
        assert client.base_url == "https://broker-service-m2m.lf.effi.com.au"

    @patch("app.api.effi.client.requests.get")
    def test_search_leads(self, mock_get):
        """Test searching leads with various filters."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Items": [TEST_LEAD],
            "TotalCount": 1,
            "CurrentPage": 1,
            "PageSize": 20,
            "TotalPages": 1,
        }
        mock_get.return_value = mock_response

        # Create client
        client = EffiClient(api_key=TEST_API_KEY)

        # Test with various filter parameters
        filters = {
            "status": "New",
            "name": "John",
            "email": "example.com",
            "phone": "123",
            "postal_code": "2000",
            "broker_id": "456",
            "min_loan_amount": 100000,
            "max_loan_amount": 500000,
            "created_from": "2023-01-01",
            "created_to": "2023-12-31",
            "page": 1,
            "page_size": 20,
        }

        result = client.search_leads(**filters)

        # Verify the request was made with correct parameters
        mock_get.assert_called_once()
        call_args = mock_get.call_args

        # Check that URL is correct
        assert (
            call_args[0][0]
            == "https://broker-service-m2m.lf.effi.com.au/api/Leads/Search"
        )

        # Check query parameters
        params = call_args[1]["params"]
        assert params["status"] == filters["status"]
        assert params["search"] == filters["name"]
        assert params["email"] == filters["email"]
        assert params["phone"] == filters["phone"]
        assert params["postalCode"] == filters["postal_code"]
        assert params["brokerId"] == filters["broker_id"]
        assert params["minAmount"] == filters["min_loan_amount"]
        assert params["maxAmount"] == filters["max_loan_amount"]
        assert params["from"] == filters["created_from"]
        assert params["to"] == filters["created_to"]
        assert params["top"] == filters["page_size"]
        assert params["skip"] == (filters["page"] - 1) * filters["page_size"]

        # Check request headers
        headers = call_args[1]["headers"]
        assert headers["x-api-key"] == TEST_API_KEY

        # Check result
        assert result == mock_response.json.return_value
        assert "Items" in result
        assert result["Items"][0] == TEST_LEAD
        assert result["TotalCount"] == 1

    @patch("app.api.effi.client.requests.get")
    def test_search_leads_minimal_params(self, mock_get):
        """Test searching leads with minimal parameters."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Items": [],
            "TotalCount": 0,
            "CurrentPage": 1,
            "PageSize": 50,
            "TotalPages": 0,
        }
        mock_get.return_value = mock_response

        # Create client
        client = EffiClient(api_key=TEST_API_KEY)

        # Test with minimal parameters
        result = client.search_leads()

        # Verify the request was made with minimal parameters
        mock_get.assert_called_once()
        call_args = mock_get.call_args

        # Check that URL is correct
        assert (
            call_args[0][0]
            == "https://broker-service-m2m.lf.effi.com.au/api/Leads/Search"
        )

        # Check query parameters - should only have pagination defaults
        params = call_args[1]["params"]
        assert len(params) == 2  # Only skip and top
        assert params["top"] == 20  # Default page size
        assert params["skip"] == 0  # Default skip (page 1)

        # Check result
        assert result == mock_response.json.return_value
        assert result["TotalCount"] == 0

    @patch("app.api.effi.client.requests.get")
    def test_search_leads_error_handling(self, mock_get):
        """Test error handling in search_leads."""
        # Mock a connection error
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        # Create client
        client = EffiClient(api_key=TEST_API_KEY)

        # Test exception handling
        with pytest.raises(Exception) as exc_info:
            client.search_leads()

        # Verify the error message
        assert "Error searching leads: Connection error" in str(exc_info.value)
