import requests
import json

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
        print("\n" + sop_data.get("sop"))
        print("-------------------------------------------------------")
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
    
    generate_sop_example(
        topic="Cybersecurity Incident Response: Phishing Attack",
        details="Focus on initial detection, containment, eradication, and reporting steps for an employee-reported phishing email targeting credentials."
    )