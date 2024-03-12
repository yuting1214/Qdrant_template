import requests
from dotenv import load_dotenv
import os

# Define your API key
_ = load_dotenv('./environment/.env')
Mistral_API_KEY = os.getenv('MISTRAL_API_KEY')

# Define the endpoint URL
ENDPOINT_URL = 'https://api.mistral.ai/v1/models'

# Define headers with API key
headers = {
    'Authorization': f"Bearer {Mistral_API_KEY}",
    'Content-Type': 'application/json',
}

# Make a GET request to the API
response = requests.get(ENDPOINT_URL, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    print("Request successful!")
    print("Response:", response.json())
else:
    print("Error:", response.status_code)
    print("Response:", response.text)
