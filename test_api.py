import requests
import json

# Test the text analysis endpoint
url = "http://localhost:8000/analyze/text"
data = {
    "text": "hello how are you",
    "instruction": "Summarize this text."
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code == 200:
        print(f"JSON: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
