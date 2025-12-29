
import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api"

def check_enrollments():
    # First get a course ID (assuming basic courses exist)
    # Since we don't have a direct list courses endpoint easily accessible without auth potentially, 
    # we will try course ID 1. If it fails we might need to populate data.
    course_id = 1
    url = f"{BASE_URL}/courses/{course_id}/enrollments/"
    
    print(f"Testing URL: {url}")
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 404:
            print("Course 1 not found. Trying to find a course first...")
            # Try to populate or find a course? For now just fail.
            print("Cannot verify without a valid course. Please ensure DB has data.")
            return False

        if response.status_code == 200:
            data = response.json()
            print("Response Data (Sample):")
            print(json.dumps(data[:1] if data else [], indent=2))
            
            if not data:
                print("⚠️ No enrollments found. Verification incomplete (but endpoint works).")
                return True

            first_item = data[0]
            if "student" in first_item and isinstance(first_item["student"], dict):
                print("✅ STRICT SUCCESS: 'student' field is a nested object.")
                print(f"   Student Name: {first_item['student'].get('name')}")
                return True
            else:
                print("❌ FAILURE: 'student' field is NOT a nested object or missing.")
                print(f"   Keys found: {list(first_item.keys())}")
                return False
        else:
            print(f"❌ API Error: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

if __name__ == "__main__":
    success = check_enrollments()
    sys.exit(0 if success else 1)
