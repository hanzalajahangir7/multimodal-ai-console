import requests
import os

# Use Environment Variable for production API URL, default to localhost for dev
BASE_URL = os.getenv("API_URL", "http://localhost:8000")

def _handle_response(response):
    """Helper function to handle API responses"""
    try:
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response content: {response.text}")
        raise Exception(f"API Error: {response.status_code} - {response.text}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print(f"Response content: {response.text}")
        raise Exception(f"Invalid JSON response: {response.text}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

def upload_image(image_file, prompt):
    files = {"file": (image_file.name, image_file, image_file.type)}
    data = {"prompt": prompt}
    response = requests.post(f"{BASE_URL}/analyze/image", files=files, data=data)
    return _handle_response(response)

def upload_audio(audio_file):
    files = {"file": (audio_file.name, audio_file, audio_file.type)}
    response = requests.post(f"{BASE_URL}/analyze/audio", files=files)
    return _handle_response(response)

def analyze_text(text, instruction):
    response = requests.post(f"{BASE_URL}/analyze/text", json={"text": text, "instruction": instruction})
    return _handle_response(response)

def get_sessions():
    response = requests.get(f"{BASE_URL}/chat/sessions")
    return _handle_response(response)

def create_session(title):
    response = requests.post(f"{BASE_URL}/chat/sessions", json={"title": title})
    return _handle_response(response)

def send_message(session_id, message):
    response = requests.post(f"{BASE_URL}/chat/message", json={"session_id": session_id, "message": message})
    return _handle_response(response)

def get_history(session_id):
    response = requests.get(f"{BASE_URL}/chat/history/{session_id}")
    return _handle_response(response)

def generate_report(filename, title, sections):
    response = requests.post(f"{BASE_URL}/report", json={
        "filename": filename,
        "display_title": title,
        "sections": sections
    })
    return _handle_response(response)
