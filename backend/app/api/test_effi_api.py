import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_KEY = os.getenv("EFFI_API_KEY")
BASE_URL = "https://broker-m2m-test.effi.com.au"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}


# Test the API endpoint
def test_api():
    if not API_KEY:
        print("Error: EFFI_API_KEY not found in .env file")
        return

    try:
        url = f"{BASE_URL}/api/v1/broker/profile"
        print(f"Testing URL: {url}")

        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    test_api()
