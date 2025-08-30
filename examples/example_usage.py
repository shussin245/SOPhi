import requests
import json
import re
import os
from docx import Document

API_URL = "http://127.0.0.1:8000/generate_sop"
HEALTH_CHECK_URL = "http://127.0.0.1:8000/"

def check_api_health():
    try:
        response = requests.get(HEALTH_CHECK_URL, timeout=5)
        response.raise_for_status()
        print(f"API Health Check: {response.json()['message']}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"ERROR: Could not connect to the API at {HEALTH_CHECK_URL}.")
        print("Please ensure the FastAPI server is running (uvicorn src.main:app --reload).")
        return False
    except requests.exceptions.RequestException as e:
        print(f"ERROR during API health check: {e}")
        return False

def generate_sop_example(topic: str, details: str = ""):
    if not check_api_health():
        return

    payload = {"topic": topic, "details": details}
    headers = {"Content-Type": "application/json"}

    print(f"\n--- Requesting SOP for: '{topic}' (Details: '{details}') ---")
    try:
        response = requests.post(API_URL, data=json.dumps(payload), headers=headers, timeout=1500)
        response.raise_for_status()
        sop_data = response.json()
        sop_content = sop_data.get("sop")
        print("\n" + sop_content)
        print("-------------------------------------------------------")
        sanitized_topic = re.sub(r'[^a-zA-Z0-9\s]', '', topic)
        sanitized_topic = sanitized_topic.replace(' ', '_')[:50]
            
        output_dir = "examples/generated_sops"
        os.makedirs(output_dir, exist_ok=True)
            
        file_name = os.path.join(output_dir, f"SOP_{sanitized_topic}.docx")
            
        doc = Document()
            
        for line in sop_content.splitlines():
            doc.add_paragraph(line)
            
        doc.save(file_name)
            
        print(f"SOP saved to: {file_name}")
    except requests.exceptions.Timeout:
        print(f"ERROR: Request timed out for topic: '{topic}'. The LLM might be taking too long.")
    except requests.exceptions.RequestException as e:
        print(f"ERROR generating SOP for '{topic}': {e}")
        if e.response is not None:
            print(f"API Error Details: {e.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    generate_sop_example(
        topic="New Employee Onboarding: IT Setup for MacBook Pro",
        details="Include steps for account creation, device provisioning (MacBook Pro M1), software installation (Office 365, VS Code), network access, and security best practices."
    )